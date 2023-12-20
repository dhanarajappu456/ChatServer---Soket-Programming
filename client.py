from http import server
import socket
from threading import Thread 
import time
import random 
class User:
    
    def __init__(self,name, server_host,server_port):
        
        self.name  = name 
        self.server_host  =server_host 
        self.server_port = server_port
        
    
    def receive_msg(self, server_socket):
        
        while(True):
            print(f"received :{server_socket.recv(4096).decode()} "  )
        
    def run_client(self):
        
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((self.server_host, self.server_port))
        
        #register and receive ack
        server_socket.send(f"register,{self.name}".encode())
        print(server_socket.recv(4096).decode())
        
        time.sleep(3)
        
    
        
        #get list of frnds
        server_socket.send("list,friends".encode())
        list_frnds = server_socket.recv(4096).decode().split(",")
        print("frnds",list_frnds)
        num_friends = len(list_frnds)
        #start listening to msg
        Thread(target=self.receive_msg, args = (server_socket,), daemon= True).start()
        
        #send msg
        
        while True:
            friend = list_frnds[random.randint(0,num_friends-1)]
            server_socket.send(f"chat,{friend}".encode())
            time.sleep(random.randint(2,6))
            

a= User("amal",'localhost',8082)
t= User("tony", 'localhost',8082)
b =User("binod",'localhost',8082)

Thread(target=a.run_client).start()
Thread(target =t.run_client).start()
Thread(target = b.run_client).start()
