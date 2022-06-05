"""Support for TPLink lights."""
from __future__ import annotations

from collections.abc import Sequence
import logging
from typing import Any, Final


from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .device import LinkTapDeviceDataUpdateCoordinator
from .entity import  LinkTapEntity

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    devices: list[LinkTapDeviceDataUpdateCoordinator] = hass.data[DOMAIN][
        config_entry.entry_id
    ]["devices"]
    entities = []
    for device in devices:
        entities.extend(
            [
                InstantModeSwitch(device),
            ]
       )
    async_add_entities(entities)

class InstantModeSwitch(LinkTapEntity, SwitchEntity):
    """Representation of a LinkTap switch."""

    def __init__(
        self,
        device: LinkTapDeviceDataUpdateCoordinator,
    ) -> None:
        """Initialize the switch."""
        super().__init__(device)

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        await self.device.turn_on(**kwargs)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        await self.device.turn_off()
