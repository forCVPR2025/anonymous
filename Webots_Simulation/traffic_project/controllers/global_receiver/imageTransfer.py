import socket
import os
import cv2
import numpy as np

class SocketImagePort:
    def __init__(self,ip,id):
        command = 'ifconfig enp108s0 192.168.1.1 netmask 255.255.255.0'
        sudo_password = '1210'
        sudo_command = f'echo {sudo_password} | sudo -S {command}'
        os.system(sudo_command)
        self.udp_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.sendAddress = (ip,id)
        self.image_size = [240,320,3]
        
    def image_transfer(self, filepath):
        if os.path.exists(filepath):
            frame = cv2.imread(filepath)
            if frame is None:
                frame = np.zeros(shape=self.image_size)
        else:
            frame = np.zeros(shape=self.image_size)
        img_encode = cv2.imencode('.jpeg', frame)[1]
        data_encode = np.array(img_encode)
        data = data_encode.tobytes()
        # 发送数据:
        self.udp_socket.sendto(data, self.sendAddress)
        # cv2.imshow("11",frame)
        # cv2.waitKey(0)