#Matplotlib Tutorial 2 on Transforms
#src: https://matplotlib.org/tutorials/advanced/transforms_tutorial.html#sphx-glr-tutorials-advanced-transforms-tutorial-py
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

x = np.arange(0, 10, 0.005)
y = np.exp(-x/2.) * np.sin(2*np.pi*x)

fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_xlim(0, 10)
ax.set_ylim(-1, 1)
ax.set_title("Dampened Oscillation")
ax.set_xlabel("Time (s)")
ax.set_ylabel("Amplitude (V)")
fig.suptitle('Plot Tutorial 2', fontsize=16)

xdata, ydata = 5, 0
xdisplay, ydisplay = ax.transData.transform((xdata, ydata))

bbox = dict(boxstyle="round", fc="0.8")
arrowprops = dict(
    arrowstyle="->",
    connectionstyle="angle,angleA=0,angleB=90,rad=10")

offset = 72
ax.annotate('data = (%.1f, %.1f)' % (xdata, ydata),
            (xdata, ydata), xytext=(-2*offset, offset), textcoords='offset points',
            bbox=bbox, arrowprops=arrowprops)

disp = ax.annotate('display = (%.1f, %.1f)' % (xdisplay, ydisplay),
                   (xdisplay, ydisplay), xytext=(0.5*offset, -offset),
                   xycoords='figure pixels',
                   textcoords='offset points',
                   bbox=bbox, arrowprops=arrowprops)

circ = mpatches.Circle((0.5, 0.5), 0.05, transform=ax.transAxes,
                       facecolor='lightblue', alpha=0.5)
#ax.set_aspect('equal')
ax.add_patch(circ)


plt.show()
