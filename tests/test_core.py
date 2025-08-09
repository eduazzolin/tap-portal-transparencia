"""Tests standard tap features using the built-in SDK tests library."""

import datetime
import os

from singer_sdk.testing import get_tap_test_class

from tap_portaltransparencia.tap import TapPortalTransparencia

SAMPLE_CONFIG = {
    "auth_token": os.environ.get("TAP_PORTALTRANSPARENCIA_AUTH_TOKEN"),
    "ano": 2021,
    "emendas_config": {"nome_autor": "SCHIAVINATO"},
}


# Run standard built-in tap tests from the SDK:
TestTapPortalTransparencia = get_tap_test_class(
    tap_class=TapPortalTransparencia,
    config=SAMPLE_CONFIG,
)