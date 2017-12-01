import time # for simulating computing time
from proglog import TqdmProgressBarLogger

def my_routine(iterations=10, logger='bars'):
    """Run several loops to showcase Proglog."""
    if logger == 'bars':
        logger = TqdmProgressBarLogger()
    for i in logger.iter_bar(iteration=range(iterations)):
        for j in logger.iter_bar(animal=['dog', 'cat', 'rat', 'duck']):
            time.sleep(0.1) # Simulate some computing time

my_routine()
