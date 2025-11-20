"""Media Source implementation for GLZ Radio."""

from homeassistant.components.media_source.error import Unresolvable, MediaSourceError
from homeassistant.components.media_source.models import (
    BrowseMediaSource,
    MediaSource,
    MediaSourceItem,
    MediaClass,
    PlayMedia,
)

from .const import DOMAIN, STATIONS, NAME


async def async_get_media_source(hass):
    """Set up glz media source."""
    return GlzMediaSource(hass)


class GlzMediaSource(MediaSource):
    """Provide GLZ Radio stations as a global media source."""

    name = "GLZ Radio"

    def __init__(self, hass):
        """Initialize GLZ source."""
        super().__init__(DOMAIN)
        self.hass = hass

    async def async_resolve_media(self, item: MediaSourceItem) -> PlayMedia:
        """Resolve media to a url when a user clicks a station."""
        media_id = item.identifier
        station = STATIONS[media_id]

        data = {
            "entity_id": item.target_media_player,
            "media_content_id": station.get("url"),
            "media_content_type": "audio/mpeg",
            "extra": {
                "title": station.get("name"),
                "thumb": station.get("thumbnail"),
                "metadata": {
                    "metadataType": 3,
                    "title": station.get("thumbnail"),
                    "artist": NAME,
                    "images": [{"url": station.get("thumbnail")}],
                },
            },
        }
        await self.hass.services.async_call("media_player", "play_media", data)
        data = {
            "source": item.target_media_player,
            "entity_id": "media_player.glz_radio",
        }
        await self.hass.services.async_call("media_player", "select_source", data)

        data = {
            "media_content_id": station.get("url"),
            "media_content_type": "audio/mpeg",
            "entity_id": "media_player.glz_radio",
        }
        await self.hass.services.async_call("media_player", "play_media", data)
        raise Unresolvable(f"Please ignore this error.")
        return PlayMedia(STATIONS[media_id]["thumbnail"], "audio/mpeg")

    async def async_browse_media(self, item: MediaSourceItem) -> BrowseMediaSource:
        """Build the folder structure for the media browser."""

        # If item.identifier is set, the user is trying to browse *inside* a station,
        # which is impossible since stations are files, not folders.
        if item.identifier:
            raise MediaSourceError("This source does not support subfolders.")

        # Create the list of stations for the root folder
        children = []
        for station_id, data in STATIONS.items():
            children.append(
                BrowseMediaSource(
                    domain=DOMAIN,
                    identifier=station_id,
                    media_class=MediaClass.MUSIC,
                    media_content_type="audio/mpeg",
                    title=data["name"],
                    can_play=True,
                    can_expand=False,
                    thumbnail=data["thumbnail"],
                )
            )

        # Return the main "GLZ Radio" folder
        return BrowseMediaSource(
            domain=DOMAIN,
            identifier=None,
            media_class=MediaClass.DIRECTORY,
            media_content_type="audio/mpeg",
            title="GLZ Radio",
            can_play=False,
            can_expand=True,
            children_media_class=MediaClass.MUSIC,
            children=children,
        )
