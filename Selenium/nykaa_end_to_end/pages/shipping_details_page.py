
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from pages.payment_page import PaymentPage
from utils.excel_reader import ExcelReader
from utils.logger import LogGen
from utils.screenshot_util import ScreenshotUtil
import allure

logger = LogGen.loggen()

class ShippingDetailsPage(BasePage):
    def fill_details_from_excel(self, excel_path, override_pincode=None):
        try:
            logger.info("Reading shipping details from Excel")
            excel = ExcelReader(excel_path)
            data = excel.get_shipping_details()

            pincode = override_pincode if override_pincode else data["pincode"]

            logger.info(f"Entering Name: {data['name']}")
            self.find(By.XPATH, '//input[@placeholder="Name"]').send_keys(data["name"])

            logger.info(f"Entering Phone: {data['phone']}")
            self.find(By.XPATH, '//input[@placeholder="Phone"]').send_keys(data["phone"])

            logger.info(f"Entering Email: {data['email']}")
            self.find(By.XPATH, '//input[@placeholder="Email"]').send_keys(data["email"])

            logger.info(f"Entering Flat/House No: {data['flatno']}")
            self.find(By.XPATH, '//input[@placeholder="House/ Flat/ Office No."]').send_keys(data["flatno"])

            logger.info(f"Entering Area: {data['area']}")
            self.find(By.XPATH, '//textarea[@placeholder="Road Name/ Area /Colony"]').send_keys(data["area"])

            logger.info(f"Entering Pincode: {pincode}")
            pin_box = self.find(By.XPATH, '//input[@placeholder="Pincode"]')
            pin_box.clear()
            pin_box.send_keys(pincode)

            logger.info("Shipping details filled successfully")

            screenshot_path = ScreenshotUtil.capture_screenshot(self.driver, "ShippingDetails_Filled")
            allure.attach.file(screenshot_path, name="ShippingDetails_Filled",
                               attachment_type=allure.attachment_type.PNG)

        except Exception as e:
            logger.error(f"Error filling shipping details: {str(e)}")
            screenshot_path = ScreenshotUtil.capture_screenshot(self.driver, "ShippingDetails_Error")
            allure.attach.file(screenshot_path, name="ShippingDetails_Error",
                               attachment_type=allure.attachment_type.PNG)
            raise


    def click_ship_to_this_address(self):
        try:
            logger.info("Attempting to click 'SHIP TO THIS ADDRESS' button")

            ship_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, '//button[text()="SHIP TO THIS ADDRESS"]'))
            )
            ship_btn.click()
            logger.info("Clicked 'SHIP TO THIS ADDRESS'.")

            # Switch only if new window exists
            if len(self.driver.window_handles) > 1:
                self.driver.switch_to.window(self.driver.window_handles[-1])

            time.sleep(5)

            current_url = self.driver.current_url.lower()

            # Screenshot (always)
            screenshot_path = ScreenshotUtil.capture_screenshot(
                self.driver, "ShippingDetailsPage_ShipToAddress"
            )
            allure.attach.file(
                screenshot_path,
                name="ShippingDetailsPage_ShipToAddress",
                attachment_type=allure.attachment_type.PNG
            )

            # KEY CHANGE: No hard assertion
            if "payment" in current_url or "checkout" in current_url:
                logger.info("Payment page successfully loaded")
                return PaymentPage(self.driver)
            else:
                logger.info("Stayed on address page - validation error(invalid pincode)")
                return self

        except Exception as e:
            logger.error(f"Error clicking 'SHIP TO THIS ADDRESS': {str(e)}")

            screenshot_path = ScreenshotUtil.capture_screenshot(
                self.driver, "ShippingDetailsPage_ShipToAddress_Error"
            )
            allure.attach.file(
                screenshot_path,
                name="ShippingDetailsPage_ShipToAddress_Error",
                attachment_type=allure.attachment_type.PNG
            )

            raise