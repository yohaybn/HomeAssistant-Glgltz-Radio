"""Constants for the GLZ Radio integration."""

import logging
from typing import Final

_LOGGER: Final = logging.getLogger(__name__)

DOMAIN = "glgltz_radio"
NAME = "מוזיקה מגלגלצ"
# Your provided JSON data
STATIONS = {
    "7": {
        "id": 7,
        "url": "https://glzwizzlv.bynetcdn.com/glglz_mp3?awCollectionId=misc&awEpisodeId=glglz",
        "onair_url": "https://glzxml.blob.core.windows.net/dalet/glglz-onair/onair.xml",
        "thumbnail": "https://static.mytuner.mobi/media/tvos_radios/UMXNpqqcaB.jpg",
        "name": "גלגלצ",
        "description": "גלגלצ",
    },
    "0": {
        "id": 0,
        "url": "http://glzwizzlv.bynetcdn.com/glz_mp3?awCollectionId=misc&awEpisodeId=glz",
        "onair_url": "https://glzxml.blob.core.windows.net/dalet/glz-onair/onair.xml",
        "thumbnail": "https://static.mytuner.mobi/media/tvos_radios/tRrTN96R4x.png",
        "name": "גלצ",
        "description": "גלי צהל",
    },
    "1": {
        "id": 1,
        "url": "https://api.bynetcdn.com/Redirector/glz/glglz_sofshavua/ICE-LIVE",
        "thumbnail": "https://glz.co.il/media/51451/1.png",
        "name": "סופשבוע רגוע",
        "description": "מוזיקה שנעים איתה",
        "onair_url": "https://glzxml.blob.core.windows.net/dalet/Sof_Shavua_Ragua-On-Air/onair.xml",
    },
    "2": {
        "id": 2,
        "url": "https://api.bynetcdn.com/Redirector/glz/glglz_hits/ICE-LIVE",
        "onair_url": "https://glzxml.blob.core.windows.net/dalet/New_Hits-On-Air/onair.xml",
        "thumbnail": "https://glz.co.il/media/55157/סטרימינג-חדשים.png",
        "name": "פופ-אפ!",
        "description": "להיטים מרימים... וגם מרגשים!",
    },
    "3": {
        "id": 3,
        "url": "https://api.bynetcdn.com/Redirector/glz/glglz_classicil/ICE-LIVE",
        "onair_url": "https://glzxml.blob.core.windows.net/dalet/Gal_eivri-OnAir/onair.xml",
        "thumbnail": "https://glz.co.il/media/51453/3.png",
        "name": "גל עברי",
        "description": "רק מוזיקה ישראלית",
    },
    "4": {
        "id": 4,
        "url": "https://api.bynetcdn.com/Redirector/glz/glglz_med/ICE-LIVE",
        "onair_url": "https://glzxml.blob.core.windows.net/dalet/Yam_Tichoni-OnAir/onair.xml",
        "thumbnail": "https://glz.co.il/media/51463/4.png",
        "name": "ים תיכוני",
        "description": "הצליל הים תיכוני של ישראל. שירים מעולים מפעם וגם מהיום",
    },
    "5": {
        "id": 5,
        "url": "https://api.bynetcdn.com/Redirector/glz/glglz_rock/ICE-LIVE",
        "onair_url": "https://glzxml.blob.core.windows.net/dalet/Classic_Rock-On-Air/onair.xml",
        "thumbnail": "https://glz.co.il/media/51464/5.png",
        "name": "רוק קלאסי",
        "description": "קלאסיקות הרוק הגדולות והאהובות",
    },
    "6": {
        "id": 6,
        "url": "https://api.bynetcdn.com/Redirector/glz/glglz_alt/ICE-LIVE",
        "onair_url": "https://glzxml.blob.core.windows.net/dalet/Hasorim-OnAir/onair.xml",
        "thumbnail": "https://glz.co.il/media/51465/6.png",
        "name": "עשורים",
        "description": "השירים הגדולות ביותר משנות ה-70,80,90 וה-2000",
    },
}
