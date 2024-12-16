import json
import logging
import time
from pathlib import Path

import seleniumwire.undetected_chromedriver as uc
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from .exceptions import ScraperException
from .scraper import TikTokVideoMetadataScraper

logger = logging.getLogger(__name__)


class TikTokSimulator:

    def __init__(self):
        self._driver = None
        self._scraper = TikTokVideoMetadataScraper()

    def init(self):
        logger.info("Initializing Chrome WebDriver")

        # Chrome desired capabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
        capabilities['acceptInsecureCerts'] = True

        # Initialize the Chrome WebDriver
        try:
            self._driver = uc.Chrome(
                headless=False,
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

    def dump_data(
            self,
            tag: str,
            epoch: int,
            metadata: list[dict[str, str | list | dict]],
    ):
        logger.info(f"Saving metadata for tag: {tag}, epoch: {epoch}")

        current_dir = Path(__file__).parent
        data_dir = current_dir.parent.parent / "data"
        data_dir.mkdir(parents=True, exist_ok=True)

        file_path = data_dir / f"{tag}_{epoch}.json"

        data = {
            "tag": tag,
            "epoch": epoch,
            "metadata": metadata
        }

        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)

    def run(
            self,
            tag: str = "foodie"
    ):
        logger.info(f"Running simulation for tag: {tag}")
        try:
            metadata, epoch = self._scraper.get_metadata(self._driver, tag=tag)
            self.dump_data(tag, epoch, metadata)
        except ScraperException as e:
            logger.error(f"Error running simulation: {e}")
            self.teardown()

    def teardown(self):
        logger.debug("Tearing down Chrome WebDriver")
        self._driver.quit()
