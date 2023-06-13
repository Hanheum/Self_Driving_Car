from serial import Serial
import numpy as np
from picamera2 import Picamera2
from time import time
from threading import Thread
from time import sleep

start_num = int(input('start num:'))

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

steer = ''
speed = ''
record = ''
power = ''

def capture():
    img = cam.capture_array()
    img = np.sum(img, axis=-1)
    img = img/3
    img = np.round(img)
    img = img.astype(np.uint64)
    img = img.tobytes()
    return img

'''while True:
    if record == '1':
        print('capturing')
        img = capture()
        file = open('/home/hanheum/Desktop/img_save/{}'.format(start_num), 'wb')
        file.write(img)
        file.close()
        steerspeed = str(start_num)+':'+steer+speed
        file2 = open('/home/hanheum/Desktop/speed_steer.txt', 'a')
        file2.write(steerspeed)
        file2.close()
        start_num += 1
        
    ser_read = ser.read()
    ser_read = ser_read.decode()
    if ser_read != data:
        data = ser_read
        if data in steer_list:
            steer = data
        elif data in speed_list:
            speed = data
        elif data in record_list:
            record = data
        elif data in power_list:
            power = data'''
    
def recording():
    global record, steer, speed, start_num
    while True:
        if record == '1':
            print('capturing')
            img = capture()
            file = open('/home/hanheum/Desktop/img_save/{}'.format(start_num), 'wb')
            file.write(img)
            file.close()
            steerspeed = str(start_num)+':'+steer+speed+'\n'
            file2 = open('/home/hanheum/Desktop/speed_steer.txt', 'a')
            file2.write(steerspeed)
            file2.close()
            start_num += 1
            sleep(0.15)
            
def listening():
    global data, steer, speed, record, power
    while True:
        ser_read = ser.read()
        ser_read = ser_read.decode()
        if ser_read != data:
            data = ser_read
            if data in steer_list:
                steer = data
            elif data in speed_list:
                speed = data
            elif data in record_list:
                record = data
            elif data in power_list:
                power = data

thread_record = Thread(target=recording)
thread_listen = Thread(target=listening)

thread_record.start()
thread_listen.start()