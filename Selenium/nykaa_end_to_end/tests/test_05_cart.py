import pytest
import allure
from pages.home_page import HomePage
from utils.screenshot_util import ScreenshotUtil
from utils.logger import LogGen

logger = LogGen.loggen()

@pytest.mark.usefixtures("driver", "config")
@pytest.mark.parametrize(
    "brand, section_text, category_href, category_text, filter_type, brand_name",
    [
        ("Gucci", "men", "/mens/fragrance/luxe", "luxe-fragrances", "Brand", "Gucci"),  # Positive
    ]
)
def test_cart_verification(driver, config, brand, section_text, category_href, category_text, filter_type, brand_name):

    driver.get(config["base_url"])
    logger.info("--------------------------------------")
    logger.info("STARTING CART VERIFICATION")
    logger.info("--------------------------------------")
    logger.info(f"Starting Cart Verification Test for brand: {brand}")

    try:
        # Navigate
        home = HomePage(driver)
        luxe_page = home.go_to_men(section_text).go_to_luxe_store(category_text, category_href)

        # Apply filter
        applied = luxe_page.apply_filter(brand_name, filter_type)
        assert applied, f"Filter not applied for {brand_name}"
        logger.info(f"Filter applied successfully for {brand_name}")

        # Select product & add to cart
        product_page = luxe_page.select_product()
        cart_page = product_page.add_to_cart()

        # Verify cart
        cart_page.verify_cart()
        logger.info("Assertion passed: Cart contains product")

    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        raise

    # Screenshot
    screenshot_path = ScreenshotUtil.capture_screenshot(driver, f"Cart_{brand}")
    allure.attach.file(screenshot_path, name=f"Cart_{brand}", attachment_type=allure.attachment_type.PNG)
    logger.info("--------------------------------------")
    logger.info("ENDING CART VERIFICATION")
    logger.info("--------------------------------------")