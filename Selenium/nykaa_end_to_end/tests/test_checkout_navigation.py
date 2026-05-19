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
def test_checkout_navigation(driver, config, brand, section_text, category_href, category_text, filter_type, brand_name):

    driver.get(config["base_url"])
    logger.info("CHECKOUT NAVIGATION VERIFICATION")
    logger.info(f"Starting Checkout Navigation Test for brand: {brand}")

    try:
        # Navigate
        home = HomePage(driver)
        luxe_page = home.go_to_men(section_text).go_to_luxe_store(category_text, category_href)

        # Apply filter
        applied = luxe_page.apply_filter(brand_name, filter_type)
        assert applied, f"Filter not applied for {brand_name}"
        logger.info("Filter applied successfully")

        # Product + Cart
        product_page = luxe_page.select_product()
        cart_page = product_page.add_to_cart()

        # Cart actions
        cart_page.verify_cart()
        cart_page.click_bag()
        cart_page.click_proceed()

        # Continue as guest
        shipping_page = cart_page.click_continue_as_guest()

        # Assertion (already inside method, but we double-check)
        current_url = driver.current_url.lower()
        assert "address" in current_url, "Shipping page not reached"
        logger.info("Assertion passed: Navigated to Shipping Page")

    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        raise

    # Screenshot
    screenshot_path = ScreenshotUtil.capture_screenshot(driver, f"CheckoutNavigation_{brand}")
    allure.attach.file(screenshot_path, name=f"CheckoutNavigation_{brand}", attachment_type=allure.attachment_type.PNG)