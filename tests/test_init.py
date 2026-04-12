"""Tests for MeteoAlarm integration initialization."""

from custom_components.meteoalarm import async_setup_entry, async_unload_entry
from custom_components.meteoalarm.const import DOMAIN


class TestMeteoAlarmInit:
    """Test the MeteoAlarm integration initialization."""

    def test_domain_constant(self):
        """Test that the domain is correctly defined."""
        assert DOMAIN == "meteoalarm"

    def test_import_init_module(self):
        """Test that the integration module can be imported."""
        assert async_setup_entry is not None
        assert async_unload_entry is not None
