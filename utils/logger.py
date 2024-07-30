import logging

def get_logger(name):
    # Create a logger object
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Create a file handler that logs messages to a file
    file_handler = logging.FileHandler(f"{name}.log")
    file_handler.setLevel(logging.DEBUG)

    # Create a formatter object
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)

    # Add the file handler to the logger
    logger.handlers.clear()
    logger.addHandler(file_handler)

    return logger