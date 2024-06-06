import aiohttp
import asyncio
from bs4 import BeautifulSoup
import logging
logger = logging.getLogger(__name__)

async def fetch(session, url):
    async with session.get(url, ssl=False) as response:
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        return await response.text()


async def get_links(url):
    connector = aiohttp.TCPConnector(limit_per_host=10)
    async with aiohttp.ClientSession(connector=connector) as session:
        try:
            html_content = await fetch(session, url)
        except aiohttp.ClientError as e:
            logger.info(f"Error fetching URL {url}: {e}")
            return []

        soup = BeautifulSoup(html_content, 'html.parser')
        links = soup.select("ol a")
        result = [(link.get('href'), link.text) for link in links]
        congress = soup.select("html > body > main > section > div > div > div:nth-of-type(2) > div:nth-of-type(1) > a")
        direction = soup.select(
            "html > body > main > section > div > div > div:nth-of-type(2) > div:nth-of-type(2) > a")
        section = soup.select("div[class='direction__heading']")
        info = [congress, direction, section]
        return result, info
