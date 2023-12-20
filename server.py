
from socket import socket
from threading import Lock , Thread
import time
class ChatServer:
    
    def __init__(self, port):
        self.port = port 
        self.lock  = Lock() 
        self.clients = {}
        
    def handle_client(self , client_socket):
        user = "unknown"
        print("client handle start")
        while True:
            
            data  = client_socket.recv(4096).decode()
            print("data",data)
            command , param  = data.split(",")
            
            #register the client
            if command =="register":
                
                print(f"\n{param} registered...\n")
                with self.lock:
                    self.clients[param] = client_socket

                user = param  
                client_socket.send("regd".encode())              
            #list the clients
            if  command =="list": 
                with self.lock:
                    names  = self.clients.keys()
            
                names = ",".join(names)
                client_socket.send(names.encode())
            
            #send the chat
            if command  == "chat" :
                
                to_socket = None
                with self.lock:
                    if param in self.clients:
                        to_socket = self.clients[param]
                
                if to_socket is not None:
                    to_socket.send(f"{user} says hii...\n".encode())
                else:
                    
                    print(f"\n No user by the name {param} ,{command},{param}")                        
                
                
        
    def run_server(self):
        
        socket_conn =  socket()
        socket_conn.bind(('localhost',self.port))
        #when server is busy , the incoming client req placed in queueu
        #the backlog parameter in the listen indicate the  max size of this queue
        socket_conn.listen(5)
        
        while(True):
            print ("run- server while")
            # spawn a thread to deal with a new client and immediately go back to
            # listening for new incoming connections
            client_socket , addr , =  socket_conn.accept()
            Thread(target =self.handle_client ,args = (client_socket,), daemon= True).start()
           
            
            
                
            

server   = ChatServer(8082)
server.run_server()
