import pickle
import pandas as pd
import numpy as np
import sys

from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler 
from sklearn.model_selection import train_test_split
from datetime import datetime

# Load csv data
train = pd.read_csv("/home/pi/Desktop/fyp/project/dataset/EIS/train_disease_EIS.csv")
test = pd.read_csv("{}".format(str(sys.argv[1])))

X_train = train.drop('ID', axis=1).drop('label', axis=1).values
y_train = train["label"].values    #y values
X_test  = test.drop('ID', axis=1).drop('label', axis=1).values
y_test = test["label"].values  #y values

# Feature Scaling
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

filename = '/home/pi/Desktop/fyp/project/multi_disease_detection/classification_multiclass_model_svc.sav'

# load the model from disk
loaded_model = pickle.load(open(filename, 'rb'))
predicted = loaded_model.predict(X_test)

result = []

for i in range(len(predicted)):
    if predicted[i] == 0 or predicted[i] == 2 or predicted[i] == 4 or predicted[i] == 6:
        result.append("Negative")
    elif predicted[i] == 1:
        result.append("Positive for Chicken Aneamia")
    elif predicted[i] == 3:
        result.append("Positive for H1N1 virus")
    elif predicted[i] == 5:
        result.append("Positive for Infectious Bursal Disease")
    elif predicted[i] == 7:
        result.append("Positive for Zika Virus")

#Current timestamp
dataTimeObj = datetime.now()
timestampStr = dataTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%d)")

f = open("/home/pi/Desktop/fyp/project/GUI/ML_results/Disease_results/Disease_result.txt", "w+")
f.write("Test results: {}".format(result))
f.write("\n")
f.write("Check Time : {}".format(timestampStr))
f.close()