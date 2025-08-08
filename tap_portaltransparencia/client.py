"""REST client handling, including PortalTransparenciaStream base class."""

from __future__ import annotations

import decimal
import sys
import time
import typing as t
from datetime import datetime
from importlib import resources
from zoneinfo import ZoneInfo

from singer_sdk.authenticators import APIKeyAuthenticator
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.pagination import BaseAPIPaginator, BasePageNumberPaginator
from singer_sdk.streams import RESTStream

if sys.version_info >= (3, 12):
    pass
else:
    pass

if t.TYPE_CHECKING:
    import requests
    from singer_sdk.helpers.types import Context

SCHEMAS_DIR = resources.files(__package__) / "schemas"


class IncrementalPaginator(BasePageNumberPaginator):
    """
    "De 00:00 às 06:00: até 700 requisições por minuto, Nos demais horários: 400 requisições por minuto"
    https://portaldatransparencia.gov.br/api-de-dados/cadastrar-email

    Rate limit based on:
    https://github.com/MeltanoLabs/tap-slack.git
    """
    now = datetime.now(ZoneInfo("America/Sao_Paulo")).time()
    MAX_REQUESTS_PER_MINUTE = 700 if now.hour < 6 else 400

    def get_next(self, response: requests.Response) -> int | None:
        time.sleep(60.0 / self.MAX_REQUESTS_PER_MINUTE)
        return self._value + 1

    def has_more(self, response: requests.Response) -> bool:
        return bool(response.json())


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
        """Cria uma nova instância de auxiliar de paginação.

        Retorna:
            Uma instância de auxiliar de paginação.
        """
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
