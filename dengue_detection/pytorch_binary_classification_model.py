import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import torch.nn as nn
import torch
import torch.nn.functional as F
import seaborn as sn

# Import tensor dataset & data loader
from torch.utils.data import TensorDataset, DataLoader
from sklearn.preprocessing import StandardScaler 
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix,plot_confusion_matrix

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
model = torch.load("D:/unmc degree/year 4/fyp/project_git/classification_model.pth")

#Predicting for X_test
y_pred = model(X_test)
y_pred = y_pred.detach().numpy()

# If the prediction is greater than 0.5 then the output is 1 else the output is 0
y_pred =(y_pred>0.5)

print ('\nClasification report:\n', classification_report(y_test, y_pred))
print ('\nConfussion matrix:\n',confusion_matrix(y_test, y_pred))

df_cm = pd.DataFrame(confusion_matrix(y_test, y_pred),index=["no dengue","dengue"], columns=["no dengue","dengue"])
sn.heatmap(df_cm,cmap=plt.cm.Blues, annot = True,fmt="d",linewidths=.5)
plt.title('Confusion matrix')
plt.show()
