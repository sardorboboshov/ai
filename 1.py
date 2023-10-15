from collections import defaultdict, deque
ID = 'U2010050'
size = int(ID[-2:]) % 8 + 7
print("=====================")
print("My student ID is", ID)
print(f"My chessboard size is [{ID[-2:]} mod 8 + 7] => {size}x{size}", )
print("=====================")
start = input("Enter the initial position (e.g., 'a1' to 'i9'): ")
end = input("Enter the final position (e.g., 'a1' to 'i9'): ")

def isValid(pos):
    row,col = pos[-1:], pos[0]
    if not('0' <= row <= '99' and 'a' <= col <= 'n'):
        return (False,'','')
    row, col = int(row) - 1, ord(col) - ord('a')
    return (0<=row<size and 0<=col<size, row, col)
valid = False
while not valid:
    validStart, row_s, col_s = isValid(start)
    validEnd, row_e, col_e = isValid(end)
    valid = validStart and validEnd
    if valid: 
        break
    print("invalid values, please try valid values again...")
    start = input("Enter the initial position (e.g., 'a1' to 'i9'): ")
    end = input("Enter the final position (e.g., 'a1' to 'i9'): ")

directions = ((-2,-1), (-2,1), (-1,-2), (-1,2), (1,-2), (1,2), (2,-1), (2,1))


def isValidPos(visited,y,x,size):
    return 0<=y<size and 0<=x<size and (y,x) not in visited

def bfs(qs, vs, parents, size, toggle):
    opp = 1^toggle
    (y,x,step,yp,xp) = qs[toggle].popleft()
    if (y,x) in vs[opp]:
        if toggle == 1:
          parents[(y,x)].append((yp,xp))
        else:
          parents[(y,x)] = [(yp,xp)] + parents[(y,x)]
        return (vs[opp][(y,x)] + step - 1, y, x, step-1)

    if (y,x) not in vs[toggle]:   
        vs[toggle][(y,x)] = step
        parents[(y,x)].append((yp, xp))
        for dy,dx in directions:
            newy, newx = y+dy, x+dx
            if isValidPos(vs[toggle], newy,newx,size):
                qs[toggle].append((newy, newx, step+1, y, x))
    return -1,-1,-1,-1
# FUNCTION
def bi_directional_search(row_s,col_s,row_e,col_e, size):
    vs = [defaultdict(int), defaultdict(int)]
    parents = defaultdict(list)
    parents_f = defaultdict(list)
    toggle = 1
    ans = -1
    qs = [deque(), deque()]
    qs[0].append((row_s, col_s, 1, row_s, col_s))
    qs[1].append((row_e, col_e, 1, row_e, col_e))
    midy = midx = midstep = 0
    while qs[0] and qs[1] and ans == -1:
        ans, midy, midx, midstep = bfs(qs, vs, parents, size, toggle)
        if toggle: midstep = ans - midstep
        toggle = 1^toggle
    return ans, midy, midx, midstep, parents, vs

ans, midy, midx, midstep, parents, vs = bi_directional_search(row_s, col_s, row_e, col_e, size)
def drawPath(midy, midx, parents,size, midstep):
    p1, p2 = parents[(midy, midx)]
    matrix = [['.' for i in range(size+1)] for j in range(size+1)]
    print(midy, midx,midstep)
    for i in range(1,size+1):
        matrix[0][i] = chr(ord('a') + i - 1)
        matrix[i][0] = i
    matrix[midy+1][midx+1] = midstep
    q = deque()
    q.append((p1[0], p1[1] ,midstep-1))
    while q:
        y,x,step = q.popleft()
        if matrix[y+1][x+1] == '.':
            matrix[y+1][x+1] = step
        ny,nx = parents[(y,x)][0]
        if ny == y and nx == x: break
        q.append((ny,nx,step-1))
    q = deque()
    q.append((p2[0], p2[1] ,midstep+1))
    while q:
        y,x,step = q.popleft()
        if matrix[y+1][x+1] == '.':
            matrix[y+1][x+1] = step
        matrix[y+1][x+1] = step
        ny,nx = parents[(y,x)][0]
        if ny == y and nx == x: break
        q.append((ny,nx,step+1))
    return matrix
print(ans)
if ans == -1:
    print('there is no way knight can move to final position')
else:
    matrix = drawPath(midy, midx, parents, size, midstep)
    matrix[0][0] = ' '
    for i in range(size+1):
      print("  ".join([str(j) for j in matrix[i]]))
