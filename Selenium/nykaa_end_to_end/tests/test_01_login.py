import pytest
import allure
from pages.login_page import LoginPage
from utils.logger import LogGen
from utils.screenshot_util import ScreenshotUtil

logger = LogGen.loggen()

@allure.feature("Login")
@pytest.mark.usefixtures("driver", "config")
@pytest.mark.parametrize("phone,expected", [
    ("9876543210", True),
])
def test_login(driver, config, phone, expected):
    logger.info("--------------------------------------")
    logger.info("Signing in")
    logger.info("--------------------------------------")
    logger.info(f"Starting sign-in test for brand: {phone}")
    driver.get(config["base_url"])
    login_page = LoginPage(driver)

    result = login_page.login(phone)

    # SIMPLE LOGIC
    assert result, "OTP not generated - Nykaa may restrict OTP generation for automation"
    logger.info("--------------------------------------")
    logger.info("END OF SIGNING IN TEST")
    logger.info("--------------------------------------")
