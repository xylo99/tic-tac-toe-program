import socket
import sys


class Client:
    def __init__(self, ip, client_start):
        self.client_start = b"-c" if client_start else b'FALSE'
        self.IP = ip if ip else '127.0.0.1'
        self.port = 13037

    def run_client(self):
        # connect if there are no socket errors
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.IP, self.port))
            # we indicate whether or not the client starts to the server
            s.send(self.client_start)
            data = s.recv(1024)
            print(data.decode())
        except socket.error as e:
            s.close()
            print(f"Could not open socket, reason:\n {e}")
            sys.exit(1)

        while True:
            data = s.recv(1024).decode()
            if data:
                if data == 'e':
                    print(data)
                    break
                else:
                    print(data)
            data = input('> ')
            s.sendall(data.encode())
        s.close()
