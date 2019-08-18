
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
    max_weight = weight

    for direction in directions:
        buf = tuples2matrix(board)
        x = posx + direction[0]
        y = posy + direction[1]
        if 0 <= x < n and 0 <= y < n:
            next_step = buf[y][x]
            buf[posy][posx], buf[y][x] = buf[y][x], buf[posy][posx]
            new_board = matrix2tuples(buf)
            new_board_weight = check_board(new_board)
            if (not (new_board in history)) and (new_board_weight >= weight):
                result.append((new_board_weight,new_board, trail+[next_step]))
                if new_board_weight > weight:
                    max_weight = new_board_weight
                    history.clear()
                    print("A STEP FOWARD!", new_board, new_board_weight , board, weight)
                history.add(new_board)
    return [r for r in result if r[0] == max_weight]



def check_board(board):
    n = len(board)
    temp = [[(j*n)+i+1 for i in range(n)]for j in range(n)]
    temp[n-1][n-1]=0
    temp = matrix2tuples(temp)
    
    if board == temp:
        return (n,n,n,n*2,n)

    fixed_rows =0
    fixed_cols =0
    fixed_nums =0
    dist = n*2
    blank_dist = n
    for i in range(n-2):
        if temp[i] == board[i]:
            fixed_rows = i + 1
        else:
            break            

    for x in range(n-3):
        if tuple(board[y][x] for y in range(n)) == tuple(temp[y][x] for y in range(n)):
            fixed_cols = x + 1
        else:
            break

    fixed_cols = fixed_rows if fixed_cols > fixed_rows else fixed_cols
    fixed_rows = fixed_cols+1 if fixed_rows > fixed_cols + 1 else fixed_rows

    if fixed_rows == fixed_cols:
        for x in range(n-2):
            if board[fixed_rows][x] == temp[fixed_rows][x]:
                fixed_nums = x+1
            else:
                break
    else:
        for y in range(n-2):
            if board[y][fixed_cols] == temp[y][fixed_cols]:
                fixed_nums = y+1
            else:
                break
    if (fixed_rows == n - 2) and (fixed_cols==n-3):
        fixed_nums = 0
        return (fixed_rows,fixed_cols,fixed_nums,dist)

    if (fixed_nums < n -2):
        next_number = temp[fixed_rows][fixed_nums] if fixed_rows == fixed_cols else temp[fixed_nums][fixed_cols]
        pos = [(x,y) for x in range(n) for y in range(n) if board[y][x]==next_number][0]
        pos_blank = [(x,y) for x in range(n) for y in range(n) if board[y][x]==0][0]
        dist = n*2 - max(abs(pos[0]-fixed_nums), abs(pos[1]-fixed_rows)) if fixed_rows == fixed_cols else n*2 - max(abs(pos[0]-fixed_nums), abs(pos[1]-fixed_cols))
        #blank_dist = n- max(abs(pos[0]-pos_blank[0]),abs(pos[1]-pos_blank[1]),2)
        #print(board,fixed_rows,fixed_cols,fixed_nums,dist)
    elif not fixed_rows == n-3 :
        up_corner = (fixed_cols == fixed_rows)
        n1 = temp[fixed_rows][fixed_nums] if up_corner else temp[fixed_nums][fixed_cols]
        n2 = temp[fixed_rows][fixed_nums+1] if up_corner else temp[fixed_nums+1][fixed_cols]
        p1 = [(x,y) for x in range(n) for y in range(n) if board[y][x]==n1][0]
        p2 = [(x,y) for x in range(n) for y in range(n) if board[y][x]==n2][0]
        x0 = fixed_nums + 1 if up_corner else fixed_cols + 1
        y0 = fixed_rows + 1 if up_corner else fixed_nums + 1
        pos_blank = [(x,y) for x in range(n) for y in range(n) if board[y][x]==0][0]
        dist = n*2 -max(abs(p1[0]-x0),abs(p1[1]-y0),1) - max(abs(p2[0]-x0),abs(p2[1]-y0),1)
        if max(abs(p1[0]-x0),abs(p1[1]-y0),1) > 1:
            blank_dist = n - max(abs(p1[0]-pos_blank[0]),abs(p1[1]-pos_blank[1]),1)
        else:
            blank_dist = n - max(abs(p2[0]-pos_blank[0]),abs(p2[1]-pos_blank[1]),2)
        #print(board,fixed_rows,fixed_cols,fixed_nums,dist,(x0,y0),p1,p2)

    #print(fixed_rows,fixed_nums, temp[fixed_rows][fixed_nums],board[fixed_rows][fixed_nums],board)
    #print (fixed_rows,fixed_cols,fixed_nums)
    return (fixed_rows,fixed_cols,fixed_nums,dist,blank_dist)

def slide_puzzle(ar):
    board = matrix2tuples(ar)
    history = set()
    queue = [(check_board(board),board,[])]
    n = len(board)
    if check_board(board) == (n,n,n,2*n,n):
        return []
    max_w = (0,0,0,0)
    while queue:
        w,board,trail = queue.pop()
        if w < max_w:
            continue
        elif w > max_w:
            max_w = w
            history.clear()
        new_steps = steps(board, trail, history)
        for w, board,trail in new_steps:
            if check_board(board) == (n,n,n,n*2,n):
                return trail
            if w == max_w:
                queue.insert(0,(w,board,trail))
            elif w > max_w:
                #max_w = w
                queue.insert(0,(w,board,trail))
                #queue = [(w,board,trail)]
        
        
    # l = list(history)
    # l.sort()
    # for board in l:
    #     print(board)
    return []

if __name__ == "__main__":
    puzzle1 = [
        [4,1,3],
        [2,8,0],
        [7,6,5]]
    # puzzle2 = [
    #     [1, 3, 6, 4],
    #     [ 10, 2, 8, 0],
    #     [ 5,13, 7,15],
    #     [14, 9,12,11]]
    puzzle3 = [
        [ 3, 7,14,15,10],
        [ 1, 0, 5, 9, 4],
        [16, 2,11,12, 8],
        [17, 6,13,18,20],
        [21,22,23,19,24]]
    puzzle2 = [
        [ 1, 2, 3, 4],
        [ 5, 6, 8, 7],
        [ 9,15,11,14],
        [13, 10,12,0]]
    puzzle4 = [
        [ 1, 2, 3, 4],
        [ 5, 6, 7, 8],
        [ 9,10,11,12],
        [13, 15,14,0]]    
    print(check_board(matrix2tuples(puzzle2)))
    #print(check_board(matrix2tuples(puzzle4)))
    #print(matrix2tuples(puzzle2))
    print(slide_puzzle(puzzle3))
