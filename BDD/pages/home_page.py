from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from pages.men_page import MenPage
from utils.logger import LogGen
from utils.screenshot_util import ScreenshotUtil
import allure

logger = LogGen.loggen()

class HomePage(BasePage):
    def go_to_men(self, section_text: str) -> MenPage:
        try:
            logger.info(f"Attempting to navigate to section: {section_text}")
            men_link = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, f'//a[text()="{section_text}"]'))
            )
            men_link.click()
            logger.info(f"Clicked on {section_text} link")

            # Switch to new tab/window if opened
            self.driver.switch_to.window(self.driver.window_handles[-1])
            logger.info("Switched to new window/tab")

            # Assertion to confirm navigation
            current_url = self.driver.current_url.lower()
            assert section_text in current_url, f"{section_text} page not loaded! Current URL: {current_url}"
            logger.info(f"Assertion passed: {section_text} page successfully loaded")

            return MenPage(self.driver)

        except AssertionError as ae:
            logger.error(f"Assertion failed: {str(ae)}")
            raise
        except Exception as e:
            logger.error(f"Error navigating to {section_text} section: {str(e)}")
            raise

    def search_product(self, search_text: str):
        try:
            logger.info(f"Searching for product: {search_text}")

            search_box = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, '//input[@placeholder="Search on Nykaa"]'))
            )
            search_box.clear()
            search_box.send_keys(search_text)
            logger.info("Entered search text")
            search_box.send_keys("\n")
            logger.info("Pressed Enter for search")

            # Case 1: Invalid input → look for error message
            try:
                error_element = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, '//div[contains(text(),"Thanks")]'))
                )
                if error_element.is_displayed():
                    logger.info("Assertion passed: Error message displayed for invalid search")
                    return "error"
            except TimeoutException:
                logger.info("No error message found, checking for valid results...")

            # Case 2: Valid input → check URL or product results
            current_url = self.driver.current_url.lower()
            if search_text.lower() in current_url:
                logger.info(f"Assertion passed: URL contains {search_text}")
                screenshot_path = ScreenshotUtil.capture_screenshot(self.driver, f"Search_Valid_{search_text}")
                allure.attach.file(screenshot_path, name=f"Search_Valid_{search_text}", attachment_type=allure.attachment_type.PNG)
                return "results"

            product_elements = self.driver.find_elements(By.XPATH, '//div[contains(@class,"product")]')
            if product_elements:
                logger.info("Assertion passed: Product results displayed")
                screenshot_path = ScreenshotUtil.capture_screenshot(self.driver, f"Search_Results_{search_text}")
                allure.attach.file(screenshot_path, name=f"Search_Results_{search_text}", attachment_type=allure.attachment_type.PNG)
                return "results"

            # If neither case matched
            logger.error("Search did not return error or results")
            screenshot_path = ScreenshotUtil.capture_screenshot(self.driver, f"Search_Unknown_{search_text}")
            allure.attach.file(screenshot_path, name=f"Search_Unknown_{search_text}", attachment_type=allure.attachment_type.PNG)
            return "unknown"

        except NoSuchElementException as ne:
            logger.error(f"Search box not found: {ne}")
            screenshot_path = ScreenshotUtil.capture_screenshot(self.driver, "Search_NoElement")
            allure.attach.file(screenshot_path, name="Search_NoElement", attachment_type=allure.attachment_type.PNG)
            raise
        except AssertionError as ae:
            logger.error(f"Assertion failed: {ae}")
            screenshot_path = ScreenshotUtil.capture_screenshot(self.driver, "Search_AssertionFailure")
            allure.attach.file(screenshot_path, name="Search_AssertionFailure", attachment_type=allure.attachment_type.PNG)
            raise
        except Exception as e:
            logger.error(f"Unexpected error during search: {e}")
            screenshot_path = ScreenshotUtil.capture_screenshot(self.driver, "Search_Exception")
            allure.attach.file(screenshot_path, name="Search_Exception", attachment_type=allure.attachment_type.PNG)
            raise

    def validate_empty_cart(self):
        try:
            logger.info("Validating empty cart")

            # Click bag icon
            bag_click = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, '//button[@id="header-bag-icon"]'))
            )
            bag_click.click()
            logger.info("Clicked bag icon")

            # Wait for empty cart message (Nykaa specific)
            empty_msg = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, '//p[contains(text(),"Empty")]')
                )
            )

            assert empty_msg.is_displayed(), "Empty cart message not displayed"
            logger.info("Assertion passed: Cart is empty")

            screenshot_path = ScreenshotUtil.capture_screenshot(self.driver, "HomePage_EmptyCart")
            allure.attach.file(
                screenshot_path,
                name="HomePage_EmptyCart",
                attachment_type=allure.attachment_type.PNG
            )

            return True

        except AssertionError as ae:
            logger.error(f"Assertion failed: {str(ae)}")

            screenshot_path = ScreenshotUtil.capture_screenshot(self.driver, "HomePage_EmptyCart_Failure")
            allure.attach.file(
                screenshot_path,
                name="HomePage_EmptyCart_Failure",
                attachment_type=allure.attachment_type.PNG
            )
            raise

        except Exception as e:
            logger.error(f"Error validating empty cart: {str(e)}")

            screenshot_path = ScreenshotUtil.capture_screenshot(self.driver, "HomePage_EmptyCart_Error")
            allure.attach.file(
                screenshot_path,
                name="HomePage_EmptyCart_Error",
                attachment_type=allure.attachment_type.PNG
            )
            raise