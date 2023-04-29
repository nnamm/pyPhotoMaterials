"""Utility"""

import logging
import sys

import requests

import settings

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)


def bool_from_str(text: str) -> bool:
    """Convert text to boolean function.

    Convert boolean text to Boolean type in settings.ini.

    Args:
        text (str): Boolean text. (ex. True or False)

    Returns:
        bool: True if "true", False if "false".

    """
    if text.lower() == "true":
        return True
    if text.lower() == "false":
        return False
    raise ValueError("text is invalid.")


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
        headers = {
            "Authorization": f"Bearer {settings.bitly_access_token}",
            "Content-Type": "application/json",
        }
        data = f'{{"long_url": "{long_url}", "domain": "{settings.bitly_domain}"}}'

        res = requests.post(settings.bitly_api_url, headers=headers, data=data)
        if res.status_code != 200:
            logger.warn({"action": "get_short_url", "warn": "bit.ly error, retry"})
            return short_url
        short_url = res.json()["link"]
    except requests.exceptions.RequestException as err:
        logger.error({"action": "get_short_url", "error": err})
    return short_url
