import pytest
from pages.home_page import HomePage
from pages.login_page import LoginPage
from utils.excel_reader import ExcelReader
from utils.logger import LogGen

logger = LogGen.loggen()

@pytest.mark.usefixtures("driver", "config")
class TestNykaaE2E:
    @pytest.mark.parametrize(
        "section_text, category_href, category_text, filter_type, brand_name, payment_method",
        [
            ("men", "/mens/fragrance/luxe", "luxe-fragrances", "Brand", "Gucci", "Cash on delivery")
        ]
    )
    def test_nykaa_end_to_end(
        self, driver, config, section_text, category_text, category_href, filter_type, brand_name, payment_method
    ):
        try:

            logger.info("--------------------------------------")
            logger.info("STARTING END-TO-END NYKAA TEST")
            logger.info("--------------------------------------")

            driver.get(config["base_url"])
            logger.info(f"Opened base URL: {config['base_url']}")

            # Optional login
            # excel = ExcelReader(config["excel_path"])
            # phone = excel.get_phone()
            # login = LoginPage(driver)
            # login.login(phone)

            home = HomePage(driver)
            logger.info("Home page loaded successfully")

            men = home.go_to_men(section_text)
            assert section_text in driver.current_url.lower(), f"{section_text} page not loaded!"
            logger.info(f"Navigation successful: {section_text} page loaded")

            luxe = men.go_to_luxe_store(category_text, category_href)
            assert category_text in driver.current_url.lower(), f"{category_text} page not loaded!"
            logger.info(f"Navigation successful: {category_text} page loaded")

            logger.info(f"Applying filter: {filter_type} -> {brand_name}")
            luxe.apply_filter(brand_name, filter_type)
            logger.info(f"Filter applied successfully: {brand_name}")

            product = luxe.select_product()
            logger.info("Product selected from Luxe Store")

            cart = product.add_to_cart()
            logger.info("Product added to cart")

            cart.click_bag()
            logger.info("Navigated to cart page")

            cart.click_proceed()
            logger.info("Clicked Proceed on cart page")

            shipping = cart.click_continue_as_guest()
            logger.info("Continuing as guest")

            shipping.fill_details_from_excel(config["excel_path"])
            logger.info("Shipping details filled from Excel")

            payment = shipping.click_ship_to_this_address()
            logger.info("Navigated to payment page")

            payment.click_payment_method(payment_method)
            logger.info(f"Payment method selected: {payment_method}")

            logger.info("Order flow completed successfully")
            logger.info("--------------------------------------")
            logger.info("END TO END COMPLETED SUCCESSFULLY.")
            logger.info("--------------------------------------")

        except AssertionError as ae:
            logger.error(f"Assertion failed: {str(ae)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in end-to-end test: {str(e)}")
            raise
