"""REST client handling, including PortalTransparenciaStream base class."""

from __future__ import annotations

import decimal
import time
import typing as t
from datetime import datetime
from importlib import resources
from zoneinfo import ZoneInfo

from singer_sdk.authenticators import APIKeyAuthenticator
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.pagination import BaseAPIPaginator, BasePageNumberPaginator
from singer_sdk.streams import RESTStream

if t.TYPE_CHECKING:
    import requests
    from singer_sdk.helpers.types import Context

SCHEMAS_DIR = resources.files(__package__) / "schemas"


class IncrementalPaginator(BasePageNumberPaginator):

    # This constant was not present in the documentation, but rather inferred from the API behavior in both endpoints.
    # In a production environment, it is recommended to verify this value with the API support or remove it and set the
    # has_more method to return True until there are no more records.
    RECORDS_PER_PAGE = 15

    def has_more(self, response: requests.Response) -> bool:
        # return bool(response.json())
        return len(response.json()) >= self.RECORDS_PER_PAGE


class PortalTransparenciaStream(RESTStream):
    """PortalTransparencia stream class."""

    records_jsonpath = "$[*]"

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        return "https://api.portaldatransparencia.gov.br"

    @property
    def authenticator(self) -> APIKeyAuthenticator:
        """Return a new authenticator object.

        Returns:
            An authenticator instance.
        """
        return APIKeyAuthenticator.create_for_stream(
            self,
            key="chave-api-dados",
            value=self.config.get("auth_token", ""),
            location="header",
        )

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed.

        Returns:
            A dictionary of HTTP headers.
        """
        return {}

    def get_new_paginator(self) -> BaseAPIPaginator | None:
        return IncrementalPaginator(start_value=1)

    def get_url_params(
            self,
            context: Context | None,  # noqa: ARG002
            next_page_token: t.Any | None,  # noqa: ANN401
    ) -> dict[str, t.Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary of URL query parameters.
        """
        params: dict = {}
        if next_page_token:
            params["pagina"] = next_page_token
        if self.config.get("emendas_config", {}).get("ano"):
            params["ano"] = self.config.get("emendas_config").get("ano")
        if self.config.get("emendas_config", {}).get("nome_autor"):
            params["nomeAutor"] = self.config.get("emendas_config").get("nome_autor").upper()
        return params

    def parse_response(self, response: requests.Response) -> t.Iterable[dict]:
        """Parse the response and return an iterator of result records.

        Args:
            response: The HTTP ``requests.Response`` object.

        Yields:
            Each record from the source.
        """
        # TODO: Parse response body and return a set of records.
        yield from extract_jsonpath(
            self.records_jsonpath,
            input=response.json(parse_float=decimal.Decimal),
        )

    def post_process(
            self,
            row: dict,
            context: Context | None = None,  # noqa: ARG002
    ) -> dict | None:
        """As needed, append or transform raw data to match expected structure.

        Note: As of SDK v0.47.0, this method is automatically executed for all stream types.
        You should not need to call this method directly in custom `get_records` implementations.

        Args:
            row: An individual record from the stream.
            context: The stream context.

        Returns:
            The updated record dictionary, or ``None`` to skip the record.
        """
        # TODO: Delete this method if not needed.
        return row

    def _get_required_delay(self) -> float:
        """
        "De 00:00 às 06:00: até 700 requisições por minuto, Nos demais horários: 400 requisições por minuto"
        - https://portaldatransparencia.gov.br/api-de-dados/cadastrar-email
        """
        now = datetime.now(ZoneInfo("America/Sao_Paulo")).time()
        if now.hour < 6:
            return 60 / 650
        else:
            return 60 / 350

    def _request(self, prepared_request: requests.PreparedRequest, context: Context | None) -> requests.Response:
        """
        Overriding the _request method to include a delay to comply with the API rate limits.
        https://portaldatransparencia.gov.br/api-de-dados/cadastrar-email
        """

        # Applying the required delay before making the request
        required_delay = self._get_required_delay()
        time.sleep(required_delay)

        # Making the actual request with the original _request method
        response = super()._request(prepared_request, context)

        return response
