import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import torch.nn as nn
import torch
import torch.nn.functional as F
import seaborn as sn
import sys

# Import tensor dataset & data loader
from torch.utils.data import TensorDataset, DataLoader
from torch.autograd import Variable
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix,plot_confusion_matrix,accuracy_score
from datetime import datetime

# Load csv data
train = pd.read_csv("/home/pi/Desktop/fyp/project/dataset/EIS/train_disease_EIS.csv")
test = pd.read_csv("{}".format(str(sys.argv[1])))

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

# wrap up with Variable in pytorch
X_train = Variable(torch.Tensor(X_train).float())
X_test = Variable(torch.Tensor(X_test).float())
y_train = Variable(torch.Tensor(y_train).long())
y_test = Variable(torch.Tensor(y_test).long())

N_EPOCHS = 1000                     # times to run the model on complete data
INPUT_DIM = X_train.shape[1]        # input layer dimension
H1 = 122                             # hidden dimension #1
H2 = 122                             # hidden dimension #2
H3 = 48                             # hidden dimension #3
OUTPUT_DIM = 8                      # output layer dimension
lr = 0.001                          # learning rate

# Define NN
class NN_Model(nn.Module):
    # Initialize the layers
    def __init__(self,INPUT_DIM,H1,H2,OUTPUT_DIM):
        super(NN_Model,self).__init__()
        self.input = nn.Linear(INPUT_DIM, H1)
        self.layer2 = nn.Linear(H1, H2)
        self.layer3 = nn.Linear(H2, H3)
        self.output = nn.Linear(H2, OUTPUT_DIM)
        self.batchnorm1 = nn.BatchNorm1d(num_features = H1)
        self.batchnorm2 = nn.BatchNorm1d(num_features = H2)
        self.dropout1 = nn.Dropout(p=0.3)
        self.dropout2 = nn.Dropout(p=0.5)

    # Perform the computation
    def forward(self, X):

        X = F.relu(self.input(X))
        #X = self.dropout1(X)
        X = self.batchnorm1(X)
        X = F.relu(self.layer2(X))
        #X = self.batchnorm2(X)
        #X = self.dropout2(X)
        #X = F.relu(self.layer3(X))
        X = F.log_softmax(self.output(X), dim = 1)
        #X = F.softplus(self.fc3(X))
        return X

# Model class must be defined somewhere
model = torch.load("/home/pi/Desktop/fyp/project/multi_disease_detection/classification_multiclass_model.pth")
#Predicting for X_test
predict_out = model(X_test)
_, predicted = torch.max(predict_out, 1)

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