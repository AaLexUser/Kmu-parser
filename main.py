import asyncio

from scraper import get_links
from processor import process_data, process_winners
from csv_scraper import get_winners

from tqdm import tqdm
import logging
logger = logging.getLogger(__name__)

base_url = "https://kmu.itmo.ru/digests/section/"


def update_db():
    pbar = tqdm(range(265, 800), desc="Processing")
    page_parsed = 0
    for i in pbar:
        pbar.set_description(f"Processing page {i}")
        url = base_url + str(i)
        result = asyncio.run(get_links(url))
        if result:
            page_parsed += 1
            links, info = result
            process_data(links, info)
    logger.debug(f"Total processed {page_parsed} pages")

if __name__ == "__main__":
    import logging
    # rewrite file every time
    logging.basicConfig(filename='parsing.log', level=logging.INFO, filemode='w')
    update_db()
    winners = get_winners("csv/winners_xii.csv", "ФИО")
    process_winners(winners, 'xii')
