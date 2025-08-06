"""Stream type classes for tap-portaltransparencia."""

from __future__ import annotations

import typing as t
from importlib import resources

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_portal_transparencia.client import PortalTransparenciaStream

SCHEMAS_DIR = resources.files(__package__) / "schemas"


class EmendaStream(PortalTransparenciaStream):
    """Define custom stream."""

    name = "emenda"
    path = "/api-de-dados/emendas"
    primary_keys: []  # Null because this stream contains records with "S/A" as ID #TODO
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "emenda.json"

    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        """Return a context dictionary for child streams."""
        return {
            "cod_emenda": record["codigoEmenda"],
        }


class DocumentoEmendaStream(PortalTransparenciaStream):
    """Define custom stream."""

    name = "documento_emenda"
    path = "/api-de-dados/emendas/documentos/{cod_emenda}"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "documento_emenda.json"
