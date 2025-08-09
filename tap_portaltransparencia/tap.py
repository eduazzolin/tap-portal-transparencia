"""PortalTransparencia tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

from tap_portaltransparencia import streams


class TapPortalTransparencia(Tap):
    """PortalTransparencia tap class."""

    name = "tap-portaltransparencia"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "auth_token",
            th.StringType(nullable=False),
            required=True,
            secret=True,  # Flag config as protected.
            title="chave-api-dados",
            description="The token to authenticate against the API service",
        ),
        th.Property(
            "emendas_config",
            th.ObjectType(
                th.Property(
                    "ano",
                    th.IntegerType(nullable=True),
                    required=False,
                    title="ano",
                    description="The year to be extracted from the API",
                ),
                th.Property(
                    "nome_autor",
                    th.StringType(nullable=True),
                    required=False,
                    title="nome_autor",
                    description="The name of the author to be extracted from the API",
                ),
            ),
            description="Parameters to be sent to the Emendas endpoint",
            required=False
        ),
    ).to_dict()

    def discover_streams(self) -> list[streams.PortalTransparenciaStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            streams.EmendaStream(self),
            streams.DocumentoEmendaStream(self),
        ]


if __name__ == "__main__":
    TapPortalTransparencia.cli()
