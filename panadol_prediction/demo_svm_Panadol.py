import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle
import sys
import threading
from sklearn.preprocessing import StandardScaler
from datetime import datetime

class Thread3(threading.Thread):
    def __init__(self, progress):
        threading.Thread.__init__(self)
        self.progress = progress
    def run(self):
        self.progress.start()  # Update progress bar
        # Load csv data
        train = pd.read_csv("/home/pi/Desktop/fyp/project/dataset/DPV/train_dpv.csv")
        test = pd.read_csv("{}".format(str(sys.argv[1])))

        X_train = train.drop('ID', axis=1).drop('label', axis=1).values
        y_train = train["label"].values    #y values
        X_test  = test.drop('ID', axis=1).drop('label', axis=1).values
        y_test = test["label"].values  #y values

        # Feature Scaling
        sc = StandardScaler()
        X_train = sc.fit_transform(X_train)
        X_test = sc.transform(X_test)

        # Model class must be defined somewhere
        filename = "/home/pi/Desktop/fyp/project/panadol_prediction/regression_model_svr.sav"

        # load the model from disk
        loaded_model = pickle.load(open(filename, 'rb'))
        y_pred = loaded_model.predict(X_test)
        #print(y_pred)

        #Current timestamp
        dataTimeObj = datetime.now()
        timestampStr = dataTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%d)")

        f = open("/home/pi/Desktop/fyp/project/GUI/ML_results/Panadol_results/Panadol_result.txt", "w+")
        f.write("Concentration of Panadol detected is: {}".format(y_pred))
        f.write("\n")
        f.write("Check Time : {}".format(timestampStr))
        f.close()
        self.progress.stop()    # Stop update progress bar
        self.progress.quit()    # Quit