import pytest
import configparser
from selenium import webdriver

@pytest.fixture(scope="session")
def config():
    parser = configparser.ConfigParser()
    parser.read("config/config.properties")
    return parser["DEFAULT"]

@pytest.fixture(scope="session")
def driver(config):
    browser = config.get("browser", "chrome").lower()
    if browser == "chrome":
        driver = webdriver.Chrome()
    elif browser == "firefox":
        driver = webdriver.Firefox()
    else:
        raise ValueError(f"Unsupported browser: {browser}")

    driver.maximize_window()
    driver.implicitly_wait(config.getint("implicit_wait", 10))
    yield driver
    driver.quit()
