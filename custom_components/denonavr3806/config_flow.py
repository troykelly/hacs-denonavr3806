"""Config flow for Denon AVR 3806 integration."""
import logging

import voluptuous as vol

from homeassistant import config_entries, core, exceptions
import homeassistant.helpers.config_validation as cv
from homeassistant.const import (
    CONF_HOST,
    CONF_PORT,
    CONF_NAME,
)

from denon_avr_serial_over_ip import DenonAVR

from .const import (
    DOMAIN,
    DEFAULT_NAME,
    DEFAULT_HOST,
    DEFAULT_PORT,
    DESCRIPTION_NAME,
    DESCRIPTION_HOST,
    DESCRIPTION_PORT,
)  # pylint:disable=unused-import

_LOGGER = logging.getLogger(__name__)

# DATA_SCHEMA = vol.Schema(
#     {
#         vol.Required(CONF_NAME, default=DEFAULT_NAME): vol.All(str, vol.Length(min=1)),
#         vol.Required(CONF_HOST): vol.All(str, vol.Length(min=1)),
#         vol.Required(CONF_PORT, default=23): vol.All(int, vol.Length(min=1)),
#     }
# )


DATA_SCHEMA = vol.Schema(
    {
        vol.Required(
            CONF_NAME, default=DEFAULT_NAME, description=DESCRIPTION_NAME
        ): vol.All(str, vol.Length(min=1)),
        vol.Required(
            CONF_HOST, default=DEFAULT_HOST, description=DESCRIPTION_HOST
        ): vol.All(str, vol.Length(min=1)),
        vol.Required(
            CONF_PORT, default=DEFAULT_PORT, description=DESCRIPTION_PORT
        ): vol.All(vol.Coerce(int), vol.Range(min=1, max=65535)),
    }
)


async def validate_input(hass: core.HomeAssistant, data):
    """Validate the user input allows us to connect.

    Data has the keys from DATA_SCHEMA with values provided by the user.
    """

    api = DenonAVR(host=data["host"], port=data["port"], loop=hass.loop)

    try:
        await api.connect()
    except:
        raise CannotConnect

    return {
        "title": "Denon AVR",
        "name": data["name"],
        "host": data["host"],
        "port": data["port"],
    }


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Denon AVR 3806."""

    VERSION = 1
    # TODO pick one of the available connection classes in homeassistant/config_entries.py
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)

                return self.async_create_entry(title=info["title"], data=user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )


class CannotConnect(exceptions.HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(exceptions.HomeAssistantError):
    """Error to indicate there is invalid auth."""
