def matrix2tuples(x): return tuple(tuple(row) for row in x)

def tuples2matrix(x): return [list(row) for row in x]


def steps(board, trail, history):
    result, posx, posy = [], 0, 0
    for idx, line in enumerate(board):
        if line.count(0) == 1:
            posx = line.index(0)
            posy = idx
            break
    n = len(board)
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    weight = check_board(board)

    for direction in directions:
        buf = tuples2matrix(board)
        x = posx + direction[0]
        y = posy + direction[1]
        if 0 <= x < n and 0 <= y < n:
            next_step = buf[y][x]
            buf[posy][posx], buf[y][x] = buf[y][x], buf[posy][posx]
            new_board = matrix2tuples(buf)
            if (not (new_board in history)) and ( check_board(new_board) >= weight):
                result.append((check_board(new_board),new_board, trail+[next_step]))
            history.add(new_board)
        #print(new_board)
    #print(result)
    return result



def check_board(board):
    n = len(board)
    temp = [[(j*4)+i+1 for i in range(n)]for j in range(n)]
    temp[n-1][n-1]=0
    temp = matrix2tuples(temp)
    if board == temp:
        return (-1,-1,-1)

    fixed_rows =0
    fixed_cols =0
    fixed_nums =0
    for i in range(n-2):
    if temp[i] == board[i]:
        fixed_rows = i + 1
    else:
        break
    for x in range(n-2):
    if tuple(board[y][x] for y in range(n)) == tuple(temp[y][x] for y in range(n)):
        fixed_cols = x + 1
    else:
        break
    fixed_cols = fixed_rows if fixed_cols > fixed_rows else fixed_cols
    fixed_rows = fixed_cols+1 if fixed_rows > fixed_cols + 1 else fixed_rows

    if fixed_rows == fixed_cols:
        for x in range(n-2):
            if board[fixed_rows][x] == temp[fixed_rows][x]:
            fixed_nums = x + 1
        else:
            break
    else:
        for y in range(n-2):
            if board[y][fixed_cols] != temp[y][fixed_cols]:
                fixed_nums = y
    return (fixed_rows,fixed_cols,fixed_nums)

def slide_puzzle(ar):
    board = matrix2tuples(ar)
    history = set()
    queue = [(check_board(board),board,[])]
    n = len(board)
    if check_board(board) == (-1,-1,-1):
    return []
    while queue:
        w,board,trail = queue.pop()
        new_steps = steps(board, trail, history)
        for w, board,trail in new_steps:
        if check_board(board) == (-1,-1,-1):
        return trail
        queue.insert(0,(w,board,trail))
        #print('que length =',len(que
