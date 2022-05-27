"""Support for Flo Water Monitor binary sensors."""
from __future__ import annotations

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .device import LinkTapDeviceDataUpdateCoordinator
from .entity import LinkTapEntity


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Flo sensors from config entry."""
    devices: list[LinkTapDeviceDataUpdateCoordinator] = hass.data[DOMAIN][
        config_entry.entry_id
    ]["devices"]
    entities: list[BinarySensorEntity] = []
    for device in devices:
        entities.append(LinkTapLeakDetectedBinarySensor(device))
        entities.append(LinkTapClogDetectedBinarySensor(device))
        entities.append(LinkTapHasNoWaterDetectedBinarySensor(device))
        entities.append(LinkTapValveBrokenDetectedBinarySensor(device))
        async_add_entities(entities)


class LinkTapLeakDetectedBinarySensor(LinkTapEntity, BinarySensorEntity):
    """Binary sensor that reports if water is detected (for leak detectors)."""

    _attr_device_class = BinarySensorDeviceClass.PROBLEM

    def __init__(self, device):
        """Initialize the pending alerts binary sensor."""
        super().__init__("leak_detected", "Leak Detected", device)

    @property
    def is_on(self):
        """Return true if the Flo device is detecting water."""
        return self._device.is_leaking

    
class LinkTapClogDetectedBinarySensor(LinkTapEntity, BinarySensorEntity):
    """Binary sensor that reports if water is detected (for leak detectors)."""

    _attr_device_class = BinarySensorDeviceClass.PROBLEM

    def __init__(self, device):
        """Initialize the pending alerts binary sensor."""
        super().__init__("clog_detected", "Clog Detected", device)

    @property
    def is_on(self):
        """Return true if the LinkTap device is clogged"""
        return self._device.is_clogged
    
class LinkTapHasNoWaterDetectedBinarySensor(LinkTapEntity, BinarySensorEntity):
    """Binary sensor that reports if water is detected (for leak detectors)."""

    _attr_device_class = BinarySensorDeviceClass.PROBLEM

    def __init__(self, device):
        """Initialize the pending alerts binary sensor."""
        super().__init__("has_nowater", "Has no Water", device)

    @property
    def is_on(self):
        """Return true if the LinkTap device is clogged"""
        return self._device.has_nowater
                    
class LinkTapValveBrokenDetectedBinarySensor(LinkTapEntity, BinarySensorEntity):
    """Binary sensor that reports if water is detected (for leak detectors)."""

    _attr_device_class = BinarySensorDeviceClass.PROBLEM

    def __init__(self, device):
        """Initialize the pending alerts binary sensor."""
        super().__init__("valve_broken", "Valve Broken", device)

    @property
    def is_on(self):
        """Return true if the LinkTap device is clogged"""
        return self._device.is_valve_broken                       
