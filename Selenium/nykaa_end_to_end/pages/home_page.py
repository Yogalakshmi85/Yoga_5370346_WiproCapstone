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
            screenshot_path = ScreenshotUtil.capture_screenshot(self.driver, f"HomePage_{section_text}")
            allure.attach.file(screenshot_path, name=f"HomePage_{section_text}",
                               attachment_type=allure.attachment_type.PNG)

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

            # Capture screenshot and attach to Allure
            screenshot_path = ScreenshotUtil.capture_screenshot(self.driver, f"MenPage_{section_text}")
            allure.attach.file(screenshot_path, name=f"HomePage_{section_text}", attachment_type=allure.attachment_type.PNG)

            return MenPage(self.driver)

        except AssertionError as ae:
            logger.error(f"Assertion failed: {str(ae)}")
            # Capture screenshot on failure
            screenshot_path = ScreenshotUtil.capture_screenshot(self.driver, f"HomePage_{section_text}_Failure")
            allure.attach.file(screenshot_path, name=f"HomePage_{section_text}_Failure", attachment_type=allure.attachment_type.PNG)
            raise
        except Exception as e:
            logger.error(f"Error navigating to {section_text} section: {str(e)}")
            # Capture screenshot on unexpected error
            screenshot_path = ScreenshotUtil.capture_screenshot(self.driver, f"HomePage_{section_text}_Error")
            allure.attach.file(screenshot_path, name=f"HomePage_{section_text}_Error", attachment_type=allure.attachment_type.PNG)
            raise
