"""Flo device object."""
from __future__ import annotations

import asyncio
from datetime import datetime, timedelta
from typing import Any

from linktap.LinkTap import LinkTap
from async_timeout import timeout

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
import homeassistant.util.dt as dt_util

from .const import DOMAIN, LOGGER


class LinkTapDeviceDataUpdateCoordinator(DataUpdateCoordinator):
    """LinkTap device object."""

    def __init__(
        self, hass: HomeAssistant, api_client: LinkTap, gateway_id: str, linktaper_id: str
    ) -> None:
        """Initialize the device."""
        self.hass: HomeAssistant = hass
        self.api_client: API = api_client
        self._gateway_id: str = gateway_id
        self._linktaper_id: str = linktaper_id
        self._manufacturer: str = "LinkTap"
        self._device_information: dict[str, Any] = {}
        self._water_usage: dict[str, Any] = {}
        super().__init__(
            hass,
            LOGGER,
            name=f"{DOMAIN}-{linktaper_id}",
            update_interval=timedelta(seconds=30),
        )

    async def _async_update_data(self):
        """Update data via library."""
        try:
            async with timeout(10):
                await asyncio.gather(
                    *[
                        self._update_device(),
                    ]
                )
        except Exception as error:
            raise UpdateFailed(error) from error

    async def _update_device(self, *_) -> None:
        """Update the device information from the API."""
        all_information = await self.hass.async_add_executor_job(self.api_client.get_all_devices)
        for gateway in all_information['devices']:
            for linktap in gateway['taplinker']:
                if linktap['taplinkerId'] == self._linktaper_id:
                    self._device_information = linktap
                    self._device_information['gateway_version'] = gateway['version']
                    self._device_information['status'] = gateway['status']                    
        LOGGER.error("LinkTap device data: %s", self._device_information)
