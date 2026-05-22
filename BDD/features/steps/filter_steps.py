import allure
from behave import when, then
from selenium.common import TimeoutException, NoSuchElementException, ElementClickInterceptedException

from utils.logger import LogGen
from utils.screenshot_util import ScreenshotUtil

logger = LogGen.loggen()

@when('I apply filter "{filter_type}" with value "{filter_value}"')
def step_impl(context, filter_type, filter_value):
    try:
        context.filter_result = context.category_page.apply_filter(filter_type, filter_value)
        screenshot_path = ScreenshotUtil.capture_screenshot(context.driver, f"Filter_{filter_type}_{filter_value}")
        allure.attach.file(screenshot_path, name=f"Filter_{filter_type}_{filter_value}", attachment_type=allure.attachment_type.PNG)
        logger.info(f"Applied {filter_type} filter: {filter_value}, result: {context.filter_result}")
    except TimeoutException as te:
        logger.error(f"Timeout applying {filter_type} filter {filter_value}: {te}")
        context.filter_result = False
    except NoSuchElementException as ne:
        logger.error(f"{filter_type} filter element not found: {ne}")
        context.filter_result = False
    except ElementClickInterceptedException as ice:
        logger.error(f"Click intercepted applying {filter_type} filter {filter_value}: {ice}")
        context.filter_result = False

@then('products should be shown "{expected}"')
def step_impl(context, expected):
    try:
        expected_bool = expected.lower() == "true"
        if expected_bool:
            assert context.filter_result, f"Expected products for filter but none found"
            logger.info("Assertion passed: Products found for valid filter")
        else:
            assert not context.filter_result, f"Unexpected products shown for invalid filter"
            logger.info("Assertion passed: No products for invalid filter")

        screenshot_path = ScreenshotUtil.capture_screenshot(context.driver, f"FilterValidation_{expected}")
        allure.attach.file(screenshot_path, name=f"FilterValidation_{expected}", attachment_type=allure.attachment_type.PNG)

    except AssertionError as ae:
        logger.error(f"Assertion failed: {ae}")
        screenshot_path = ScreenshotUtil.capture_screenshot(context.driver, "FilterValidation_Failure")
        allure.attach.file(screenshot_path, name="FilterValidation_Failure", attachment_type=allure.attachment_type.PNG)
        raise
