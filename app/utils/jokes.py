import random
import logging
from typing import Optional

import requests
from bs4 import BeautifulSoup


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "https://anekdotov.net/anekdot/black/index-page-"


def fetch_jokes_page(page_number: int) -> BeautifulSoup:
    """
    Fetch the jokes page from the specified URL and return the parsed HTML
    content.

    Args:
        page_number (int): The page number to fetch.

    Returns:
        BeautifulSoup: The parsed HTML content of the page.
    """
    url = f"{BASE_URL}{page_number}.html"
    logger.info(f"Fetching URL: {url}")
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def extract_jokes(soup: BeautifulSoup) -> list:
    """
    Extract jokes from the parsed HTML content.

    Args:
        soup (BeautifulSoup): The parsed HTML content.

    Returns:
        list: A list of joke elements.
    """
    jokes = soup.find_all("div", class_="anekdot")
    logger.info(f"Extracted {len(jokes)} jokes from the page.")
    return jokes


def get_random_joke() -> Optional[str]:
    """
    Get a random joke from the website.

    Returns:
        Optional[str]: A random joke text if available, otherwise None.
    """
    try:
        page_number = random.randint(1, 35)
        soup = fetch_jokes_page(page_number)
        jokes = extract_jokes(soup)
        if jokes:
            joke = random.choice(jokes)
            logger.info("Random joke selected.")
            return joke.text.strip()
        else:
            logger.warning("No jokes found on the page.")
            return None
    except requests.RequestException as e:
        logger.error(f"Error fetching jokes: {e}")
        return None
