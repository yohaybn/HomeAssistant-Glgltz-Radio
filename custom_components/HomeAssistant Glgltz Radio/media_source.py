"""Expose GlgltzRadio as a media source."""
from __future__ import annotations

# import mimetypes


from homeassistant.components.media_player import BrowseError, MediaClass, MediaType
from homeassistant.components.media_source.error import Unresolvable
from homeassistant.components.media_source.models import (
    BrowseMediaSource,
    MediaSource,
    MediaSourceItem,
    PlayMedia,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN


async def async_get_media_source(hass: HomeAssistant) -> GlgltzRadioMediaSource:
    """Set up GlgltzRadio Browser media source."""
    entry = hass.config_entries.async_entries(DOMAIN)
    return GlgltzRadioMediaSource(hass, entry)


class GlgltzRadioMediaSource(MediaSource):
    """Provide Radio stations as media sources."""

    name = "Glgltz Radio Browser"

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize RadioMediaSource."""
        super().__init__(DOMAIN)
        self.hass = hass
        self.entry = entry

    @property
    def stations(self) -> BrowseMediaSource | None:
        """Return the stations."""
        return self.hass.data.get(DOMAIN).get("stations")

    async def async_resolve_media(self, item: MediaSourceItem) -> PlayMedia:
        """Resolve selected TV station to a streaming URL."""
        stations = self.stations
        if stations is None:
            raise Unresolvable("Glgltz Radio Browser not initialized")

        station = stations[item.identifier]
        return PlayMedia(station["url"], MediaType.MUSIC)

    async def async_browse_media(
        self,
        item: MediaSourceItem,
    ) -> BrowseMediaSource:
        """Return media."""

        return BrowseMediaSource(
            domain=DOMAIN,
            identifier=None,
            media_class=MediaClass.CHANNEL,
            media_content_type=MediaType.MUSIC,
            title="גלגלצ",
            can_play=False,
            can_expand=True,
            thumbnail="https://upload.wikimedia.org/wikipedia/he/thumb/4/40/Galgalz.svg/150px-Galgalz.svg.png",
            children_media_class=MediaClass.DIRECTORY,
            children=[*await self._async_build_channels()],
        )

    async def _async_build_channels(self) -> list[BrowseMediaSource]:
        items: list[BrowseMediaSource] = []

        for station in self.stations:

                items.append(
                    BrowseMediaSource(
                        domain=DOMAIN,
                        identifier=self.stations[station]["id"],
                        media_class=MediaClass.MUSIC,
                        media_content_type="audio/mpeg",
                        title=self.stations[station]["name"],
                        can_play=True,
                        can_expand=False,
                        thumbnail=self.stations[station]["thumbnail"],
                    )
                )

        return items
