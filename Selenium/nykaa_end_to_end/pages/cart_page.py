

import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from pages.shipping_details_page import ShippingDetailsPage
from utils.logger import LogGen
from utils.screenshot_util import ScreenshotUtil
import allure

logger = LogGen.loggen()

class CartPage(BasePage):
    def verify_cart(self):
        try:
            item = self.get_text(By.XPATH, '//button[@id="header-bag-icon"]')
            assert item is not None, "Cart is empty!"
            logger.info("Assertion passed: Cart has items.")

            screenshot_path = ScreenshotUtil.capture_screenshot(self.driver, "CartPage_VerifyCart")
            allure.attach.file(screenshot_path, name="CartPage_VerifyCart", attachment_type=allure.attachment_type.PNG)

        except AssertionError as ae:
            logger.error(f"Assertion failed: {str(ae)}")
            screenshot_path = ScreenshotUtil.capture_screenshot(self.driver, "CartPage_VerifyCart_Failure")
            allure.attach.file(screenshot_path, name="CartPage_VerifyCart_Failure", attachment_type=allure.attachment_type.PNG)
            raise
        except Exception as e:
            logger.error(f"Error verifying cart: {str(e)}")
            screenshot_path = ScreenshotUtil.capture_screenshot(self.driver, "CartPage_VerifyCart_Error")
            allure.attach.file(screenshot_path, name="CartPage_VerifyCart_Error", attachment_type=allure.attachment_type.PNG)
            raise

    def click_bag(self):
        try:
            bag_click = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, '//button[@id="header-bag-icon"]'))
            )
            bag_click.click()
            logger.info("Clicked bag icon.")
            time.sleep(2)

            screenshot_path = ScreenshotUtil.capture_screenshot(self.driver, "CartPage_BagClicked")
            allure.attach.file(screenshot_path, name="CartPage_BagClicked", attachment_type=allure.attachment_type.PNG)

        except Exception as e:
            logger.error(f"Error clicking bag icon: {str(e)}")
            screenshot_path = ScreenshotUtil.capture_screenshot(self.driver, "CartPage_BagClicked_Error")
            allure.attach.file(screenshot_path, name="CartPage_BagClicked_Error", attachment_type=allure.attachment_type.PNG)
            raise

    def click_proceed(self):
        try:
            proceed_click = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, '//button[.//span[text()="Proceed"]]'))
            )
            proceed_click.click()
            logger.info("Clicked Proceed button.")
            time.sleep(2)

            screenshot_path = ScreenshotUtil.capture_screenshot(self.driver, "CartPage_ProceedClicked")
            allure.attach.file(screenshot_path, name="CartPage_ProceedClicked", attachment_type=allure.attachment_type.PNG)

        except Exception as e:
            logger.error(f"Error clicking Proceed: {str(e)}")
            screenshot_path = ScreenshotUtil.capture_screenshot(self.driver, "CartPage_ProceedClicked_Error")
            allure.attach.file(screenshot_path, name="CartPage_ProceedClicked_Error", attachment_type=allure.attachment_type.PNG)
            raise

    def click_continue_as_guest(self):
        try:
            cont_click = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, '//button[text()="Continue as guest"]'))
            )
            cont_click.click()
            logger.info("Clicked Continue as guest.")
            time.sleep(5)

            # Assertion: ensure shipping details page is loaded
            assert "address" in self.driver.current_url.lower(), \
                f"Shipping page not loaded! Current URL: {self.driver.current_url}"
            logger.info("Assertion passed: Shipping details page loaded.")

            screenshot_path = ScreenshotUtil.capture_screenshot(self.driver, "CartPage_ContinueAsGuest")
            allure.attach.file(screenshot_path, name="CartPage_ContinueAsGuest", attachment_type=allure.attachment_type.PNG)

            return ShippingDetailsPage(self.driver)

        except AssertionError as ae:
            logger.error(f"Assertion failed: {str(ae)}")
            screenshot_path = ScreenshotUtil.capture_screenshot(self.driver, "CartPage_ContinueAsGuest_Failure")
            allure.attach.file(screenshot_path, name="CartPage_ContinueAsGuest_Failure", attachment_type=allure.attachment_type.PNG)
            raise
        except Exception as e:
            logger.error(f"Error clicking Continue as guest: {str(e)}")
            screenshot_path = ScreenshotUtil.capture_screenshot(self.driver, "CartPage_ContinueAsGuest_Error")
            allure.attach.file(screenshot_path, name="CartPage_ContinueAsGuest_Error", attachment_type=allure.attachment_type.PNG)
            raise
