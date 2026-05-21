from behave import given, when, then
from pages.login_page import LoginPage
from utils.logger import LogGen
from utils.screenshot_util import ScreenshotUtil
import allure
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException

logger = LogGen.loggen()

@given("I am on the Nykaa homepage")
def step_impl(context):
    try:
        context.login_page = LoginPage(context.driver)
        logger.info("Opened Nykaa homepage")

        assert "nykaa" in context.driver.current_url.lower(), "Homepage not loaded correctly"
        screenshot_path = ScreenshotUtil.capture_screenshot(context.driver, "Homepage_Loaded")
        allure.attach.file(screenshot_path, name="Homepage_Loaded", attachment_type=allure.attachment_type.PNG)

    except AssertionError as ae:
        logger.error(f"Assertion failed: {ae}")
        raise
    except TimeoutException as te:
        logger.error(f"Timeout waiting for homepage: {te}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in homepage step: {e}")
        raise

@when("I click Sign in")
def step_impl(context):
    try:
        context.login_page.click_signin()
        logger.info("Clicked Sign in button")

        assert context.driver.find_element(*context.login_page.popup_phone).is_displayed(), "Phone input not visible after Sign in"
        screenshot_path = ScreenshotUtil.capture_screenshot(context.driver, "Signin_Clicked")
        allure.attach.file(screenshot_path, name="Signin_Clicked", attachment_type=allure.attachment_type.PNG)

    except NoSuchElementException as ne:
        logger.error(f"Element not found during Sign in: {ne}")
        raise
    except ElementClickInterceptedException as ice:
        logger.error(f"Click intercepted on Sign in: {ice}")
        raise
    except AssertionError as ae:
        logger.error(f"Assertion failed: {ae}")
        raise

@when('I enter phone number "{phone}"')
def step_impl(context, phone):
    try:
        context.login_page.enter_phone(phone)
        logger.info(f"Entered phone number: {phone}")
        entered_value = context.driver.find_element(*context.login_page.popup_phone).get_attribute("value")

        assert entered_value == phone, "Phone number not entered correctly"
        screenshot_path = ScreenshotUtil.capture_screenshot(context.driver, "Phone_Entered")
        allure.attach.file(screenshot_path, name="Phone_Entered", attachment_type=allure.attachment_type.PNG)

    except NoSuchElementException as ne:
        logger.error(f"Phone input not found: {ne}")
        raise
    except AssertionError as ae:
        logger.error(f"Assertion failed: {ae}")
        raise

@when("I click Send OTP")
def step_impl(context):
    try:
        context.login_page.send_otp()
        logger.info("Clicked Send OTP")

        assert "auth" in context.driver.current_url, "Auth page not loaded after Send OTP"
        screenshot_path = ScreenshotUtil.capture_screenshot(context.driver, "Send_OTP_Clicked")
        allure.attach.file(screenshot_path, name="Send_OTP_Clicked", attachment_type=allure.attachment_type.PNG)

    except TimeoutException as te:
        logger.error(f"Timeout waiting for Auth page: {te}")
        raise
    except AssertionError as ae:
        logger.error(f"Assertion failed: {ae}")
        raise

@when('I re-enter phone number "{phone}" on Auth page')
def step_impl(context, phone):
    try:
        context.login_page.reenter_phone_on_auth(phone)
        logger.info(f"Re-entered phone number on Auth page: {phone}")
        entered_value = context.driver.find_element(*context.login_page.auth_phone).get_attribute("value")

        assert entered_value == phone, "Phone number not re-entered correctly on Auth page"
        screenshot_path = ScreenshotUtil.capture_screenshot(context.driver, "AuthPhone_Reentered")
        allure.attach.file(screenshot_path, name="AuthPhone_Reentered", attachment_type=allure.attachment_type.PNG)

    except NoSuchElementException as ne:
        logger.error(f"Auth phone input not found: {ne}")
        raise
    except AssertionError as ae:
        logger.error(f"Assertion failed: {ae}")
        raise

@when("I click Get OTP")
def step_impl(context):
    try:
        result = context.login_page.get_otp()
        if result:
            logger.info("OTP Verification page displayed (UI flow successful)")

            screenshot_path = ScreenshotUtil.capture_screenshot(context.driver, "OTP_Verification_Page")
            allure.attach.file(screenshot_path, name="OTP_Verification_Page", attachment_type=allure.attachment_type.PNG)
            assert context.login_page.is_otp_page_loaded(), "OTP verification page did not load"
        else:
            logger.info("OTP click was blocked (expected negative case)")

            screenshot_path = ScreenshotUtil.capture_screenshot(context.driver, "Get_OTP_Blocked")
            allure.attach.file(screenshot_path, name="Get_OTP_Blocked", attachment_type=allure.attachment_type.PNG)
            assert not context.login_page.is_otp_page_loaded(), "Unexpectedly loaded OTP page"

    except ElementClickInterceptedException as ice:
        logger.error(f"Click intercepted on Get OTP: {ice}")
        raise
    except AssertionError as ae:
        logger.error(f"Assertion failed: {ae}")
        raise

@then("OTP verification page should be displayed")
def step_impl(context):
    try:
        result = context.login_page.is_otp_page_loaded()

        assert result, "OTP verification page did not load"
        logger.info("Assertion passed: OTP verification page displayed")
        screenshot_path = ScreenshotUtil.capture_screenshot(context.driver, "OTP_Verification_Page")
        allure.attach.file(screenshot_path, name="OTP_Verification_Page", attachment_type=allure.attachment_type.PNG)

    except TimeoutException as te:
        logger.error(f"Timeout waiting for OTP page: {te}")
        raise
    except AssertionError as ae:
        logger.error(f"Assertion failed: {ae}")
        raise
