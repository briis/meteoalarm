"""Tests for MeteoAlarm config flow."""

from custom_components.meteoalarm.config_flow import (
    STEP_USER_DATA_SCHEMA,
    ConfigFlow,
)
from custom_components.meteoalarm.const import (
    CONF_COUNTRY,
    CONF_LANGUAGE,
    CONF_NAME,
    CONF_PROVINCE,
)


class TestConfigFlow:
    """Test the MeteoAlarm config flow."""

    def test_config_flow_creation(self):
        """Test that config flow can be instantiated."""
        config_flow = ConfigFlow()
        assert config_flow.VERSION == 1

    def test_config_flow_constants(self):
        """Test that the schema has required constants."""
        # Check that the schema has the required keys
        schema = STEP_USER_DATA_SCHEMA.schema
        assert CONF_COUNTRY in schema
        assert CONF_PROVINCE in schema
        assert CONF_LANGUAGE in schema
        assert CONF_NAME in schema
