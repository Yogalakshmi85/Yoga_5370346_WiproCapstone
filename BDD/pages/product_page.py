from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from pages.cart_page import CartPage
from utils.logger import LogGen
from utils.screenshot_util import ScreenshotUtil
import allure

logger = LogGen.loggen()

class ProductPage(BasePage):
    def add_to_cart(self):
        try:
            logger.info("Starting add to cart process")

            add_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, '//button[.//span[text()="Add to Bag"]]'))
            )
            add_btn.click()
            logger.info("Clicked 'Add to Bag' button")

            cart_icon = self.wait.until(
                EC.presence_of_element_located((By.XPATH, '//span[contains(text(),"Bag")]'))
            )

            assert cart_icon.is_displayed(), "Add to cart failed! Bag icon not visible"
            logger.info("Assertion passed: Product successfully added to cart")

            return CartPage(self.driver)

        except AssertionError as ae:
            logger.error(f"Assertion failed in add_to_cart: {str(ae)}")
            screenshot_path = ScreenshotUtil.capture_screenshot(self.driver, "AddToCart_Assertion_Failure")
            allure.attach.file(screenshot_path, name="AddToCart_Assertion_Failure",
                               attachment_type=allure.attachment_type.PNG)
            raise

        except TimeoutException as te:
            logger.error(f"Timeout in add_to_cart: {str(te)}")
            screenshot_path = ScreenshotUtil.capture_screenshot(self.driver, "AddToCart_Timeout")
            allure.attach.file(screenshot_path, name="AddToCart_Timeout", attachment_type=allure.attachment_type.PNG)
            raise

        except Exception as e:
            logger.error(f"Error adding product to cart: {str(e)}")
            screenshot_path = ScreenshotUtil.capture_screenshot(self.driver, "AddToCart_Error")
            allure.attach.file(screenshot_path, name="AddToCart_Error", attachment_type=allure.attachment_type.PNG)
            raise