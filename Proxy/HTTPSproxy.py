import socket,random
import sys,time
import ssl 
import threading  
import datetime 
# Create a server socket, bind it to a port and start listening
portaDoServer = 8855
bufferSize = 7000
serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Prepare a server socket
serverSock.bind(('', portaDoServer))
serverSock.listen(1000)
socket.setdefaulttimeout(0.4)
ip=[]
hour1=[]
min1=[]
hour2=[]
min2=[]
 
# Get list of all lines in file

with open("data.txt", 'r') as fh:
    linha=0
    for line in fh:
        line = line.rstrip("\n")
        line = line.rstrip("\t")
        if(linha==0):
            ip.append(line)
            linha=1
        elif(linha==1):
            hour1.append(line)
            linha=2
        elif(linha==2):
            min1.append(line)
            linha=3
        elif(linha==3):
            hour2.append(line)
            linha=4
        elif(linha==4):
            min2.append(line)
            linha=0

def ipTest(enderecoClient):
 
    ipNum=str(enderecoClient[:1])
    ipNum=ipNum.replace(',', '',2)
    ipNum=ipNum.replace("'", '',2)
    ipNum=ipNum.replace('(', '',2)
    ipNum=ipNum.replace(')', '',2)
    if ipNum in ip:
        index = ip.index(ipNum)
        tm= datetime.datetime.now()
        now_time = tm.time()
        start = datetime.time(int(hour1[index]), int(min1[index]))
        end = datetime.time(int(hour2[index]),int(min2[index]))         
        if hour2[index] >= hour1[index]:
            if start <= now_time <= end:
                 return True             
            else:
                 return False              
        else:
            if start >= now_time >= end:
                 return True                
            else:
                 return False
                 
 
    
    
    
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
         
               
         if (message.find(b'Connect')!= -1 ) :
             start = message.find(b'Host: ') 
             end = message.find(b'\r', start+6)
             hostn=message[start+6:end]
             hostn = hostn.replace(b':443', b'')
             with open('Nomes.txt') as f:
                 lines = f.readlines()
             for text in lines:
                 if text in hostn.decode("utf-8"):
                    clientSock.sendall(b"HTTP/1.1 403 Forbidden\r\nConnection: close\r\nContent-Type: text/html\r\n\r\n<!DOCTYPE html>\r\n<html>\r\n\t<head>\r\n\t\t<title>403 - Forbidden</title>\r\n\t</head>\r\n\t<body>\r\n\t\t<h1>Site Banido</1>\r\n\t</body>\r\n</html>")
                    return 0
             
             clientSock.sendall(b'200 OK\r\n\r\n')
             
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
     

while True:
    # Start receiving data from the client
    

    clientSock, enderecoClient = serverSock.accept()

    if(ipTest(enderecoClient)):
      clientSock.sendall(b"HTTP/1.1 403 Forbidden\r\nConnection: close\r\nContent-Type: text/html\r\n\r\n<!DOCTYPE html>\r\n<html>\r\n\t<head>\r\n\t\t<title>403 - Forbidden</title>\r\n\t</head>\r\n\t<body>\r\n\t\t<h1>Site Banido</1>\r\n\t</body>\r\n</html>")
    else:
        t = threading.Thread(target = conecaoClient,args=(clientSock,enderecoClient)).start()

    