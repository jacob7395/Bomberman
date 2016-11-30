import datetime
from datetime import timedelta
import time

x = time.clock()
d = x + 0.001


print(d)
print(x)

while (x < d):
    x = time.clock()
    print(x)
    time.sleep(0.1)
