import time
from proglog import TqdmProgressBarLogger

logger = TqdmProgressBarLogger()
for i in logger.iter_bar(main=range(10)):
    for j in logger.iter_bar(sub=range(10)):
        time.sleep(0.1)
    if i == 3:
        logger(message="We just passed i=3")
print ('Done.')
