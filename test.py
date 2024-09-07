import pygame
import random
import heapq
import copy

# Initialize the board
all_squares = [1, 2, 3, 4, 5, 6, 7, 8]
squares = []
visited = set()

while all_squares:
    choice = random.randint(0, len(all_squares) - 1)
    squares.append(all_squares[choice])
    all_squares.remove(all_squares[choice])

random_insert = random.randint(0, len(squares))
squares.insert(random_insert, -1)

goal_board = [1, 2, 3, 4, 5, 6, 7, 8, -1]

def swap(square, board):
    empty_index = board.index(-1)
    best_index = board.index(square)
    board[empty_index] = square
    board[best_index] = -1

def calculate_total_manhattan_distance(board):
    total = 0
    for i, square in enumerate(board):
        if square == -1:
            continue
        correct_row = goal_board.index(square) // 3
        correct_col = goal_board.index(square) % 3
        current_row = i // 3
        current_col = i % 3
        total += abs(current_row - correct_row) + abs(current_col - correct_col)
    return total

def get_adjacent_squares(empty_index, board):
    adjacent_squares = []
    empty_row = empty_index // 3
    empty_col = empty_index % 3
    
    if empty_row > 0:
        adjacent_squares.append(board[empty_index - 3])
    if empty_row < 2:
        adjacent_squares.append(board[empty_index + 3])
    if empty_col > 0:
        adjacent_squares.append(board[empty_index - 1])
    if empty_col < 2:
        adjacent_squares.append(board[empty_index + 1])
    
    return adjacent_squares

def choose_best_square(adjacent_squares):
    priority_queue = []
    
    for square in adjacent_squares:
        temp_board = copy.deepcopy(squares)
        swap(square, temp_board)
        board_tuple = tuple(temp_board)
        if board_tuple in visited:
            continue
        visited.add(board_tuple)
        f = calculate_total_manhattan_distance(temp_board)
        heapq.heappush(priority_queue, (f, square))
    
    if priority_queue:
        _, best = heapq.heappop(priority_queue)
        swap(best, squares)

def main():
    pygame.init()
    screen = pygame.display.set_mode((900, 900))
    text = pygame.font.Font(None, 100)
    pygame.display.set_caption("Puzzle Project")
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        grid_size = 300      
        color = (230, 230, 250)
        screen.fill(color)  

        empty_index = squares.index(-1)
        adjacent_squares = get_adjacent_squares(empty_index, squares)
        choose_best_square(adjacent_squares)

        for i, square in enumerate(squares):
            row = i // 3
            col = i % 3
            x = col * grid_size
            y = row * grid_size
            pygame.draw.rect(screen, (0, 0, 0), (x, y, grid_size, grid_size), 2)  
            if square != -1:
                text_screen = text.render(str(square), True, (0, 0, 0))
                text_rect = text_screen.get_rect(center=(x + grid_size // 2, y + grid_size // 2))
                screen.blit(text_screen, text_rect.topleft)
        
        pygame.display.flip()

        if squares == goal_board:
            pygame.time.wait(1000)  # Wait a moment to show the solved state
            running = False

    pygame.quit()
  
if __name__ == '__main__': 
    main()
