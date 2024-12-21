import time
from logger import Logger

logger = Logger()


def timer_decorator(func):
    """
    A decorator to log the time taken by a function to execute.

    :param func: The function being decorated.
    :return: The wrapper function.
    """

    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        time_taken = end_time - start_time
        logger.info(f"Function '{func.__name__}' executed in {time_taken:.4f} seconds.")
        return result

    return wrapper
