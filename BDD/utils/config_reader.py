import configparser
from utils.logger import LogGen

logger = LogGen.loggen()


class ConfigReader:
    config = configparser.ConfigParser()  #  ConfigParser is class and config is a object
    config.read("config/config.ini")

    @staticmethod
    def get_base_url():
        url = ConfigReader.config.get(
            "DEFAULT", #in config.txt it is in default mode
            "base_url"
        )
        logger.info(f"Base URL fetched : {url}")
        return url

    @staticmethod
    def get_browser():
        browser = ConfigReader.config.get(
            "DEFAULT",
            "browser"
        )
        logger.info(f"Browser fetched : {browser}")
        return browser

    @staticmethod
    def get_timeout():
        timeout = ConfigReader.config.getint(
            "DEFAULT",
            "timeout"
        )
        logger.info(f"Timeout fetched : {timeout}")
        return timeout

    @staticmethod
    def get_implicit_wait():
        implicit_wait = ConfigReader.config.getint(
            "DEFAULT",
            "implicit_wait"
        )
        logger.info(
            f"Implicit wait fetched : "
            f"{implicit_wait}"
        )
        return implicit_wait

    @staticmethod
    def get_headless():
        headless = ConfigReader.config.getboolean(
            "DEFAULT",
            "headless"
        )
        logger.info(f"Headless mode : {headless}")
        return headless



    #5 funcs each is for each lines in config.ini