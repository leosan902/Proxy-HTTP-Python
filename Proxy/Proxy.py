import socket,random
import sys,time

import threading  
mutex = threading.Lock()  
# Create a server socket, bind it to a port and start listening
portaDoServer = 8888

bufferSize = 600
serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Prepare a server socket
serverSock.bind(('', portaDoServer))
serverSock.listen(1000)

def pegarSite(filetouse,hostn,clientSock):
    
    
   
    x= random.randint(1,100)
    print('\nThread '+str(x)+' Created\n'  )
    Host = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Host.connect((hostn, 80))
    
    fullData=b''
    print(filetouse)
    Host.sendall(filetouse)
   
    while 1:
        # receive data from web server
        data = Host.recv(4026)

        if (len(data) > 0):
            fullData+=data
        else:
            break
                  
    clientSock.send(fullData)
    if filetouse.find(b'Connection: close')!= -1:
        clientSock.close()
        Host.close()
    
    print('\nThread '+str(x)+' Terminated \n' )
    
    
    

while True:
    # Start receiving data from the client
    
    print ('Ready to serve...')
    clientSock, enderecoClient = serverSock.accept()
    print ('Received a connection from: ', enderecoClient)
    message = clientSock.recv(bufferSize)
   

    if message!= b'' :
        start = message.find(b'Host: ') 
        end = message.find(b'\r', start+6)
        hostn=message[start+6:end]
        fileExist = b"false"
        start = message.find(b' ') 
        end = message.find(b' ', start+1)
        filetouse=message[start+1:end]
        if (filetouse==(b"http://wallacefund.info/")):
           print("Site Banido")
           clientSock.sendall(b"HTTP/1.1 403 Forbidden\r\nConnection: close\r\nContent-Type: text/html\r\n\r\n<!DOCTYPE html>\r\n<html>\r\n\t<head>\r\n\t\t<title>403 - Forbidden</title>\r\n\t</head>\r\n\t<body>\r\n\t\t<h1>Site "+hostn+b" Banido</1>\r\n\t</body>\r\n</html>")
           message= b''
           clientSock.close()
        if ( message.find(b'wallacefund')!= -1):
           print("Site Banido")
           clientSock.sendall(b"HTTP/1.1 403 Forbidden\r\nConnection: close\r\nContent-Type: text/html\r\n\r\n<!DOCTYPE html>\r\n<html>\r\n\t<head>\r\n\t\t<title>403 - Forbidden</title>\r\n\t</head>\r\n\t<body>\r\n\t\t<h1>palavra "+b"wallacefund"+b" Banido</1>\r\n\t</body>\r\n</html>")
           message= b''
           clientSock.close()

    # Extract the filename from the gien message
    if message!= b'':
               
               
        
        try:
             #Check whether the file exists in the cache
            f = open(hostn.replace(b"www.", b"", 1), "rb")
            outputdata = f.readlines()
            fileExist = b"true"
            print ('File Exists!')
            resp = b""
            
            for s in outputdata:
                resp += s
            if(resp.find(b'domain=.')!= -1):
                 start = resp.find(b'domain=.') 
                 end = resp.find(b'\r', start)
                 originalHost=resp[start+8:end]
            # Send the content of the requested file to the client
            
            clientSock.sendall(resp)
            print ('Read from cache')

            # Error handling for file not found in cache
        except IOError:
           
            if fileExist == b"false":
                # Create a socket on the proxyserver
               
                
                t = threading.Thread(target = pegarSite,args= (message,hostn,clientSock)).start()
                  
              
                #messageSite = c.recv(bufferSize)
                    
                #try:
                #    tmpFile = open(b"./" + hostn, 'ab+')
                #    tmpFile.write(full_msg)
                
                
                #    tmpFile.close()
                #except :
                #    pass
                
                    

            else:
                # HTTP response message for file not found
                # Do stuff here
                print ('File Not Found...Stupid Andy')
                a = 2
        # Close the socket and the server sockets
        

# Do stuff here