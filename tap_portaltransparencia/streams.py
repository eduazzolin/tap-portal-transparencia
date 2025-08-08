"""Stream type classes for tap-portaltransparencia."""

from __future__ import annotations

import typing as t
from importlib import resources
from typing import Optional, Any, Dict

from tap_portaltransparencia.client import PortalTransparenciaStream

SCHEMAS_DIR = resources.files(__package__) / "schemas"


class EmendaStream(PortalTransparenciaStream):
    """
    # chave primária:
       - possui valores repetidos, como "S/I" e "REL. GERAL" #TODO

    # incrementalidade:
       - não possui campo de data, somente ano
         é possível e comum adicionar documentos a emendas de anos anteriores,
         portanto não é seguro usar lógico incremental basedo em ano
    """

    name = "emenda"
    path = "/api-de-dados/emendas"
    primary_keys: t.ClassVar[list[str]] = ["codigoEmenda"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "emenda.json"

    def get_url_params(self, context: Optional[dict], next_page_token: Optional[Any]) -> Dict[str, Any]:
        params = super().get_url_params(context, next_page_token)
        emendas_config = self.config.get("emendas_config", {})
        if emendas_config.get("ano"):
            params["ano"] = emendas_config.get("ano")
        if emendas_config.get("nome_autor"):
            params["nomeAutor"] = emendas_config.get("nome_autor").upper()
        return params

    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
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
