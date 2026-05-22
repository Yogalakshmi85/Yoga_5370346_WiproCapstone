from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
# from utils.excel_reader import ExcelReader
from utils.logger import LogGen
from utils.screenshot_util import ScreenshotUtil
import allure

logger = LogGen.loggen()

class PaymentPage(BasePage):
    def click_payment_method(self, payment_method):
        try:
            logger.info(f"Attempting to select payment method: {payment_method}")
            option = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, f'//*[contains(text(),"{payment_method}")]'))
            )
            option.click()
            logger.info(f"Clicked on {payment_method} option")

            # Verify activation by checking confirmation section
            confirmation = self.wait.until(
                EC.visibility_of_element_located((By.XPATH, f'//*[contains(text(),"{payment_method}")]'))
            )
            assert confirmation is not None, f"{payment_method} option not activated!"
            logger.info(f"Assertion passed: {payment_method} option activated")

        except AssertionError as ae:
            logger.error(f"Assertion failed: {str(ae)}")
            screenshot_path = ScreenshotUtil.capture_screenshot(self.driver, f"PaymentPage_{payment_method}_Failure")
            allure.attach.file(screenshot_path, name=f"PaymentPage_{payment_method}_Failure", attachment_type=allure.attachment_type.PNG)
            raise
        except Exception as e:
            logger.error(f"Error selecting payment method {payment_method}: {str(e)}")
            screenshot_path = ScreenshotUtil.capture_screenshot(self.driver, f"PaymentPage_{payment_method}_Error")
            allure.attach.file(screenshot_path, name=f"PaymentPage_{payment_method}_Error", attachment_type=allure.attachment_type.PNG)
            raise

