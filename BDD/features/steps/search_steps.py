from behave import given, when, then
from pages.home_page import HomePage
from utils.logger import LogGen
from utils.screenshot_util import ScreenshotUtil
import allure
from selenium.common.exceptions import NoSuchElementException, TimeoutException

logger = LogGen.loggen()

@given("I am inside Nykaa homepage")
def step_impl(context):
    try:
        context.home_page = HomePage(context.driver)
        logger.info("Opened Nykaa homepage")
        assert "nykaa" in context.driver.current_url.lower(), "Homepage not loaded correctly"
        screenshot_path = ScreenshotUtil.capture_screenshot(context.driver, "Homepage_Loaded")
        allure.attach.file(screenshot_path, name="Homepage_Loaded", attachment_type=allure.attachment_type.PNG)
    except (AssertionError, TimeoutException, NoSuchElementException) as e:
        logger.error(f"Homepage validation failed: {e}")
        screenshot_path = ScreenshotUtil.capture_screenshot(context.driver, "Homepage_Error")
        allure.attach.file(screenshot_path, name="Homepage_Error", attachment_type=allure.attachment_type.PNG)
        raise

@when('I search for product "{search_text}"')
def step_impl(context, search_text):
    try:
        context.search_text = search_text
        context.search_result = context.home_page.search_product(search_text)
        logger.info(f"Searched for product: {search_text}")
    except (NoSuchElementException, TimeoutException) as e:
        logger.error(f"Search failed: {e}")
        screenshot_path = ScreenshotUtil.capture_screenshot(context.driver, f"Search_{search_text}_Error")
        allure.attach.file(screenshot_path, name=f"Search_{search_text}_Error", attachment_type=allure.attachment_type.PNG)
        raise

@then("I should see an error message for invalid search")
def step_impl(context):
    try:
        assert context.search_result == "error", f"Expected error for {context.search_text}, got {context.search_result}"
        logger.info("Assertion passed: Invalid search error message displayed")
    except AssertionError as ae:
        logger.error(f"Assertion failed: {ae}")
        screenshot_path = ScreenshotUtil.capture_screenshot(context.driver, "InvalidSearch_Failure")
        allure.attach.file(screenshot_path, name="InvalidSearch_Failure", attachment_type=allure.attachment_type.PNG)
        raise

@then("I should see product results displayed")
def step_impl(context):
    try:
        assert context.search_result == "results", f"Expected results for {context.search_text}, got {context.search_result}"
        logger.info("Assertion passed: Product results displayed")
    except AssertionError as ae:
        logger.error(f"Assertion failed: {ae}")
        screenshot_path = ScreenshotUtil.capture_screenshot(context.driver, "ValidSearch_Failure")
        allure.attach.file(screenshot_path, name="ValidSearch_Failure", attachment_type=allure.attachment_type.PNG)
        raise

@then("I validate empty cart")
def step_impl(context):
    try:
        result = context.home_page.validate_empty_cart()
        assert result, "Empty cart validation failed"
        logger.info("Assertion passed: Cart is empty")
        screenshot_path = ScreenshotUtil.capture_screenshot(context.driver, "Empty_Cart")
        allure.attach.file(screenshot_path, name="Empty_Cart", attachment_type=allure.attachment_type.PNG)
    except (NoSuchElementException, TimeoutException, AssertionError) as e:
        logger.error(f"Empty cart validation failed: {e}")
        screenshot_path = ScreenshotUtil.capture_screenshot(context.driver, "EmptyCart_Error")
        allure.attach.file(screenshot_path, name="EmptyCart_Error", attachment_type=allure.attachment_type.PNG)
        raise
