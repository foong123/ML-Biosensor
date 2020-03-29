import pandas as pd
import numpy as np
import pickle

from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler,LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

train = pd.read_csv("D:/unmc degree/year 4/fyp/project_git/multi-disease/train_multiclass_disease_EIS.csv")
test = pd.read_csv("D:/unmc degree/year 4/fyp/project_git/multi-disease/test_multiclass_disease_EIS.csv")

# Seperating Predictors and Outcome values from train and test sets
X_train = train.drop('ID', axis=1).drop('label', axis=1).values
y_train = train.label.values.astype(object)
#print(Y_train_label)
X_test = test.drop('ID', axis=1).drop('label', axis=1).values
y_test = test.label.values.astype(object)

# Normalizing data
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

# Transforming non numerical labels into numerical labels
encoder = LabelEncoder()
# encoding train labels 
encoder.fit(y_train)
y_train = encoder.transform(y_train)
# print(y_train)
# encoding test labels
encoder.fit(y_test)
y_test = encoder.transform(y_test)
# print(y_test)

filename = 'classification_model_svr.sav'

# load the model from disk
loaded_model = pickle.load(open(filename, 'rb'))
y_pred = loaded_model.predict(X_test)
print(y_pred)
print(y_test)
#Model Evaluation 
print ('\nClasification report:\n', classification_report(y_test, y_pred))
print ('\nConfussion matrix:\n',confusion_matrix(y_test, y_pred))