"""Support for GLZ Radio stations."""

import logging
import aiohttp
import xml.etree.ElementTree as ET
from datetime import timedelta, datetime
import pytz
from homeassistant.components.media_player import (
    MediaPlayerEntity,
    MediaPlayerEntityFeature,
    MediaType,
    MediaClass,
    BrowseMedia,
    ATTR_MEDIA_TITLE,
    ATTR_MEDIA_ARTIST,
    ATTR_MEDIA_ALBUM_NAME,
)
from homeassistant.const import (
    STATE_IDLE,
    STATE_PLAYING,
    ATTR_ENTITY_PICTURE,
)
from homeassistant.util import Throttle

from .const import STATIONS, NAME

_LOGGER = logging.getLogger(__name__)
UPDATE_THROTTLE = timedelta(seconds=3)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the GLZ Radio platform from a config entry."""
    async_add_entities([GlzRadioPlayer(hass)])


class GlzRadioPlayer(MediaPlayerEntity):
    """Representation of a GLZ Radio Player."""

    def __init__(self, hass):
        """Initialize the player."""
        self.hass = hass
        self._state = STATE_IDLE
        self._attr_name = "GLZ Radio"
        self._attr_unique_id = "glz_radio_player_ui"
        self._attr_has_entity_name = True

        # Internal state
        self._current_station_id = None
        self._station_name = "GLZ Radio"
        self._song_title = None
        self._song_artist = None
        self._media_image_url = None
        self._onair_url = None
        self._stream_url = None
        self._next_track_time = None
        # Remote Player Logic
        self._remote_player_entity = (
            None  # The entity_id of the real speaker (e.g., media_player.nest_hub)
        )
        self._source_list = ["Local (Virtual)"]
        self._selected_source = "Local (Virtual)"

    @property
    def state(self):
        return self._state

    @property
    def supported_features(self):
        """Flag media player features that are supported."""
        features = (
            MediaPlayerEntityFeature.PLAY_MEDIA
            | MediaPlayerEntityFeature.BROWSE_MEDIA
            | MediaPlayerEntityFeature.STOP
            | MediaPlayerEntityFeature.PLAY
            | MediaPlayerEntityFeature.SELECT_SOURCE  # Enable Source Selection
        )
        return features

    @property
    def media_content_type(self):
        return MediaType.MUSIC

    @property
    def media_title(self):
        if self._song_title:
            return (
                f"{self._song_artist} - {self._song_title}"
                if self._song_title
                else self._station_name
            )
        return self._station_name

    @property
    def media_artist(self):
        return self._song_artist

    @property
    def media_image_url(self):
        return self._media_image_url

    @property
    def source_list(self):
        """Return a list of available input sources (other media players)."""
        # Dynamically find all other media_players in Home Assistant
        players = ["Local (Virtual)"]
        all_entities = self.hass.states.async_entity_ids("media_player")
        for entity_id in all_entities:
            if entity_id != self.entity_id:  # Don't list myself
                players.append(entity_id)
        return players

    @property
    def source(self):
        """Return the current input source."""
        return self._selected_source

    async def async_select_source(self, source):
        """Select input source."""
        self._selected_source = source
        if source == "Local (Virtual)":
            self._remote_player_entity = None
        else:
            self._remote_player_entity = source

        # If we are currently playing, we might want to restart playback on the new source
        # But for now, just save the preference.
        self.async_write_ha_state()

    async def async_play_media(self, media_type, media_id, **kwargs):
        """Play a piece of media."""
        selected_station = None

        # Find station by ID or URL
        if media_id in STATIONS:
            selected_station = STATIONS[media_id]
        else:
            for s_id, data in STATIONS.items():
                if data["url"] == media_id:
                    selected_station = data
                    break

        if selected_station:
            self._station_name = selected_station["name"]
            self._media_image_url = selected_station["thumbnail"]
            self._onair_url = selected_station.get("onair_url")
            self._stream_url = selected_station["url"]

            self._state = STATE_PLAYING
            self._song_title = None
            self._song_artist = None
            self._next_track_time = None

            # 1. Update Metadata (Fetch XML)
            await self.async_update_onair_info()
            self.async_write_ha_state()

            # 2. Handle Audio Output
            if self._remote_player_entity:
                # If a remote player (Nest Hub) is selected, send the audio THERE.
                # We also send the metadata (Title/Image) so the Nest Hub screen updates!
                title = (
                    f"{self._song_artist} - {self._song_title}"
                    if self._song_title
                    else self._station_name
                )
                data = {
                    "entity_id": self._remote_player_entity,
                    "media_content_id": self._stream_url,
                    "media_content_type": "audio/mpeg",
                    "extra": {
                        "title": self._station_name,
                        "thumb": self._media_image_url,
                        "metadata": {
                            "metadataType": 3,
                            "title": self._station_name,
                            "artist": NAME,
                            "images": [{"url": self._media_image_url}],
                        },
                    },
                }
                await self.hass.services.async_call("media_player", "play_media", data)
                self.update_remote_attributes()

        else:
            _LOGGER.error("Station not found for media_id: %s", media_id)

    async def async_media_stop(self):
        """Stop the media player."""
        self._state = STATE_IDLE
        self._song_title = None
        self._song_artist = None

        # Stop remote player too
        if self._remote_player_entity:
            await self.hass.services.async_call(
                "media_player", "media_stop", {"entity_id": self._remote_player_entity}
            )

        self.async_write_ha_state()

    async def async_browse_media(self, media_content_type=None, media_content_id=None):
        """Implement the websocket media browsing helper."""
        return await self.hass.async_add_executor_job(
            self._build_browse_media, media_content_type, media_content_id
        )

    def _build_browse_media(self, media_content_type, media_content_id):
        """Create the BrowseMedia objects."""
        if media_content_type in [None, "library"]:
            children = []
            for station_id, data in STATIONS.items():
                children.append(
                    BrowseMedia(
                        title=data["name"],
                        media_class=MediaClass.MUSIC,
                        media_content_id=station_id,
                        media_content_type=MediaType.MUSIC,
                        can_play=True,
                        can_expand=False,
                        thumbnail=data["thumbnail"],
                    )
                )

            return BrowseMedia(
                title="GLZ Radio Stations",
                media_class=MediaClass.DIRECTORY,
                media_content_id="glz_root",
                media_content_type="library",
                can_play=False,
                can_expand=True,
                children=children,
            )

    @Throttle(UPDATE_THROTTLE)
    async def async_update(self):
        """Get the latest details from the OnAir XML."""
        if self._state == STATE_PLAYING and self._onair_url:
            await self.async_update_onair_info()

    async def async_update_onair_info(self):
        """Fetch XML and parse artist/title from <Current> tag."""

        if self._next_track_time:
            time_format = "%Y-%m-%dT%H:%M:%S.%f"
            next_track_time = datetime.strptime(self._next_track_time, time_format)
            next_track_time = next_track_time.replace(tzinfo=pytz.UTC)
            current_time = pytz.timezone(self.hass.config.time_zone).localize(
                datetime.now()
            )
            if next_track_time < current_time:
                return
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self._onair_url) as response:
                    if response.status == 200:
                        xml_data = await response.text()
                        root = ET.fromstring(xml_data)

                        next_node = root.find("Next")
                        if next_node is not None:
                            next_time_node = next_node.find("startTime")
                            if next_time_node is not None:
                                self._next_track_time = next_time_node.text
                        # 1. Find the <Current> tag
                        current_node = root.find("Current")
                        if current_node is not None:
                            # 2. Extract titleName and artistName
                            title_node = current_node.find("titleName")
                            artist_node = current_node.find("artistName")

                            new_title = (
                                title_node.text
                                if title_node is not None
                                else self._station_name
                            )
                            new_artist = (
                                artist_node.text if artist_node is not None else NAME
                            )

                            self._song_title = new_title
                            self._song_artist = new_artist
                            if self._remote_player_entity:
                                self.update_remote_attributes()
                            self.async_write_ha_state()
                        else:
                            # Fallback or clear if no current info
                            pass

        except Exception as e:
            _LOGGER.debug("Error fetching onair info: %s", e)

    def update_remote_attributes(self):
        inputStateObject = self.hass.states.get(self._remote_player_entity)
        inputState = inputStateObject.state
        inputAttributesObject = inputStateObject.attributes.copy()
        inputAttributesObject[ATTR_MEDIA_TITLE] = (
            self._song_title if self._song_title else self._station_name
        )
        inputAttributesObject[ATTR_MEDIA_ARTIST] = self._song_artist
        self.hass.states.async_set(
            self._remote_player_entity,
            inputState,
            inputAttributesObject,
        )
