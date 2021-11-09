# based on code from https://stackabuse.com/minimax-and-alpha-beta-pruning-in-python

import time
import numpy as np


class Game:
	MINIMAX = 0
	ALPHABETA = 1
	HUMAN = 2
	AI = 3

	def __init__(self, recommend=True):
		self.initialize_game()
		self.recommend = recommend

	def initialize_game(self, n=3, b=None, s=3):
		if b is None:
			b = []

		self.last_move = (-1, -1)
		self.blocks = b
		self.n = n
		self.s = s
		self.block_count = len(b)
		self.block_symbol = "👎"
		self.current_state = np.full((n, n), ".").tolist()
		for block in b:
			self.current_state[block[0]][block[1]] = self.block_symbol

		# Player X always plays first
		self.player_turn = 'X'

	def draw_board(self):
		print()
		for y in range(0, self.n):
			for x in range(0, self.n):
				print(F'{self.current_state[x][y]}', end="")
			print()
		print()

	def is_valid(self, px, py):
		if px < 0 or px > 2 or py < 0 or py > 2:
			return False
		elif self.current_state[px][py] != '.':
			return False
		else:
			return True

	def is_end(self):
		horizontal = self.check_e(0, self.last_move) + self.check_w(0, self.last_move) + 1
		vertical = self.check_n(0, self.last_move) + self.check_s(0, self.last_move) + 1
		main_diagonal = self.check_sw(0, self.last_move) + self.check_ne(0, self.last_move) + 1
		second_diagonal = self.check_se(0, self.last_move) + self.check_nw(0, self.last_move) + 1

		if horizontal >= self.s or vertical >= self.s or main_diagonal >= self.s or second_diagonal >= self.s:
			return self.current_state[self.last_move[0]][self.last_move[1]]

		if not any("." in x for x in self.current_state):
			return "."

		return None


	def check_n(self, count, move):
		px, py = move
		if py - 1 < 0:
			return count

		## Check its a block
		if self.current_state[px][py - 1] == self.block_symbol or self.current_state[px][py - 1] == ".":
			return count

		## check its not same, the return none

		## else it must be same so recurse count + 1
		if self.current_state[px][py] != self.current_state[px][py - 1]:
			return count
		else:
			if count >= self.s:
				return count
			return self.check_n(count + 1, (px, py - 1))

	def check_s(self, count, move):
		px, py = move
		if py + 1 >= self.n:
			return count

		## Check its a block
		if self.current_state[px][py + 1] == self.block_symbol or self.current_state[px][py + 1] == ".":
			return count

		## check its not same, the return none

		## else it must be same so recurse count + 1
		if self.current_state[px][py] != self.current_state[px][py + 1]:
			return count
		else:
			if count >= self.s:
				return count
			return self.check_s(count + 1, (px, py + 1))

	def check_w(self, count, move):
		px, py = move
		if px - 1 < 0:
			return count

		## Check its a block
		if self.current_state[px - 1][py] == self.block_symbol or self.current_state[px - 1][py] == ".":
			return count

		## check its not same, the return none

		## else it must be same so recurse count + 1
		if self.current_state[px][py] != self.current_state[px - 1][py]:
			return count
		else:
			if count >= self.s:
				return count
			return self.check_w(count + 1, (px - 1, py))

	def check_e(self, count, move):
		px, py = move
		if px + 1 >= self.n:
			return count

		## Check its a block
		if self.current_state[px + 1][py] == self.block_symbol or self.current_state[px + 1][py] == ".":
			return count

		## check its not same, the return none

		## else it must be same so recurse count + 1
		if self.current_state[px][py] != self.current_state[px + 1][py]:
			return count
		else:
			if count >= self.s:
				return count
			return self.check_e(count + 1, (px + 1, py))

	def check_ne(self, count, move):
		px, py = move
		if px - 1 < 0 or py + 1 >= self.n:
			return count

		## Check its a block
		if self.current_state[px - 1][py + 1] == self.block_symbol or self.current_state[px - 1][py + 1] == ".":
			return count

		## check its not same, the return none

		## else it must be same so recurse count + 1
		if self.current_state[px][py] != self.current_state[px - 1][py + 1]:
			return count
		else:
			if count >= self.s:
				return count
			return self.check_ne(count + 1, (px - 1, py + 1))

	def check_nw(self, count, move):
		px, py = move
		if px - 1 < 0 or py - 1 < 0:
			return count

		## Check its a block
		if self.current_state[px - 1][py - 1] == self.block_symbol or self.current_state[px - 1][py - 1] == ".":
			return count

		## check its not same, the return none

		## else it must be same so recurse count + 1
		if self.current_state[px][py] != self.current_state[px - 1][py - 1]:
			return count
		else:
			if count >= self.s:
				return count
			return self.check_nw(count + 1, (px - 1, py - 1))

	def check_se(self, count, move):
		px, py = move
		if px + 1 >= self.n or py + 1 >= self.n:
			return count

		## Check its a block
		if self.current_state[px + 1][py + 1] == self.block_symbol or self.current_state[px + 1][py + 1] == ".":
			return count

		## check its not same, the return none

		## else it must be same so recurse count + 1
		if self.current_state[px][py] != self.current_state[px + 1][py + 1]:
			return count
		else:
			if count >= self.s:
				return count
			return self.check_se(count + 1, (px + 1, py + 1))

	def check_sw(self, count, move):
		px, py = move
		if px + 1 >= self.n or py - 1 < 0:
			return count

		## Check its a block
		if self.current_state[px + 1][py - 1] == self.block_symbol or self.current_state[px + 1][py - 1] == ".":
			return count

		## check its not same, the return none

		## else it must be same so recurse count + 1
		if self.current_state[px][py] != self.current_state[px + 1][py - 1]:
			return count
		else:
			if count >= self.s:
				return count
			return self.check_sw(count + 1, (px + 1, py - 1))


	def check_end(self):
		self.result = self.is_end()
		# Printing the appropriate message if the game has ended
		if self.result != None:
			if self.result == 'X':
				print('The winner is X!')
			elif self.result == 'O':
				print('The winner is O!')
			elif self.result == '.':
				print("It's a tie!")
			self.initialize_game()
		return self.result

	def input_move(self):
		while True:
			print(F'Player {self.player_turn}, enter your move:')
			px = int(input('enter the x coordinate: '))
			py = int(input('enter the y coordinate: '))
			if self.is_valid(px, py):
				return (px, py)
			else:
				print('The move is not valid! Try again.')

	def switch_player(self):
		if self.player_turn == 'X':
			self.player_turn = 'O'
		elif self.player_turn == 'O':
			self.player_turn = 'X'
		return self.player_turn

	def minimax(self, max=False):
		# Minimizing for 'X' and maximizing for 'O'
		# Possible values are:
		# -1 - win for 'X'
		# 0  - a tie
		# 1  - loss for 'X'
		# We're initially setting it to 2 or -2 as worse than the worst case:
		value = 2
		if max:
			value = -2
		x = None
		y = None
		result = self.is_end()
		if result == 'X':
			return (-1, x, y)
		elif result == 'O':
			return (1, x, y)
		elif result == '.':
			return (0, x, y)
		for i in range(0, self.n):
			for j in range(0, self.n):
				if self.current_state[i][j] == '.':
					if max:
						self.current_state[i][j] = 'O'
						(v, _, _) = self.minimax(max=False)
						if v > value:
							value = v
							x = i
							y = j
					else:
						self.current_state[i][j] = 'X'
						(v, _, _) = self.minimax(max=True)
						if v < value:
							value = v
							x = i
							y = j
					self.current_state[i][j] = '.'
		return (value, x, y)

	def alphabeta(self, alpha=-2, beta=2, max=False):
		# Minimizing for 'X' and maximizing for 'O'
		# Possible values are:
		# -1 - win for 'X'
		# 0  - a tie
		# 1  - loss for 'X'
		# We're initially setting it to 2 or -2 as worse than the worst case:
		value = 2
		if max:
			value = -2
		x = None
		y = None
		result = self.is_end()
		if result == 'X':
			return (-1, x, y)
		elif result == 'O':
			return (1, x, y)
		elif result == '.':
			return (0, x, y)
		for i in range(0, self.n):
			for j in range(0, self.n):
				if self.current_state[i][j] == '.':
					if max:
						self.current_state[i][j] = 'O'
						(v, _, _) = self.alphabeta(alpha, beta, max=False)
						if v > value:
							value = v
							x = i
							y = j
					else:
						self.current_state[i][j] = 'X'
						(v, _, _) = self.alphabeta(alpha, beta, max=True)
						if v < value:
							value = v
							x = i
							y = j
					self.current_state[i][j] = '.'
					if max:
						if value >= beta:
							return (value, x, y)
						if value > alpha:
							alpha = value
					else:
						if value <= alpha:
							return (value, x, y)
						if value < beta:
							beta = value
		return (value, x, y)

	def play(self, algo=None, player_x=None, player_o=None):
		if algo == None:
			algo = self.ALPHABETA
		if player_x == None:
			player_x = self.HUMAN
		if player_o == None:
			player_o = self.HUMAN
		while True:
			self.draw_board()
			if self.check_end():
				return
			start = time.time()
			if algo == self.MINIMAX:
				if self.player_turn == 'X':
					(_, x, y) = self.minimax(max=False)
					(_, x, y) = self.minimax(max=True)
			else:  # algo == self.ALPHABETA
				if self.player_turn == 'X':
					(m, x, y) = self.alphabeta(max=False)
				else:
					(m, x, y) = self.alphabeta(max=True)
			end = time.time()
			if (self.player_turn == 'X' and player_x == self.HUMAN) or (
					self.player_turn == 'O' and player_o == self.HUMAN):
				if self.recommend:
					print(F'Evaluation time: {round(end - start, 7)}s')
					print(F'Recommended move: x = {x}, y = {y}')
				(x, y) = self.input_move()
			if (self.player_turn == 'X' and player_x == self.AI) or (self.player_turn == 'O' and player_o == self.AI):
				print(F'Evaluation time: {round(end - start, 7)}s')
				print(F'Player {self.player_turn} under AI control plays: x = {x}, y = {y}')
			self.last_move = (x, y)
			self.current_state[x][y] = self.player_turn
			self.switch_player()


def main():
	g = Game(recommend=True)
	g.play(algo=Game.ALPHABETA, player_x=Game.AI, player_o=Game.AI)
	g.play(algo=Game.MINIMAX, player_x=Game.AI, player_o=Game.HUMAN)


if __name__ == "__main__":
	main()
