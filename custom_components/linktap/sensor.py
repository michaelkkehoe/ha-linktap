"""Support for Flo Water Monitor sensors."""
from __future__ import annotations

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    PERCENTAGE,
    SIGNAL_STRENGTH_DECIBELS_MILLIWATT
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .device import LinkTapDeviceDataUpdateCoordinator
from .entity import LinkTapEntity

NAME_BATTERY = "Battery"
NAME_DEVICE_WATER_FLOW = "Device flow rate"
VOLUME_MILLILITERS_PER_MINUTE: Final = "mL/m"

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

class LinkTapFlowVelocitySensor(LinkTapEntity, SensorEntity):
    """Monitors the flow velocity when watering"""

    _attr_device_class = "flow_rate"
    _attr_native_unit_of_measurement = VOLUME_MILLILITERS_PER_MINUTE

    def __init__(self, device):
        """Initialize the flow velocity sensor."""
        super().__init__("vel", "Flow Velocity", device)
        self._state: float = None

    @property
    def native_value(self) -> float | None:
        """Return the current  water flow velocity"""
        return self._device.flow_velocity


class LinkTapSignalStrengthSensor(LinkTapEntity, SensorEntity):
    """Monitors the signal strength of the device"""

    _attr_device_class = SensorDeviceClass.SIGNAL_STRENGTH
    _attr_native_unit_of_measurement = SIGNAL_STRENGTH_DECIBELS_MILLIWATT
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, device):
        """Initialize the flow velocity sensor."""
        super().__init__("signal_strength", "Signal Strength", device)
        self._state: float = None

    @property
    def native_value(self) -> float | None:
        """Return the current  water flow velocity"""
        return self._device.signal_strength
