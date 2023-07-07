import tensorflow as tf
import numpy as np
from PIL import Image
from random import shuffle

img_dir = 'C:\\Users\\chh36\\Desktop\\images\\'
steer_speed_dir = 'C:\\Users\\chh36\\Desktop\\speed_steer3.txt'

file = open(steer_speed_dir, 'r').read()
lines = file.split('\n')

train_indexs = []
test_indexs = []
train_steers = []
test_steers = []

def to_vec(steer):
    dictionary = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    if steer in dictionary:
        location = dictionary.index(steer)
        return location
    else:
        raise Exception('steer key is not in the dictionary')

def one_hot_encoding(idx, length):
    vec = np.zeros([length])
    vec[idx] = 1
    return vec

count = 0
max_num = 2590

shuffle(lines)

train_images = []
test_images = []

for line in lines:
    if count < max_num:
        temp1 = line.split(':')
        index = temp1[0]
        steer = temp1[1][0]
        steer = to_vec(steer)
        steer = one_hot_encoding(steer, 10)
        try:
            img = Image.open(img_dir+'{}.png'.format(index)).convert('L')
            img = np.array(img)
            train_images.append(img)
        except:
            continue
        train_steers.append(steer)
    else:
        temp1 = line.split(':')
        index = temp1[0]
        steer = temp1[1][0]
        steer = to_vec(steer)
        steer = one_hot_encoding(steer, 10)
        try:
            img = Image.open(img_dir + '{}.png'.format(index)).convert('L')
            img = np.array(img)
            test_images.append(img)
        except:
            continue
        test_steers.append(steer)
    count += 1

train_steers = np.array(train_steers)
test_steers = np.array(test_steers)

train_images = np.array(train_images)
train_images = train_images.astype('float32')
train_images = np.reshape(train_images, [train_images.shape[0], 64, 64, 1])/255.0

test_images = np.array(test_images)
test_images = test_images.astype('float32')
test_images = np.reshape(test_images, [test_images.shape[0], 64, 64, 1])/255.0

print(train_steers.shape)
print(train_images.shape)
print(test_steers.shape)
print(test_images.shape)

network2 = [
    tf.keras.layers.Conv2D(filters=32, kernel_size=(3, 3), input_shape=(64, 64, 1), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(filters=32, kernel_size=(3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(units=100, activation='relu'),
    tf.keras.layers.Dense(units=100, activation='relu'),
    tf.keras.layers.Dropout(0.6),
    tf.keras.layers.Dense(units=10, activation='softmax')
]

steer_model = tf.keras.Sequential(network2)
steer_model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
steer_model.fit(x=train_images, y=train_steers, validation_data=(test_images, test_steers), epochs=45)