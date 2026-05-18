import pytest
from pages.home_page import HomePage
from pages.login_page import LoginPage
from utils.excel_reader import ExcelReader

@pytest.mark.usefixtures("driver", "config")
def test_nykaa_end_to_end(driver, config):
    driver.get(config["base_url"])

    # Optional login
    # excel = ExcelReader(config["excel_path"])
    # phone = excel.get_phone()
    # login = LoginPage(driver)
    # login.login(phone)

    home = HomePage(driver)
    men = home.go_to_men()
    luxe = men.go_to_luxe_store()

    luxe.apply_filter()
    product = luxe.select_product()
    cart = product.add_to_cart()
    cart.click_bag()

    print("End-to-end Nykaa test passed successfully.")
