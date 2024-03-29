# -*- coding: utf-8 -*-
"""Oort.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Mh8CLqjl_mRxxrFeF9fyyGaswGQDygVa
"""



import tensorflow as tf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from os import listdir
from tensorflow.keras.preprocessing import sequence
import tensorflow as tfs
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Flatten
from tensorflow.keras.layers import LSTM

from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import load_model
from tensorflow.keras.callbacks import ModelCheckpoint

from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dropout
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Flatten, Conv2D, MaxPooling2D,LeakyReLU
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import os
import cv2, random

height=28
width=28
depth=1

inputShape = (height, width, depth)

# Prepare the train and test dataset.
from tensorflow import keras
batch_size = 64
(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

# Normalize data
x_train = x_train.astype("float32") / 255.0
x_train = np.reshape(x_train, (-1, 28, 28, 1))

x_test = x_test.astype("float32") / 255.0
x_test = np.reshape(x_test, (-1, 28, 28, 1))

from  keras.utils import np_utils
# y_train = np_utils.to_categorical(y_train)
# y_test= np_utils.to_categorical(y_test)
print(y_train[0])
print(y_train.shape,y_test.shape)
print(x_train.shape)
print(y_train[0],x_train[0])

from sklearn.utils import shuffle
x_train, y_train= shuffle(x_train, y_train, random_state=0)
X=[]
Y=[]
j=0
for i in range(40):
  X.append(x_train[j:j+3000])
  Y.append(y_train[j:j+3000])
  j+=1450

X=np.array(X)
Y=np.array(Y)
print(X.shape,Y.shape)

from tensorflow.keras.layers import BatchNormalization
class MODEL:
    @staticmethod
    def build():
        model = Sequential()
        model.add(Conv2D(128,(3,3),strides=(2, 2), padding="same",input_shape=inputShape) )
        model.add(LeakyReLU(alpha=0.2))
        model.add(MaxPooling2D(pool_size=(2, 2), strides=(1, 1), padding="same"))
        model.add(Dropout(0.25))

        # model.add(Conv2D(128/nl, (3, 3), strides=(2, 2), padding="same") )
        model.add(Conv2D(8, (3, 3), strides=(2, 2), padding="same") )
        
        model.add(Conv2D(16, (3, 3), strides=(2, 2), padding="same") )
        model.add(Conv2D(32, (3, 3), strides=(2, 2), padding="same") )
        model.add(Conv2D(64, (3, 3), strides=(2, 2), padding="same") )
        model.add(Flatten())
        # model.add(Dense(256/nl,activation='relu')) #add if acc <90
        # model.add(Dense(32/nl,activation='relu'))
        model.add(Dense(10,activation='softmax'))#for output layer
        return model

from sklearn.metrics import accuracy_score
def test_model(X_test, Y_test,  model, comm_round):
    # cce = tf.keras.losses.SparseCategoricalCrossentropy()
    # #logits = model.predict(X_test, batch_size=100)
    # logits = model.predict(X_test)
    # loss = cce(Y_test, logits)
    # acc = accuracy_score(tf.argmax(logits, axis=1), tf.argmax(Y_test, axis=1))
    # print('comm_round: {} | global_acc: {:.3%} | global_loss: {}'.format(comm_round, acc, loss))
    model.compile(  optimizer=keras.optimizers.Adam(),
    loss=keras.losses.SparseCategoricalCrossentropy(from_logits=False),
    metrics=[keras.metrics.SparseCategoricalAccuracy()],
)
    # loss,acc=model.evaluate(x_test,y_test)
    acc,loss=model.evaluate(x_test,y_test)
    return acc, loss
def scale_model_weights(weight, scalar):
    '''function for scaling a models weights'''
    weight_final = []
    steps = len(weight)
    for i in range(steps):
        weight_final.append(scalar * weight[i])
    return weight_final

def sum_scaled_weights(scaled_weight_list):
    '''Return the sum of the listed scaled weights. The is equivalent to scaled avg of the weights'''
    avg_grad = list()
    #get the average grad accross all client gradients
    for grad_list_tuple in zip(*scaled_weight_list):
        layer_mean = tf.math.reduce_sum(grad_list_tuple, axis=0)
        avg_grad.append(layer_mean)
      
    return avg_grad

from tensorflow import keras
import math

class LossHistory(keras.callbacks.Callback):
    def on_epoch_begin(self, epoch,logs={}):
        self.losses = []
        # self.val_losses = []

    def on_batch_end(self, batch, logs={}):
        # self.losses = []
        self.losses.append(logs.get('loss'))
        
        # self.val_losses.append(logs.get('val_loss'))

global1= MODEL()
global_model = global1.build()
comms_round = 50
# print(trainy[2].shape)
f= open("oortMNIST.txt", "a+") 
f.close()
f1= open("oortMNISTGlobal.txt", "a+") 
f1.close()

totalparticipants=40
epoch=np.random.randint(2,6,totalparticipants)
print(epoch)
epsilon=0.4
selectedp=random.sample(range(0, totalparticipants),int(epsilon*totalparticipants))
print(selectedp)
timep=np.random.uniform(1,10,totalparticipants)
print(timep)
preferredTime=5.0
Util=np.array([[i,0.0] for i in range(totalparticipants)])
prevutilsum=10000.0*totalparticipants
alpha=2
delta=0.5
from tensorflow.keras import backend as K
for comm_round in range(200):
  f= open("oortMNIST.txt", "a+") 
  f1= open("oortMNISTGlobal.txt", "a+") 
  global_weights = global_model.get_weights()
  scaled_local_weight_list = list()
  index=list({0,1,2,3,4})
  #random.shuffle(index)
  # print(index)
  f.write("\nCommunication Round:%d \n" %comm_round)
  print("Communication Round:",comm_round,"\n")
  feedback=[0 for i in range(totalparticipants)]
  f.write("\nSelected Participants:%s \n" %selectedp)
  f.write("\nUtility of all Participants:%s \n" %list(Util))

  for ind in selectedp:
    print("CLIENT NO: ",ind)
    
    local = MODEL()
    local_model=local.build()
    
    local_model.compile(optimizer=keras.optimizers.Adam(),
    loss=keras.losses.SparseCategoricalCrossentropy(from_logits=False),
    metrics=[keras.metrics.SparseCategoricalAccuracy()],
    
)
    local_model.set_weights(global_weights)
    #trainy[ind]=np.array(trainy[ind]).reshape(-1,1)
    history = LossHistory()
    local_model.fit(X[ind],Y[ind], epochs=epoch[ind],callbacks=[history])#,batch_size=1)#,validation_data=(x_test,y_test))
    # print("Accuracy: ",history.history["accuracy"][4])
    # local_model.evaluate(x_test, y_test)
    # testsampley=np.array([Y[ind][0]])
    # # print(testsampley)
    # testsamplex=np.array([X[ind][0]])
    # # print(testsamplex)
    # lloss,lacc=test_model(testsamplex,testsampley, local_model, comm_round)
    # print("LOSS",lloss,"ACC",lacc)


    # print(history.losses)
    # print(len(history.losses))
    losses=[]
    losses=history.losses
    losses=[i*i for i in losses]
    # print(losses)

    stat_util=len(losses)*math.sqrt(np.sum(losses)/len(losses))
    print(stat_util)
    utindex=0
    for i in range(len(Util)):
      if(Util[i][0]==ind):
        utindex=i
        break
    utindex=int(utindex)
    prev_util=Util[utindex][1]
    if(preferredTime<timep[ind]):
      sys_util=(preferredTime/timep[ind])*alpha
      Util[utindex]=[int(ind),stat_util*sys_util]

    else:
      Util[utindex]=[int(ind),stat_util]

    print(Util[utindex])
    # print("UTINDEX",utindex)
    if(comm_round!=0):

      if(Util[utindex][1]>prev_util):
        feedback[ind]=-1
    
    if(comm_round==199):
      f.write("Client No: %d\n" %ind)
      local_loss, local_acc = test_model(x_test,y_test, local_model, comm_round)
      f.write("Communication Round: %d Local Model ACCURACY: %f LOSS: %f \n" %(comm_round ,local_acc ,local_loss))
    scaling_factor=1.0/len(selectedp) #1/no.ofclients
    scaled_weights = scale_model_weights(local_model.get_weights(), scaling_factor)

    scaled_local_weight_list.append(scaled_weights)
    K.clear_session()

  average_weights = sum_scaled_weights(scaled_local_weight_list)
  # np.ndarray.sort(Util)
  # print(Util)
  for pp in range(totalparticipants):
    if(int(Util[pp][0]) not in selectedp):
      Util[pp][1]+=5.0
  Util=Util[Util[:, 1].argsort()[::-1]]
  # print(Util)
  # Util=Util[::,::-1]
  # Util = Util[::, Util[0,].argsort()[::-1]]
  # print(Util)
  cutoff=int((1-epsilon)*totalparticipants)-1
  c=0.95
  cutoffval=c*Util[cutoff][1]
  # print("Cutoff",cutoff)

  print("Cutoffval",cutoffval)
  selectedp=[]
  countr=0
  for pp in range(totalparticipants):
    if(Util[pp][1]>=cutoffval):
      if(feedback[int(Util[pp][0])]!=-1):
        selectedp.append(int(Util[pp][0]))
        # print("hello",pp)
      else:
        countr=countr+1

    elif(countr>0):
       selectedp.append(int(Util[pp][0]))
      #  print("hello11",pp)
       countr=countr-1
  print("selectedp",selectedp)
  print("Util",Util)
  if(prevutilsum>Util[:,1].sum()):
    preferredTime=preferredTime+delta
  
  prevutilsum=Util[:,1].sum()
  #global_model.compile(loss='categorical_crossentropy', optimizer=adam, metrics=['accuracy'])
  global_model.set_weights(average_weights)
  #val_acc,val_loss=global_model.evaluate(x_train,y_train)
  #print(val_loss,val_acc)
  global_loss, global_acc = test_model(x_test,y_test, global_model, comm_round)
  f.write("\nCommunication Round: %d GLOBAL MODEL ACCURACY: %f LOSS: %f \n" %(comm_round ,global_acc ,global_loss))
  print("GLOBAL ACC",global_acc,"GLOBAL LOSS",global_loss)
  f1.write("%f \t %f \n" %(global_acc ,global_loss))

        


  


  f.close()
  f1.close()

print(Y[0][0])

testsampley=np.array([Y[0][0]])
# print(testsampley)
testsamplex=np.array([X[0][0]])
# print(testsamplex)
loss,acc=local_model.evaluate(testsamplex,testsampley,batch_size=1)
print(loss)



Y=np.reshape(Y,(-1,1))

print(global_loss)

print(Util)
np.ndarray.sort(Util)
Util=Util[::-1]
print(Util)

print(Util)

Util=[[a,b+100] for a,b in Util if b==0.0]

print(Util)

print(Util[:,1].sum())

