from collections import deque

class Maze:
    def __init__(self):
        self.grid = []
        self.width = 0
        self.height = 0
        self.removed_walls = 0
        

    def check_and_update(self, x, y, queue):
        if 0 <= x < self.width and 0 <= y < self.height and self.grid[y][x] == 0:
            self.grid[y][x] = -1
            queue.append((x, y))

    def apply_flood_fill(self, start_x, start_y):
        process_queue = deque([(start_x, start_y)])
        self.check_and_update(start_x, start_y, process_queue)

        while process_queue:
            x, y = process_queue.popleft()
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                self.check_and_update(x + dx, y + dy, process_queue)

            next_y = y + 1
            if self.grid[next_y][x] == 1:
                self.check_and_update(x - 1, next_y, process_queue)
            elif self.grid[next_y][x] == 2:
                self.check_and_update(x + 1, next_y, process_queue)

            prev_y = y - 1
            if self.grid[prev_y][x] == 1:
                self.check_and_update(x + 1, prev_y, process_queue)
            elif self.grid[prev_y][x] == 2:
                self.check_and_update(x - 1, prev_y, process_queue)

    def process_edges(self):
        for y in range(self.height):
            self.check_and_update(0, y, deque())
            self.check_and_update(self.width - 1, y, deque())

        for x in range(self.width):
            self.check_and_update(x, 0, deque())
            self.check_and_update(x, self.height - 1, deque())

    def is_closed(self, x, y):
        if x + 1 < self.width and y + 1 < self.height:
            return (self.grid[y][x] == 1 and self.grid[y][x+1] == 2 and self.grid[y+1][x] == 2 and self.grid[y+1][x+1] == 1)
        return False

    def find_regions(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == 0:
                    self.apply_flood_fill(x, y)
                    self.removed_walls += 1
                elif self.is_closed(x, y):
                    self.removed_walls += 1

def convert_to_int(char):
    return {'.' : 0, '/' : 1, '\\': 2}.get(char, 2)

def process_maze():
    maze = Maze()
    maze.height, maze.width = map(int, input().split())
    maze.grid = [[-1] * (maze.width + 2)]
    for _ in range(maze.height):
        row_input = input()
        row = [-1] + [convert_to_int(char) for char in row_input] + [-1]
        maze.grid.append(row)
    maze.grid.append([-1] * (maze.width + 2))

    maze.width += 2
    maze.height += 2

    return maze

def main():
    maze = process_maze()
    maze.process_edges()
    maze.find_regions()

    print(maze.removed_walls)

main()
