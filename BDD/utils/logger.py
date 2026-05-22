import logging, os

class LogGen:
    @staticmethod
    def loggen():
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)

        logger = logging.getLogger("automation")   # named logger avoids pytest root conflict
        logger.setLevel(logging.INFO)

        logger.propagate = False

        if not any(isinstance(h, logging.FileHandler) for h in logger.handlers):
            file_handler = logging.FileHandler(os.path.join(log_dir, "automation.log"), mode="a")
            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        return logger
