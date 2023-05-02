import tensorflow as tf

network = [
    tf.keras.layers.Conv2D(filters=32, kernel_size=(3, 3), input_shape=(64, 64, 1), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(filters=16, kernel_size=(3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(units=100, activation='relu'),
    tf.keras.layers.Dense(units=2, activation='relu')
]

model = tf.keras.Sequential(network)
model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mse'])
model.save('D:\\PycharmProjects\\self_driving_car_server\\model')