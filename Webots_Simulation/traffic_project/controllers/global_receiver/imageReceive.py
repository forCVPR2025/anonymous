# -*- coding: utf-8 -*-

# import socket
# import cv2
# import numpy as np

# import time

# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# # 绑定端口:
# s.bind(('', 7788))

# print('Bind UDP on 7788...')

# while True:
#     # 接收数据:
#     data, addr = s.recvfrom(8000000000)
#     #解码
#     nparr = np.fromstring(data, np.uint8)
#     #解码成图片numpy
#     img_decode = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
#     print(time.time())
    
    
import socket
import os
import numpy as np
import cv2

class SocketImagePort:
    def __init__(self, _data_size, id):
        command = 'ifconfig enp108s0 192.168.1.1 netmask 255.255.255.0'
        sudo_password = '1210'
        sudo_command = f'echo {sudo_password} | sudo -S {command}'
        os.system(sudo_command)
        # os.system('ifconfig enp108s0 192.168.1.1 netmask 255.255.255.0')
        
        self.udp_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.udp_socket.bind(('',id))
        
        self.data_size = int(_data_size)
        
        ### Set Socket Port#################
        self.s = b''
        self.slist = []
        self.data = [0] * self.data_size
        self.sdata = ["0"] * self.data_size
        
    # 接收一次包，第一个数据为时序信号，第二个数据为图像转numpy
    def receive(self):
        # 接收数据:
        data, _ = self.udp_socket.recvfrom(8000000000)
        if self.s != b'':
            self.slist = self.s.decode('utf-8').rstrip().split(',') # 去除最后换行符,并按照逗号分割
            # 从串口中获取通道数和数据
            if self.slist[0] != '' and self.slist[1] != '':
                for i in range(self.data_size):
                    self.data[i] = float(self.slist[i])
                    self.sdata[i] = self.slist[i]
        #解码
        nparr = np.fromstring(data[1], np.uint8)
        #解码成图片numpy
        img_decode = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        return data[0],img_decode

