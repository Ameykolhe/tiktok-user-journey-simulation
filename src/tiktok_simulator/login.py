import logging
import time

import seleniumwire.undetected_chromedriver as uc
from selenium.webdriver import DesiredCapabilities


def main():
    capabilities = DesiredCapabilities.CHROME
    capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
    capabilities['acceptInsecureCerts'] = True

    # Initialize the Chrome WebDriver
    driver = uc.Chrome(
        headless=False,
        user_data_dir="./chrome-data",
        desired_capabilities=capabilities,
        version_main=131,
        log_level=logging.DEBUG,
        enable_cdp_events=True
    )

    time.sleep(2)

    driver.get("https://www.tiktok.com/login/phone-or-email/phone-password")

    input("Press Enter to continue...")

    driver.quit()


if __name__ == "__main__":
    main()
