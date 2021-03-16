import common

#helpful, but not needed
class variables:
	counter=0

def game_completed(sudoku):
	for y in range(9):
		for x in range(9):
			if sudoku[y][x] == 0:
				return False
	return True

def get_unassigned_variable(sudoku):
	result = []
	for y in range(9):
		for x in range(9):
			if sudoku[y][x]== 0:
				result.append(y)
				result.append(x)
				return result

def remove_value(sudoku, y, x):
	sudoku[y][x] = 0
	return sudoku

def put_value(sudoku, y, x, z):
	sudoku[y][x] = z
	return sudoku

def get_values(sudoku, var):
	result = []
	for i in range(1, 10):
		if common.can_yx_be_z(sudoku, var[0], var[1], i):
			result.append(i)
	return result

def keep_going(sudoku):
	for i in range(9):
		for j in range(9):
			if sudoku[i][j] == 0:
				var = []
				var.append(i)
				var.append(j)
				result = get_values(sudoku,var)
				if len(result) == 0:
					return False
	return True

def sudoku_backtracking(sudoku):
	variables.counter = 0
	result = sudoku_backtracking_helper(variables.counter, sudoku, False)
	return result[0]

def sudoku_backtracking_helper(counter, sudoku, fail):
	counter = counter + 1
	potential_values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
	if game_completed(sudoku):
		fail = False
		return counter, fail
	else:
		var = get_unassigned_variable(sudoku)
		for i in potential_values:
			if common.can_yx_be_z(sudoku, var[0], var[1], i):
				put_value(sudoku, var[0], var[1], i)
				counter, fail = sudoku_backtracking_helper(counter, sudoku, fail)
				if not fail:
					return counter, fail
				sudoku = remove_value(sudoku, var[0], var[1])
		fail = True
		return counter, fail

def sudoku_forwardchecking(sudoku):
	variables.counter = 0
	#put your code here
	result = sudoku_forwardchecking_helper(variables.counter, sudoku, False)
	return result[0]

def sudoku_forwardchecking_helper(counter, sudoku, fail):
	counter = counter + 1
	if game_completed(sudoku):
		fail = False
		return counter, fail
	else:
		var = get_unassigned_variable(sudoku)
		potential_values = get_values(sudoku, var)
		for i in potential_values:
			put_value(sudoku, var[0], var[1], i)
			if keep_going(sudoku):
				counter, fail = sudoku_forwardchecking_helper(counter, sudoku, fail)
				if not fail:
					return counter, fail
			sudoku = remove_value(sudoku, var[0], var[1])
		fail = True
		return counter, fail




