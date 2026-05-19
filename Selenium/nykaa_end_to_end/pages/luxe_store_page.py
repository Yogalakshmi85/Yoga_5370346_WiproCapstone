from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from pages.product_page import ProductPage
from utils.logger import LogGen
from utils.screenshot_util import ScreenshotUtil
import allure

logger = LogGen.loggen()

class LuxeStorePage(BasePage):
    def apply_filter(self, brand_name, filter_type):
        try:
            logger.info(f"Expanding {filter_type} filter")
            brand_filter = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, f'//span[text()="{filter_type}"]'))
            )
            brand_filter.click()

            logger.info(f"Selecting brand: {brand_name}")
            brand_option = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, f'//label[contains(.,"{brand_name}")]'))
            )
            brand_option.click()

            # Wait until products are refreshed
            products = self.wait.until(
                EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class,"product-listing")]//h2'))
            )

            # Verify at least one product contains the brand name
            brand_products = [p.text for p in products if brand_name.lower() in p.text.lower()]
            if not brand_products:
                logger.warning(f"No products found for {brand_name}")
                return False

            logger.info(f"{brand_name} filter verified with products: {brand_products[:3]}")
            screenshot_path = ScreenshotUtil.capture_screenshot(self.driver, f"LuxeStorePage_Filter_{brand_name}")
            allure.attach.file(screenshot_path, name=f"LuxeStorePage_Filter_{brand_name}",
                               attachment_type=allure.attachment_type.PNG)
            return True

        except (TimeoutException, NoSuchElementException) as e:
            logger.error(f"Filter {filter_type} for {brand_name} not found: {str(e)}")
            screenshot_path = ScreenshotUtil.capture_screenshot(self.driver, f"LuxeStorePage_Filter_{brand_name}_Error")
            allure.attach.file(screenshot_path, name=f"LuxeStorePage_Filter_{brand_name}_Error",
                               attachment_type=allure.attachment_type.PNG)
            return False

        except AssertionError as ae:
            logger.error(f"Assertion failed: {str(ae)}")
            screenshot_path = ScreenshotUtil.capture_screenshot(self.driver, f"LuxeStorePage_Filter_{brand_name}_Failure")
            allure.attach.file(screenshot_path, name=f"LuxeStorePage_Filter_{brand_name}_Failure", attachment_type=allure.attachment_type.PNG)
            raise
        except Exception as e:
            logger.error(f"Error applying filter {filter_type} for {brand_name}: {str(e)}")
            screenshot_path = ScreenshotUtil.capture_screenshot(self.driver, f"LuxeStorePage_Filter_{brand_name}_Error")
            allure.attach.file(screenshot_path, name=f"LuxeStorePage_Filter_{brand_name}_Error", attachment_type=allure.attachment_type.PNG)
            raise

    def select_product(self):
        try:
            logger.info("Selecting first product card")
            product = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, '//div[@class="product-listing"]//a[1]'))
            )
            product.click()

            self.driver.switch_to.window(self.driver.window_handles[-1])
            logger.info("Switched to product tab")


            return ProductPage(self.driver)

        except Exception as e:
            logger.error(f"Error selecting product: {str(e)}")
            screenshot_path = ScreenshotUtil.capture_screenshot(self.driver, "LuxeStorePage_ProductSelection_Error")
            allure.attach.file(screenshot_path, name="LuxeStorePage_ProductSelection_Error", attachment_type=allure.attachment_type.PNG)
            raise
