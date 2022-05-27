"""Base entity class for Flo entities."""
from __future__ import annotations

from typing import Any

from homeassistant.helpers.device_registry import CONNECTION_NETWORK_MAC
from homeassistant.helpers.entity import DeviceInfo, Entity

from .const import DOMAIN
from .device import LinkTapDeviceDataUpdateCoordinator


class LinkTapEntity(Entity):
    """A base class for LinkTap entities."""

    _attr_force_update = False
    _attr_should_poll = False

    def __init__(
        self,
        entity_type: str,
        name: str,
        device: LinkTapDeviceDataUpdateCoordinator,
        **kwargs,
    ) -> None:
        """Init LinkTap entity."""
        self._attr_name = name
        self._attr_unique_id = f"{device.linktaper_id}_{entity_type}"

        self._device: LinkTapDeviceDataUpdateCoordinator = device
        self._state: Any = None

    @property
    def device_info(self) -> DeviceInfo:
        """Return a device description for device registry."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._device.linktaper_id)},
            manufacturer=self._device.manufacturer,
            name=self._device.device_name,
        )

    @property
    def available(self) -> bool:
        """Return True if device is available."""
        if self._device.status == "Connected":
            return True
        return False

    async def async_update(self):
        """Update Flo entity."""
        await self._device.async_request_refresh()

    async def async_added_to_hass(self):
        """When entity is added to hass."""
        self.async_on_remove(self._device.async_add_listener(self.async_write_ha_state))
