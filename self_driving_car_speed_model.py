import tensorflow as tf

import numpy as np

from PIL import Image

from os import listdir



dataset_dir = 'C:\\Users\\chh36\\Desktop\\'

training_dir = ['empty_view\\restored_img', 'saving_dir']



images, labels = [], []
test_img, test_lbl = [], []

max_num = 1100

for i, category in enumerate(training_dir):
    count = 0
    titles = listdir(dataset_dir+category)

    label = np.zeros([2])

    label[i] = 1

    for title in titles:

        img = Image.open(dataset_dir+category+'\\'+title).convert('L')

        img = np.array(img)
        if count < max_num:
            images.append(img)

            labels.append(label)
        else:
            test_img.append(img)
            test_lbl.append(label)

        count += 1

images = np.array(images)
labels = np.array(labels)
test_img = np.array(test_img)
test_lbl = np.array(test_lbl)

images = np.reshape(images, (images.shape[0], 64, 64, 1))
images = images.astype(np.float32)
test_img = np.reshape(test_img, (test_img.shape[0], 64, 64, 1))
test_img = test_img.astype(np.float32)

images = images/255.0
test_img = test_img/255.0

print(images.shape)
print(test_img.shape)

network = [

    tf.keras.layers.Conv2D(filters=32, kernel_size=(3, 3), input_shape=(64, 64, 1), activation='relu'),

    tf.keras.layers.MaxPooling2D((2, 2)),

    tf.keras.layers.Conv2D(filters=16, kernel_size=(3, 3), activation='relu'),

    tf.keras.layers.MaxPooling2D((2, 2)),

    tf.keras.layers.Flatten(),

    tf.keras.layers.Dense(units=100, activation='relu'),

    tf.keras.layers.Dense(units=2, activation='softmax')

]



speed_model = tf.keras.Sequential(network)

speed_model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

speed_model.fit(x=images, y=labels, validation_data=(test_img, test_lbl), epochs=10)

speed_model.save('D:\\PycharmProjects\\self_driving_car_server\\speed_model')