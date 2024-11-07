#coding=utf-8
import pty
import os
import select
import sys
import time
import threading
import serial

class SerialPort:
    def __init__(self, _data_size, _init_list):
        self.master, self.slavename = self.mkpty()
        
        self.ser=serial.Serial(self.slavename,115200,timeout=0.5)
        
        self.ser.close()
        self.ser.open()
        print(self.ser.isOpen())
        
        # 单独打开一个服务器进行数据转发
        self.server = threading.Thread(target=self.server_loop,args=())
        self.server.start()
        
        self.data_size = int(_data_size)
        
        ### Set Serial Port#################（这里设置为一个client，必须在server成功创建之后才能够成功创建，否则报错）
        self.s = b''
        self.slist = []
        self.data = _init_list
        self.sdata = ["0"] * self.data_size

        #### New Thread Start  #####################
        self.serial_loop = threading.Thread(target=self._serial_update)
        self.serial_loop.start()
    
    def mkpty(self):
        master, slave = pty.openpty()
        slaveName = os.ttyname(slave)
        print('\nslave device names: ', slaveName)
        return master, slaveName
    
    def server_loop(self):
        while True:
            rl, wl, el = select.select([self.master], [], [], 1)
            for self.master in rl:
                data = os.read(self.master, 128)
                os.write(self.master, data)
        
    # 更新串口数据线程(不加while循环不会自循环)
    def _serial_update(self):
        while True:
            self.s = self.ser.readline() #是读一行，以\n结束，要是没有\n就一直读，阻塞。
            if self.s != b'':
                self.slist = self.s.decode('utf-8').rstrip().split(',') # 去除最后换行符,并按照逗号分割
                # 从串口中获取通道数和数据
                if self.slist[0] != '' and self.slist[1] != '':
                    for i in range(self.data_size):
                        self.data[i] = float(self.slist[i])
                        self.sdata[i] = self.slist[i]
                        
    def read(self):
        return self.data, self.sdata
    