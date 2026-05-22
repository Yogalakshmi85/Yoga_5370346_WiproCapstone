from behave import given, when, then
from selenium.webdriver.support.wait import WebDriverWait

from pages.payment_page import PaymentPage
from utils.logger import LogGen
from utils.screenshot_util import ScreenshotUtil
import allure
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    ElementClickInterceptedException
)

logger = LogGen.loggen()

@when('I navigate to "{section}"')
def step_impl(context, section):
    try:
        context.men_page = context.home_page.go_to_men(section)
        assert section in context.driver.current_url.lower(), f"{section} page not loaded!"
        logger.info(f"Navigation successful: {section} page loaded")
        screenshot_path = ScreenshotUtil.capture_screenshot(context.driver, f"Section_{section}")
        allure.attach.file(screenshot_path, name=f"Section_{section}", attachment_type=allure.attachment_type.PNG)
    except AssertionError as ae:
        logger.error(f"Assertion failed: {ae}")
        screenshot_path = ScreenshotUtil.capture_screenshot(context.driver, f"Section_{section}_Failure")
        allure.attach.file(screenshot_path, name=f"Section_{section}_Failure", attachment_type=allure.attachment_type.PNG)
        raise
    except TimeoutException as te:
        logger.error(f"Timeout navigating to section: {te}")
        screenshot_path = ScreenshotUtil.capture_screenshot(context.driver, f"Section_{section}_Timeout")
        allure.attach.file(screenshot_path, name=f"Section_{section}_Timeout", attachment_type=allure.attachment_type.PNG)
        raise

@when('I go to "{category}" with href "{href}"')
def step_impl(context, category, href):
    try:
        context.category_page = context.men_page.go_to_specific_category(category, href)
        assert category in context.driver.current_url.lower(), f"{category} page not loaded!"
        logger.info(f"Navigation successful: {category} page loaded")
        screenshot_path = ScreenshotUtil.capture_screenshot(context.driver, f"{category}")
        allure.attach.file(screenshot_path, name=f"{category}", attachment_type=allure.attachment_type.PNG)

    except AssertionError as ae:
        logger.error(f"Assertion failed: {ae}")
        raise
    except NoSuchElementException as ne:
        logger.error(f"Category element not found: {ne}")
        raise

@then("I should land on {category} page")
def step_impl(context, category):
    try:
        current_url = context.driver.current_url.lower()
        assert category in current_url, f"page not loaded! Current URL: {current_url}"
        logger.info("Assertion passed: category page loaded successfully")
    except AssertionError as ae:
        logger.error(f"Assertion failed: {ae}")
        raise

@when("I apply filters")
def step_impl(context):
    try:
        for row in context.table:
            filter_type = row["filter_type"]
            filter_value = row["filter_value"]

            result = context.category_page.apply_filter(filter_type, filter_value)
            assert result, f"Filter {filter_type} -> {filter_value} failed"


            logger.info(f"Applied filter: {filter_type} -> {filter_value}")
            screenshot_path = ScreenshotUtil.capture_screenshot(context.driver, f"Filter_{filter_value}")
            allure.attach.file(screenshot_path, name=f"Filter_{filter_value}",
                               attachment_type=allure.attachment_type.PNG)


    except AssertionError as ae:
        logger.error(f"Assertion failed: {ae}")
        raise
    except TimeoutException as te:
        logger.error(f"Timeout applying filters: {te}")
        raise
    except NoSuchElementException as ne:
        logger.error(f"Filter element not found: {ne}")
        raise

@then('products should be filtered correctly')
def step_impl(context):
    try:
        # Already verified inside apply_filter
        logger.info(f"Assertion passed: Products filtered")
    except Exception as e:
        logger.error(f"Unexpected error verifying filter: {e}")
        raise

@then("I select a product")
def step_impl(context):
    try:
        product_concern = context.table[0]["product_concern"]
        context.product_page = context.category_page.select_product(product_concern)

        assert context.product_page is not None, "Product page not loaded!"
        logger.info("Product selected successfully")
        screenshot_path = ScreenshotUtil.capture_screenshot(context.driver, "Product_Selected")
        allure.attach.file(screenshot_path, name="Product_Selected", attachment_type=allure.attachment_type.PNG)

    except AssertionError as ae:
        logger.error(f"Assertion failed: {ae}")
        raise
    except TimeoutException as te:
        logger.error(f"Timeout selecting product: {te}")
        raise
    except NoSuchElementException as ne:
        logger.error(f"Product element not found: {ne}")
        raise

@then("I add the product to cart")
def step_impl(context):
    try:
        logger.info("Attempting to add product to cart")

        context.cart_page = context.product_page.add_to_cart()

        assert context.cart_page is not None, "Cart page not loaded!"
        logger.info("Product added to cart successfully")

        screenshot_path = ScreenshotUtil.capture_screenshot(context.driver, "Product_Added_To_Cart")
        allure.attach.file(
            screenshot_path,
            name="Product_Added_To_Cart",
            attachment_type=allure.attachment_type.PNG
        )

    except AssertionError as ae:
        logger.error(f"Assertion failed: {ae}")
        raise
    except TimeoutException as te:
        logger.error(f"Timeout while adding product to cart: {te}")
        raise


@then("I verify the cart")
def step_impl(context):
    try:
        logger.info("Verifying cart contents")

        context.cart_page.verify_cart()

        screenshot_path = ScreenshotUtil.capture_screenshot(context.driver, "Cart_Verified")
        allure.attach.file(screenshot_path, name="Cart_Verified", attachment_type=allure.attachment_type.PNG)

        logger.info("Cart verification successful")

    except AssertionError as ae:
        logger.error(f"Assertion failed: {ae}")
        raise

@then("I open the cart")
def step_impl(context):
    try:
        logger.info("Opening cart")

        context.cart_page.click_bag()

        screenshot_path = ScreenshotUtil.capture_screenshot(context.driver, "Cart_Opened")
        allure.attach.file(screenshot_path, name="Cart_Opened", attachment_type=allure.attachment_type.PNG)

        logger.info("Cart opened successfully")

    except Exception as e:
        logger.error(f"Error opening cart: {e}")
        raise

@then("I proceed to checkout")
def step_impl(context):
    try:
        logger.info("Proceeding to checkout")

        context.cart_page.click_proceed()

        screenshot_path = ScreenshotUtil.capture_screenshot(context.driver, "Proceed_Clicked")
        allure.attach.file(screenshot_path, name="Proceed_Clicked", attachment_type=allure.attachment_type.PNG)

        logger.info("Proceed clicked successfully")

    except Exception as e:
        logger.error(f"Error during proceed: {e}")
        raise

@then("I continue as guest")
def step_impl(context):
    try:
        logger.info("Continuing as guest")

        context.shipping_page = context.cart_page.click_continue_as_guest()

        assert context.shipping_page is not None, "Shipping page not loaded!"

        screenshot_path = ScreenshotUtil.capture_screenshot(context.driver, "Continue_As_Guest")
        allure.attach.file(screenshot_path, name="Continue_As_Guest", attachment_type=allure.attachment_type.PNG)

        logger.info("Successfully navigated to shipping page")

    except AssertionError as ae:
        logger.error(f"Assertion failed: {ae}")
        raise

@when('I enter shipping details from "{file_name}"')
def step_fill_shipping(context, file_name):
    try:
        logger.info(f"Entering shipping details using file: {file_name}")

        override_pincode = getattr(context, "override_pincode", None)

        context.shipping_page.fill_details_from_csv(
            file_name,
            override_pincode=override_pincode
        )

        current_url = context.driver.current_url.lower()
        assert "address" in current_url, "Not on shipping details page!"

        logger.info("Shipping details entered successfully")

        screenshot_path = ScreenshotUtil.capture_screenshot(
            context.driver, "Step_ShippingDetails_Entered"
        )
        allure.attach.file(
            screenshot_path,
            name="Step_ShippingDetails_Entered",
            attachment_type=allure.attachment_type.PNG
        )

    except AssertionError as ae:
        logger.error(f"Assertion failed in shipping step: {ae}")
        raise

    except TimeoutException as te:
        logger.error(f"Timeout while entering shipping details: {te}")
        raise

    except NoSuchElementException as ne:
        logger.error(f"Element not found in shipping form: {ne}")
        raise

@when("I click ship to this address")
def step_click_ship(context):
    try:
        logger.info("Clicking 'Ship to this address' button")

        context.next_page = context.shipping_page.click_ship_to_this_address()

        screenshot_path = ScreenshotUtil.capture_screenshot(
            context.driver, "Step_Click_Ship"
        )
        allure.attach.file(
            screenshot_path,
            name="Step_Click_Ship",
            attachment_type=allure.attachment_type.PNG
        )

        logger.info("Clicked ship button successfully")

    except TimeoutException as te:
        logger.error(f"Timeout clicking ship button: {te}")
        raise

    except NoSuchElementException as ne:
        logger.error(f"Ship button not found: {ne}")
        raise

@then("I should be navigated correctly based on pincode")
def step_validate_navigation(context):
    try:
        current_url = context.driver.current_url.lower()

        logger.info(f"Validating navigation. Current URL: {current_url}")

        if "payment" in current_url or "checkout" in current_url:
            logger.info("Successfully navigated to Payment Page")

        elif "address" in current_url:
            logger.warning("Stayed on address page → Invalid pincode scenario handled")

        else:
            raise AssertionError(f"Unexpected navigation: {current_url}")

        screenshot_path = ScreenshotUtil.capture_screenshot(
            context.driver, "Step_Navigation_Result"
        )
        allure.attach.file(
            screenshot_path,
            name="Step_Navigation_Result",
            attachment_type=allure.attachment_type.PNG
        )

    except AssertionError as ae:
        logger.error(f"Assertion failed in navigation validation: {ae}")
        raise

@then("I should be navigated to payment page if pincode is valid")
def step_validate_payment_page(context):
    try:
        logger.info("Validating navigation to Payment Page for valid pincode")

        current_url = context.driver.current_url.lower()
        logger.info(f"Current URL: {current_url}")

        wait = WebDriverWait(context.driver, 10)

        wait.until(
            lambda driver: "payment" in driver.current_url.lower()
        )

        assert "payment" in context.driver.current_url.lower(), \
            f"Navigation failed! Current URL: {context.driver.current_url}"
        logger.info("Assertion passed: Successfully navigated to Payment Page")

        screenshot_path = ScreenshotUtil.capture_screenshot(
            context.driver, "Step_PaymentPage_Validated"
        )
        allure.attach.file(
            screenshot_path,
            name="Step_PaymentPage_Validated",
            attachment_type=allure.attachment_type.PNG
        )

    except AssertionError as ae:
        logger.error(f"Assertion failed: {ae}")

        screenshot_path = ScreenshotUtil.capture_screenshot(
            context.driver, "Step_PaymentPage_Validation_Failure"
        )
        allure.attach.file(
            screenshot_path,
            name="Step_PaymentPage_Validation_Failure",
            attachment_type=allure.attachment_type.PNG
        )

        raise

    except TimeoutException as te:
        logger.error(f"Timeout during payment page validation: {te}")
        raise

@then("I select payment method")
def step_select_payment(context):
    try:
        logger.info("Selecting a payment method")

        payment_method = context.table[0]["payment_method"]
        context.payment_page = PaymentPage(context.driver)
        context.payment_page.click_payment_method(payment_method)

        logger.info(f"{payment_method} selected successful")

        screenshot_path = ScreenshotUtil.capture_screenshot(
            context.driver, "Step_payment_Selected"
        )
        allure.attach.file(
            screenshot_path,
            name="Step_payment_Selected",
            attachment_type=allure.attachment_type.PNG
        )

    except TimeoutException as te:
        logger.error(f"Timeout selecting payment: {te}")
        raise

    except NoSuchElementException as ne:
        logger.error(f"payment element not found: {ne}")
        raise

