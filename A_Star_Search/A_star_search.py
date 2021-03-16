import common

class node:
	def __init__(self, parent, yx):
		self.parent = parent
		self.yx = yx

def find_start(map):
	height = common.constants.MAP_HEIGHT
	width = common.constants.MAP_WIDTH
	starting_point = [-1, -1]
	for i in range(height):
		for j in range(width):
			if map[i][j] == 2:
				starting_point = [i, j]
	return starting_point

def find_end(map):
	height = common.constants.MAP_HEIGHT
	width = common.constants.MAP_WIDTH
	end_point = [-1, -1]
	for i in range(height):
		for j in range(width):
			if map[i][j] == 3:
				end_point = [i, j]
	return end_point

def is_space(map, y, x):
	if map[y][x] == 0:
		return True
	return False

def is_valid(y, x):
	if y <= common.constants.MAP_HEIGHT - 1 and y >= 0 and x <= common.constants.MAP_WIDTH - 1 and x >= 0:
		return True
	return False

def is_detination(map, y, x):
	if map[y][x] == 3:
		return True
	return False


def is_moving(map, y, x):
	if (is_valid(y, x) == True and is_space(map, y, x)==True) or (is_valid(y, x)==True and is_detination(map, y, x)==True):
		return True
	return False


def get_index(n):
	width = common.constants.MAP_WIDTH
	result = n.yx[1] * width + n.yx[0]
	return result

# First [y][x+1], then [y+1][x], then [y][x-1], and finally [y-1][x]
def get_all_direction(y, x):
	result = [[y, x+1], [y+1, x], [y, x-1], [y-1, x]]
	return result

def get_all_nodes(map, current):
	# list of list
	temp = get_all_direction(current.yx[0], current.yx[1])
	end = find_end(map)
	nodes = []
	for i in temp:
		if is_moving(map, i[0], i[1]):
			temp_node = node(current, i)
			nodes.append(temp_node)
	return nodes

def updat_nodes(map, current, closed):
	nodes = get_all_nodes(map, current)
	for i in nodes:
		if i in closed:
			nodes.remove(i)
	return nodes

def f_function(map, p, dis_list):
	end = find_end(map)
	dis = get_index(p)
	m = abs(p.yx[1] - end[1]) + abs(p.yx[0] - end[0])
	return dis_list[dis] + m

def find_move(map, possible_moves, dis_list):
	min_f = f_function(map, possible_moves[0], dis_list)
	min_p = possible_moves[0]
	for i in possible_moves:
		if f_function(map, i, dis_list) < min_f:
			min_p = i
		if f_function(map,i, dis_list) == min_f and i.yx[1] < min_p.yx[1]:
			min_p = i
		if f_function(map, i, dis_list) == min_f and i.yx[1] == min_p.yx[1] and i.yx[0] < min_p.yx[0]:
			min_p = i
	return min_p

def astar_search(map):
	found = False
	# access the map using "map[y][x]"
	# y between 0 and common.constants.MAP_HEIGHT-1
	# x between 0 and common.constants.MAP_WIDTH-1
	start = find_start(map)
	current = node(None, start)
	end = find_end(map)
	closed = []
	possible_moves = []
	dis_list = [0] * common.constants.MAP_HEIGHT * common.constants.MAP_WIDTH
	possible_moves.append(current)
	while len(possible_moves) != 0:
		if current.yx != end and current not in closed:
			map[current.yx[0]][current.yx[1]] = 4
			nodes = updat_nodes(map, current, closed)
			for i in nodes:
				possible_moves.append(i)
				node_index = get_index(i)
				current_index = get_index(current)
				dis_list[node_index] = dis_list[current_index] + 1
			closed.append(current)
			possible_moves.remove(current)
			if len(possible_moves) != 0:
				current = find_move(map, possible_moves, dis_list)
				if current.yx[0] == end[0] and current.yx[1] == end[1]:
					while current:
						map[current.yx[0]][current.yx[1]] = 5
						current = current.parent
					return True
	return found

