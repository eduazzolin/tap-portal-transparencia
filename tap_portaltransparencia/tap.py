"""PortalTransparencia tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

from tap_portaltransparencia import streams


class TapPortalTransparencia(Tap):
    """PortalTransparencia tap class."""

    name = "tap-portaltransparencia"

    # TODO: Update this section with the actual config values you expect:
    config_jsonschema = th.PropertiesList(
        th.Property(
            "auth_token",
            th.StringType(nullable=False),
            required=True,
            secret=True,  # Flag config as protected.
            title="chave-api-dados",
            description="The token to authenticate against the API service",
        ),
    ).to_dict()

    def discover_streams(self) -> list[streams.PortalTransparenciaStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams. #TODO
        """
        return [
            streams.EmendaStream(self),
            streams.DocumentoEmendaStream(self),
        ]


if __name__ == "__main__":
    TapPortalTransparencia.cli()
