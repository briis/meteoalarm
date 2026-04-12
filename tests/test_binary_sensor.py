"""Tests for MeteoAlarm binary sensor."""

from datetime import timedelta
from unittest.mock import MagicMock

import pytest
from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.util import dt as dt_util

from custom_components.meteoalarm.binary_sensor import MeteoAlertBinarySensor


@pytest.fixture
def mock_meteoalert_api():
    """Create a mock Meteoalert API instance."""
    api = MagicMock()
    api.get_alert = MagicMock(return_value={})
    return api


@pytest.fixture
def sample_alert():
    """Return sample alert data."""
    future_time = (dt_util.utcnow() + timedelta(hours=1)).isoformat()
    return {
        "title": "Extreme Weather Warning",
        "description": "Severe storms expected",
        "level": "Red",
        "onset": dt_util.utcnow().isoformat(),
        "expires": future_time,
        "headlines": ["Storm Warning"],
        "severity": "Extreme",
    }


class TestMeteoAlertBinarySensor:
    """Test the MeteoAlert binary sensor."""

    def test_init(self, mock_meteoalert_api):
        """Test initialization of the binary sensor."""
        sensor = MeteoAlertBinarySensor(mock_meteoalert_api, "test_sensor")

        assert sensor._attr_name == "test_sensor"
        assert sensor._attr_device_class == BinarySensorDeviceClass.SAFETY
        assert sensor._api is mock_meteoalert_api

    def test_init_with_entry_id(self, mock_meteoalert_api):
        """Test initialization with entry_id."""
        sensor = MeteoAlertBinarySensor(
            mock_meteoalert_api, "test_sensor", entry_id="entry_123"
        )

        assert sensor._attr_unique_id == "entry_123_test_sensor"

    @pytest.mark.asyncio
    async def test_update_no_alert(self, mock_meteoalert_api):
        """Test update when there's no active alert."""
        mock_meteoalert_api.get_alert = MagicMock(return_value=None)

        sensor = MeteoAlertBinarySensor(mock_meteoalert_api, "test_sensor")
        await sensor.async_update()

        assert sensor.is_on is False
        assert sensor.extra_state_attributes == {}

    @pytest.mark.asyncio
    async def test_update_with_active_alert(self, mock_meteoalert_api, sample_alert):
        """Test update when there's an active alert."""
        mock_meteoalert_api.get_alert = MagicMock(return_value=sample_alert)

        sensor = MeteoAlertBinarySensor(mock_meteoalert_api, "test_sensor")
        await sensor.async_update()

        assert sensor.is_on is True
        assert sensor.extra_state_attributes == sample_alert

    @pytest.mark.asyncio
    async def test_update_with_expired_alert(self, mock_meteoalert_api):
        """Test update when alert is expired."""
        past_time = (dt_util.utcnow() - timedelta(hours=1)).isoformat()
        expired_alert = {
            "title": "Expired Warning",
            "expires": past_time,
        }
        mock_meteoalert_api.get_alert = MagicMock(return_value=expired_alert)

        sensor = MeteoAlertBinarySensor(mock_meteoalert_api, "test_sensor")
        await sensor.async_update()

        assert sensor.is_on is False
        assert sensor.extra_state_attributes == {}

    @pytest.mark.asyncio
    async def test_update_with_invalid_expiry_date(self, mock_meteoalert_api):
        """Test update with invalid expiry date format."""
        invalid_alert = {
            "title": "Invalid Alert",
            "expires": "invalid_date",
        }
        mock_meteoalert_api.get_alert = MagicMock(return_value=invalid_alert)

        sensor = MeteoAlertBinarySensor(mock_meteoalert_api, "test_sensor")
        await sensor.async_update()

        assert sensor.is_on is False
        assert sensor.extra_state_attributes == {}

    @pytest.mark.asyncio
    async def test_update_api_error(self, mock_meteoalert_api):
        """Test update when API raises an error."""
        mock_meteoalert_api.get_alert = MagicMock(side_effect=Exception("API Error"))

        sensor = MeteoAlertBinarySensor(mock_meteoalert_api, "test_sensor")
        await sensor.async_update()

        assert sensor.is_on is False
        assert sensor.extra_state_attributes == {}

    def test_attribution(self, mock_meteoalert_api):
        """Test that attribution is set correctly."""
        sensor = MeteoAlertBinarySensor(mock_meteoalert_api, "test_sensor")

        assert sensor.attribution == "Information provided by MeteoAlarm"

    def test_device_class(self, mock_meteoalert_api):
        """Test that device class is set to SAFETY."""
        sensor = MeteoAlertBinarySensor(mock_meteoalert_api, "test_sensor")

        assert sensor.device_class == BinarySensorDeviceClass.SAFETY
