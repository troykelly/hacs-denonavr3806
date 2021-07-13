"""
Support for Denon AVR 3806 with IP to Serial.

For more details about this platform, please refer to the documentation at
https://github.com/troykelly/python-denon-avr-serial-over-ip/wiki
"""
from datetime import timedelta

import hashlib
import logging

import voluptuous as vol

from homeassistant.components.media_player import MediaPlayerEntity

from homeassistant.components.media_player.const import (
    SUPPORT_NEXT_TRACK,
    SUPPORT_PAUSE,
    SUPPORT_PLAY,
    SUPPORT_PREVIOUS_TRACK,
    SUPPORT_SELECT_SOURCE,
    SUPPORT_STOP,
    SUPPORT_TURN_OFF,
    SUPPORT_TURN_ON,
    SUPPORT_VOLUME_MUTE,
    SUPPORT_VOLUME_SET,
)
from homeassistant.const import (
    CONF_HOST,
    CONF_PORT,
    CONF_NAME,
    STATE_OFF,
    STATE_ON,
    STATE_UNKNOWN,
)

import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.typing import HomeAssistantType
from .const import DOMAIN, DEFAULT_NAME

_LOGGER = logging.getLogger(__name__)

DEFAULT_SCAN_INTERVAL = timedelta(seconds=30)
SCAN_INTERVAL = DEFAULT_SCAN_INTERVAL


SUPPORT_DENON = (
    SUPPORT_VOLUME_SET
    | SUPPORT_VOLUME_MUTE
    | SUPPORT_TURN_ON
    | SUPPORT_TURN_OFF
    | SUPPORT_SELECT_SOURCE
)
SUPPORT_MEDIA_MODES = (
    SUPPORT_PAUSE
    | SUPPORT_STOP
    | SUPPORT_PREVIOUS_TRACK
    | SUPPORT_NEXT_TRACK
    | SUPPORT_PLAY
)


async def async_setup_entry(hass: HomeAssistantType, entry, async_add_entities):
    """Configure a dispatcher connection based on a config entry."""

    api = hass.data[DOMAIN][entry.entry_id]

    if not "entity_ref" in hass.data[DOMAIN]:
        hass.data[DOMAIN]["entity_ref"] = {}

    if not "tasks" in hass.data[DOMAIN]:
        hass.data[DOMAIN]["tasks"] = {}

    hass.data[DOMAIN]["entity_ref"]["master"] = DenonDevice(
        hass, api.zone1, entry.data["name"]
    )
    hass.data[DOMAIN]["entity_ref"]["zone2"] = DenonDevice(
        hass, api.zone2, entry.data["name"]
    )
    hass.data[DOMAIN]["entity_ref"]["zone3"] = DenonDevice(
        hass, api.zone3, entry.data["name"]
    )

    entities = list()
    for entity_id in hass.data[DOMAIN]["entity_ref"]:
        _LOGGER.debug(
            "Adding entity (%s) %s to list with state: %s",
            hass.data[DOMAIN]["entity_ref"][entity_id].unique_id,
            hass.data[DOMAIN]["entity_ref"][entity_id].name,
            hass.data[DOMAIN]["entity_ref"][entity_id].state,
        )
        entities.append(hass.data[DOMAIN]["entity_ref"][entity_id])

    async_add_entities(entities)

    hass.data[DOMAIN]["tasks"]["update_tracker"] = api.poll(SCAN_INTERVAL)


class DenonDevice(MediaPlayerEntity):
    """Representation of a Denon device."""

    def __init__(self, hass, zone, name):
        """Initialize the Denon device."""
        self.__ha_name = name
        self.__zone = zone
        self.__hass = hass
        self.__zone.subscribe(self.async_device_changed)

    async def async_update(self):
        """Get the latest details from the device."""

    def async_device_changed(self, *args, **kwargs):
        """Send changed data to HA"""
        self.async_schedule_update_ha_state()

    @property
    def should_poll(self):
        return False

    @property
    def name(self):
        """Return the name of the device."""
        return f"{self.__ha_name} {self.__zone.name}"

    @property
    def unique_id(self):
        """Return the unique id of the device"""
        hash_object = hashlib.md5(self.__zone.unique_id.encode())
        return hash_object.hexdigest()

    @property
    def device_class(self):
        """Return the device class"""
        return "receiver"

    @property
    def state(self):
        """Return the state of the device."""
        if self.__zone.state == "On":
            return STATE_ON
        elif self.__zone.state == "Off":
            return STATE_OFF
        else:
            return STATE_UNKNOWN

    @property
    def volume_level(self):
        """Volume level of the media player (0..1)."""
        return self.__zone.volume_level

    @property
    def is_volume_muted(self):
        """Return boolean if volume is currently muted."""
        return self.__zone.is_volume_muted

    @property
    def source_list(self):
        """Return the list of available input sources."""
        return self.__zone.source_list

    @property
    def media_title(self):
        """Return the current media info."""
        return self.__zone.media_title

    @property
    def supported_features(self):
        """Flag media player features that are supported."""
        if self.__zone.media_mode:
            return SUPPORT_DENON | SUPPORT_MEDIA_MODES
        return SUPPORT_DENON

    @property
    def source(self):
        """Return the current input source."""
        return self.__zone.source

    def turn_off(self):
        """Turn off media player."""
        return self.__zone.turn_off()

    def volume_up(self):
        """Volume up media player."""
        return self.__zone.volume_up()

    def volume_down(self):
        """Volume down media player."""
        return self.__zone.volume_down()

    def set_volume_level(self, volume):
        """Set volume level, range 0..1."""
        return self.__zone.set_volume_level(volume)

    def mute_volume(self, mute):
        """Mute (true) or unmute (false) media player."""
        return self.__zone.mute_volume(mute)

    def media_play(self):
        """Play media player."""
        return self.__zone.media_play()

    def media_pause(self):
        """Pause media player."""
        return self.__zone.media_pause()

    def media_stop(self):
        """Pause media player."""
        return self.__zone.media_stop()

    def media_next_track(self):
        """Send the next track command."""
        return self.__zone.media_next_track()

    def media_previous_track(self):
        """Send the previous track command."""
        return self.__zone.media_previous_track()

    def turn_on(self):
        """Turn the media player on."""
        return self.__zone.turn_on()

    def select_source(self, source):
        """Select input source."""
        return self.__zone.select_source(source)
