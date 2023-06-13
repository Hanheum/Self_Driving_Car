import numpy as np
from picamera2 import Picamera2
from socket import *
from struct import unpack
from time import time
import serial

cam = Picamera2()
cam_config = cam.create_still_configuration(main={"size":(64, 64)})
cam.configure(cam_config)
cam.start()

HOST = '218.155.15.247'
PORT = 6474

ser = serial.Serial('/dev/ttyUSB0', 9600)

def try_connecting():
    trials = 0
    cli_sock = socket(AF_INET, SOCK_STREAM)
    while True:
        try:
            cli_sock.connect((HOST, PORT))
            print('connected')
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
    img = np.rot90(img)
    img = np.rot90(img)
    img = img.tobytes()
    return img

def send_img(cli, img):
    for i in range(32):
        cli.send(img[i*1024:(i+1)*1024])
        
def recv_data(cli):
    data = cli.recv(2)
    data = data.decode()
    v = data[0]
    d = data[1]
    print('recved')
    return v, d

def action(v, d):
    if v == '0':
        ser.write(b'e')
        ser.write(b'E')
        print('stop')
    else:
        ser.write(d.encode())
        print(d)
        ser.write(b'F')
        print('drive')

client = try_connecting()
while True:
    start = time()
    img = capture()
    try:
        send_img(client, img)
        v, d = recv_data(client)
        action(v, d)
        end = time()
        print(round(end-start, 3))
    except Exception as e:
        print(e)
        client = try_connecting()