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
            await self._update_device()
        except Exception as error:
            raise UpdateFailed(error) from error
    @property
    def location(self) -> str:
        return self._device_information['gateway_location']
    
    @property
    def id(self) -> str:
        return self._linktaper_id
    
    @property
    def device_name(self) -> str:
        LOGGER.error(self._device_information)
        return self._device_information['taplinkerName']
    
    @property
    def manufacturer(self) -> str:
        """Return manufacturer for device."""
        return self._manufacturer

    @property
    def battery_level(self) -> float:
        """Return the battery level for battery-powered device, e.g. leak detectors."""
        LOGGER.error(float(self._device_information["batteryStatus"].strip("%")))
        return float(self._device_information["batteryStatus"].strip("%"))
    
    @property 
    def sw_version(self) -> float:
        return self._device_information['gateway_version']
 
    @property
    def gw_connected(self) -> bool:
        if self._device_information['gateway_status'] == "Connected":
            return True
        return False
 
    @property
    def signal_strength(self) -> int:
        return self._device_information['signal']

    @property
    def is_clogged(self) -> bool:
        return self._device_information['clogFlag']  

    @property
    def is_leaking(self) -> bool:
        return self._device_information['leakFlag']  

    @property
    def has_nowater(self) -> bool:
        return self._device_information['noWater']  

    @property
    def is_valve_broken(self) -> bool:
        return self._device_information['valveBroken']  

    @property
    def has_fall(self) -> bool:
        return self._device_information['fall']  
    
    async def _update_device(self) -> None:
        """Update the device information from the API."""
        all_information = await self.hass.async_add_executor_job(self.api_client.get_all_devices)
        for gateway in all_information['devices']:
            for linktap in gateway['taplinker']:
                if linktap['taplinkerId'] == self._linktaper_id:
                    self._device_information = linktap
                    self._device_information['gateway_version'] = gateway['version']
                    self._device_information['gateway_status'] = gateway['status']
                    self._device_information['gateway_location'] = gateway['location']
        LOGGER.error("LinkTap device data: %s", self._device_information)
