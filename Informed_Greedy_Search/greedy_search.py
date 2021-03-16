QUEENS = 10

def is_inrange(x):
    if 0 <= x and x < QUEENS:
        return True
    return False

# make a copy
def deep_copy(board):
    copy = [[0 for a in range(QUEENS)] for b in range(QUEENS)]
    for i in range(QUEENS):
        for j in range(QUEENS):
            copy[i][j] = board[i][j]
    return copy


# only have one queen in each col
def store_queens(board):
    result = [0 for a in range(QUEENS)]
    for j in range(len(board)):
        for i in range(len(board)):
            if board[i][j] == 1:
                result[j] = i
                break
    return result

def get_attack(counter):
    return (counter * (counter-1))

# check the attacks in the same row
def find_attack_row(board):
    result = 0
    for row in board:
        counter = 0
        for i in row:
            if i == 1:
                counter = counter + 1
        row_attack = get_attack(counter)
        result = result + row_attack
    return result


def get_diagnol_sum(x, y):
    result = [x, y]
    sum = x + y
    for i in range(sum):
        if is_inrange(i) == True and is_inrange(sum-i) == True:
            result.append(i)
            result.append(sum-i)
    return result


def get_diagnol_diff(x, y):
    result = [x, y]
    diff = abs(x - y)
    for i in range(x):
        result.append(i)
        if (i+diff) < QUEENS:
            result.append(i + diff)
        else:
            result.append(i - diff)
    return result

def get_cell(board, li):
    result = []
    i = 0
    while( i< len(li)):
        result.append(board[li[i]][li[i+1]])
        if (i + 2) < len(li):
            i = i + 2
        else:
            break
    return result

def find_attack_diagnol_sum_up(board):
    result = 0
    for i in range(QUEENS):
        temp = get_diagnol_sum(i, 0)
        temp_list = get_cell(board, temp)
        counter = 0
        for i in temp_list:
            if i == 1:
                counter = counter + 1
        row_attack = get_attack(counter)
        result = result + row_attack
    return result

def find_attack_diagnol_diff_up(board):
    result = 0
    for i in range(QUEENS):
        temp = get_diagnol_diff(i, QUEENS-1)
        temp_list = get_cell(board, temp)
        counter = 0
        for i in temp_list:
            if i == 1:
                counter = counter + 1
        row_attack = get_attack(counter)
        result = result + row_attack
    return result

def sum_helper(x, y):
    result = [ ]
    sum = x + y
    for i in range(sum):
        if is_inrange(i) == True and is_inrange(sum-i) == True:
            result.append(i)
            result.append(sum-i)
    return result

def find_attack_diagnol_sum_down(board):
    result = 0
    for i in range(1, QUEENS):
        temp = sum_helper(QUEENS - 1, i)
        temp_list = get_cell(board, temp)
        counter = 0
        for i in temp_list:
            if i == 1:
                counter = counter + 1
        row_attack = get_attack(counter)
        result = result + row_attack
    return result

def diff_helper(x, y):
    result = [x, y]
    diff = abs(x - y)
    for i in range(x):
        if 0 <= (i + diff) < QUEENS and i < y:
            result.append(i + diff)
            result.append(i)
    return result

def find_attack_diagnol_diff_down(board):
    result = 0
    for i in range(QUEENS - 1):
        temp = diff_helper(QUEENS-1 , i)
        temp_list = get_cell(board, temp)
        counter = 0
        for i in temp_list:
            if i == 1:
                counter = counter + 1

        row_attack = get_attack(counter)
        result = result + row_attack
    return result

def count_attack(board):
    return find_attack_row(board) + \
           find_attack_diagnol_sum_down(board) + \
           find_attack_diagnol_sum_up(board) + \
           find_attack_diagnol_diff_up(board) + \
           find_attack_diagnol_diff_down(board)

def find_min(attacks):
    minimum = 100
    for row in attacks:
        for i in row:
            if i < minimum:
                minimum = i
    return minimum

def find_all_mins(attacks):
    results = []
    min = find_min(attacks)
    for i in range(QUEENS):
        for j in range(QUEENS):
            if attacks[i][j] == min:
                results.append(i)
                results.append(j)
    return results

def find_min_cols(attacks):
    results = find_all_mins(attacks)
    a = 1
    cols = []
    while a < len(results):
        cols.append(results[a])
        a = a + 2
    return cols

def find_min_rows(attacks):
    results = find_all_mins(attacks)
    a = 0
    rows = []
    while a < len(results):
        rows.append(results[a])
        a = a + 2
    return rows

def deal_tie(board, attacks, attack_tracker, queen_list):
    min_attacks = find_min(attacks)
    if min_attacks < attack_tracker:
        indexs = find_all_mins(attacks)
        cols = find_min_cols(attacks)
        col = min(cols)
        col_index = cols.index(col)
        rows = find_min_rows(attacks)
        row = rows[col_index]
        board[queen_list[col]][col] = 0
        board[row][col] = 1
        queen_list[col] = row
    result = find_min(attacks)
    return result

def gradient_search(board):
    continous = 100
    start_attack = count_attack(board)
    queen_list = store_queens(board)
    while continous > 0:
        board_copy = deep_copy(board)
        attack_tracker = count_attack(board)
        attacks = [[0 for a in range(QUEENS)] for b in range(QUEENS)]
        for i in range(QUEENS):
            attacks[queen_list[i]][i] = count_attack(board)
            board_copy[queen_list[i]][i] = 0
            for j in range(QUEENS):
                if j != queen_list[i]:
                    board_copy[j][i] = 1
                    attacks[j][i] = count_attack(board_copy)
                    board_copy[j][i] = 0
            board_copy[queen_list[i]][i] = 1
        start_attack = deal_tie(board, attacks, attack_tracker, queen_list)
        continous = attack_tracker - start_attack
    if start_attack == 0:
        return True
    else:
        return False


