import logging

def get_logger(name):
    # 创建一个logger对象
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # 创建一个文件处理器，将日志消息记录到文件中
    file_handler = logging.handlers.TimedRotatingFileHandler(f"{name}.log", when="midnight", interval=1, backupCount=7)
    file_handler.setLevel(logging.DEBUG)

    # 创建一个格式化器对象
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)

    # 将文件处理器添加到logger中
    logger.handlers.clear()
    logger.addHandler(file_handler)

    return logger