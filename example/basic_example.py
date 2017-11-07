'''In this example we go through the same loops twice, the
first time all loops will be plotted, the second time the inner
loop will not be plotted.
'''

import time
from proglog import TqdmProgressBarLogger

# Go through the loops and display progress bars

logger = TqdmProgressBarLogger()
for i in logger.iter_bar(main=range(10)):
    for j in logger.iter_bar(sub=range(10)):
        time.sleep(0.1)
    if i == 3:
        logger(message="We just passed i=3")
print ('Done. Now the same, ignoring the `sub` bar:')


# Go through the loops and display progress bar for outer loop only

logger = TqdmProgressBarLogger(ignored_bars=['sub'])
for i in logger.iter_bar(main=range(10)):
    for j in logger.iter_bar(sub=range(10)):
        time.sleep(0.1)
    if i == 3:
        logger(message="We just passed i=3")
print ('Done.')
