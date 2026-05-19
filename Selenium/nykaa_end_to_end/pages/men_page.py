from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from pages.luxe_store_page import LuxeStorePage
from utils.logger import LogGen
from utils.screenshot_util import ScreenshotUtil
import allure

logger = LogGen.loggen()

class MenPage(BasePage):
    def go_to_luxe_store(self, category_text, category_href):
        try:
            logger.info(f"Attempting to navigate to Luxe Store: {category_text}")

            # Wait until the Luxe Store banner link is clickable
            luxe_link = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, f'//a[contains(@href,"{category_href}")]/img[@alt="luxe-man-focus"]')
                )
            )
            luxe_link.click()
            logger.info(f"Clicked Luxe Store banner for {category_text}")

            # Switch to new tab/window if opened
            self.driver.switch_to.window(self.driver.window_handles[-1])
            logger.info("Switched to new window/tab")

            # Assertion to confirm navigation
            current_url = self.driver.current_url.lower()
            assert category_text in current_url, f"{category_text} page not loaded! Current URL: {current_url}"
            logger.info(f"Assertion passed: {category_text} page successfully loaded")

            # Capture screenshot and attach to Allure
            screenshot_path = ScreenshotUtil.capture_screenshot(self.driver, f"CategoryPage_{category_text}")
            allure.attach.file(screenshot_path, name=f"CategoryPage_{category_text}", attachment_type=allure.attachment_type.PNG)

            return LuxeStorePage(self.driver)

        except AssertionError as ae:
            logger.error(f"Assertion failed: {str(ae)}")
            screenshot_path = ScreenshotUtil.capture_screenshot(self.driver, f"CategoryPage_{category_text}_Failure")
            allure.attach.file(screenshot_path, name=f"CategoryPage_{category_text}_Failure", attachment_type=allure.attachment_type.PNG)
            raise
        except Exception as e:
            logger.error(f"Error navigating to Luxe Store {category_text}: {str(e)}")
            screenshot_path = ScreenshotUtil.capture_screenshot(self.driver, f"CategoryPage_{category_text}_Error")
            allure.attach.file(screenshot_path, name=f"CategoryPage_{category_text}_Error", attachment_type=allure.attachment_type.PNG)
            raise
