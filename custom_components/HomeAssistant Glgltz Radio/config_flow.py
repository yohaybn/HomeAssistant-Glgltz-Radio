"""Adds config flow for GlgltzRadio."""
from __future__ import annotations

from homeassistant import config_entries
import voluptuous as vol


from .const import DOMAIN, LOGGER


class GlgltzRadioFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for GlgltzRadio."""



    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            # Here you can perform any necessary validation or configuration steps
            return self.async_create_entry(title="Custom Integration", data={})
        return self.async_show_form(step_id="user", data_schema=vol.Schema({}))

    async def async_setup(hass: core.HomeAssistant, config: dict):
        """Set up the custom integration."""
        hass.data[DOMAIN] = {}
        return True

#
#    VERSION = 1
#    MINOR_VERSION = 1
#
#    async def async_step_user(self, user_input=None):
#        #if user_input is None:
#        #    return await self._async_show_form(step="user")
##
#        ## Validate user input here
#        ## ...
#        return self.async_set_entry(title="title", data="data")
#        #return self.async_create_entry(title=user_input["name"], data=user_input)
#
#    async def _async_show_form(self, step="user", data=None, errors=None):
#        """Show the configuration form to the user."""
#        return self.async_show_form(
#            step=step,
#            data_schema=async_schema(data),
#            errors=errors,
#            # Additional form options (optional)
#        )
#    async def async_create_entry(self, title, data):
#        """Create a config entry from user data."""
#        return self.async_set_entry(title=title, data=data)
