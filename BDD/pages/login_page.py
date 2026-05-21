from selenium.common import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)

        self.signin_btn = (By.XPATH, "//button[contains(text(),'Sign in')]")
        self.popup_phone = (By.XPATH, "//input[@type='tel']")
        self.popup_send_otp = (By.XPATH, "//button[contains(text(),'Send OTP')]")
        self.auth_phone = (By.XPATH, "//input[@type='tel']")
        self.auth_get_otp = (By.XPATH, "//button[contains(text(),'Get OTP')]")
        self.otp_verification = (By.XPATH, "//span[contains(text(),'OTP Verification')]")

    def click_signin(self):
        self.wait.until(EC.element_to_be_clickable(self.signin_btn)).click()

    def enter_phone(self, phone):
        phone_input = self.wait.until(EC.visibility_of_element_located(self.popup_phone))
        phone_input.send_keys(phone)

    def send_otp(self):
        self.wait.until(EC.element_to_be_clickable(self.popup_send_otp)).click()
        # Wait until Auth page loads
        self.wait.until(EC.url_contains("auth"))

    def reenter_phone_on_auth(self, phone):
        phone_input = self.wait.until(EC.visibility_of_element_located(self.auth_phone))
        phone_input.clear()
        phone_input.send_keys(phone)

    def get_otp(self):
        try:
            self.wait.until(EC.element_to_be_clickable(self.auth_get_otp)).click()
            return True
        except ElementClickInterceptedException as e:
            return False

    def is_otp_page_loaded(self):
        try:
            self.wait.until(EC.presence_of_element_located(self.otp_verification))
            return True
        except:
            return False
