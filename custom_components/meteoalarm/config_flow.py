"""Config flow for MeteoAlarm integration."""

from __future__ import annotations

import asyncio
import logging
from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.exceptions import HomeAssistantError
from meteoalertapi import Meteoalert

from .const import CONF_COUNTRY, CONF_LANGUAGE, CONF_NAME, CONF_PROVINCE, DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_COUNTRY): str,
        vol.Required(CONF_PROVINCE): str,
        vol.Optional(CONF_LANGUAGE, default="en"): str,
        vol.Optional(CONF_NAME, default="meteoalarm"): str,
    }
)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for MeteoAlarm."""

    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> Any:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                await self._validate_input(user_input)
            except CannotConnectError:
                errors["base"] = "cannot_connect"
            except InvalidAuthError:
                errors["base"] = "invalid_auth"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(
                    title=user_input[CONF_NAME], data=user_input
                )

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )

    async def _validate_input(self, data: dict[str, Any]) -> None:
        """Validate the user input allows us to connect."""
        # Test the connection to the API
        try:
            api = Meteoalert(
                data[CONF_COUNTRY], data[CONF_PROVINCE], data[CONF_LANGUAGE]
            )
            # Try to get alert to validate
            await asyncio.to_thread(api.get_alert)
        except KeyError:
            raise InvalidAuthError from None
        except Exception as exc:  # pylint: disable=broad-except
            _LOGGER.exception("Error connecting to MeteoAlarm API")
            raise CannotConnectError from exc


class CannotConnectError(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuthError(HomeAssistantError):
    """Error to indicate there is invalid auth."""
