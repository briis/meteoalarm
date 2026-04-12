"""Binary Sensor for MeteoAlarm.eu."""

from __future__ import annotations

import asyncio
import logging
from datetime import timedelta
from typing import TYPE_CHECKING

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.util import dt as dt_util
from meteoalertapi import Meteoalert

from .const import CONF_COUNTRY, CONF_LANGUAGE, CONF_NAME, CONF_PROVINCE

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

_LOGGER = logging.getLogger(__name__)

ATTRIBUTION = "Information provided by MeteoAlarm"

DEFAULT_NAME = "meteoalarm"

SCAN_INTERVAL = timedelta(minutes=5)


async def async_setup_entry(
    _hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the MeteoAlarm binary sensor from a config entry."""
    config = config_entry.data

    country = config[CONF_COUNTRY]
    province = config[CONF_PROVINCE]
    language = config[CONF_LANGUAGE]
    name = config[CONF_NAME]

    try:
        api = Meteoalert(country, province, language)
    except KeyError:
        _LOGGER.exception("Wrong country digits or province name")
        return

    async_add_entities(
        [MeteoAlertBinarySensor(api, name, config_entry.entry_id)],
        update_before_add=True,
    )


class MeteoAlertBinarySensor(BinarySensorEntity):
    """Representation of a MeteoAlert binary sensor."""

    _attr_attribution = ATTRIBUTION
    _attr_device_class = BinarySensorDeviceClass.SAFETY

    def __init__(self, api: Meteoalert, name: str, entry_id: str | None = None) -> None:
        """Initialize the MeteoAlert binary sensor."""
        self._attr_name = name
        if entry_id:
            self._attr_unique_id = f"{entry_id}_{name}"
        self._api = api

    async def async_update(self) -> None:
        """Update device state."""
        self._attr_extra_state_attributes = {}
        self._attr_is_on = False

        try:
            alert = await asyncio.to_thread(self._api.get_alert)
            if alert:
                expiration_date = dt_util.parse_datetime(alert["expires"])

                if expiration_date is not None and expiration_date > dt_util.utcnow():
                    self._attr_extra_state_attributes = alert
                    self._attr_is_on = True
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception("Error updating MeteoAlarm sensor")
