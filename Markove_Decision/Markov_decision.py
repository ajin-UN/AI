import common

def find_spots(map):
	result = []
	pizza = []
	customer = []
	for i in range(6):
		for j in range(6):
			if map[i][j] == 1:
				pizza.append(i)
				pizza.append(j)
			elif map[i][j] == 2:
				customer.append(i)
				customer.append(j)
	result.append(pizza)
	result.append(customer)
	return result

def find_rivals(map):
	result = []
	for i in range(6):
		for j in range(6):
			if map[i][j] == 3:
				result.append([i, j])
	return result

def deal_best(best_list):
	if not best_list:
		for i in best_list:
			if i > 4:
				best_list.remove(i)
		if not best_list:
			return min(i for i in best_list)
		else:
			return best_list[0]
	return best_list[0]

def valid_loc(y, x):
	if y >= 1 and y <= 4 and x >= 1 and x <= 4:
		return True
	return False

def value_partial(values, y, x, battery_drop_cost, discount):
	if y < 0:
		if x < 0:
			x = 0
			y = 0
		elif x > 5:
			x = 5
			y = 0
		else:
			y = 0
	elif y > 5:
		if x < 0:
			x = 0
			y = 5
		elif x > 5:
			x = 5
			y = 5
		else:
			y = 5
	elif x < 0:
		x = 0
	elif x > 5:
		x = 5
	value = values[y][x] * discount - battery_drop_cost
	return value

def value_formula(action, values, y, x , battery_drop_cost, discount):
	y_add = value_partial(values, y + 1, x, battery_drop_cost, discount)
	y_minus = value_partial(values, y - 1, x, battery_drop_cost, discount)
	x_add = value_partial(values, y, x + 1, battery_drop_cost, discount)
	x_minus = value_partial(values, y, x - 1, battery_drop_cost, discount)
	y_add_double = value_partial(values, y + 1, x, battery_drop_cost * 2, discount)
	y_minus_double = value_partial(values, y - 1, x, battery_drop_cost * 2, discount)
	x_add_double = value_partial(values, y, x + 1, battery_drop_cost * 2, discount)
	x_minus_double = value_partial(values, y, x - 1, battery_drop_cost * 2, discount)
	if action == 1:
		value = (0.7 * y_add) + (0.15 * x_add) + (0.15 * x_minus)
		return value
	if action == 2:
		value = (0.7 * x_minus) + (0.15 * y_add) + (0.15 * y_minus)
		return value
	if action == 3:
		value = (0.7 * y_minus) + (0.15 * x_add) + (0.15 * x_minus)
		return value
	if action == 4:
		value = (0.7 * x_add) + (0.15 * y_add) + (0.15 * y_minus)
		return value
	if action == 5:
		value = (0.8 * y_add_double) + (0.1 * x_add_double) + (0.1 * x_minus_double)
		return value
	if action == 6:
		value = (0.8 * x_minus_double) + (0.1 * y_add_double) + (0.1 * y_minus_double)
		return value
	if action == 7:
		value = (0.8 * y_minus_double) + (0.1 * x_add_double) + (0.1 * x_minus_double)
		return value
	if action == 8:
		value = (0.8 * x_add_double) + (0.1 * y_add_double) + (0.1 * y_minus_double)
		return value

def drone_flight_planner (map,policies, values, delivery_fee, battery_drop_cost, dronerepair_cost, discount):
	# PUT YOUR CODE HERE
	# access the map using "map[y][x]"
	# access the policies using "policies[y][x]"
	# access the values using "values[y][x]"
	# y between 0 and 5
	# x between 0 and 5
	# function must return the value of the cell corresponding to the starting position of the drone
	#

	results = find_spots(map)
	pizza_loc = results[0]
	customer_loc = results[1]
	rival_locs = find_rivals(map)
	for i in rival_locs:
		values[i[0]][i[1]] = -dronerepair_cost
	values[customer_loc[0]][customer_loc[1]] = delivery_fee
	start_y = pizza_loc[0]
	start_x = pizza_loc[1]
	delta = 0.5
	while delta > 0.001:
		delta = 0.001
		for i in range(6):
			for j in range(6):
				if map[i][j] == 0 or map[i][j] == 1:
					origin = values[i][j]
					values_list = []
					index_list = []
					for a in range(1, 9):
						value = value_formula(a, values, i, j, battery_drop_cost, discount)
						values_list.append(value)
					values[i][j] = max(values_list)
					for a in range(1, 9):
						if values[i][j] == values_list[a-1]:
							index_list.append(a)
					best_index = deal_best(index_list)
					policies[i][j] = best_index
					delta = max(delta, abs(origin - values[i][j]))
	return values[start_y][start_x]
