import pytest
import allure
from pages.home_page import HomePage
from utils.logger import LogGen
from utils.screenshot_util import ScreenshotUtil
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

logger = LogGen.loggen()

@pytest.mark.usefixtures("driver", "config")
class TestShippingNegative:

    @pytest.mark.parametrize(
        "section_text, category_href, category_text, filter_type, brand_name, invalid_pincode",
        [
            ("men", "/mens/fragrance/luxe", "luxe-fragrances", "Brand", "Gucci", "123456")
        ]
    )
    def test_invalid_pincode(
        self, driver, config,
        section_text, category_text, category_href,
        filter_type, brand_name, invalid_pincode
    ):
        try:
            logger.info("--------------------------------------")
            logger.info("SHIPPING DETAILS VERIFICATION")
            logger.info("--------------------------------------")
            logger.info("START INVALID PINCODE TEST")

            driver.get(config["base_url"])

            home = HomePage(driver)
            men = home.go_to_men(section_text)

            luxe = men.go_to_luxe_store(category_text, category_href)
            luxe.apply_filter(brand_name, filter_type)

            product = luxe.select_product()
            cart = product.add_to_cart()

            cart.click_bag()
            cart.click_proceed()

            shipping = cart.click_continue_as_guest()

            # Fill with invalid pincode
            shipping.fill_details_from_excel(
                config["excel_path"],
                override_pincode=invalid_pincode
            )

            logger.info(f"Entered invalid pincode: {invalid_pincode}")

            # click button to trigger validation
            shipping.click_ship_to_this_address()

            # Validate error AFTER click
            error_element = shipping.wait.until(
                EC.presence_of_element_located((By.XPATH, '//p[contains(text(),"Invalid")]'))
            )

            assert error_element.is_displayed(), "Invalid pincode error not displayed"

            logger.info("Assertion passed: Invalid pincode validation shown")

            screenshot_path = ScreenshotUtil.capture_screenshot(driver, "Invalid_Pincode_Error")
            allure.attach.file(
                screenshot_path,
                name="Invalid_Pincode_Error",
                attachment_type=allure.attachment_type.PNG
            )

            logger.info("--------------------------------------")
            logger.info("END OF SHIPPING DETAILS VERIFICATION")
            logger.info("--------------------------------------")

        except AssertionError as ae:
            logger.error(f"Assertion failed: {str(ae)}")
            raise

        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise