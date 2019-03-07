#! /bin/python3
from socket import *

# default params
serverAddr = ('localhost', 50000)       

import sys, re                          

def usage():
    print("usage: %s [--serverAddr host:port]"  % sys.argv[0])
    sys.exit(1)

try:
    args = sys.argv[1:]
    while args:
        sw = args[0]; del args[0]
        if sw == "--serverAddr":
            addr, port = re.split(":", args[0]); del args[0]
            serverAddr = (addr, int(port))
        else:
            print("unexpected parameter %s" % args[0])
            usage()
except:
    usage()

clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(0.5)
option = input('put or get?')

clientSocket.sendto(option.encode(), serverAddr)

#confirm
msg, address = clientSocket.recvfrom(2048)
print("from %s: rec'd '%s'" % (repr(serverAddr), msg))

file = input('File name?\n')
f = open(file, 'r')

#send file name
clientSocket.sendto(file.encode(), serverAddr)

#confirm
msg, address = clientSocket.recvfrom(2048)
print("from %s: rec'd '%s'" % (repr(serverAddr), msg))

#send by 100's need if else for put and get options 
while True:
    acknowledged = False
    print(acknowledged)
    line = f.read(100)
    line = line.strip()
    line = line.encode()
    if not line:
        break
    clientSocket.sendto(line, serverAddr)
    #spam
    while not acknowledged:
        try:
            ACK, address = clientSocket.recvfrom(2048)
            if ACK.decode() == 'ACK':
                acknowledged = True
                print(acknowledged)
        except timeout:
            tries = 0
            print('session timed out...\n')
            print('resending...')
            clientSocket.sendto(line, serverAddr)
            tries += 1
            if tries == 6: 
                exit()

print(ACK)