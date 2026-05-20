import pytest
import allure
from pages.home_page import HomePage
from utils.logger import LogGen
from utils.screenshot_util import ScreenshotUtil

logger = LogGen.loggen()

@allure.feature("Search")
@pytest.mark.parametrize("search_input", ["@$%^"])
@pytest.mark.usefixtures("driver", "config")
def test_search_invalid(driver, config, search_input):
    logger.info("--------------------------------------")
    logger.info("STARTING INVALID SEARCH VERIFICATION")
    logger.info("--------------------------------------")
    logger.info(f"Starting test for brand: {search_input}")


    driver.get(config["base_url"])
    home_page = HomePage(driver)

    result = home_page.search_product(search_input)

    try:
        assert result, "Search did not show error for invalid input"

        logger.info("Test passed: Invalid search handled correctly")

        logger.info("--------------------------------------")
        logger.info("ENDING INVALID SEARCH VERIFICATION")
        logger.info("--------------------------------------")

    except AssertionError as e:
        logger.error(str(e))
        raise