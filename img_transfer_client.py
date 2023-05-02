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
        
def recv_data(cli):
    data = cli.recv(16)
    v = data[0:8]
    d = data[8:16]
    v = unpack('d', v)[0]
    d = unpack('d', d)[0]
    return v, d

def action(v, d):
    #print(v, d)
    pass

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