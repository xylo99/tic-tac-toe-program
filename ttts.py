# Tic Tac Toe over TCP
# v0.1
# Ted
# email: thandy1@umbc.edu
# Originally made in: 2018-10
# Updated: 2019-04, 2019-05,
# This script implements a tic tac toe service over tcp. This server implements the game 
# to be played with a client over TCP. No matter the result of the game, the client 
# gets removed and the server starts listening for new clients.

import threading 
import socket
import select
import sys

###############BEGIN-GAME-IMPLEMENTATION#################
class TTTGame():

   def __init__(self):
        """ Constants for the game"""
        self.N           = 3
        self.CIRCLE      = 1
        self.EMPTY       = 0
        self.CROSS       = 2
        self.board = [[]]
        self.board = [[self.EMPTY for i in xrange(self.N)] for i in xrange(self.N)]
        '''row and column variables for the AI moves'''
        self.AI_row = 0
        self.AI_col = 0
	
   def clear_board(self):
	for i in xrange(self.N):
		for j in xrange(self.N):
			board[i][j] = EMPTY
	
   def draw_border(self):
	boarder = "              "
	for i in xrange(self.N):
		if i == self.N - 1:
			boarder = boarder + "---"
		else:
			boarder = boarder + "----"
	boarder = boarder + " \n"
        return boarder
	
   def print_board(self):
        tab = ""
	tab = "               "
	for i in xrange(self.N):
		tab  = tab + str(i+1) + "   "
	tab = tab + "\n"
	
	tab = tab + self.draw_border()
	row_char = 'A'
		
	for i in xrange(self.N):
		tab = tab + "           " + row_char
		tab = tab + " | "
		for j in xrange(self.N):
			if self.board[i][j] == self.CROSS:
				tab = tab + "X" + " | "
			elif self.board[i][j] == self.EMPTY:
				tab = tab + " " + " | "
			else:
				tab = tab + "O" + " | "
		tab = tab + "\n"
		row_char = chr(ord(row_char) + 1)
		
	self.draw_border()
	tab = tab + ""
        return tab
		
   def make_move(self, row, col, seed):
	self.board[row][col] = seed
		
   def is_cell_empty(self, row, col):	
	return self.board[row][col] == self.EMPTY
		
   def check_for_win(self, row, col, seed):
	""" Check the row where the move was played """
	if self.board[row][0] == seed and self.board[row][1] == seed and self.board[row][2] == seed:
		return True
		
	""" Check the column where the move was played """
	if self.board[0][col] == seed and self.board[1][col] == seed and self.board[2][col] == seed:
		return True
		
	""" Check if move was made on the diagonal """
	if row == col:
		if self.board[0][0] == seed and self.board[1][1] == seed and self.board[2][2] == seed:
			return True
		
	""" Check if move was made on the anti diagonal """
	if row + col == 2:
		if self.board[0][2] == seed and self.board[1][1] == seed and self.board[2][0] == seed:
			return True
		
	return False

   def is_valid_move(self, move):
	if len(move) != 2:
		return False
	if move[0] != 'a' and move[0] != 'b' and move[0] != 'c':
		return False
	if int(move[1]) > 3 or int(move[1]) < 1:
		return False
	if not self.is_cell_empty(ord(move[0]) - ord('a'), int(move[1]) - 1):
		return False
			
	return True

   def isDraw(self, plays):
      return plays == 6

   """ Just makes a move in the next available spot """
   def AI_move(self):
	found = False
	for i in xrange(self.N):
		for j in xrange(self.N):
			if self.board[i][j] == self.EMPTY:
				self.board[i][j] = self.CROSS
                                self.AI_row = i
                                self.AI_col = j
				found = True
				break
		if found == True:
			break

   def get_AI_row(self):
       return self.AI_row

   def get_AI_col(self):
       return self.AI_col

   #Menu to send client
   def print_menu(self, first_mv):
	menu = "     ********************************************\n" + "                    TIC TAC TOE MENU             \n" + "     ********************************************\n" + "     All players get circles.\n" + "     The AI will get crosses. To place a move \n" + "     on the board, first type the row letter\n" + "     then the column number, e.g. a1, c3, etc...\n"  + "     After you make your move, the AI will make \n" + "     one in response. \n"

        if first_mv == '-c':
           menu = menu + "since it was indicated that the client starts first, then please make a move.\n"
        else:
           menu = menu + "since it was not indicated that the client starts first, then the AI will make the first move.\n"
           self.AI_move()
        return menu
#######################################################################
#####################END-GAME-IMPLEMENTATION###########################

"""Client thread"""
class Client(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        pass

    def setup(self, __client, __address):
        self.client = __client
        self.address = __address

    def connect(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #the game is processed here
    def run(self):
        #########First Batch of Messages#########
        game = TTTGame()
        ''' the client sends the first message in this exchange '''
        data = self.client.recv(1024)
        menu = game.print_menu(data)
        board = game.print_board()
        move_number = 0
        self.client.sendall(menu)
        self.client.sendall(board)
        ############End First Batch###############
        #########Second Batch of Messages#########
        while True:
            data = self.client.recv(1024)
            if data:
               data.lower()
               correct_move = game.is_valid_move(data)
               if correct_move:
                  #parse the user data 
	          row = ord(data[0]) - ord('a')
                  col = int(data[1]) - 1
                  game.make_move(row, col, 1)
                  game.AI_move()
                  board = game.print_board()
                  a_row = game.get_AI_row()
                  a_col = game.get_AI_col()
                  #########Third Batch of Messages##########
                  #Check if the game is over
                  if game.check_for_win(row, col, 1):
                     board = game.print_board()
                     self.client.send('e' + board + '\nGAMEOVER: You Won!')
                     print('removing client', self.address)
                     break
                  if game.check_for_win(a_row, a_col, 2):
                     board = game.print_board()
                     self.client.send('e' + board + '\nGAMEOVER: You Lost!')
                     print('removing client', self.address)
                     break
                  if game.isDraw(move_number):
                     board = game.print_board()
                     self.client.send('e' + board + '\nGAMEOVER: Draw!')
                     print('removing client', self.address)
                     break
                  #########End Third Batch####################
        ##############End Second Batch########################
                  self.client.sendall(board)
                  move_number += 2
               else:
                  self.client.sendall("invalid move. please try again.")
            else:
                break

class Server(object):
       def __init__(self):
           self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
           self.server.bind(('127.0.0.1', 13037))
       
       def run(self):
           self.server.listen(5)
           print 'listening for new connections....'
           inputs = [self.server]

           while True:
              try:
                 inputsocket, outputsocket, throwsocket = select.select(inputs, [], []);
                 for s in inputsocket:
                    if s == self.server:
                       sock, address = self.server.accept();
                       print('new connection from ', address)
                       client = Client()
                       client.setup(sock, address)
                       client.start()
              except KeyboardInterrupt:
                 print "Keyboard interrupt detected, connection will close after threads are ended."
                 break
           print "initiate connection close..."
           self.server.close()

if __name__ == '__main__':
    server = Server()
    server.run()

