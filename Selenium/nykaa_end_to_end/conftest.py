# # # import pytest
# # # import configparser
# # # from selenium import webdriver
# # #
# # # @pytest.fixture(scope="session")
# # # def config():
# # #     parser = configparser.ConfigParser()
# # #     parser.read("config/config.properties")
# # #     return parser["DEFAULT"]
# # #
# # # @pytest.fixture(scope="session")
# # # def driver(config):
# # #     browser = config.get("browser", "chrome").lower()
# # #     if browser == "chrome":
# # #         driver = webdriver.Chrome()
# # #     elif browser == "edge":
# # #         driver = webdriver.Edge()
# # #     else:
# # #         raise ValueError(f"Unsupported browser: {browser}")
# # #
# # #     driver.maximize_window()
# # #     driver.implicitly_wait(config.getint("implicit_wait", 10))
# # #     yield driver
# # #     driver.quit()
# #
# #
# #
# # import pytest
# # import configparser
# # import subprocess
# # import os
# # from selenium import webdriver
# # from selenium.webdriver.chrome.options import Options as ChromeOptions
# # from selenium.webdriver.edge.options import Options as EdgeOptions
# #
# # def pytest_addoption(parser):
# #     parser.addoption("--config", action="store", default="config/config.properties")
# #
# # @pytest.fixture(scope="session")
# # def config(pytestconfig):
# #     parser = configparser.ConfigParser()
# #     parser.read(pytestconfig.getoption("--config"))
# #     return parser["DEFAULT"]
# #
# # @pytest.fixture(scope="session")
# # def driver(config):
# #     browser = config.get("browser", "chrome").lower()
# #     if browser == "chrome":
# #         options = ChromeOptions()
# #         if config.getboolean("headless", False):
# #             options.add_argument("--headless")
# #         driver = webdriver.Chrome(options=options)
# #     elif browser == "edge":
# #         options = EdgeOptions()
# #         if config.getboolean("headless", False):
# #             options.add_argument("--headless")
# #         driver = webdriver.Edge(options=options)
# #     else:
# #         raise ValueError(f"Unsupported browser: {browser}")
# #
# #     driver.maximize_window()
# #     driver.implicitly_wait(config.getint("implicit_wait", 10))
# #     yield driver
# #     driver.quit()
# #
# # def pytest_sessionfinish(session, exitstatus):
# #     """Hook to generate Allure HTML report automatically after tests finish."""
# #     results_dir = os.path.join("reports", "allure-results")
# #     report_dir = os.path.join("reports", "allure-report")
# #
# #     if not os.path.exists(results_dir) or not os.listdir(results_dir):
# #         print("\nNo Allure results found. Skipping report generation.")
# #         return
# #
# #     try:
# #         subprocess.run(
# #             ["allure", "generate", results_dir, "-o", report_dir, "--clean"],
# #             check=True
# #         )
# #         print(f"\nAllure report generated at: {report_dir}")
# #     except FileNotFoundError:
# #         print("\nAllure CLI not found. Please install Allure and add it to PATH.")
# #     except Exception as e:
# #         print(f"\nFailed to generate Allure report automatically: {e}")
#
#
# import pytest
# import configparser
# import subprocess
# import os
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options as ChromeOptions
# from selenium.webdriver.edge.options import Options as EdgeOptions
#
# def pytest_addoption(parser):
#     parser.addoption("--config", action="store", default="config/config.properties")
#
# @pytest.fixture(scope="session")
# def config(pytestconfig):
#     parser = configparser.ConfigParser()
#     parser.read(pytestconfig.getoption("--config"))
#     return parser["DEFAULT"]
#
# @pytest.fixture(scope="session")
# def driver(config):
#     browser = config.get("browser", "chrome").lower()
#     if browser == "chrome":
#         options = ChromeOptions()
#         if config.getboolean("headless", False):
#             options.add_argument("--headless")
#         driver = webdriver.Chrome(options=options)
#     elif browser == "edge":
#         options = EdgeOptions()
#         if config.getboolean("headless", False):
#             options.add_argument("--headless")
#         driver = webdriver.Edge(options=options)
#     else:
#         raise ValueError(f"Unsupported browser: {browser}")
#
#     driver.maximize_window()
#     driver.implicitly_wait(config.getint("implicit_wait", 10))
#     yield driver
#     driver.quit()
#
# def pytest_sessionstart(session):
#     """Ensure required report directories exist before tests run."""
#     base_dir = "reports"
#     os.makedirs(os.path.join(base_dir, "allure-results"), exist_ok=True)
#     os.makedirs(os.path.join(base_dir, "screenshots"), exist_ok=True)
#     os.makedirs(os.path.join(base_dir, "allure-report"), exist_ok=True)
#
# def pytest_sessionfinish(session, exitstatus):
#     """Generate Allure HTML report automatically after tests finish."""
#     results_dir = os.path.join("reports", "allure-results")
#     report_dir = os.path.join("reports", "allure-report")
#
#     if not os.listdir(results_dir):
#         print("\nNo Allure results found. Skipping report generation.")
#         return
#
#     try:
#         subprocess.run(
#             ["allure", "generate", results_dir, "-o", report_dir, "--clean"],
#             check=True
#         )
#         print(f"\nAllure report generated at: {report_dir}")
#         index_html = os.path.join(report_dir, "index.html")
#         if os.path.exists(index_html):
#             print(f"Open the report in your browser: {index_html}")
#     except FileNotFoundError:
#         print("\nAllure CLI not found. Please install Allure and add it to PATH.")
#     except Exception as e:
#         print(f"\nFailed to generate Allure report automatically: {e}")


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

    # 👇 USE EXACT PATH FROM YOUR SYSTEM
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