import matplotlib.pyplot as pl
import math
import numpy as np
x0 = .75
y0 = .2
x1 = 1.25
y1 = 0.475
xarr = []
yarr = []
xarr.append(x0)
xarr.append(x1)
yarr.append(y0)
yarr.append(y1)
pl.plot(xarr,yarr)

x = np.array(range(100))
y = math.exp(-x) +x -1 
pl.plot(x,y)
pl.show()