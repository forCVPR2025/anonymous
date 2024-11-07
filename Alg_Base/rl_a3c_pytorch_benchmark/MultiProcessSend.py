from socket import *
from random import randint
import time
import threading
class SendActionSocket():
    def __init__(self,ip='192.168.1.1',port_action=7788,port_control = 7784,port_process = 7787):
        self.ip = ip
        self.udp_sendactionsocket = socket(AF_INET,SOCK_DGRAM)
        self.udp_sendconsocket = socket(AF_INET,SOCK_DGRAM)
        self.Target_addr_action = (ip,port_action)
        self.Target_addr_control = (ip,port_control)
        self.Target_addr_process = (ip,port_process)
    # 输入为编码好的Bytes
    def send_signal(self,sendData,action=False,process = False,port = None):
        if process:
            self.udp_sendactionsocket.sendto(sendData,self.Target_addr_process)
        else:
            if action:
                if port is None:
                    self.udp_sendactionsocket.sendto(sendData,self.Target_addr_action)
                else:
                    self.udp_sendactionsocket.sendto(sendData,(self.ip,port))
            else:
                self.udp_sendconsocket.sendto(sendData,self.Target_addr_control)

    """
        send_action: send an action to the env server through socket,it can be devided into 2 parts
            1. send a control signal to inform the env server
            2. send action data to the env server
        Input:
            action: action chosen by Agent
        Output:
            Void
    """
    def send_action(self,action,port=None):
        signal = ""
        for i in range(len(action)):
            signal += str(action[i])
            if i != len(action)-1:
                signal += "," 
        signal += "\n"
        signal_bytes = bytes(signal,'utf-8')
        self.send_signal(signal_bytes,action=True,port=port)


BASE_PORT = 6000

def test_multi_send():
    send_con = bytes("1",'utf-8')
    udp_socket = socket(AF_INET,SOCK_DGRAM)
    for i in range(1700):
        now_port = BASE_PORT+i
        udp_socket.sendto(send_con,("127.0.0.1",now_port))

class MultiProcessSend():
    def __init__(self,NumProcess) -> None:
        self.Number_process = NumProcess
        self.send_socket=SendActionSocket(ip = "127.0.0.1")
        self.send_socket.send_signal(bytes(str(self.Number_process)+"\n",'utf-8'),process=True) # Inform Env of Num worker
        self.ProcessPort_list = []
        self.action_list = []
        self.Create_Process()
        

    """
        Create_Process: Allocate Port for Multi-Process
        Input:
            self.Number_process: Number of Process User want to use(Receive from get_NumProcess())
        Output:
            self.ProcessPort_list: 2D List(Shape:[NumProcess,5]) contains 5 socket for corresponding port and for all Process
                Socket 1: Webots Send Image to Client
                Socket 2: Webots Send State Machine Flag to Client
                Socket 3: Webots Send Env State , reward and done to Client
                Socket 4: Client Send Control to Webots(Action or Reset)
                Socket 5: Client Send Action to Webots
    """
    def Create_Process(self):
        for i in range(self.Number_process):
            Curr_Port = []
            for port in range(5):
                now_port = BASE_PORT + i*5 + port
                Curr_Port.append(now_port)
            self.ProcessPort_list.append(Curr_Port)
            self.action_list.append([])

    def send_actionlist(self,idx):
        epoch = 0
        while True:
            epoch += 1
            print(epoch,self.ProcessPort_list[idx][4],self.action_list[idx])
            self.send_socket.send_action(self.action_list[idx],port=self.ProcessPort_list[idx][4])
            time.sleep(0.5)
    
    def main(self):
        for i in range(self.Number_process):
            t = threading.Thread(target=self.send_actionlist,args = (i,))
            t.start()
        t3 = threading.Thread(target=self.set_actionlist)
        t3.start()
    
    def set_actionlist(self):
        while True:
            action_list = []
            for i in range(NumProcess):
                action_list.append([randint(1,10),randint(1,10),randint(1,10),randint(1,10)])
            self.action_list = action_list
            # time.sleep(5)
            # print("set_action_list:",self.action_list)

if __name__ == "__main__":
    NumProcess = 16
    action_list = []
    Mps = MultiProcessSend(NumProcess=NumProcess)
    Mps.main()