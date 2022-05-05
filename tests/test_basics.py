import time  # for simulating computing time
from proglog import default_bar_logger
from proglog import TqdmProgressBarLogger


def my_routine(iterations=10, logger="bar"):
    """Run several loops to showcase Proglog."""
    logger = default_bar_logger(logger)  # shorthand to generate a bar logger
    for i in logger.iter_bar(iteration=range(iterations)):
        for j in logger.iter_bar(animal=["dog", "cat", "rat", "duck"]):
            time.sleep(0.02)  # simulate some computing time


def test_basic_log():
    my_routine()


def test_tqdm_log():
    logger = TqdmProgressBarLogger(ignored_bars=("animal",), min_time_interval=1.0)
    my_routine(logger=logger)
