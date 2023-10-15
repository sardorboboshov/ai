from ast import List
from collections import deque


class Solution:
    def shortestPathBinaryMatrix(self, grid: List[List[int]]) -> int:
        n = len(grid)
        
        def generate_child(x, y, visited):
            children = []
            for i, j in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                child_x, child_y = i + x, j + y
                if (child_x, child_y) in visited:
                    continue
                if 0 <= child_x < n and 0 <= child_y < n:
                    if grid[child_x][child_y] == 0:
                        children.append((child_x, child_y))
            return children
        
        def bfs_one_step(queue, visited, op_visited):
            x, y, step = queue.popleft()
            if (x, y) in op_visited:
                return step + op_visited[(x, y)] - 1
                
            if (x, y) not in visited:
                visited[(x, y)] = step
                children = generate_child(x, y, visited)
                for new_x, new_y in children:
                    queue.append((new_x, new_y, step + 1))
            return -1
        
        if grid[0][0] == 1 or grid[-1][-1] == 1:
            return -1
        
        if n == 1: return 1
        
        f_queue = deque([(0, 0, 1)])
        b_queue = deque([(n-1, n-1, 1)])
        b_visited = {}
        f_visited = {}
        parity = 0
        res = -1
        while(f_queue and b_queue and res == -1): # no result will be found if one of the path is being cut
            if parity == 0:
                # forward
                res = bfs_one_step(f_queue, f_visited, b_visited)
            else:
                # backward
                res = bfs_one_step(b_queue, b_visited, f_visited)
                
            parity = 1 - parity
            
        return res
