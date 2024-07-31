import logging
import logging.handlers

def get_logger(name):
    # Create a logger object
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Create a time rotated file handler
    file_handler = logging.handlers.TimedRotatingFileHandler(f"logs/{name}.log", when="d", interval=1)
    file_handler.setLevel(logging.DEBUG)

    # Create a formatter object
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)

    # Add the file handler to the logger
    logger.handlers.clear()
    logger.addHandler(file_handler)

    return logger