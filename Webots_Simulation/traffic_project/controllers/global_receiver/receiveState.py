import socket
import os
import threading

class SocketPort:
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
        self.data = [0.] * self.data_size
        self.sdata = ["0"] * self.data_size
        
        
    '''
    description: 缓存内容读取
    param {*} self
    return {*}
    '''    
    def read(self):
        self.s,_=self.udp_socket.recvfrom(self.data_size * 8) # 一次接收
        if self.s != b'':
            self.slist = self.s.decode('utf-8').strip('(').rstrip(')').split(',') # 去除前后括号,并按照逗号分割
            # 从串口中获取通道数和数据
            if self.slist[0] != '' and self.slist[1] != '':
                for i in range(self.data_size):
                    self.data[i] = float(self.slist[i])
                    self.sdata[i] = self.slist[i]
        return self.data, self.sdata