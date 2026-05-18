import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CartPage(BasePage):
    def verify_cart(self):
        item = self.get_text(By.XPATH, '//button[@id="header-bag-icon"]')
        assert item is not None, "Cart is empty!"

    def click_bag(self):
        bag_click = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//button[@id="header-bag-icon"]'))
        )
        bag_click.click()
        time.sleep(2)
