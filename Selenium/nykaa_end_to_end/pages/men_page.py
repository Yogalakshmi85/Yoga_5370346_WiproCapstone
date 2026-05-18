from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from pages.luxe_store_page import LuxeStorePage

class MenPage(BasePage):
    def go_to_luxe_store(self):
        # Now find Luxe Store banner link
        luxe_link = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//a[contains(@href,"/mens/fragrance/luxe-fragrances")]'))
        )
        luxe_link.click()
        self.driver.switch_to.window(self.driver.window_handles[-1])

        return LuxeStorePage(self.driver)
