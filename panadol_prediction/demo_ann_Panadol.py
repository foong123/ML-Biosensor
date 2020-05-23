import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import torch.nn as nn
import torch
import torch.nn.functional as F
import threading
#print ('Argument List:', str(sys.argv))
#print (str(sys.argv[1]))

from sklearn.preprocessing import StandardScaler
from datetime import datetime

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

class Thread1(threading.Thread):
    def __init__(self, progress, input_filename):
        threading.Thread.__init__(self)
        self.progress = progress
        self.input_filename = input_filename
    def run(self):
        self.progress.start()  # Update progress bar
        train = pd.read_csv("/home/pi/Desktop/fyp/project/dataset/DPV/train_dpv.csv")
        test = pd.read_csv("{}".format(str(self.input_filename)))

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

        # Model class must be defined somewhere
        model = torch.load("/home/pi/Desktop/fyp/project/panadol_prediction/regression_model.pth")

        #Predicting for X_test
        y_pred = model(X_test)
        y_pred = y_pred.detach().numpy()
        #print(y_pred[0,0])

        results = []
        for i in range(len(y_pred)):
            results.append(y_pred[i,0])

        #print(results)

        #Current timestamp
        dataTimeObj = datetime.now()
        timestampStr = dataTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%d)")

        f = open("/home/pi/Desktop/fyp/project/GUI/ML_results/Panadol_results/Panadol_result.txt", "w+")
        f.write("Concentration of Panadol detected is: {}".format(results))
        f.write("\n")
        f.write("Check Time : {}".format(timestampStr))
        f.close()
        self.progress.stop()    # Stop update progress bar
        self.progress.quit()    # Quit
