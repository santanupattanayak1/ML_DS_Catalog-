#iceberg Kaggle

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from os.path import join as opj
import cv2
import matplotlib.pyplot as plt
from skimage.feature import hog
from skimage import data, color, exposure
#Load the data.
train = pd.read_json("/home/santanu/Downloads/Kaggle Iceberg/train.json")
test = pd.read_json("/home/santanu/Downloads/Kaggle Iceberg/test.json")

#Generate the training data
#Create 3 bands having HH, HV and avg of both
X_band_1=np.array([np.array(band).astype(np.float32).reshape(75, 75) for band in train["band_1"]])
X_band_2=np.array([np.array(band).astype(np.float32).reshape(75, 75) for band in train["band_2"]])
X_band_12 = (X_band_1 + X_band_2)/2
X_train = np.concatenate([X_band_1[:, :, :, np.newaxis], X_band_2[:, :, :, np.newaxis],((X_band_1+X_band_2)/2)[:, :, :, np.newaxis]], axis=-1)
XX_train = []
for i in xrange(X_train.shape[0]):
    img =  X_train[i,:,:,:]
    img =  cv2.resize(img,(197,197),interpolation=cv2.INTER_AREA)
    XX_train.append(img) 

XX_train = np.array(XX_train)

for i in xrange(XX_train.shape[0]):
    XX_train[i,:,:,0] = XX_train[i,:,:,0] - np.mean(XX_train[i,:,:,0])
    XX_train[i,:,:,1] = XX_train[i,:,:,1] - np.mean(XX_train[i,:,:,1])
    XX_train[i,:,:,2] = XX_train[i,:,:,2] - np.mean(XX_train[i,:,:,2])



X_band_1a=np.array([np.array(band).astype(np.float32).reshape(75, 75) for band in test["band_1"]])
X_band_2a=np.array([np.array(band).astype(np.float32).reshape(75, 75) for band in test["band_2"]])
X_band_12a = (X_band_1a + X_band_2a)/2

X_test = np.concatenate([X_band_1a[:, :, :, np.newaxis], X_band_2a[:, :, :, np.newaxis],((X_band_1a+X_band_2a)/2)[:, :, :, np.newaxis]], axis=-1)

XX_test = []
for i in xrange(X_test.shape[0]):
    img =  X_test[i,:,:,:]
    img =  cv2.resize(img,(197,197),interpolation=cv2.INTER_AREA)
    XX_test.append(img)
XX_test  = np.array(XX_test)


for i in xrange(XX_test.shape[0]):
    XX_test[i,:,:,0] = XX_test[i,:,:,0] - np.mean(XX_test[i,:,:,0])
    XX_test[i,:,:,1] = XX_test[i,:,:,1] - np.mean(XX_test[i,:,:,1])
    XX_test[i,:,:,2] = XX_test[i,:,:,2] - np.mean(XX_test[i,:,:,2])

#XX_train = np.array(XX_train)
#XX_test  = np.array(XX_test)
from sklearn.model_selection import KFold
from keras import applications
from keras.preprocessing.image import ImageDataGenerator
from keras import optimizers
from keras.models import Sequential, Model 
from keras.layers import Dropout, Flatten, Dense, GlobalAveragePooling2D
from keras import backend as k 
from keras.callbacks import ModelCheckpoint, LearningRateScheduler, TensorBoard, EarlyStopping
import os
import gc
import keras
import keras as k
from keras.layers import Conv2D, MaxPooling2D,Concatenate,concatenate
from keras.layers.core import Dense, Dropout, Flatten
from keras.layers.convolutional import Convolution2D, MaxPooling2D, ZeroPadding2D,MaxPooling1D,AveragePooling1D
from keras.optimizers import SGD
from keras.callbacks import EarlyStopping
from keras.callbacks import EarlyStopping, ModelCheckpoint, CSVLogger, Callback
from keras import callbacks
from keras.applications.inception_v3 import InceptionV3
from keras.preprocessing import image
#from keras.applications.resnet50 import preprocess_input, decode_predictions
from keras.models import Sequential

from keras.layers import Convolution2D,ZeroPadding2D,MaxPooling2D,Flatten,Dense,Dropout
def inception_pseudo():
    

    model = InceptionV3(weights='imagenet',include_top=False)
    x = model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(512, activation='relu')(x)
    x = Dropout(0.5)(x)
    x = Dense(512, activation='relu')(x)
    x = Dropout(0.5)(x)
    out = Dense(1,activation='sigmoid')(x)
    model_final = Model(input = model.input,outputs=out)

    for layer in model.layers[0:30]:
        layer.trainable = False
    return model_final

target_train=train['is_iceberg']

k = 0
kf = KFold(n_splits=5, random_state=0, shuffle=True)

for train_index, test_index in kf.split(X_train):
    k += 1 
    X_train1,X_test1 = XX_train[train_index],XX_train[test_index]
    y_train1, y_test1 = target_train[train_index],target_train[test_index]
    
    #adam = optimizers.Adam(lr=0.00001, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0)
    model_final = inception_pseudo()
    
    datagen = ImageDataGenerator(
             horizontal_flip = True,
                             vertical_flip = True,
                             width_shift_range = 0.1,
                             height_shift_range = 0.1,
                             channel_shift_range=0,
                             zoom_range = 0.2,
                             rotation_range = 20)

        #datagen.fit(x_train)

        #sgd = SGD(lr=1e-2, decay=1e-6, momentum=0.9, nesterov=True)

    #sgd = SGD(lr=1e-1, decay=1e-6, momentum=0.9, nesterov=True)
    adam = optimizers.Adam(lr=0.0001, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0)


    model_final.compile(optimizer=adam, loss=["binary_crossentropy"])
    reduce_lr = keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.50,
                              patience=5, min_lr=0.000001)
    #early = keras.callbacks.EarlyStopping(monitor='val_loss', min_delta=0, patience=5, verbose=0, mode='auto')
    
    callbacks = [
                EarlyStopping(monitor='val_loss', patience=25, mode='min', verbose=1),
             CSVLogger('keras-5fold-run-01-v1-epochs_ib.log', separator=',', append=False),reduce_lr,
                ModelCheckpoint(
                        'kera1-5fold-run-01-v1-fold-' + str('%02d' % (k + 1)) + '-run-' + str('%02d' % (1 + 1)) + '.check',
                        monitor='val_loss', mode='min', # mode must be set to max or Keras will be confused
                        save_best_only=True,
                        verbose=1)
            ]
    
    model_final.fit_generator(datagen.flow(X_train1,y_train1, batch_size=16),
                    #steps_per_epoch=50, epochs=5,verbose=1,validation_data=datagen.flow(X_test1,y_test1),validation_steps=(len(X_test1)//32)+1)
                #steps_per_epoch=25, epochs=100,verbose=1,validation_data=datagen.flow(X_test1,y_test1),validation_steps=25)
                steps_per_epoch=100, epochs=100,verbose=1,validation_data=(X_test1,y_test1),callbacks=callbacks)
 
    #model_final.fit(X_train1,y_train1,
    #          batch_size=32,
    #          epochs=100,
    #          callbacks=[early],
    #          verbose=1,
    #          validation_data=(X_test1,y_test1))
    model_name = 'kera1-5fold-run-01-v1-fold-' + str('%02d' % (k + 1)) + '-run-' + str('%02d' % (1 + 1)) + '.check'
    import h5py
    f = h5py.File('kera1-5fold-run-01-v1-fold-' + str('%02d' % (k + 1)) + '-run-' + str('%02d' % (1 + 1)) + '.check','r+')
    del f['optimizer_weights']
    f.close()
    del model_final
    model_final  = keras.models.load_model(model_name)
    model_name1 = '/home/santanu/Downloads/Kaggle Iceberg/' + 'nn_model_icv3_' + str(k) 
    model_final.save(model_name1)
    del model_final
    
    

