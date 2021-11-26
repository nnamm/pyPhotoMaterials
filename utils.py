"""Utility"""

import logging
import sys

import requests

import settings

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)


def bool_from_str(text: str):
    """Convert text to boolean function.

    Convert boolean text to Boolean type in settings.ini.

    Args:
        text (str): Boolean text. (ex. True or False)

    Returns:
        bool: True if "true", False "false".

    """
    if text.lower() == "true":
        return True
    if text.lower() == "false":
        return False


def get_short_url(long_url: str) -> str:
    """Get short URL function.

    Shorten the specified Full-URL using Bitly.

    Args:
        long_url: Full-URL to be shortened.

    Returns:
        short_url: Shortened URL if success, blank string otherwise.

    """

    short_url = ""
    try:
        params = {"access_token": settings.bitly_access_token, "longurl": long_url}
        short_url = requests.get(settings.bitly_api_url, params=params).json()["data"][
            "url"
        ]
    except requests.exceptions.RequestException as e:
        logger.error({"action": "get_short_url", "error": e})
    return short_url
