#CovidGraph
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score

numdays = 45 #must be greater than 2

df = pd.DataFrame(
    {
    'Northeast'  :  [55982803,pd.Series(np.zeros(numdays))],
    'Midwest':  [68329004,pd.Series(np.zeros(numdays))],
    'South'  :  [125580448,pd.Series(np.zeros(numdays))],
    'West'   :  [78347268,pd.Series(np.zeros(numdays))]
    }
)
dIR = 0.0004 #Daily infection rate

for region in df.columns.values:
    df[region].iloc[1][1] = df[region].iloc[0]* dIR #initialize day 1 infections
    for i in range(2,numdays):
        df[region].iloc[1][i] = df[region].iloc[1][i-1] * math.e ** (dIR*i)
        #df[region].iloc[1][i] = df[region].iloc[1][i-1] * (1.0+dIR)
    print("The {} region max infections at {} days is {:,.0f}".format(region,numdays,df[region].iloc[1][numdays-1]))

#x = [1,2,3,5,6,7,8,9,10,12,13,14,15,16,18,19,21,22]
#y = [100,90,80,60,60,55,60,65,70,70,75,76,78,79,90,99,99,100]

x = np.arange(numdays)
y1 =  df[df.columns.values[0]].iloc[1]
y2 = df[df.columns.values[1]].iloc[1]
y3 = df[df.columns.values[2]].iloc[1]
y4 = df[df.columns.values[3]].iloc[1]

mymodel = np.poly1d(np.polyfit(x, y1, 3))

myline = np.linspace(1, numdays-1, 100)

ax=plt.scatter(x,y1,label=df.columns.values[0])
plt.scatter(x,y2,label=df.columns.values[1])
plt.scatter(x,y3,label=df.columns.values[2])
plt.scatter(x,y4,label=df.columns.values[3])
plt.plot(myline, mymodel(myline))
plt.yticks()
plt.title("Covid Infections")
plt.xlabel("Time")
plt.ylabel("Total Infected")
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x: "{:,}".format(int(x))))
plt.legend()
plt.text(max(x)*0.8,min(y1),"Fit: {:.0%}".format(r2_score(y1,mymodel(x))))
plt.show()
print("The R2 fit score is {:.3}".format(r2_score(y1,mymodel(x))))