from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from pages.men_page import MenPage
from selenium.webdriver.support import expected_conditions as EC

class HomePage(BasePage):
    def go_to_men(self):
        men_link = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//a[text()="men"]'))
        )
        men_link.click()
        self.driver.switch_to.window(self.driver.window_handles[-1])

        return MenPage(self.driver)
