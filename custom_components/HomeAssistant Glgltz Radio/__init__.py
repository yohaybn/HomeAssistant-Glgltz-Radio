"""The galgaltz_radio integration."""
import logging
from .const import DOMAIN
from types import SimpleNamespace
import json
import os
_LOGGER = logging.getLogger(__name__)

_JSON_FILE = os.path.join(os.path.dirname(__file__), "stations.json")


def read_stations_json():
    with open(_JSON_FILE) as f:
        data = json.load(f)
    return data
async def async_setup_entry(hass, config):
    """Handle the service call."""
    _LOGGER.debug("async_setup")
    
    sta=read_stations_json()
    _LOGGER.debug(sta)
    hass.data[DOMAIN]= sta
   

    return True
