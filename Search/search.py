import common
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

def df_search(map):
	found = False
	# PUT YOUR CODE HERE
	# access the map using "map[y][x]"
	# y between 0 and common.constants.MAP_HEIGHT-1
	# x between 0 and common.constants.MAP_WIDTH-1
	start_point_y = find_start(map)[0]
	start_point_x = find_start(map)[1]
	found = df_helper(map, start_point_y, start_point_x)
	return found

# First [y][x+1], then [y+1][x], then [y][x-1], and finally [y-1][x]
def df_helper(map, y, x):
	if map[y][x] == 3:
		map[y][x] = 5
		return True
	else:
		map[y][x] = 4
		if is_moving(map, y, x+1)==True :
			holder = df_helper(map, y, x+1)
			if holder == True:
				map[y][x] = 5
				return True
		if is_moving(map, y+1, x) == True:
			holder = df_helper(map, y+1, x)
			if holder == True:
				map[y][x] = 5
				return True
		if is_moving(map, y, x-1) == True:
			holder = df_helper(map, y, x-1)
			if holder == True:
				map[y][x] = 5
				return True
		if is_moving(map, y-1, x) == True:
			holder = df_helper(map, y-1, x)
			if holder == True:
				map[y][x] = 5
				return True
		return False

def get_index(y, x):
	width = common.constants.MAP_WIDTH
	result = y * width + x
	return result

# First [y][x+1], then [y+1][x], then [y][x-1], and finally [y-1][x]
def get_all_direction(y, x):
	result = [[y, x+1], [y+1, x], [y, x-1], [y-1, x]]
	return result

def is_visted(node , visted_list):
	temp_index = get_index(node[0], node[1])
	return visted_list[temp_index]

def initial_visited(size):
	result = []
	for i in range(size):
		result.append(False)
	return result

def bf_search(map):
	found = False
	height = common.constants.MAP_HEIGHT
	width = common.constants.MAP_WIDTH
	visited = initial_visited(height*width)
	#[y, x]
	start_point = find_start(map)
	end_point = find_end(map)
	queue = []
	result =[]
	queue.append(start_point)
	while len(queue) > 0:
		if queue[0] == start_point:
			temp = queue.pop(0)
			result.append(temp)
		else:
			result = queue.pop(0)
		queue_front = result[-1]
		queue_front_index = get_index(queue_front[0], queue_front[1])
		if end_point == queue_front:
			for r in result:
				map[r[0]][r[1]] = 5
			found = True
			return found
		elif visited[queue_front_index] == False:
			#list of list with all directions node
			new_node_list = get_all_direction(queue_front[0], queue_front[1])
			temp_list = []
			for n in new_node_list:
				if is_moving(map, n[0], n[1]) == True and is_visted(n, visited) == False:
					temp_list.append(n)
			for t in temp_list:
				new_result = list(result)
				new_result.append(t)
				queue.append(new_result)
			map[queue_front[0]][queue_front[1]] = 4
			visited[queue_front_index] = True
	return found