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
   
    message = str(clientSock.recv(bufferSize).decode())
    print(message)
    # Extract the filename from the given message
    if message!= '':
        
        message.split(' ')[1]
        filename = message.split()[1].partition("/")[2]
        print (filename)
        fileExist = "false"
        filetouse = "/" + filename
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
            if fileExist == "false":
                # Create a socket on the proxyserver
                print ('Creating socket on proxyserver')
                c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                hostn = filename.replace("www.", "", 1)
                print ('Host Name: ', hostn)
                try:
                    # Connect to the socket to port 80
                    c.connect((hostn, 80))
                    print ('Socket connected to port 80 of the host\n')
                    
                    filename= filename.encode('utf-8')
                    print(b'GET / HTTP/1.1\r\nHost: '+filename+b'\r\nConnection: keep-alive\r\n\r\n')
                    c.sendall(b'GET / HTTP/1.1\r\nHost: '+filename+b'\r\nConnection: keep-alive\r\n\r\n')
                    # Create a temporary file on this socket and ask port 80
                    # for the file requested by the client 
                    #fileobj = c.makefile('r', None)
                    #fileobj.write("GET " + "http://" + filename+ " HTTP/1.1\r\n")
                   
                   
                        
                  
                    messageSite = c.recv(bufferSize)
   
                    while True:
                            messageSite += c.recv(bufferSize)
                                                          
                            if messageSite.endswith(b'\r\n0\r\n\r\n'):
                             break
                                     
                 
                    print(messageSite)
  
                    tmpFile = open(b"./" + filename, "wb")
                    tmpFile.write(messageSite)
                    clientSock.sendall(messageSite)

                except:
                    print ('Illegal request')

            else:
                # HTTP response message for file not found
                # Do stuff here
                print ('File Not Found...Stupid Andy')
                a = 2
        # Close the socket and the server sockets
        clientSock.close()

# Do stuff here