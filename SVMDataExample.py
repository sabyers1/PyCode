#SVMDataExample.py 
#Tutorial on Support Vector Machine classification algorithm
#provided by Rohith Gandi  https://towardsdatascience.com/support-vector-machine-introduction-to-machine-learning-algorithms-934a444fca47

#get the sample dataset
import pandas as pd

df = pd.read_csv('./iris.csv') #data covers three species of iris flower
df = df.drop(['Id'],axis=1) #get rid of unneeded ID column of data.
target = df['Species']
s = set() #create unordered set of data
for val in target:
    s.add(val)
s = list(s)
rows = list(range(100,150))
df = df.drop(df.index[rows]) #remove last species of iris so binary set of data.

#visualize the sample dataset
import matplotlib.pyplot as plt

#assumes first 50 datapoint are 1 species and last 50 datapoints are 2nd species
x = df['SepalLengthCm']
y = df['PetalLengthCm']

setosa_x = x[:50]
setosa_y = y[:50]

versicolor_x = x[50:]
versicolor_y = y[50:]

fig=plt.figure(figsize=(6,8))
#fig= plt.figure(figsize=plt.figaspect(2.))
plt.subplot(211)
plt.scatter(setosa_x,setosa_y,marker='+',color='green',label='setosa')
plt.scatter(versicolor_x,versicolor_y,marker='_',color='red',label='versicolor')
plt.legend()
plt.ylabel('Petal Length (cm)')
#plt.xlabel('Sepal Length (cm)')
plt.title("Iris Species Visualization")
#fig.savefig('Data Visualization.png')
#plt.show() # Waits for user to close figure.
#print('Waiting to close visualization window...')
#plt.draw()
#plt.waitforbuttonpress(1) # Still displays but only waits 'x' seconds
#print("Window interaction closed.")

#train the sample dataset
from sklearn.utils import shuffle
#from sklearn.cross_validation import train_test_split
from sklearn.model_selection import train_test_split
import numpy as np
## Drop rest of the features and extract the target values
df = df.drop(['SepalWidthCm','PetalWidthCm'],axis=1)
Y = []
target = df['Species']
for val in target:
    if(val == 'Iris-setosa'):
        Y.append(-1)
    else:
        Y.append(1)
df = df.drop(['Species'],axis=1)
X = df.values.tolist()
## Shuffle and split the data into training and test set
X, Y = shuffle(X,Y)
x_train = []
y_train = []
x_test = []
y_test = []

x_train, x_test, y_train, y_test = train_test_split(X, Y, train_size=0.9)

x_train = np.array(x_train)
y_train = np.array(y_train)
x_test = np.array(x_test)
y_test = np.array(y_test)

y_train = y_train.reshape(90,1)
y_test = y_test.reshape(10,1)


plt.subplot(212)
#fig=plt.figure(figsize=(8,6))
plt.xlim(min(x)*0.95,max(x)*1.05)
plt.ylim(min(y)*0.95,max(y)*1.05)
i = 0
for fclass in y_train[:,0]:
    if fclass == 1:
        plt.plot(x_train[i,0],x_train[i,1],'r*')
    else :
        plt.plot(x_train[i,0],x_train[i,1],'go')
    i += 1
i = 0
for fclass in y_test[:,0]:
    if fclass == 1:
        plt.plot(x_test[i,0],x_test[i,1],'y+')
    else :
        plt.plot(x_test[i,0],x_test[i,1],'bp')
    i += 1

#plt.scatter(x_train[:,0],x_train[:,1],marker='_',color='black',label='Training')
#plt.scatter(x_test[:,0],x_test[:,0],marker='+',color='orange',label='Test')
#plt.legend()
#plt.text(0.15, 0.4,"Text on Chart",transform=fig.transFigure)
plt.xlabel('Sepal Length (cm)')
plt.ylabel('Petal Length (cm)')
plt.title('Testing outcome')
#plt.show() # Waits for user to close figure.


## Support Vector Machine 
import numpy as np

train_f1 = x_train[:,0]
train_f2 = x_train[:,1]

train_f1 = train_f1.reshape(90,1)
train_f2 = train_f2.reshape(90,1)

w1 = np.zeros((90,1))
w2 = np.zeros((90,1))

epochs = 1
alpha = 0.0001

print("Training on sample...")
while(epochs < 10000):
    y = w1 * train_f1 + w2 * train_f2
    prod = y * y_train
    #print(epochs)
    count = 0
    for val in prod:
        if(val >= 1):
            cost = 0
            w1 = w1 - alpha * (2 * 1/epochs * w1)
            w2 = w2 - alpha * (2 * 1/epochs * w2)
            
        else:
            cost = 1 - val 
            w1 = w1 + alpha * (train_f1[count] * y_train[count] - 2 * 1/epochs * w1)
            w2 = w2 + alpha * (train_f2[count] * y_train[count] - 2 * 1/epochs * w2)
        count += 1
    epochs += 1
print("Training cost calculated...")

#final prediction of data
from sklearn.metrics import accuracy_score

## Clip the weights 
index = list(range(10,90))
w1 = np.delete(w1,index)
w2 = np.delete(w2,index)

w1 = w1.reshape(10,1)
w2 = w2.reshape(10,1)
## Extract the test data features 
test_f1 = x_test[:,0]
test_f2 = x_test[:,1]

test_f1 = test_f1.reshape(10,1)
test_f2 = test_f2.reshape(10,1)
## Predict
y_pred = w1 * test_f1 + w2 * test_f2
predictions = []
for val in y_pred:
    if(val > 1):
        predictions.append(1)
    else:
        predictions.append(-1)

print("Accuracy score of training: {:.2f}".format(accuracy_score(y_test,predictions)))
plt.text(min(x), max(y)*.95,"Score: {:.2f}".format(accuracy_score(y_test,predictions))) #default transform is transData
plt.show()

