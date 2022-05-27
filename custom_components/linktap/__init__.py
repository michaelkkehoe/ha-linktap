"""The flo integration."""
import asyncio
import logging

from linktap.LinkTap import LinkTap

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_API_KEY, CONF_USERNAME, Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN
from .device import LinkTapDeviceDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

# PLATFORMS = [Platform.BINARY_SENSOR, Platform.SENSOR, Platform.SWITCH]
PLATFORMS = [Platform.BINARY_SENSOR, Platform.SENSOR]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up flo from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {}
    try:
        hass.data[DOMAIN][entry.entry_id]["client"] = client = LinkTap(
            entry.data[CONF_USERNAME], entry.data[CONF_API_KEY]
        )
    except Exception as err:
        raise ConfigEntryNotReady from err
    linktap_data = await hass.async_add_executor_job(client.get_all_devices)

    _LOGGER.error("Linktap Devices: %s", linktap_data)
    
    hass.data[DOMAIN][entry.entry_id]["devices"] = devices = [
        LinkTapDeviceDataUpdateCoordinator(hass, client, gateway['gatewayId'], device["taplinkerId"])
        for gateway in linktap_data['devices']
        for device in gateway['taplinker']
    ]

    tasks = [device.async_refresh() for device in devices]
    await asyncio.gather(*tasks)
    hass.config_entries.async_setup_platforms(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
