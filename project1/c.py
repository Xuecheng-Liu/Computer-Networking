import select, socket, sys, Queue
# Echo client program
import socket
import time
count = 0
HOST = 'localhost'    # The remote host
PORT = 5113              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
inputs = [s, sys.stdin]
inputs = [s, sys.stdin]
newData = 0
while inputs:
    readable, writable, exceptional = select.select(inputs, inputs, inputs)
    for socket in readable:
        if socket is s:
            #print "receive message from the server "
            data = s.recv(1024)
            print 'Received', repr(data)
        elif socket is sys.stdin:
            msgToSend = raw_input()
            s.sendall(msgToSend)
s.close()
