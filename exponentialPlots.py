#Exponential Graph example

import matplotlib.pyplot as plt
import math
import numpy as np

t = np.linspace(0.001,2,100)
a, b, c = [[],[],[]]
for i in t:
    a.append(math.log(i))
    b.append(math.e ** i)
    c.append(a[-1]+b[-1])
#print (["{0:0.2f}".format(i) for i in a])
plt.plot(t,a,label="Natural logarithm")
plt.plot(t,b,label="Natural exponent")
plt.plot(t,c,label="Combined")
plt.legend()
plt.show()