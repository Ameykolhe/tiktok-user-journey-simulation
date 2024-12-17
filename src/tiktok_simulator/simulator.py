import json
import logging
import time

import seleniumwire.undetected_chromedriver as uc
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from .constants import DATA_DIR
from .exceptions import ScraperException
from .scraper import TikTokVideoMetadataScraper
from .user_journey import UserJourney, UserJourneyTopN
from .utils import Singleton

logger = logging.getLogger(__name__)


class TikTokSimulator(metaclass=Singleton):
    """
    TikTokSimulator class is a singleton class that simulates user journeys on TikTok.
    It uses the Selenium WebDriver to interact with the TikTok website and scrape metadata.
    """

    def __init__(self):
        self.tag = None
        self.user_journey_data = None
        self.epoch = None
        self.metadata = None
        self._driver = None
        self._scraper = TikTokVideoMetadataScraper()

        self._user_journey: UserJourney = UserJourneyTopN()

    def init(self):
        """
        Initializes the Chrome WebDriver.
        """
        logger.info("Initializing Chrome WebDriver")

        # Chrome desired capabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
        capabilities['acceptInsecureCerts'] = True

        # Initialize the Chrome WebDriver
        try:
            self._driver = uc.Chrome(
                headless=True,
                user_data_dir="./chrome-data",
                desired_capabilities=capabilities,
                version_main=131,
                log_level=logging.DEBUG,
                enable_cdp_events=True
            )

            time.sleep(2)
        except Exception as e:
            logger.error(f"Error initializing Chrome WebDriver: {e}")
            exit(1)

    def set_user_journey(self, user_journey: UserJourney):
        self._user_journey = user_journey

    def dump_data(self):
        """
        Saves the metadata to a JSON file.
        """

        logger.info(f"Saving metadata for tag: {self.tag}, epoch: {self.epoch}")

        file_path = DATA_DIR / f"{self.tag}_{self.epoch}_{self._user_journey.name}_{self._user_journey.get_user_interest().name}.json"

        data = {
            "tag": self.tag,
            "epoch": self.epoch,
            "metadata": self.metadata,
            "user_journey_data": self.user_journey_data
        }

        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)

    def run(
            self,
            tag: str = "foodie",
            skip_scraping: bool = False
    ):
        """
        Runs the TikTok simulation.
        :param tag: hashtag to search for
        :param skip_scraping: whether to skip scraping metadata
        """

        logger.info(f"Running simulation for tag: {tag}")
        if self._driver is None:
            self.init()
        try:
            self.tag = tag
            if self.metadata is None or not skip_scraping:
                self.metadata, self.epoch = self._scraper.get_metadata(self._driver, tag=self.tag)
            self.user_journey_data = self._user_journey.get_user_journey_data(self.metadata)
            self.dump_data()
        except ScraperException as e:
            logger.error(f"Error running simulation: {e}")
            self.teardown()

    def teardown(self):
        """
        Closes the Chrome WebDriver.
        """
        logger.debug("Tearing down Chrome WebDriver")
        self._driver.quit()
