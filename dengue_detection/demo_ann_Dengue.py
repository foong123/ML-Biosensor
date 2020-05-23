import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import torch.nn as nn
import torch
import torch.nn.functional as F
import sys
import threading

# Import tensor dataset & data loader
from sklearn.preprocessing import StandardScaler 
from datetime import datetime

class Thread2(threading.Thread):
    def __init__(self, progress):
        threading.Thread.__init__(self)
        self.progress = progress
    def run(self):
        self.progress.start()  # Update progress bar

        train = pd.read_csv("/home/pi/Desktop/fyp/project/dataset/dengue/train_EIS_dengue.csv")
        test = pd.read_csv("{}".format(str(sys.argv[1])))

        X_train = train.drop('ID', axis=1).drop('label', axis=1).values
        y_train = train["label"].values    #y values
        X_test  = test.drop('ID', axis=1).drop('label', axis=1).values
        y_test = test["label"].values  #y values

        # Feature Scaling
        sc = StandardScaler()
        X_train = sc.fit_transform(X_train)
        X_test = sc.transform(X_test)

        #Convert datatype of given numpy array to float32
        X_train = X_train.astype('float32')
        y_train = y_train.astype('float32')
        X_test = X_test.astype('float32')
        y_test = y_test.astype('float32')

        #add numpy to tensor 
        X_train = torch.from_numpy(X_train)
        y_train = torch.from_numpy(y_train)
        X_test = torch.from_numpy(X_test)

        N_EPOCHS = 400                  # times to run the model on complete data
        INPUT_DIM = X_train.shape[1]    # input layer dimension
        H1 = 20                         # hidden dimension #1
        OUTPUT_DIM = 1                  # output layer dimension
        lr = 1e-3                       # learning rate

        # Define NN
        class NN_Model(nn.Module):
            # Initialize the layers
            def __init__(self,INPUT_DIM,H1,OUTPUT_DIM):
                super(NN_Model,self).__init__()
                self.input = nn.Linear(INPUT_DIM, H1)       # Adding the input layer and the first hidden layer
                self.dropout1 = nn.Dropout(p=0.5)
                #self.layer2 = nn.Linear(H1, H2)             # Adding the second hidden layer
                self.output = nn.Linear(H1, OUTPUT_DIM)     # Adding the output layer

            # Perform the computation
            def forward(self, x):
                x = F.relu(self.input(x))
                x = self.dropout1(x)
                #x = F.relu(self.layer2(x))
                x = F.sigmoid(self.output(x))
                return x

        # Model class must be defined somewhere
        model = torch.load("/home/pi/Desktop/fyp/project/dengue_detection/classification_model.pth")

        #Predicting for X_test
        y_pred = model(X_test)
        y_pred = y_pred.detach().numpy()

        result = []

        # If the prediction is greater than 0.5 then the output is 1 else the output is 0
        y_pred =(y_pred>0.5)

        for i in range(len(y_pred)):
            if y_pred[i] == 1:
                result.append("Positive")
            else:
                result.append("Negative")

        #Current timestamp
        dataTimeObj = datetime.now()
        timestampStr = dataTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%d)")

        f = open("/home/pi/Desktop/fyp/project/GUI/ML_results/Dengue_results/Dengue_result.txt", "w+")
        f.write("Test results: {}".format(result))
        f.write("\n")
        f.write("Check Time : {}".format(timestampStr))
        f.close()
        self.progress.stop()    # Stop update progress bar
        self.progress.quit()    # Quit