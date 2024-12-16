import json
import logging
import time
from datetime import datetime, timezone

import seleniumwire.undetected_chromedriver as uc
from selenium.common import NoSuchElementException, TimeoutException
from seleniumwire.utils import decode as sw_decode

from .constants import MAX_RETRIES
from .exceptions import ScraperException

logger = logging.getLogger(__name__)


class TikTokVideoMetadataScraper:
    """
    A class designed for scraping metadata from TikTok video searches.

    This class provides functionality to interact with TikTok's search pages and APIs in order to
    retrieve metadata associated with videos based on a specific hashtag. It features methods for
    executing scraper logic, handling retries on failure, and fetching parsed metadata from requests
    made during the scraping process.
    """

    def __init__(self):
        self.search_url = "https://www.tiktok.com/search/video?q=%23{tag}&t={epoch}"
        self.search_api = "https://www.tiktok.com/api/search/item/full/"

    def _scrape(
            self,
            driver: uc.Chrome,
            url: str,
            retry=0
    ):

        """
        Internal method to handle scraping logic with retries.
        :param driver: Selenium web driver
        :param url: search url
        :param retry: current retry count
        :return:
        """

        if retry > MAX_RETRIES:
            raise ScraperException("Error scraping metadata: max retry count reached", url=url)

        try:
            driver.get(url)
            time.sleep(5)
        except AssertionError as e:
            logger.error(e)
            self._scrape(driver, url, retry + 1)
        except NoSuchElementException as e:
            logger.error(e)
            self._scrape(driver, url, retry + 1)
        except TimeoutException as e:
            logger.error(e)
            self._scrape(driver, url, retry + 1)

    def get_metadata(
            self,
            driver: uc.Chrome,
            tag: str = "foodie",
            epoch: int = int(datetime.now(timezone.utc).timestamp())
    ) -> (list[dict[str, str | list | dict]], int):
        """
        Retrieves metadata from TikTok video searches.
        :param driver: Selenium web driver
        :param tag: hashtag to search for
        :param epoch: epoch time in seconds
        :return: list of metadata dictionaries and epoch time
        """
        epoch = int(datetime.now(timezone.utc).timestamp()) if epoch is None else epoch
        logger.info(f"Scraping metadata for tag: {tag}, epoch: {epoch}")
        try:
            url = self.search_url.format(tag=tag, epoch=epoch)
            self._scrape(driver, url)

            item_list = []
            for request in driver.requests:
                if self.search_api in request.url:
                    try:
                        data = sw_decode(request.response.body,
                                         request.response.headers.get('Content-Encoding', 'identity')).decode("utf8")
                        item_list.extend(json.loads(data)["item_list"])
                    except ValueError:
                        logger.error(f"Error scraping metadata: cannot decode response for {request.url}")

            return item_list, epoch

        except Exception as e:
            logger.error(f"Error scraping metadata: {e}")
