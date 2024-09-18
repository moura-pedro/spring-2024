from collections import deque

class Maze:
    def __init__(self):
        self.width = 0
        self.height = 0
        self.grid = []
        self.total_regions = 0

    def check_and_update(self, x, y, queue):
        if self.grid[y][x] == 0:
            self.grid[y][x] = -1
            queue.append((x, y))

    def apply_flood_fill(self, start_x, start_y):
        process_queue = deque([(start_x, start_y)])
        self.grid[start_y][start_x] = -1
        while process_queue:
            x, y = process_queue.popleft()
            self.check_and_update(x + 1, y, process_queue)
            self.check_and_update(x - 1, y, process_queue)
            self.check_and_update(x, y + 1, process_queue)
            self.check_and_update(x, y - 1, process_queue)
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

    def handle_border(self, x, y):
        if self.grid[y][x] == 0:
            self.apply_flood_fill(x, y)

    def process_borders(self):
        for y in range(self.height):
            self.handle_border(1, y)
            self.handle_border(self.width - 2, y)
        for x in range(self.width):
            self.handle_border(x, 1)
            self.handle_border(x, self.height - 2)

    def is_diamond(self, x, y):
        return (self.grid[y][x] == 1 and self.grid[y][x+1] == 2 and
                self.grid[y+1][x] == 2 and self.grid[y+1][x+1] == 1)

    def find_regions(self):
        regions = 0
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == 0:
                    regions += 1
                    self.apply_flood_fill(x, y)
                elif self.is_diamond(x, y):
                    regions += 1
        self.total_regions = regions

def convert_char_to_int(char):
    if char == '.':
        return 0
    elif char == '/':
        return 1
    return 2

# Setup and solve the maze
def main():
    maze = Maze()
    maze.height, maze.width = map(int, input().split())
    maze.grid.append([-1] * (maze.width + 2))
    for _ in range(maze.height):
        row_input = input()
        row = [-1] + [convert_char_to_int(char) for char in row_input] + [-1]
        maze.grid.append(row)
    maze.grid.append([-1] * (maze.width + 2))

    maze.width += 2
    maze.height += 2

    maze.process_borders()
    maze.find_regions()

    print(maze.total_regions)

main()
