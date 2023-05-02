import tensorflow as tf
import numpy as np
from socket import *
from struct import pack

HOST = ''
PORT = 3653

img_size = 32768

model = tf.keras.models.load_model('./model')

server_sock = socket(AF_INET, SOCK_STREAM)
server_sock.bind((HOST, PORT))
server_sock.listen()

class client_:
    def __init__(self, cli):
        self.cli = cli

    def recv_img(self):
        recved = b''
        recved_len = 0
        while recved_len<img_size:
            data = self.cli.recv(1024)
            recved += data
            recved_len += len(data)
        recved = np.frombuffer(recved, dtype=np.uint64)
        recved = np.reshape(recved, (1, 64, 64, 1))
        recved = recved.astype(np.float32)/255.
        return recved

    def send_result(self, v, d):
        v = pack('d', v)
        d = pack('d', d)
        data = v+d
        self.cli.send(data)

def try_connecting():
    cli, addr = server_sock.accept()
    print('connected by {}'.format(addr))
    return cli

cli = try_connecting()
client = client_(cli)

while True:
    try:
        img = client.recv_img()
        result = model.predict(img)[0]
        client.send_result(*result)
        print('sent result')
    except Exception as e:
        print(e)
        cli = try_connecting()
        client.cli = cli