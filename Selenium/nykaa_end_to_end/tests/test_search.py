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
    logger.info("INVALID SEARCH VERIFICATION")
    logger.info(f"Starting test for brand: {search_input}")

    driver.get(config["base_url"])
    home_page = HomePage(driver)

    result = home_page.search_product(search_input)

    try:
        assert result, "Search did not show error for invalid input"

        logger.info("Test passed: Invalid search handled correctly")

        screenshot_path = ScreenshotUtil.capture_screenshot(driver, "Test_Search_Pass")
        allure.attach.file(
            screenshot_path,
            name="Test_Search_Pass",
            attachment_type=allure.attachment_type.PNG
        )

    except AssertionError as e:
        logger.error(str(e))

        screenshot_path = ScreenshotUtil.capture_screenshot(driver, "Test_Search_Fail")
        allure.attach.file(
            screenshot_path,
            name="Test_Search_Fail",
            attachment_type=allure.attachment_type.PNG
        )

        raise