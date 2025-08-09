"""Stream type classes for tap-portaltransparencia."""

from __future__ import annotations

import typing as t
from importlib import resources
from typing import Any, Mapping, Optional

from tap_portaltransparencia.client import PortalTransparenciaStream

SCHEMAS_DIR = resources.files(__package__) / "schemas"


class EmendaStream(PortalTransparenciaStream):
    """
    # primary_key: no primary key is defined, as the API does not provide a
     unique identifier. There are cases like "S/I" e "REL. GERAL" as "codigoEmenda"
     with multiple records for data under 2020.

    # replication_key: no replication key is defined, as the API does not provide a
     date field. Also, it is common to add documents to amendments from previous years,
     so using year as a replication key is not safe.
    """

    name = "emenda"
    path = "/api-de-dados/emendas"
    primary_keys = []  #: t.ClassVar[list[str]] = ["codigoEmenda"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "emenda.json"

    def get_url_params(
            self,
            context: Mapping[str, Any] | None,
            next_page_token: Any | None,
    ) -> dict[str, Any]:
        params = super().get_url_params(context, next_page_token)
        emendas_config = self.config.get("emendas_config", {})
        if emendas_config.get("ano"):
            params["ano"] = emendas_config.get("ano")
        if emendas_config.get("nome_autor"):
            params["nomeAutor"] = emendas_config.get("nome_autor").upper()
        return params

    def get_child_context(
            self,
            record: dict,
            context: Mapping[str, Any] | None,
    ) -> dict | None:
        codigo = record["codigoEmenda"]
        if codigo and codigo.isdigit():
            return {
                "codigoEmenda": codigo,
            }
        else:
            return None


class DocumentoEmendaStream(PortalTransparenciaStream):
    name = "documento_emenda"
    path = "/api-de-dados/emendas/documentos/{codigoEmenda}"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "documento_emenda.json"
    parent_stream_type = EmendaStream
