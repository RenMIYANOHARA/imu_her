import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random
from sklearn import decomposition
from sklearn.neighbors import KNeighborsClassifier


os.chdir('../')
cwd=os.getcwd()   #Get the current working directory
path_save=cwd+'\\Database\\'

exercices_names=['baseball','basketball','bow','jump','kendo','panch','push up','soccer','squat','swing']   #エクササイズ名


#Read the files in the Database
DB_X=np.load(path_save+"DB_X.npy")
DB_Y=np.load(path_save+"DB_Y.npy")
info=np.load(path_save+"info.npy")

#Randomize the sample
p=np.array([i for i in range(DB_X.shape[0])])    #hairetu
random.shuffle(p)

n=DB_X.shape[0]
n_sample_train=int(n*0.8)

#Separate train and test data
train_X=DB_X[p][:n_sample_train]
test_X=DB_X[p][n_sample_train:]

train_Y=DB_Y[p][:n_sample_train]
test_Y=DB_Y[p][n_sample_train:]

info_train=info[p][:n_sample_train]
info_test=info[p][n_sample_train:]

model=decomposition.PCA(n_components=2)    #Use the Principal component analysis
model.fit(X=train_X)

z_train=model.transform(X=train_X)
z_test=model.transform(X=test_X)

#Plot latent space
unique_class=np.unique(train_Y)   #Function to create an array with duplicates removed from np.array

cmap=plt.get_cmap('nipy_spectral')
colors=cmap(np.linspace(0,1,len(unique_class)))
colors=dict(zip(unique_class,colors))


figl=plt.figure(figsize=(16,8))
axl=figl.add_subplot(1,1,1)

for ind in unique_class:

    indices=[train_Y==ind]

    PC1=z_train[:,0][indices]
    PC2=z_train[:, 1][indices]

    axl.scatter(PC1,PC2,color=colors[ind],
                label=exercices_names[ind],
                s=40,marker='o')

    for i,txt in enumerate(info_train[indices]):
        axl.annotate(txt, (PC1[i],PC2[i]))

    indices=[test_Y==ind]

    PC1 = z_test[:, 0][indices]
    PC2 = z_test[:, 1][indices]

    axl.scatter(PC1, PC2, color=colors[ind],
                label=exercices_names[ind],
                s=40, linewidths='1',
                marker='P')

    for i,txt in enumerate(info_test[indices]):
        axl.annotate(txt, (PC1[i],PC2[i]))


axl.legend()

model=KNeighborsClassifier(n_neighbors=3,n_jobs=-1)
model.fit(z_train,train_Y)

print("train score:",model.score(z_train,train_Y))
print("test score:",model.score(z_test,test_Y))

data=z_test

model.predict(data)
print(model.predict(data))

for i in model.predict(data):
    print(exercices_names[i])