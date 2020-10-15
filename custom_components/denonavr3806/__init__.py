"""The Denon AVR 3806 integration."""
import asyncio

import voluptuous as vol

from homeassistant import exceptions
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from denon_avr_serial_over_ip import DenonAVR

from .const import DOMAIN

CONFIG_SCHEMA = vol.Schema({DOMAIN: vol.Schema({})}, extra=vol.ALLOW_EXTRA)

PLATFORMS = ["media_player"]


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Denon AVR 3806 component."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Denon AVR 3806 from a config entry."""

    if not DOMAIN in hass.data:
        hass.data[DOMAIN] = {}

    host = entry.data["host"] if "host" in entry.data else None
    port = entry.data["port"] if "port" in entry.data else None

    hass.data[DOMAIN][entry.entry_id] = DenonAVR(loop=hass.loop, host=host, port=port)

    if host and port:
        try:
            await hass.data[DOMAIN][entry.entry_id].connect()
        except:
            raise CannotConnect

    for component in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, component)
        )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, component)
                for component in PLATFORMS
            ]
        )
    )
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


class CannotConnect(exceptions.HomeAssistantError):
    """Error to indicate we cannot connect."""
