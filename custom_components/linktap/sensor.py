"""Support for Flo Water Monitor sensors."""
from __future__ import annotations

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    PERCENTAGE,
    PRESSURE_PSI,
    TEMP_FAHRENHEIT,
    VOLUME_GALLONS,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .device import LinkTapDeviceDataUpdateCoordinator
from .entity import LinkTapEntity

WATER_ICON = "mdi:water"
GAUGE_ICON = "mdi:gauge"
NAME_DAILY_USAGE = "Today's Water Usage"
NAME_CURRENT_SYSTEM_MODE = "Current System Mode"
NAME_FLOW_RATE = "Water Flow Rate"
NAME_WATER_TEMPERATURE = "Water Temperature"
NAME_AIR_TEMPERATURE = "Temperature"
NAME_WATER_PRESSURE = "Water Pressure"
NAME_HUMIDITY = "Humidity"
NAME_BATTERY = "Battery"


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Flo sensors from config entry."""
    devices: list[LinkTapDeviceDataUpdateCoordinator] = hass.data[DOMAIN][
        config_entry.entry_id
    ]["devices"]
    entities = []
    for device in devices:
        entities.extend(
            [
                LinkTapBatterySensor(device),
            ]
       )
    async_add_entities(entities)


class LinkTapBatterySensor(LinkTapEntity, SensorEntity):
    """Monitors the battery level for battery-powered leak detectors."""

    _attr_device_class = SensorDeviceClass.BATTERY
    _attr_native_unit_of_measurement = PERCENTAGE

    def __init__(self, device):
        """Initialize the battery sensor."""
        super().__init__("battery", NAME_BATTERY, device)
        self._state: float = None

    @property
    def native_value(self) -> float | None:
        """Return the current battery level."""
        return self._device.battery_level
