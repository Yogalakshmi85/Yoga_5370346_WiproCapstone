from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)

        # Step 1 - Popup
        self.signin_btn = (By.XPATH, "//button[contains(text(),'Sign in')]")
        self.popup_phone = (By.XPATH, "//input[@type='tel']")
        self.popup_send_otp = (By.XPATH, "//button[contains(text(),'Send OTP')]")

        # Step 2 - Auth page
        self.auth_phone = (By.XPATH, "//input[@type='tel']")
        self.auth_get_otp = (By.XPATH, "//button[contains(text(),'Get OTP')]")

    def login(self, phone):
        self.wait.until(EC.element_to_be_clickable(self.signin_btn)).click()

        self.wait.until(EC.visibility_of_element_located(self.popup_phone)).send_keys(phone)

        self.wait.until(EC.element_to_be_clickable(self.popup_send_otp)).click()

        self.wait.until(EC.url_contains("auth"))

        phone_input = self.wait.until(EC.visibility_of_element_located(self.auth_phone))
        phone_input.clear()
        phone_input.send_keys(phone)

        get_otp_btn = self.wait.until(EC.presence_of_element_located(self.auth_get_otp))

        # Manual OTP
        input("Enter OTP manually and press ENTER...")

        self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'OTP Verification')]"))
        )

        print("Otp verification page loaded")
