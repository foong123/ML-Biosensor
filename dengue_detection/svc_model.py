import pickle
import pandas as pd
import numpy as np
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler 
from sklearn.model_selection import train_test_split

# Load csv data
train = pd.read_csv("D:/unmc degree/year 4/fyp/project_git/dengue/train_EIS_dengue.csv")
test = pd.read_csv("D:/unmc degree/year 4/fyp/project_git/dengue/test_EIS_dengue.csv")

X_train = train.drop('ID', axis=1).drop('label', axis=1).values
y_train = train["label"].values    #y values
X_test  = test.drop('ID', axis=1).drop('label', axis=1).values
y_test = test["label"].values  #y values

# Feature Scaling
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

filename = 'classification_model_svr.sav'

# load the model from disk
loaded_model = pickle.load(open(filename, 'rb'))
y_pred = loaded_model.predict(X_test)

#Model Evaluation 
print ('\nClasification report:\n', classification_report(y_test, y_pred))
print ('\nConfussion matrix:\n',confusion_matrix(y_test, y_pred))