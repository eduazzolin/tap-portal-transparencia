"""Stream type classes for tap-portaltransparencia."""

from __future__ import annotations

import typing as t
from importlib import resources

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_portaltransparencia.client import PortalTransparenciaStream

SCHEMAS_DIR = resources.files(__package__) / "schemas"


class EmendaStream(PortalTransparenciaStream):
    """Define custom stream."""

    name = "emenda"
    path = "/api-de-dados/emendas"
    primary_keys: t.ClassVar[list[str]] = ["codigoEmenda"] # Null because this stream contains records with "S/A" as ID #TODO
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "emenda.json"

    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        """Return a context dictionary for child streams."""
        codigo = record["codigoEmenda"]

        if codigo and codigo.isdigit():
            return {
                "codigoEmenda": codigo,
            }


class DocumentoEmendaStream(PortalTransparenciaStream):
    """Define custom stream."""

    name = "documento_emenda"
    path = "/api-de-dados/emendas/documentos/{codigoEmenda}"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "documento_emenda.json"
    parent_stream_type = EmendaStream
