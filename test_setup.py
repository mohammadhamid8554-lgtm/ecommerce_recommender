import sys
from src.logger import logging
from src.exception import CustomException


if __name__ == "__main__":
    logging.info("Testing logging configuration...")
    try:
        a = 1 / 0
    except Exception as e:
        logging.error("Divided by zero successfully caught.")
        raise CustomException(e, sys)