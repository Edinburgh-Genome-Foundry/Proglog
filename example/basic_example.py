import time
from proglog import TqdmProgressBarLogger

logger = TqdmProgressBarLogger(bars=('main', 'sub'))
#logger(main__total=10, sub__total=10, sub__index=0, main__index=0)
messages = {0: 'Starting...', 4: 'Hang tight...', 7: 'Almost there...'}

for i in logger.iter_bar(main=range(10)):
    logger(message=messages.get(i, None))
    for j in logger.iter_bar(sub=range(10)):
        time.sleep(0.1)
print ('Done.')
