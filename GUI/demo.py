import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import torch.nn as nn
import torch
import torch.nn.functional as F
import sys

#print ('Argument List:', str(sys.argv))
#print (str(sys.argv[1]))

# Import tensor dataset & data loader
from torch.utils.data import TensorDataset, DataLoader
from sklearn.metrics import r2_score,mean_squared_error,mean_absolute_error
from sklearn.preprocessing import StandardScaler
from torch.autograd import Variable

train = pd.read_csv("/home/pi/Desktop/fyp/project/dataset/DPV/train_dpv.csv")
test = pd.read_csv("{}".format(str(sys.argv[1])))

X_train = train.drop('ID', axis=1).drop('label', axis=1).values
y_train = train['label'].values

X_test = test.drop('ID', axis=1).drop('label', axis=1).values
y_test = test['label'].values

# Feature Scaling
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

#Convert datatype of given numpy array to float32
X_test = X_test.astype('float32')
y_test = y_test.astype('float32')
X_test = torch.from_numpy(X_test)


INPUT_DIM = X_train.shape[1]    # input layer dimension
H1 = 93                         # hidden dimension #1
H2 = 90                         # hidden dimension #2
OUTPUT_DIM = 1                  # output layer dimension

class Regression(nn.Module):
    # Initialize the layers
    def __init__(self,INPUT_DIM,H1,H2,OUTPUT_DIM):
        super(Regression,self).__init__()
        self.input = nn.Linear(INPUT_DIM, H1)       # Adding the input layer and the first hidden layer
        self.layer2 = nn.Linear(H1, H2)             # Adding the second hidden layer
        #self.dropout1 = nn.Dropout(p=0.2)
        self.output = nn.Linear(H2, OUTPUT_DIM)     # Adding the output layer

    # Perform the computation
    def forward(self, x):
        x = F.relu(self.input(x))
        #x = self.dropout1(x)
        x = F.relu(self.layer2(x))
        x = self.output(x)
        return x

# Model class must be defined somewhere
model = torch.load("/home/pi/Desktop/fyp/project/panadol_prediction/regression_model.pth")

#Predicting for X_test
y_pred = model(X_test)
y_pred = y_pred.detach().numpy()

f = open("/home/pi/Desktop/fyp/project/GUI/Panadol_results/Panadol_result.txt", "w+")
f.write("Concentration of Panadol detected is: {}".format(y_pred))
f.write("\n")
f.close()

#y_pred = [y_pred[x].item() for x in range(len(y_pred))]
#y_test = [y_test[x].item() for x in range(len(y_test))]

# Comparing Actual and predicted values
#df = {}
#df['Actual Concentration'] = y_test
#df['Predicted Concentration'] = y_pred
#df = pd.DataFrame(df)
#print(df)

#percent_error = 0.0

#for i in range(len(y_pred)):

#    a = float(y_pred[i])
#    b = float(y_test[i])
#    c = abs(a-b)/b *100.0
#    percent_error = c + percent_error
      
#percent_error = percent_error/len(y_pred)

#print('percent_error: ', percent_error)
#print('R2: ', r2_score(y_pred = y_pred, y_true = y_test))
#print('mean squared error: ', mean_squared_error(y_pred = y_pred, y_true = y_test))
#print('mean absolute error: ', mean_absolute_error(y_pred = y_pred, y_true = y_test))

#Visualizing Actual and predicted values
#plt.plot(y_test, color = 'red', label = 'Real data')
#plt.plot(y_pred, color = 'blue', label = 'Predicted data')
#plt.title(percent_error)
#plt.legend()
#plt.grid()
#plt.show()
