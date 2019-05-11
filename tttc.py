# Tic Tac Toe over TCP
# v0.1
# Ted
# email: thandy1@umbc.edu
# Originally made in: 2018-10
# Updated: 2019-04, 2019-05,
# This script implements a TCP client to communicate with a TCP server to play the game
# of tic tac toe.

import socket
import sys

IP   = ''
port = 13037
s    = None
client_start = 'FALSE'

#connect if ther are no socket errors
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    if len(sys.argv) == 3:
       IP = sys.argv[2]
    else:
       client_start = sys.argv[1]
       IP = sys.argv[3]
    s.connect((IP, port))
    #we indicate whether or not the client starts to the server
    s.send(client_start)
    data = s.recv(1024)
    print data
except socket.error, (value, message):
    if s:
        s.close()
    print "Could not open socket: " + message
    sys.exit(1)
#send and recieve gamedata until we recieve indication to end the connection
while True:
    data = s.recv(1024)
    if data:
       if data[:1] == 'e':
          print data[1:]
          break
       else:
          print data
    data = raw_input('> ')
    s.sendall(data)
s.close()
