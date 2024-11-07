import socket
import os

class SocketPort():
    def __init__(self, ip, id):
        command = 'ifconfig enp108s0 192.168.1.1 netmask 255.255.255.0'
        sudo_password = '1210'
        sudo_command = f'echo {sudo_password} | sudo -S {command}'
        os.system(sudo_command)
        self.udp_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.sendAddress = (ip,id)
        
    def send(self, state):
        b = bytes(str(state)[1:-1] + "\n", 'utf-8')
        self.udp_socket.sendto(b,self.sendAddress)
        
    def sendStr(self, stateStr):
        b = bytes(stateStr, 'utf-8')
        self.udp_socket.sendto(b,self.sendAddress)

