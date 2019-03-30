from tensorflow.keras.optimizers import *
from tensorflow.keras.layers import *
from tensorflow.keras.models import Sequential
import cv2
import numpy as np
import os
from random import shuffle
from tqdm import tqdm
import tensorflow as tf
from keras.utils.np_utils import to_categorical
import pprint
import json
import pickle


train_data = 'train'
test_data = 'test'



def one_hot_label(label):
    if label == 'benign':
        ohl = np.array([1, 0])
    else:
        ohl = np.array([0, 1])
    return ohl


def train_data_with_label():
    train_images = []
    for i in tqdm(os.listdir(train_data)):
        if (".jpg" in i):
          imgpath = os.path.join(train_data, i)
          img = cv2.imread(imgpath, cv2.IMREAD_GRAYSCALE)
          img = cv2.resize(img, (64, 64))

          jsonpath = os.path.join(train_data, i)
          pre, ext = os.path.splitext(jsonpath)
          jsonpath = pre + ".json"
          datastore = json.loads(open(jsonpath).read())
          label = str(datastore["meta"]["clinical"]["benign_malignant"])
          train_images.append([np.array(img), one_hot_label(label)])
    shuffle(train_images)
    return train_images


def test_data_function():
    test_images = []
    for i in tqdm(os.listdir(test_data)):
        path = os.path.join(test_data, i)
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, (64, 64))
        test_images.append([np.array(img)])
    return test_images


training_images = train_data_with_label()
testing_images = test_data_function()
tr_img_data = np.array([i[0] for i in training_images]).reshape(-1, 64, 64, 1)
tr_lbl_data = np.array([i[1] for i in training_images])

# y_train = to_categorical(y_train)
# y_test = to_categorical(y_test)

# tst_img_data = np.array([i[0] for i in testing_images]).reshape(-1, 64, 64, 1)
# tst_lbl_data = np.array([i[1] for i in testing_images])

model = Sequential()
model.add(InputLayer(input_shape=[64, 64, 1]))
model.add(Conv2D(filters=32, kernel_size=5, strides=1,
                 padding='same', activation='relu'))
model.add(MaxPool2D(pool_size=5, padding='same'))

model.add(Conv2D(filters=50, kernel_size=5, strides=1,
                 padding='same', activation='relu'))
model.add(MaxPool2D(pool_size=5, padding='same'))

model.add(Conv2D(filters=80, kernel_size=5, strides=1,
                 padding='same', activation='relu'))
model.add(MaxPool2D(pool_size=5, padding='same'))

model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(512, activation='relu'))
model.add(Dropout(rate=0.5))
model.add(Dense(2, activation='softmax'))
optimizer = Adam(lr=1e-3)

model.compile(optimizer=optimizer,
              loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(x=tr_img_data, y=tr_lbl_data, epochs=50, batch_size=1)
model.summary()

img = testing_images[0][0].reshape(-1, 64, 64, 1)
model_out = model.predict([img])
pprint.pprint(model_out)

