from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from pages.category_page import Category
from utils.logger import LogGen
from utils.screenshot_util import ScreenshotUtil
import allure

logger = LogGen.loggen()

class MenPage(BasePage):
    def go_to_specific_category(self, category_text, category_href):
        try:
            logger.info(f"Attempting to navigate to {category_text}: {category_text}")

            cate_link = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, f'//a[contains(@href,"{category_href}")]/img[@alt="{category_text}"]')
                )
            )
            cate_link.click()
            logger.info(f"Clicked Category banner for {category_text}")


            # Switch to new tab/window if opened
            self.driver.switch_to.window(self.driver.window_handles[-1])
            logger.info("Switched to new window/tab")

            # Assertion to confirm navigation
            current_url = self.driver.current_url.lower()
            assert category_text in current_url, f"{category_text} page not loaded! Current URL: {current_url}"
            logger.info(f"Assertion passed: {category_text} page successfully loaded")

            return Category(self.driver)

        except AssertionError as ae:
            logger.error(f"Assertion failed: {str(ae)}")
            screenshot_path = ScreenshotUtil.capture_screenshot(self.driver, f"CategoryPage_{category_text}_Failure")
            allure.attach.file(screenshot_path, name=f"CategoryPage_{category_text}_Failure", attachment_type=allure.attachment_type.PNG)
            raise
        except Exception as e:
            logger.error(f"Error navigating to category {category_text}: {str(e)}")
            screenshot_path = ScreenshotUtil.capture_screenshot(self.driver, f"CategoryPage_{category_text}_Error")
            allure.attach.file(screenshot_path, name=f"CategoryPage_{category_text}_Error", attachment_type=allure.attachment_type.PNG)
            raise
