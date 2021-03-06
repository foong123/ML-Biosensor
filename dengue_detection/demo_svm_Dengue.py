import pickle
import pandas as pd
import numpy as np
import threading

from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler 
from datetime import datetime

class Thread4(threading.Thread):
    def __init__(self, progress, input_filename):
        threading.Thread.__init__(self)
        self.progress = progress
        self.input_filename = filename
    def run(self):
        self.progress.start()  # Update progress bar

        # Load csv data
        train = pd.read_csv("/home/pi/Desktop/fyp/project/dataset/dengue/train_EIS_dengue.csv")
        test = pd.read_csv("{}".format(str(self.input_filename)))

        X_train = train.drop('ID', axis=1).drop('label', axis=1).values
        y_train = train["label"].values    #y values
        X_test  = test.drop('ID', axis=1).drop('label', axis=1).values
        y_test = test["label"].values  #y values

        # Feature Scaling
        sc = StandardScaler()
        X_train = sc.fit_transform(X_train)
        X_test = sc.transform(X_test)

        filename = '/home/pi/Desktop/fyp/project/dengue_detection/classification_model_svr.sav'
        filename = 'classification_model_svr.sav'

        # load the model from disk
        loaded_model = pickle.load(open(filename, 'rb'))
        y_pred = loaded_model.predict(X_test)

        result = []

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
