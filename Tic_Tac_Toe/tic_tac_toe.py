import common

class constants:
	Tie = 0
	X_wins = 1
	O_wins = -1
	# Not_finish = -2


def copy(board):
	new_board = [0] * 9
	for i in range(9):
		new_board[i] = board[i]
	return new_board


def check_winner(board):
	result = common.game_status(board)
	full = True
	for i in range(9):
		if board[i] == common.constants.NONE:
			full = False
	if result == common.constants.X:
		return constants.X_wins
	elif result == common.constants.O:
		return constants.O_wins
	elif result == common.constants.NONE and full:
		return constants.Tie
	return None


def simbol(result):
	if (result==constants.X_wins):
		return common.constants.X
	elif (result==constants.O_wins):
		return common.constants.O
	return common.constants.NONE


def next_move(board, turn):
	result = []
	for i in range(9):
		if board[i] == common.constants.NONE:
			board_copy = copy(board)
			board_copy[i] = turn
			result.append(board_copy)
	return result


def max_helper(board, turn):
	result = check_winner(board)
	if result == None:
		temp = -100
		moves = next_move(board, common.constants.X)
		for i in moves:
			temp = max(temp, min_helper(i, turn))
		return temp
	return result


def min_helper(board, turn):
	result = check_winner(board)
	if result == None:
		temp = 100
		moves = next_move(board, common.constants.O)
		for i in moves:
			temp = min(temp, max_helper(i, turn))
		return temp
	return result


def min_max_helper(board, turn):
	if turn == common.constants.X:
		result = max_helper(board, turn)
	else:
		result = min_helper(board, turn)
	return result


def minmax_tictactoe(board, turn):
	#put your code here:
	#it must return common.constants.X(1), common.constants.O(2) or common.constants.NONE(0) for tie.
	#use the function common.game_status(board), to evaluate a board
	#it returns common.constants.X(1) if X wins, common.constants.O(2) if O wins or common.constants.NONE(0) if tie or game is not finished
	#the program will keep track of the number of boards evaluated
	#result = common.game_status(board);
	result = min_max_helper(board, turn)
	result = simbol(result)
	return result






def a_helper(board, turn, ab_list):
	result = check_winner(board)
	if result == None:
		temp = -100
		moves = next_move(board, common.constants.X)
		for i in moves:
			ab = ab_list.copy()
			temp = max(temp, b_helper(i, turn, ab))
			if ab_list[1] <= temp:
				return temp
			ab_list[0] = max(ab_list[0], temp)
		return temp
	return result


def b_helper(board, turn, ab_list):
	result = check_winner(board)
	if result == None:
		temp = 100
		moves = next_move(board, common.constants.O)
		for i in moves:
			ab = ab_list.copy()
			temp = min(temp, a_helper(i, turn, ab))
			if ab_list[0] >= temp:
				return temp
			ab_list[1] = min(ab_list[1], temp)
		return temp
	return result


def ab_helper(board, turn):
	ab_list = [-100, 100]
	if turn == common.constants.X:
		result = a_helper(board, turn, ab_list)
	else:
		result = b_helper(board, turn, ab_list)
	return result


def abprun_tictactoe(board, turn):
	#put your code here:
	#it must return common.constants.X(1), common.constants.O(2) or common.constants.NONE(0) for tie.
	#use the function common.game_status(board), to evaluate a board
	#it returns common.constants.X(1) if X wins, common.constants.O(2) if O wins or common.constants.NONE(0) if tie or game is not finished
	#the program will keep track of the number of boards evaluated
	#result = common.game_status(board);
	result = ab_helper(board, turn)
	result = simbol(result)
	return result



