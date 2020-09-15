""" Mersene_Twister.py is a Monte Carlo method simulation for approximating pi"""

import numpy as np
from matplotlib import pyplot

# generate N pseudorandom independent x and y-values on interval [0,1)
N = 10000
x_array = np.random.rand(N)
y_array = np.random.rand(N)

# Number of pts within the quarter circle x^2 + y^2 < 1 centered at the origin with radius r=1.
N_qtr_circle = sum(x_array ** 2 + y_array ** 2 < 1)

# True area of quarter circle is pi/4 and has N_qtr_circle points within it.
# True area of the square is 1 and has N points within it, hence we approximate pi with
pi_approx = 4 * float(N_qtr_circle) / N  # Typical values: 3.13756, 3.15156

# Create visualization of simulation technique
# split random arrays into two series, one inside circle and one outside.
xya = list(zip(x_array,y_array))  # pair x,y points for evaluation of location
inside_x, inside_y  = zip(*[pt for pt in xya if pt[0]**2 + pt[1]**2 < 1])
outside_x,outside_y = zip(*[pt for pt in xya if pt[0]**2 + pt[1]**2 >= 1])

# plot the inside and outside points used for approximation
pyplot.scatter(inside_x,inside_y,marker='.',color='green')
pyplot.scatter(outside_x,outside_y,marker='.',color='red')

# create dividing line for circle where y = sqrt(1-x^2)
x=[j for j in np.linspace(0.0,1.0,num=40)]
y=[(1.0-k**2)**0.5 for k in x]
pyplot.plot(x,y)

approx = "Pi approx: {:.5f} for N={:,}".format(pi_approx,N)
pyplot.title(approx)
pyplot.show()