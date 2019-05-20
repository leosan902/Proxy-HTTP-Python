import socket 
import sys,time


# Create a server socket, bind it to a port and start listening
portaDoServer = 8888
maxConnections = 5
bufferSize = 4096
serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Prepare a server socket
serverSock.bind(('', portaDoServer))
serverSock.listen(maxConnections)

while True:
    # Start receiving data from the client
    print ('Ready to serve...')
    clientSock, enderecoClient = serverSock.accept()
    print ('Received a connection from: ', enderecoClient)
    message = clientSock.recv(bufferSize)
    print(message)
    # Extract the filename from the given message
    if message!= b'':
        
        message.split(b' ')[1]
        filename = message.split()[1].partition(b"/")[2]
        print (filename)
        
        if filename.startswith(b'www'):
            x=0
        else:
            x=1
        fileExist = b"false"
        filetouse = b"/" + filename
        print(filetouse)
        
        try:
             #Check whether the file exists in the cache
            f = open(filetouse[1:], "rb")
            outputdata = f.read()
            fileExist = b"true"
            print ('File Exists!')

            # ProxyServer finds a cache hit and generates a response message
            clientSock.send(b"HTTP/1.1 200 OK\r\n")
            clientSock.send(b"Content-Type:text/html\r\n")

            # Send the content of the requested file to the client
            
            clientSock.sendall(outputdata)
            print ('Read from cache')

            # Error handling for file not found in cache
        except IOError:
            print ('File Exist: ', fileExist)
            if fileExist == b"false":
                # Create a socket on the proxyserver
                print ('Creating socket on proxyserver')
                c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                c.settimeout(0.5)
                hostn = filename.replace(b"www.", b"", 1)
                print ('Host Name: ', hostn)
                full_msg=b''
                
                # Connect to the socket to port 80
                if(x==0):                       
                    c.connect((hostn, 80))
                    
                    originalHost = hostn
                    print ('Socket connected to port 80 of the host\n')
                    print(b'GET / HTTP/1.1\r\nHost: '+filename+b'\r\nConnection: keep-alive\r\n\r\n')
                    c.sendall(b'GET / HTTP/1.1\r\nHost: '+filename+b'\r\nConnection: keep-alive\r\n\r\n')
                    #messageSite = c.recv(bufferSize)
                    print(3)
                    while True:
                         try:
                            messageSite = c.recv(bufferSize)
                            print(messageSite)
                            full_msg +=messageSite
                         except socket.timeout: 
                              break
                                    

                        
                else :
                    c.connect((originalHost, 80))
                    print(b'GET '+ filetouse +b' HTTP/1.1\r\nHost: www.'+originalHost+b'\r\nConnection: keep-alive\r\n\r\n')
                    c.sendall(b'GET '+ filetouse +b' HTTP/1.1\r\nHost: www.'+originalHost+b'\r\nConnection: keep-alive\r\n\r\n')
                    
                    while True:                     
                                                        
                         try:
                            messageSite = c.recv(bufferSize)
                            print(messageSite)
                            full_msg +=messageSite
                         except socket.timeout: 
                             break
                              
                                                      
                            
                                  
                print(2)
                    
              
                print(full_msg)
                #tmpFile = open(b"./" + hostn, "ab")
                #tmpFile.write(full_msg)
                clientSock.sendall(full_msg)
                   
                
                    

            else:
                # HTTP response message for file not found
                # Do stuff here
                print ('File Not Found...Stupid Andy')
                a = 2
        # Close the socket and the server sockets
        

# Do stuff here