import tensorflow as tf
import numpy as np
from PIL import Image

speed_steer_dir = 'text file directory'
img_dir = 'image directory'
saving_dir = 'saving directory'

split_ratio = 0.1
dictionary = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

def to_one_hot(key, arr_len):
    arr = np.zeros([arr_len])
    num = dictionary.index(key)
    arr[num] = 1
    return arr

file = open(speed_steer_dir, 'r').read()
file = file.split('\n')

images = []
steers = []

for i in file:
    title, rest = i.split(':')
    steer = rest[0]

    try:
        image = Image.open('{}\\{}.png'.format(img_dir, title+'.png')).convert('L')
        image = np.array(image)
        images.append(image)
    except:
        continue
    steer = to_one_hot(steer, len(dictionary))
    steers.append(steer)

steers = np.asarray(steers)
steers = np.reshape(steers, [steers.shape[0], len(dictionary)])

images = np.asarray(images)
images = np.reshape(images, (images.shape[0], 64, 64, 1))
images = images.astype(np.float32)/255.

split_point = int(images.shape[0]*split_ratio)
train_images, test_images = images[0:split_point], images[split_point:-1]
train_steers, test_steers = steers[0:split_point], steers[split_point:-1]

network = [
    tf.keras.layers.Conv2D(64, (3, 3), input_shape=(64, 64, 1), activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.MaxPool2D((2, 2)),
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu'),
    tf.keras.layers.MaxPool2D((2, 2)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(100, activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(10, activation='softmax')
]

model = tf.keras.Sequential(network)
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(x=train_images, y=train_steers, validation_data=(test_images, test_steers), epochs=50)

model.save(saving_dir)