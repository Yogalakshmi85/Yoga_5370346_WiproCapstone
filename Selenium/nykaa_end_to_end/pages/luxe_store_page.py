from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from pages.product_page import ProductPage

class LuxeStorePage(BasePage):
    def apply_filter(self):
        # Expand Brand filter
        brand_filter = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//span[text()="Brand"]'))
        )
        brand_filter.click()

        # Click Gucci brand option
        gucci_option = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//label[contains(.,"Gucci")]'))
        )
        gucci_option.click()
        active_filter = self.wait.until(
            EC.presence_of_element_located((By.XPATH, '//span[contains(text(),"Gucci")]'))
        )
        assert active_filter is not None, "Gucci filter not applied!"
        print("Gucci filter verified.")

    def select_product(self):
        # Click the first product card
        product = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//div[@class="product-listing"]//a[1]'))
        )
        product.click()

        # Switch to new product tab
        self.driver.switch_to.window(self.driver.window_handles[-1])
        return ProductPage(self.driver)
