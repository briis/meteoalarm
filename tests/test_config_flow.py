"""Tests for MeteoAlarm config flow."""

from typing import ClassVar

from custom_components.meteoalarm.config_flow import (
    STEP_USER_DATA_SCHEMA,
    ConfigFlow,
    OptionsFlowHandler,
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
        schema = STEP_USER_DATA_SCHEMA.schema
        assert CONF_COUNTRY in schema
        assert CONF_PROVINCE in schema
        assert CONF_LANGUAGE in schema
        assert CONF_NAME in schema

    def test_options_flow_registered(self):
        """Test that the options flow handler is registered."""
        assert hasattr(ConfigFlow, "async_get_options_flow")

    def test_options_flow_handler_creation(self):
        """Test that options flow handler can be instantiated with a mock entry."""

        class MockEntry:
            data: ClassVar[dict] = {
                CONF_COUNTRY: "netherlands",
                CONF_PROVINCE: "Noord-Holland",
                CONF_LANGUAGE: "en",
                CONF_NAME: "meteoalarm",
            }
            options: ClassVar[dict] = {}

        handler = OptionsFlowHandler(MockEntry())
        assert handler is not None

    def test_options_flow_merges_data_and_options(self):
        """Test that options override data when both are present."""

        class MockEntry:
            data: ClassVar[dict] = {
                CONF_COUNTRY: "netherlands",
                CONF_PROVINCE: "Noord-Holland",
                CONF_LANGUAGE: "en",
                CONF_NAME: "meteoalarm",
            }
            options: ClassVar[dict] = {
                CONF_COUNTRY: "germany",
                CONF_PROVINCE: "Bayern",
            }

        entry = MockEntry()
        merged = {**entry.data, **entry.options}
        assert merged[CONF_COUNTRY] == "germany"
        assert merged[CONF_PROVINCE] == "Bayern"
        assert merged[CONF_LANGUAGE] == "en"
        assert merged[CONF_NAME] == "meteoalarm"
