import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error,mean_squared_error, r2_score
import pickle

# Load csv data
train = pd.read_csv("D:/unmc degree/year 4/fyp/project_git/DPV/train_dpv.csv")
test = pd.read_csv("D:/unmc degree/year 4/fyp/project_git/DPV/test_dpv.csv")

X_train = train.drop('ID', axis=1).drop('label', axis=1).values
y_train = train["label"].values    #y values
X_test  = test.drop('ID', axis=1).drop('label', axis=1).values
y_test = test["label"].values  #y values

# Feature Scaling
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

#Debug
#print("Train_X", X_train)
#print("Train_y", y_train)

#print("X_test", X_test)
#print("y_test", y_test)

filename = 'regression_model_svr.sav'

# load the model from disk
loaded_model = pickle.load(open(filename, 'rb'))
y_pred = loaded_model.predict(X_test)

#Visualizing Actual and predicted values
plt.plot(y_test, color = 'red', label = 'Real data')
plt.plot(y_pred, color = 'blue', label = 'Predicted data')
plt.title('Prediction')
plt.legend()
plt.show()

y_pred = [y_pred[x] for x in range(len(y_pred))]
y_test = [y_test[x] for x in range(len(y_test))]

# Comparing Actual and predicted values
df = {}
df['Actual Concentration'] = y_test
df['Predicted Concentration'] = y_pred
df = pd.DataFrame(df)
print(df)

percent_error = 0.0

for i in range(len(y_pred)):

    a = float(y_pred[i])
    b = float(y_test[i])
    c = abs(a-b)/b *100.0
    percent_error = c + percent_error
      
percent_error = percent_error/len(y_pred)

print('percent_error: ', percent_error)
print('mean absolute error: ', mean_absolute_error(y_pred = y_pred, y_true = y_test))
print('mean squared error: ', mean_squared_error(y_pred = y_pred, y_true = y_test))
print('R2: ', r2_score(y_pred = y_pred, y_true = y_test))