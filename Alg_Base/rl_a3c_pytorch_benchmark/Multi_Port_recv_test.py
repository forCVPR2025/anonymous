from socket import *
import queue
import threading
from multiprocessing import Process
import logging 

def setup_logger(logger_name, log_file, level=logging.INFO):
    l = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(asctime)s : %(message)s')
    fileHandler = logging.FileHandler(log_file, mode='a')
    fileHandler.setFormatter(formatter)

    l.setLevel(level)
    l.addHandler(fileHandler)

BASE_PORT = 6000

def test_effective():
    udp_list = []
    base_port = 6000
    for i in range(1700):
        now_port = base_port+i
        udp_socket = socket(AF_INET,SOCK_DGRAM)
        udp_socket.bind(("",now_port))
        udp_list.append(udp_socket)

    for i in range(1700):
        print(base_port+i,udp_list[i].recvfrom(1024)[0])

class MultiProcessRecv():
    def __init__(self,_init_list,data_size = 4) -> None:
        self.data_size = data_size
        self.is_rec = False # Whether Receive Data
        self.is_step = False # Whether Trigger a step
        self.is_reset = False # Whether Trigger a reset
        self.Number_process = self.get_NumProcess()
        self.s = [b'']*self.Number_process
        self.data = [_init_list]*self.Number_process
        self.slist = [['']]*self.Number_process
        self.ProcessSocket_list = []
        self.queuelist = []
        self.Action_list = []
        self.Create_Process()
        self.Receive_queue()
        setup_logger("test_sr","./logs/send_recv_test.log")
        self.logger_testsr = logging.getLogger("test_sr")

    """
        get_NumProcess(port = 7787): Receive Number of Process set by client
        Input:
            Port: The port used to receive Number Process
        Output:
            Number_process: Number of Process
    """
    def get_NumProcess(self,Processport=7787):
        udp_socket = socket(AF_INET,SOCK_DGRAM)
        udp_socket.bind(('',Processport))
        Numprocess_bytes = udp_socket.recvfrom(256)[0]
        Number_process = int(Numprocess_bytes)
        return Number_process

    """
        Create_Process: Allocate Port for Multi-Process
        Input:
            self.Number_process: Number of Process User want to use(Receive from get_NumProcess())
        Output:
            self.ProcessSocket_list: 2D List(Shape:[NumProcess,5]) contains 5 socket for corresponding port and for all Process
                Socket 1: Webots Send Image to Client
                Socket 2: Webots Send State Machine Flag to Client
                Socket 3: Webots Send Env State , reward and done to Client
                Socket 4: Client Send Control to Webots(Action or Reset)
                Socket 5: Client Send Action to Webots
    """
    def Create_Process(self):
        for i in range(self.Number_process):
            Curr_Process = []
            for port in range(5):
                now_port = BASE_PORT + i*5 + port
                udp_socket = socket(AF_INET,SOCK_DGRAM)
                udp_socket.bind(('',now_port))
                Curr_Process.append(udp_socket)
            self.ProcessSocket_list.append(Curr_Process)

    """
        Receive_queue(self,NumProcess): Init the queue list for multi-process
        Input:
            self.Number_process: Number of Process get from get_NumProcess(port = 7787) Function
        Output:
            self.queuelist: A list of queue with size = NumProcess,Each queue save action from corresponding process
    """
    def Receive_queue(self):
        for i in range(self.Number_process):
            self.queuelist.append(queue.Queue(maxsize=1))

    """
        Single_action: Sigle Recv Action function for each thread
            1. Decode the Action Data
            2. Push the Action Data into queue if empty
    """
    def Single_action(self,idx):
        epoch=0
        while True:
            epoch+=1
            self.s[idx],_=self.ProcessSocket_list[idx][4].recvfrom(1024) # 一次接收
            if self.s[idx] != b'' and self.s[idx] != b'\n':
                self.slist[idx] = self.s[idx].decode('utf-8').rstrip().split(',') # 去除最后换行符,并按照逗号分割
                for i in range(self.data_size):
                    self.data[idx][i] = float(self.slist[idx][i])
                # print(epoch,BASE_PORT+5*idx+4,self.data[idx])
                if not self.queuelist[idx].full():
                    self.queuelist[idx].put(str(self.data[idx]))

    """
        Recv_action: Start all the Thread for getting Action and Pushing to the Queue
        Input: 
            None
        Output:
            self.thread_list: Include threading object for corresponding process
    """
    def Recv_action(self):
        self.thread_list = []
        for i in range(self.Number_process):
            t = threading.Thread(target = self.Single_action,args=(i,))
            # t = Process(target = self.Single_action,args=(i,))
            self.thread_list.append(t)
        for j in range(self.Number_process):
            self.thread_list[j].start()

    """
        Get_step_flag(self): Judge if all the Queue are full,if so Pop all the Actio out and send a flag to Step
        Input:
            self.queuelist: A list of queue with size = NumProcess,Each queue save action from corresponding process
        Output:
            Action_list: List of Actions of Corresponding Process
    """
    def Get_step_flag(self):
        epoch = 0
        while True:
            epoch+=1
            self.is_step = False
            while not self.is_step:
                self.Action_list = []
                get_flag = True
                for process in range(self.Number_process):
                    if not self.queuelist[process].full():
                        get_flag = False
                        break
                if get_flag:
                    for getqueue in range(self.Number_process):
                        self.Action_list.append(self.queuelist[getqueue].get())
                    self.logger_testsr.info("Epoch:  "+str(epoch)+"Action_list:  "+str(self.Action_list))
                    # print(epoch,self.Action_list)
                    self.is_step = True # To-do: Reset the self.is_step flag to False After Stepping

    def main(self):
        t1 = threading.Thread(target=self.Get_step_flag)
        # t1 = Process(target=self.Get_step_flag)
        t1.start()
        self.Recv_action()

if __name__ == "__main__":
    MPR = MultiProcessRecv(_init_list = [0]*4)
    MPR.main()
