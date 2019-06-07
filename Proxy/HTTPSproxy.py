import socket,random
import sys,time
import ssl 
import threading  
mutex = threading.Lock()  
# Create a server socket, bind it to a port and start listening
portaDoServer = 8855

bufferSize = 2046
serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Prepare a server socket
serverSock.bind(('', portaDoServer))
serverSock.listen(1000)
socket.setdefaulttimeout(1)

def conecaoClient(clientSock,enderecoClient):
     while True:
         message=b''
         oldmessage=b''
         data=b''
         while 1:
            # receive data from web server
           try:
                data = clientSock.recv(bufferSize)
                message+=data
                if(message==oldmessage and message!=b''):   
                    break
                oldmessage=message
           except :
               break
         
               
         if (message.find(b'Connect')!= -1) :
             clientSock.sendall(b'200 OK\r\n\r\n')
             start = message.find(b'Host: ') 
             end = message.find(b'\r', start+6)
             hostn=message[start+6:end]
             hostn = hostn.replace(b':443', b'')
             try:
                 sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
                 sock.connect((hostn, 443))
             except :
                 pass
             message=b''

         # Extract the filename from the gien message
         if message!= b'':
            
            fullData=b''
        
            try:
                sock.send(message)
            except :
                pass
            oldfullData=b''
            data=b''
            while 1:
                # receive data from web server
              try:
                    data = sock.recv(bufferSize)
                    fullData+=data
                    
                    if(fullData.endswith(b'\n') or (fullData==oldfullData and fullData!=b'')):   
                      break
                    oldfullData=fullData
              except :
                     break
                 
               
            clientSock.sendall(fullData)
            
            if (fullData==b''):
                 clientSock.close()
                 sock.close()
                 break
            print("Client :\n")
            print(message)  
            print("Server :\n")
            print(fullData)

while True:
    # Start receiving data from the client
    
    print ('Ready to serve...')
    clientSock, enderecoClient = serverSock.accept()
    print ('Received a connection from: ', enderecoClient)
    t = threading.Thread(target = conecaoClient,args=(clientSock,enderecoClient)).start()