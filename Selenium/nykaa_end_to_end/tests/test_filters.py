import pytest
import allure
from pages.home_page import HomePage
from utils.screenshot_util import ScreenshotUtil
from utils.logger import LogGen

logger = LogGen.loggen()

@pytest.mark.usefixtures("driver", "config")
@pytest.mark.parametrize(
    "brand, expected, section_text, category_href, category_text, filter_type, brand_name",
    [
        ("Gucci", True, "men", "/mens/fragrance/luxe", "luxe-fragrances", "Brand", "Gucci"),        # Positive
        ("InvalidBrand", False, "men", "/mens/fragrance/luxe", "luxe-fragrances", "Brand", "InvalidBrand"), # Negative
    ]
)
def test_brand_filter(driver, config, brand, expected, section_text, category_href, category_text, filter_type, brand_name):
    driver.get(config["base_url"])
    logger.info("TESTING FILTER APPLICATION")
    logger.info(f"Starting filter test for brand: {brand}")

    # Navigate to Luxe Store
    home = HomePage(driver)
    luxe_page = home.go_to_men(section_text).go_to_luxe_store(category_text, category_href)

    # Apply filter
    applied = luxe_page.apply_filter(brand_name, filter_type)

    # Assertion
    if expected:
        assert applied, f"Filter element for {brand_name} not found"
        products = luxe_page.select_product()
        assert products, f"No products found for valid brand {brand}"
        logger.info(f"Assertion passed: Products found for {brand}")
    else:
        # Negative case: filter not applied OR no products
        assert not applied or not luxe_page.get_products() or "No results found" in driver.page_source, \
            f"Unexpected products shown for invalid brand {brand}"
        logger.info(f"Assertion passed: No products for invalid brand {brand}")

    # Screenshot + Allure
    screenshot_path = ScreenshotUtil.capture_screenshot(driver, f"Filter_{brand}")
    allure.attach.file(screenshot_path, name=f"Filter_{brand}", attachment_type=allure.attachment_type.PNG)
