# Copyright (c) 2026 Bjarne Riis
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


async def _validate_input(data: dict[str, Any]) -> None:
    """Validate the user input allows us to connect."""
    try:
        api = Meteoalert(data[CONF_COUNTRY], data[CONF_PROVINCE], data[CONF_LANGUAGE])
        await asyncio.to_thread(api.get_alert)
    except KeyError:
        raise InvalidAuthError from None
    except Exception as exc:  # pylint: disable=broad-except
        _LOGGER.exception("Error connecting to MeteoAlarm API")
        raise CannotConnectError from exc


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for MeteoAlarm."""

    VERSION = 1

    @staticmethod
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> OptionsFlowHandler:
        """Return the options flow handler."""
        return OptionsFlowHandler(config_entry)

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> Any:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                await _validate_input(user_input)
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


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle MeteoAlarm options."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self._config_entry = config_entry

    async def async_step_init(self, user_input: dict[str, Any] | None = None) -> Any:
        """Manage the options."""
        errors: dict[str, str] = {}
        current = {**self._config_entry.data, **self._config_entry.options}

        if user_input is not None:
            try:
                await _validate_input(user_input)
            except CannotConnectError:
                errors["base"] = "cannot_connect"
            except InvalidAuthError:
                errors["base"] = "invalid_auth"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                self.hass.config_entries.async_update_entry(
                    self._config_entry, title=user_input[CONF_NAME]
                )
                return self.async_create_entry(title="", data=user_input)

        schema = vol.Schema(
            {
                vol.Required(CONF_COUNTRY, default=current.get(CONF_COUNTRY, "")): str,
                vol.Required(
                    CONF_PROVINCE, default=current.get(CONF_PROVINCE, "")
                ): str,
                vol.Optional(
                    CONF_LANGUAGE, default=current.get(CONF_LANGUAGE, "en")
                ): str,
                vol.Optional(
                    CONF_NAME, default=current.get(CONF_NAME, "meteoalarm")
                ): str,
            }
        )

        return self.async_show_form(step_id="init", data_schema=schema, errors=errors)


class CannotConnectError(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuthError(HomeAssistantError):
    """Error to indicate there is invalid auth."""
