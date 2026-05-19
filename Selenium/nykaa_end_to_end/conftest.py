
import pytest
import configparser
import subprocess
import os
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions


# -----------------------------
# CLI option for config file
# -----------------------------
def pytest_addoption(parser):
    parser.addoption("--config", action="store", default="config/config.properties")


# -----------------------------
# Load config
# -----------------------------
@pytest.fixture(scope="session")
def config(pytestconfig):
    parser = configparser.ConfigParser()
    parser.read(pytestconfig.getoption("--config"))
    return parser["DEFAULT"]


# -----------------------------
# WebDriver setup
# -----------------------------
@pytest.fixture(scope="session")
def driver(config):
    browser = config.get("browser", "chrome").lower()

    if browser == "chrome":
        options = ChromeOptions()
        if config.getboolean("headless", False):
            options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)

    elif browser == "edge":
        options = EdgeOptions()
        if config.getboolean("headless", False):
            options.add_argument("--headless")
        driver = webdriver.Edge(options=options)

    else:
        raise ValueError(f"Unsupported browser: {browser}")

    driver.maximize_window()
    driver.implicitly_wait(config.getint("implicit_wait", 10))

    yield driver
    driver.quit()


# -----------------------------
# Create required folders
# -----------------------------
def pytest_sessionstart(session):
    base = "reports"

    os.makedirs(os.path.join(base, "allure-results"), exist_ok=True)
    os.makedirs(os.path.join(base, "screenshots"), exist_ok=True)
    os.makedirs(os.path.join(base, "allure-report"), exist_ok=True)


# -----------------------------
# Auto-generate Allure HTML report
# -----------------------------
def pytest_sessionfinish(session, exitstatus):
    import os
    import subprocess

    results_dir = os.path.join("reports", "allure-results")
    report_dir = os.path.join("reports", "allure-report")

    if not os.path.exists(results_dir) or not os.listdir(results_dir):
        print("\nNo Allure results found. Skipping report generation.")
        return

    # USE EXACT PATH FROM YOUR SYSTEM
    allure_cmd = r"C:\Users\yogalakshmi\scoop\apps\allure\current\bin\allure.bat"

    try:
        subprocess.run(
            [allure_cmd, "generate", results_dir, "-o", report_dir, "--clean"],
            check=True
        )

        print(f"\nAllure report generated at: {report_dir}")

        index_html = os.path.join(report_dir, "index.html")
        print(f"Open in browser: {index_html}")

    except Exception as e:
        print(f"\nFailed to generate Allure report: {e}")