import pytest
import allure
from pages.home_page import HomePage
from utils.logger import LogGen

logger = LogGen.loggen()

@allure.feature("Cart")
@allure.story("Validate empty cart")
def test_cart_empty(driver, config):
    driver.get(config["base_url"])
    logger.info(f"Opened base URL: {config['base_url']}")
    try:
        logger.info("--------------------------------------")
        logger.info("STARTING TEST: test_cart_empty")
        logger.info("--------------------------------------")

        home_page = HomePage(driver)

        result = home_page.validate_empty_cart()

        assert result is True, "Cart validation failed"
        logger.info("--------------------------------------")
        logger.info("TEST ENDED: Cart is empty as expected")
        logger.info("--------------------------------------")

    except AssertionError as ae:
        logger.error(f"Assertion failed in test_cart_empty: {str(ae)}")
        raise

    except Exception as e:
        logger.error(f"Error in test_cart_empty: {str(e)}")
        raise