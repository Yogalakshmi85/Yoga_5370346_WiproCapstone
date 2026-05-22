from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from pages.payment_page import PaymentPage
from utils.csv_reader import CSVReader
from utils.logger import LogGen
from utils.screenshot_util import ScreenshotUtil
import allure

logger = LogGen.loggen()

class ShippingDetailsPage(BasePage):

    def fill_details_from_csv(self, file_name, override_pincode=None):
        try:
            logger.info("Reading shipping details from CSV")

            data_list = CSVReader.read_csv(file_name)

            if not data_list:
                raise ValueError("CSV file is empty!")

            data = data_list[0]  # take first row

            pincode = override_pincode if override_pincode else data["pincode"]

            # ---- Fill form ----
            self.find(By.XPATH, '//input[@placeholder="Name"]').send_keys(data["name"])
            self.find(By.XPATH, '//input[@placeholder="Phone"]').send_keys(data["phone"])
            self.find(By.XPATH, '//input[@placeholder="Email"]').send_keys(data["email"])
            self.find(By.XPATH, '//input[@placeholder="House/ Flat/ Office No."]').send_keys(data["flatno"])
            self.find(By.XPATH, '//textarea[@placeholder="Road Name/ Area /Colony"]').send_keys(data["area"])

            pin_box = self.find(By.XPATH, '//input[@placeholder="Pincode"]')
            pin_box.clear()
            pin_box.send_keys(pincode)

            logger.info("Shipping details filled successfully")

            # ✅ Assertion (important!)
            assert pin_box.get_attribute("value") == str(pincode), "Pincode not entered correctly!"

        except ValueError as ve:
            logger.error(f"Data error: {str(ve)}")
            raise

        except Exception as e:
            logger.error(f"Error filling shipping details: {str(e)}")

            screenshot_path = ScreenshotUtil.capture_screenshot(self.driver, "ShippingDetails_Error")
            allure.attach.file(screenshot_path, name="ShippingDetails_Error",
                               attachment_type=allure.attachment_type.PNG)
            raise

    def click_ship_to_this_address(self):
        try:
            logger.info("Clicking 'SHIP TO THIS ADDRESS' button")

            ship_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, '//button[text()="SHIP TO THIS ADDRESS"]'))
            )
            ship_btn.click()

            logger.info("Clicked ship button")

            # Switch window if needed
            if len(self.driver.window_handles) > 1:
                self.driver.switch_to.window(self.driver.window_handles[-1])

            current_url = self.driver.current_url.lower()

            # ✅ Smart validation
            if "payment" in current_url or "checkout" in current_url:
                logger.info("Navigated to Payment Page successfully")
                return PaymentPage(self.driver)

            elif "address" in current_url:
                logger.warning("Still on address page → possible invalid pincode")
                return self

            else:
                raise AssertionError("Unexpected navigation after clicking ship button!")

        except AssertionError as ae:
            logger.error(f"Assertion failed: {str(ae)}")
            raise

        except Exception as e:
            logger.error(f"Error clicking ship button: {str(e)}")

            screenshot_path = ScreenshotUtil.capture_screenshot(
                self.driver, "ShippingDetails_Click_Error"
            )
            allure.attach.file(
                screenshot_path,
                name="ShippingDetails_Click_Error",
                attachment_type=allure.attachment_type.PNG
            )

            raise