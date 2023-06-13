from serial import Serial
import numpy as np
from picamera2 import Picamera2
from socket import *
from struct import unpack
from time import time

cam = Picamera2()
cam_config = cam.create_still_configuration(main={"size":(64, 64)})
cam.configure(cam_config)
cam.start()

HOST = '168.126.168.191'
PORT = 3653

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

def try_connecting():
    trials = 0
    cli_sock = socket(AF_INET, SOCK_STREAM)
    while True:
        try:
            cli_sock.connect((HOST, PORT))
            break
        except:
            trials += 1
            print('connection trials:{}'.format(trials))
    return cli_sock

def capture():
    img = cam.capture_array()
    img = np.sum(img, axis=-1)
    img = img/3
    img = np.round(img)
    img = img.astype(np.uint64)
    img = img.tobytes()
    return img

def send_img(cli, img):
    for i in range(32):
        cli.send(img[i*1024:(i+1)*1024])

cli_sock = try_connecting()
while True:
    ser_read = ser.read()
    ser_read = ser_read.decode()
    if ser_read != data:
        data = ser_read
        print(data)
        if data in steer_list:
            steer = data
        elif data in speed_list:
            speed = data
        elif data in record_list:
            record = data
        elif data in power_list:
            power = data
    
    if record == '1':
        img = capture()
        send_img(cli_sock, img)
        steerspeed = steer+speed
        cli_sock.send(steerspeed.encode())
        
    