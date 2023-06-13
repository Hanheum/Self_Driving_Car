import tensorflow as tf
import numpy as np
from serial import Serial
from picamera2 import Picamera2
from time import sleep

cam = Picamera2()
cam_config = cam.create_still_configuration(main={"size":(64, 64)})
cam.configure(cam_config)
cam.start()

data = ''
ser = Serial('/dev/ttyUSB0', 9600)

steer_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
speed_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
record_list = ['1', '2']
power_list = ['3', '4']

steer_interpreter = tf.lite.Interpreter(model_path='/home/hanheum/Desktop/steer_model.tflite')
steer_interpreter.allocate_tensors()

steer_input_details = steer_interpreter.get_input_details()
steer_output_details = steer_interpreter.get_output_details()

def steer_predicting(image):
    steer_interpreter.set_tensor(steer_input_details[0]['index'], image)
    steer_interpreter.invoke()
    output_data = steer_interpreter.get_tensor(steer_output_details[0]['index'])
    return output_data[0]

speed_interpreter = tf.lite.Interpreter(model_path='/home/hanheum/Desktop/speed_model.tflite')
speed_interpreter.allocate_tensors()

speed_input_details = speed_interpreter.get_input_details()
speed_output_details = speed_interpreter.get_output_details()

def speed_predicting(image):
    speed_interpreter.set_tensor(speed_input_details[0]['index'], image)
    speed_interpreter.invoke()
    output_data = speed_interpreter.get_tensor(speed_output_details[0]['index'])
    return output_data[0]

def capture():
    img = cam.capture_array()
    img = np.sum(img, axis=-1)
    img = img/3
    img = np.round(img)
    img = img.astype(np.float32)/255.
    img = np.rot90(img)
    img = np.rot90(img)
    img = np.reshape(img, (1, 64, 64, 1))
    return img

while True:
    img = capture()
    speed = speed_predicting(img)
    speed = np.argmax(speed)
    if speed == 0:
        ser.write(b'e')
        ser.write(b'E')
        print('stop')
    else:
        steer = steer_predicting(img)
        steer = np.argmax(steer)
        steer = steer_list[steer]
        ser.write(steer.encode())
        if steer == 'i' or steer == 'j' or steer == 'a' or steer == 'b':
            sleep(0.3)
        print(steer)
        ser.write(b'F')
        print('drive')
    