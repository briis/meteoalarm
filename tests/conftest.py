"""Fixtures for MeteoAlarm integration tests."""

from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture
def mock_meteoalert_api():
    """Mock Meteoalert API."""
    with patch("custom_components.meteoalarm.binary_sensor.Meteoalert") as mock:
        api_instance = MagicMock()
        mock.return_value = api_instance
        yield api_instance


@pytest.fixture
def mock_meteoalert_alert():
    """Return mock MeteoAlert data."""
    return {
        "title": "Extreme Weather Warning",
        "description": "Severe storms expected",
        "level": "Red",
        "onset": "2026-04-12T12:00:00Z",
        "expires": "2026-04-12T18:00:00Z",
        "headlines": ["Storm Warning"],
        "severity": "Extreme",
    }
