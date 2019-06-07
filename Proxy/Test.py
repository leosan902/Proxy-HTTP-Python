import ssl
import OpenSSL
import socket

def verify_cb(conn, cert, errun, depth, ok):
        return True

server = 'youtube.com'
port = 443
PROXY_ADDR = ("<proxy_server>", 3128)
CONNECT = "GET / HTTP/1.1\r\nHost: www.youtube.com:443\r\nConnection: close\r\n\r\n" 
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_sock = context.wrap_socket(sock, server_hostname="youtube")
s_sock.connect((server, port))


s_sock.send(str.encode(CONNECT))
fulltest=b''
while True:
   Test=s_sock.recv(4096)
   fulltest+=Test
   if(fulltest.endswith(b'\n\n\r\n0\r\n\r\n') or Test ==b''):
        break
     
print(fulltest)    
s_sock.close()