from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from pages.cart_page import CartPage

class ProductPage(BasePage):
    def add_to_cart(self):
        # Select size if required
        try:
            size_option = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, '//button[contains(text(),"100ml")]'))
            )
            size_option.click()
            print("Size selected.")
        except:
            print("No size selection needed.")

        # Now click Add to Bag
        add_btn = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//button[.//span[text()="Add to Bag"]]'))
        )
        add_btn.click()
        print("Added to cart.")
        self.driver.switch_to.window(self.driver.window_handles[-1])
        return CartPage(self.driver)
