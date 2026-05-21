from utils.logger import LogGen
from utils.config_reader import ConfigReader
from utils.screenshot_util import ScreenshotUtil

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.edge.options import Options as EdgeOptions

import os

logger = LogGen.loggen()

def before_scenario(context, scenario):
    logger.info("========================================")
    logger.info(f"STARTING SCENARIO : {scenario.name}")

    # Read Configurations
    browser = ConfigReader.get_browser()
    base_url = ConfigReader.get_base_url()
    implicit_wait = ConfigReader.get_implicit_wait()
    headless = ConfigReader.get_headless()

    # Chrome Setup
    if browser.lower() == "chrome":
        logger.info("Launching Chrome Browser")
        chrome_options = Options()
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-extensions")
        if headless:
            chrome_options.add_argument("--headless")
        context.driver = webdriver.Chrome(options=chrome_options )

    # Edge Setup
    elif browser.lower() == "edge":
        logger.info("Launching Edge Browser")
        edge_options = EdgeOptions()
        edge_options.add_argument("--disable-notifications")
        edge_options.add_argument("--disable-infobars")
        edge_options.add_argument("--disable-extensions")
        if headless:
            edge_options.add_argument("--headless")
        context.driver = webdriver.Edge( options=edge_options   )
    else:
        logger.error(f"Unsupported browser : {browser}")
        logger.info("Defaulting to Edge Browser")
        edge_options = EdgeOptions()
        edge_options.add_argument("--disable-notifications")
        edge_options.add_argument("--disable-infobars")
        edge_options.add_argument("--disable-extensions")
        if headless:
            edge_options.add_argument("--headless")
        context.driver = webdriver.Edge(options=edge_options)

    # Browser Setup
    context.driver.maximize_window()
    context.driver.implicitly_wait(implicit_wait)
    context.driver.get(base_url)
    logger.info(
        "Browser Opened & Maximized Successfully"
    )


def after_scenario(context, scenario):
    logger.info(f"Scenario Status : {scenario.status}")
    if scenario.status == "failed":
        logger.error(
            f"SCENARIO FAILED : {scenario.name}"
        )
        screenshot_path = (
            ScreenshotUtil.capture_screenshot(
                context.driver,
                scenario.name
            )
        )
        logger.info(
            f"Screenshot Saved : {screenshot_path}"
        )
    else:
        logger.info(
            f"SCENARIO PASSED : {scenario.name}"
        )

    context.driver.quit()
    logger.info("Browser Closed Successfully")
    logger.info("========================================")