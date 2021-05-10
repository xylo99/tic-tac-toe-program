from threading import Thread
import socket
import select
from game.tttg import TTTGame


class ServerUtils(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.client = None
        self.address = None

    def setup(self, __client, __address):
        self.client = __client
        self.address = __address

    def run(self):
        # instantiate game and send to client
        game = TTTGame()
        data = self.client.recv(1024)
        menu = game.print_menu(data)
        game.ai_move()
        board = game.print_board()
        move_number = 0
        self.client.sendall(menu)
        self.client.sendall(board.encode())
        # Play game with client, and wait for a new connection if no data is received.
        while True:
            data = self.client.recv(1024)
            if data:
                data = data.decode().lower()
                correct_move = game.is_valid_move(data)
                if correct_move:
                    # parse the user data
                    row = ord(data[0]) - ord('a')
                    col = int(data[1]) - 1
                    game.make_move(row, col, 1)
                    game.ai_move()
                    board = game.print_board()
                    a_row = game.get_ai_row()
                    a_col = game.get_ai_col()
                    # Check if the game is over
                    msg = ""
                    if game.check_for_win(row, col, 1):
                        board = game.print_board()
                        msg = f'{board}\nGAMEOVER: You Won!'
                    elif game.check_for_win(a_row, a_col, 2):
                        board = game.print_board()
                        msg = f'{board}\nGAMEOVER: You Lost!'
                    elif game.is_draw(move_number):
                        board = game.print_board()
                        msg = f'{board}\nGAMEOVER: Draw!'
                    if msg:
                        self.client.send(msg.encode())
                        print(f'removing client: {self.address}')
                        break
                    self.client.sendall(board.encode())
                    move_number += 2
                else:
                    self.client.sendall(b"invalid move. please try again.")
            else:
                break


class Server(object):
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(('127.0.0.1', 13037))

    def run(self):
        self.server.listen(5)
        print('listening for new connections....')
        inputs = [self.server]

        while True:
            try:
                in_sock, _, _ = select.select(inputs, [], [])
                for s in in_sock:
                    if s == self.server:
                        sock, address = self.server.accept()
                        print(f'new connection from: {address}')
                        client = ServerUtils()
                        client.setup(sock, address)
                        client.start()
                    else:
                        continue
            except KeyboardInterrupt:
                print("Keyboard interrupt detected, connection will close after threads are ended.")
                break
        print("initiate connection close...")
        self.server.close()


if __name__ == '__main__':
    server = Server()
    server.run()
