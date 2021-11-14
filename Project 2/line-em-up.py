# based on code from https://stackabuse.com/minimax-and-alpha-beta-pruning-in-python

import time
import numpy as np
from contextlib import redirect_stdout
from random import randint

class Game:
	MINIMAX = 0
	ALPHABETA = 1
	HUMAN = 2
	AI = 3

	def __init__(self, recommend=True):
		n, s, t = self.ask_conditions()
		self.n = n
		self.s = s
		self.t = t
		# set some defaults that will be overwritten
		self.max_depth_x = 5
		self.max_depth_o = 5
		self.initialize_game(n)
		self.blocks = []
		self.block_symbol = "🔲"
		self.block_count = self.add_blocks()
		self.recommend = recommend

	def initialize_game(self, n, blocks=None):
		self.last_move = (-1, -1)
		self.current_state = np.full((n, n), ".").tolist()
		# We're replaying a game so add back the blocks
		if blocks is not None:
			for block in blocks:
				self.current_state[block[0]][block[1]] = self.block_symbol

		# Player X always plays first
		self.player_turn = 'X'

	def add_blocks(self):
		block_count = int(input("How many blocks would you like to add?: "))
		if block_count != 0:
			random_block = input("Would you like randomly placed blocks? [y/N]: " or False) == "y"
		else:
			random_block = False

		if block_count > 2*self.n:
			block_count = 2*self.n
			print(F"You've attempted to add to many blocks, setting blocks to {block_count} (maximum for this board size)")

		if random_block:
			for block in range(0, block_count):
				x = randint(0, self.n - 1)
				y = randint(0, self.n - 1)
				# if the blocks are already present, keep generating a new pair until we find some that aren't
				while (x ,y) in self.blocks:
					x = randint(0, self.n - 1)
					y = randint(0, self.n - 1)
				self.current_state[x][y] = self.block_symbol
				self.blocks.append((x, y))
		else:
			for block in range(0, block_count):
				x = int(input(F"X coordinate for block {block}: "))
				y = int(input(F"Y coordinate for block {block}: "))
				self.current_state[x][y] = self.block_symbol
				self.blocks.append((x, y))
		return block_count

	def decide_depth(self, player_x, player_o):
		if player_x == self.AI:
			self.max_depth_x = int(input("How many rounds ahead should player X look (Max search depth)? [Default: 5]: ") or 5)
		if player_o == self.AI:
			self.max_depth_o = int(input("How many rounds ahead should player O look (Max search depth)? [Default: 5]: ") or 5)


	def ask_conditions(self):
		n = int(input('How large should the board be? (n x n)[Default: 3]: ') or 3)
		s = int(input("How long should a winning line be?[Default: 3]: ") or 3)
		t = int(input("How many seconds should the AI have to evaluate the best move?[Default: 5]: ") or 5)

		if n > 10:
			n = 10
			print(F"You've chosen too large of a game board, setting to {n}")
		elif n < 3:
			n = 3
			print(F"You've chosen too small of a game board, setting to {n}")

		if s > 10:
			s = 10
			print(F"You've chosen too large of a win line, setting to {s}")
		elif s < 3:
			s = 3
			print(F"You've chosen too small of a win line, setting to {s}")

		return (n, s, t)

	def draw_board(self):
		labels = range(0, self.n)
		print()
		print("  " + " ".join(map(str, labels)))
		for y in range(0, self.n):
			print(str(labels[y]) + " ", end='')
			for x in range(0, self.n):
				print(F'{self.current_state[x][y]} ', end="")
			print()
		print()

	def is_valid(self, px, py):
		if px < 0 or px > self.n - 1 or py < 0 or py > self.n - 1:
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

		## Check its a block / empty spot
		if self.current_state[px][py - 1] == self.block_symbol or self.current_state[px][py - 1] == ".":
			return count

		## check its not same, then return count
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

		## Check its a block / empty spot
		if self.current_state[px][py + 1] == self.block_symbol or self.current_state[px][py + 1] == ".":
			return count

		## check its not same, the return count
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

		## Check its a block / empty spot
		if self.current_state[px - 1][py] == self.block_symbol or self.current_state[px - 1][py] == ".":
			return count

		## check its not same, the return count
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

		## Check its a block / empty spot
		if self.current_state[px + 1][py] == self.block_symbol or self.current_state[px + 1][py] == ".":
			return count

		## check its not same, the return count
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

		## Check its a block / empty spot
		if self.current_state[px - 1][py + 1] == self.block_symbol or self.current_state[px - 1][py + 1] == ".":
			return count

		## check its not same, the return count
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

		## Check its a block / empty spot
		if self.current_state[px - 1][py - 1] == self.block_symbol or self.current_state[px - 1][py - 1] == ".":
			return count

		## check its not same, the return count
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

		## Check its a block / empty spot
		if self.current_state[px + 1][py + 1] == self.block_symbol or self.current_state[px + 1][py + 1] == ".":
			return count

		## check its not same, the return count
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

		## Check its a block / empty spot
		if self.current_state[px + 1][py - 1] == self.block_symbol or self.current_state[px + 1][py - 1] == ".":
			return count

		## check its not same, the return count
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
			self.initialize_game(self.n, blocks=self.blocks)
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

	def evaluate_state(self):
		x, y = self.last_move
		# Heuristic evaluation
		# Heuristic 1: What is the count of the longest line making this line would make?
		lines = []
		lines.append(self.check_e(0, self.last_move) + self.check_w(0, self.last_move) + 1)
		lines.append(self.check_n(0, self.last_move) + self.check_s(0, self.last_move) + 1)
		lines.append(self.check_sw(0, self.last_move) + self.check_ne(0, self.last_move) + 1)
		lines.append(self.check_se(0, self.last_move) + self.check_nw(0, self.last_move) + 1)
		a = max(lines)/self.s

		# Heuristic 2: How many free spaces are around the current move
		# Rational is that check for non-empty spaces as to promote blocking
		# very verbose, but pretty fast...
		b = x + 1 < self.n and self.current_state[x + 1][y] != "."
		b += x - 1 >= 0 and self.current_state[x - 1][y] != "."
		b += y + 1 < self.n and self.current_state[x][y + 1] != "."
		b += y - 1 < self.n and self.current_state[x][y - 1] != "."
		b += y + 1 < self.n and x + 1 < self.n and self.current_state[x + 1][y + 1] != "."
		b += x - 1 >= 0 and y - 1 >= 0 and self.current_state[x - 1][y - 1] != "."
		b += x - 1 >= 0 and y + 1 < self.n and self.current_state[x - 1][y + 1] != "."
		b += y - 1 >= 0 and x + 1 < self.n and self.current_state[x + 1][y - 1] != "."

		# Clamp heuristics to between 0 and 1
		# This can only be as long as the win condition, thus divide by s
		a = a/self.s
		# There are only 8 spaces (maximum) around the current spot
		b = b/8

		# weight heuristic a higher than b to promote blocking
		return (0.75*a + 0.25*b)/2

	def minimax(self, max=False, depth=10, start_time=time.time()):
		# Minimizing for 'X' and maximizing for 'O'
		# Possible values are:
		# -1 - win for 'X'
		# 0  - a tie
		# 1  - loss for 'X'
		# We're initially setting it to 2 or -2 as worse than the worst case:
		value = 2
		flip = 1
		if max:
			value = -2
			flip = -1
		x = None
		y = None
		result = self.is_end()
		if result == 'X':
			return (-1, x, y)
		elif result == 'O':
			return (1, x, y)
		elif result == '.':
			return (0, x, y)
		# remove some time from the original limit so the AI exits early / in time
		if depth <= 0 or time.time() - start_time >= self.t - 0.01:
			# Heuristic eval, constrained to [-1, 1]
			# depending if we're min or max flip the value to be negative/positive
			value = self.evaluate_state() * flip
			return (value, x, y)

		depth -= 1
		for i in range(0, self.n):
			for j in range(0, self.n):
				if self.current_state[i][j] == '.':
					if max:
						self.current_state[i][j] = 'O'
						(v, _, _) = self.minimax(max=False, depth=depth, start_time=start_time)
						if v > value:
							value = v
							x = i
							y = j
					else:
						self.current_state[i][j] = 'X'
						(v, _, _) = self.minimax(max=True, depth=depth, start_time=start_time)
						if v < value:
							value = v
							x = i
							y = j
					self.current_state[i][j] = '.'
		return (value, x, y)

	def alphabeta(self, alpha=-2, beta=2, max=False, depth=10, start_time=time.time()):
		# Minimizing for 'X' and maximizing for 'O'
		# Possible values are:
		# -1 - win for 'X'
		# 0  - a tie
		# 1  - loss for 'X'
		# We're initially setting it to 2 or -2 as worse than the worst case:
		value = 2
		flip = 1
		if max:
			flip = -1
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
		# remove some time from the original limit so the AI exits early / in time
		if depth <= 0 or time.time() - start_time >= self.t - 0.01:
			# Heuristic eval, constrained to [-1, 1]
			# depending if we're min or max flip the value to be negative/positive
			value = self.evaluate_state() * flip
			return (value, x, y)

		depth -= 1
		for i in range(0, self.n):
			for j in range(0, self.n):
				if self.current_state[i][j] == '.':
					if max:
						self.current_state[i][j] = 'O'
						(v, _, _) = self.alphabeta(alpha, beta, max=False, depth=depth, start_time=start_time)
						if v > value:
							value = v
							x = i
							y = j
					else:
						self.current_state[i][j] = 'X'
						(v, _, _) = self.alphabeta(alpha, beta, max=True, depth=depth, start_time=start_time)
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
		self.decide_depth(player_x, player_o)
		while True:
			self.draw_board()
			if self.check_end():
				return
			start = time.time()
			if algo == self.MINIMAX:
				if self.player_turn == 'X':
					(_, x, y) = self.minimax(max=False, start_time=start, depth=self.max_depth_x)
				else:
					(_, x, y) = self.minimax(max=True, start_time=start, depth=self.max_depth_o)
			else:  # algo == self.ALPHABETA
				if self.player_turn == 'X':
					(m, x, y) = self.alphabeta(max=False, start_time=start, depth=self.max_depth_x)
				else:
					(m, x, y) = self.alphabeta(max=True, start_time=start, depth=self.max_depth_o)
			end = time.time()
			if (self.player_turn == 'X' and player_x == self.HUMAN) or (
					self.player_turn == 'O' and player_o == self.HUMAN):
				if self.recommend:
					print(F'Evaluation time: {round(end - start, 7)}s')
					print(F'Recommended move: x = {x}, y = {y}')
				(x, y) = self.input_move()
			if (self.player_turn == 'X' and player_x == self.AI) or (self.player_turn == 'O' and player_o == self.AI):
				round_time = round(end - start, 7)
				if round_time > self.t:
					print("AI took to long to evaluate next move and has lost.")
					return
				print(F'Evaluation time: {round_time}s')
				print(F'Player {self.player_turn} under AI control plays: x = {x}, y = {y}')
			self.last_move = (x, y)
			self.current_state[x][y] = self.player_turn
			self.switch_player()

def main():
	g = Game(recommend=True)
	# with open(F"traces/gameTrace_{g.n}{g.block_count}{g.s}{g.t}.txt", 'w') as f:
	# 	with redirect_stdout(f):
	# 		g.play(algo=Game.ALPHABETA, player_x=Game.AI, player_o=Game.AI)

	g.play(algo=Game.ALPHABETA, player_x=Game.AI, player_o=Game.AI)
	g.play(algo=Game.MINIMAX, player_x=Game.AI, player_o=Game.AI)


if __name__ == "__main__":
	main()
