#! /bin/python3
from socket import *

# default params
serverAddr = ('', 50001)

import sys
def usage():
    print("usage: %s [--serverPort <port>]"  % sys.argv[0])
    sys.exit(1)

try:
    args = sys.argv[1:]
    while args:
        sw = args[0]; del args[0]
        if sw == "--serverPort":
            serverAddr = ("", int(args[0])); del args[0]
        else:
            print("unexpected parameter %s" % args[0])
            usage()
except:
    usage()

print("binding datagram socket to %s" % repr(serverAddr))

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(serverAddr)
ACK = 'ACK'
print("ready to receive")

while 1:
    option, clientAddrPort = serverSocket.recvfrom(2048)
    print("from %s: rec'd '%s'" % (repr(clientAddrPort), option))
    serverSocket.sendto('option recieved'.encode(), clientAddrPort)

    file, clientAddrPort = serverSocket.recvfrom(2048)
    serverSocket.sendto('File name recieved'.encode(), clientAddrPort)
    f = open(file.decode(), 'w')
    line, clientAddrPort = serverSocket.recvfrom(2048)
    try: 
        while line: 
            line = line.decode()
            print('writing...')
            f.write(line)
            serverSocket.settimeout(2)
            serverSocket.sendto(ACK.encode(), clientAddrPort)
            line, clientAddrPort = serverSocket.recvfrom(2048)
    except timeout: 
        f.close()
        print('File downloaded')
