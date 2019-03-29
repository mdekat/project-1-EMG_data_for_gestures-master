"""
Created on Thu Mar 28 10:24:56 2019

@author: mdk
"""

#==== Importing libraries
import numpy as np
import pandas as pd
import os

#========= importing data from different files

#--- parameters
z = 0
numrows = -1
path = '< path to directory with datafiles >'

#--- calling files and storing data to X and y
for _ , dirs, _ in os.walk(path):
    for dirpath in dirs:
        #print(path+'//'+dirpt)
        newpath = path+'\\'+dirpath
        for _ , _ , files in os.walk(newpath):
            for file in files:
                filename = (newpath+'\\'+file)
                dataset = pd.read_csv(filename,
                      delim_whitespace=True,
                      skipinitialspace=True)
                if z == 0:
                    X = dataset.iloc[1:numrows,1:-1].values
                    y = dataset.iloc[1:numrows,-1].values
                    z+=1
                elif z != 0:
                    A = dataset.iloc[1:numrows,1:-1].values
                    b = dataset.iloc[1:numrows,-1].values
                    
                    X = np.concatenate((X,A), axis = 0)
                    y = np.concatenate((y,b), axis = 0)   
    break            


#==== preparing data for Model
    
#--- Splitting the dataset into the Training set and Test set
from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 0)

#--- Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

#==== Preparing and fitting Model

#--- Logitisc Regression
from sklearn.ensemble import RandomForestClassifier
classifier = RandomForestClassifier(n_estimators = 8, criterion = 'entropy', random_state = 0)
classifier.fit(X_train,y_train)

#--- Predicting the Test set results
y_pred = classifier.predict(X_test)

#=== presenting results

#--- Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)
print(cm)

#--- Calculate ratio 
for i in range(int(y.max())+1):
    a = cm[i,i]
    b = np.sum(cm[:,i])
    c = a/b
    print('There are %s predictions of %s which is a fraction of %f of the total amount.' % (a, i, c))
