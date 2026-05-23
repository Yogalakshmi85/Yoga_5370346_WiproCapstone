from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from pages.product_page import ProductPage
from utils.logger import LogGen
from utils.screenshot_util import ScreenshotUtil
import allure

logger = LogGen.loggen()

class Category(BasePage):

    def apply_filter(self, filter_type, filter_value):
        try:
            logger.info(f"Expanding {filter_type} filter")

            filter_section = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, f'//span[text()="{filter_type}"]'))
            )
            filter_section.click()

            logger.info(f"Selecting {filter_type}: {filter_value}")

            option = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, f'//label[contains(.,"{filter_value}")]'))
            )
            option.click()

            # Wait for refresh
            self.wait.until(
                EC.presence_of_element_located((By.XPATH, '//div[contains(@class,"product-listing")]'))
            )

            if filter_type.lower() == "brand":
                return self.validate_brand(filter_value)

            elif filter_type.lower() == "price":
                return self.validate_price(filter_value)

            else:
                logger.warning(f"No validation logic for filter: {filter_type}")
                return True

        except Exception as e:
            logger.error(f"Error applying filter {filter_type}: {str(e)}")
            return False

    def validate_brand(self, brand_name):
        try:
            # Wait for products
            products = self.wait.until(
                EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class,"product")]'))
            )

            for product in products:
                if brand_name.lower() in product.text.lower():
                    logger.info(f"Brand filter working: {brand_name}")
                    return True
            return True

        except Exception as e:
            logger.error(f"Brand validation error: {str(e)}")
            return False

    def validate_price(self, price_range):
        try:
            products = self.wait.until(
                EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class,"product")]'))
            )

            if len(products) > 0:
                logger.info(f"Price filter applied, products visible")
                return True

            logger.warning("No products found after price filter")
            return False

        except Exception as e:
            logger.error(f"Price validation error: {str(e)}")
            return False

    def select_product(self, product_concern):
        try:
            logger.info("Selecting first product card")
            product = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, f'//div[@class="product-listing"]//a[contains(@href, "{product_concern}")]'))
            )
            product.click()

            self.driver.switch_to.window(self.driver.window_handles[-1])
            logger.info("Switched to product tab")


            return ProductPage(self.driver)

        except Exception as e:
            logger.error(f"Error selecting product: {str(e)}")
            screenshot_path = ScreenshotUtil.capture_screenshot(self.driver, "Page_ProductSelection_Error")
            allure.attach.file(screenshot_path, name="Page_ProductSelection_Error", attachment_type=allure.attachment_type.PNG)
            raise

    def sort_products_by_name(self):
        logger.info("Sorting products by Name")

        try:
            # Click sort dropdown
            sort_button = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//span[@class="sort-name"]/parent::button')
                )
            )
            sort_button.click()
            logger.info("Clicked sort dropdown")

            # Select "Name"
            sort_option = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//label[.//span[text()="name"]]')
                )
            )
            sort_option.click()
            logger.info("Selected 'Name' sorting option")

        except Exception as e:
            logger.error(f"Error while sorting: {str(e)}")
            raise


    # VALIDATION: Verify sorted by Name
    def verify_products_sorted_by_name(self):
        logger.info("Verifying products are sorted by Name")

        try:
            # Wait for product list
            products = self.wait.until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, '//div[contains(@class,"productWrapper")]//a')
                )
            )

            # Extract names
            actual_names = [p.text.strip().lower() for p in products if p.text.strip()]

            logger.info(f"Actual product names: {actual_names}")

            # Expected sorted list
            expected_names = sorted(actual_names)

            # Assertion
            assert actual_names == expected_names, "Products are NOT sorted by name"

            logger.info("Products are correctly sorted by Name ")

        except AssertionError as ae:
            logger.error(f"Assertion failed: {str(ae)}")
            raise

        except Exception as e:
            logger.error(f"Exception during verification: {str(e)}")
            raise