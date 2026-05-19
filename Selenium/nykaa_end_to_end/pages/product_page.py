
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
        screenshot_path = ScreenshotUtil.capture_screenshot(self.driver, "LuxeStorePage_ProductSelected")
        allure.attach.file(screenshot_path, name="LuxeStorePage_ProductSelected",
                           attachment_type=allure.attachment_type.PNG)

        try:
            # Select size if required

            try:
                size_option = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, '//button[contains(text(),"100ml")]'))
                )
                size_option.click()
                logger.info("Size option selected (100ml).")
            except Exception:
                logger.info("No size selection needed.")

            # Click Add to Bag
            add_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, '//button[.//span[text()="Add to Bag"]]'))
            )
            add_btn.click()
            logger.info("Clicked 'Add to Bag'.")

            # Switch to cart window/tab
            self.driver.switch_to.window(self.driver.window_handles[-1])
            logger.info("Switched to cart window/tab.")

            # Assertion: ensure cart icon or confirmation appears
            cart_icon = self.wait.until(
                EC.presence_of_element_located((By.XPATH, '//span[contains(text(),"Bag")]'))
            )
            assert cart_icon is not None, "Add to cart failed! Bag icon not found."
            logger.info("Assertion passed: Product successfully added to cart.")

            # Capture screenshot and attach to Allure
            screenshot_path = ScreenshotUtil.capture_screenshot(self.driver, "ProductPage_AddToCart")
            allure.attach.file(screenshot_path, name="ProductPage_AddToCart", attachment_type=allure.attachment_type.PNG)

            return CartPage(self.driver)

        except AssertionError as ae:
            logger.error(f"Assertion failed in add_to_cart: {str(ae)}")
            screenshot_path = ScreenshotUtil.capture_screenshot(self.driver, "ProductPage_AddToCart_Failure")
            allure.attach.file(screenshot_path, name="ProductPage_AddToCart_Failure", attachment_type=allure.attachment_type.PNG)
            raise
        except Exception as e:
            logger.error(f"Error adding product to cart: {str(e)}")
            screenshot_path = ScreenshotUtil.capture_screenshot(self.driver, "ProductPage_AddToCart_Error")
            allure.attach.file(screenshot_path, name="ProductPage_AddToCart_Error", attachment_type=allure.attachment_type.PNG)
            raise
