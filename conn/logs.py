import logging
import sys
import datetime

def get_logger(name:str, print_level = logging.DEBUG):
    formater = logging.Formatter(
        fmt="%(levelname)6s %(name)s[%(filename)s.%(lineno)-3d %(asctime)s] %(message)s",
        datefmt='%H:%M:%S',
    )
    time_now = datetime.datetime.now().strftime("%Y_%m_%d.%H_%M_%S")
    logger = logging.getLogger(name)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formater)
    stream_handler.setLevel(print_level)
    file_handler = logging.FileHandler(f'log/{time_now}.{name}.log')
    file_handler.setFormatter(formater)
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)
    return logger
