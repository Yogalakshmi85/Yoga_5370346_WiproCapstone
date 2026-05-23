import allure
from utils.logger import LogGen
from utils.screenshot_util import ScreenshotUtil

from behave import then
import time

@then('I sort the products')
def step_sort_products(context):
    logger = LogGen.loggen()
    logger.info("Step: I sort the products")

    try:
        context.category_page.sort_products_by_name()
        context.category_page.verify_products_sorted_by_name()

        screenshot_path = ScreenshotUtil.capture_screenshot(context.driver, "Sorting")
        allure.attach.file(screenshot_path, name="Sorting",
                           attachment_type=allure.attachment_type.PNG)

        logger.info("Step passed: Products sorted successfully")

    except AssertionError as ae:
        logger.error(f"Assertion failed in step: {str(ae)}")
        context.driver.save_screenshot("step_sort_assertion_failed.png")
        raise

    except Exception as e:
        logger.error(f"Step failed: {str(e)}")
        context.driver.save_screenshot("step_sort_exception.png")
        raise
