import pygame
import heapq
import copy
import time

#priority_queue that holds board states and their priority
priority_queue = []

#original board state
test_board = [1,2,3,-1,4,6,7,5,8]
test_board2 = [1,8,2,-1,4,3,7,6,5]
test_board3 = [4,1,3,-1,2,6,7,5,8]
test_board4 = [8,6,7,2,5,4,3,-1,1]

squares = test_board4

#goal state
goal_board = [1,2,3,4,5,6,7,8,-1]

#depth of the search tree
depth = 0

#swaps the target square and the empty square
def swap(square, board):      
    empty_index = board.index(-1)
    best_index = board.index(square)
    board[empty_index] = square
    board[best_index] = -1

#calculates how the total manhattan distance will change if one of the adjacent squares is moved into the empty space
def calculate_total_manhattan_distance(square):
    global depth
    #theoretical board where the square is swapped with the empty square
    temp_board = copy.deepcopy(squares)
    swap(square, temp_board)
    total = 0
    #calculating manhattan distance for each square in the temp board and adding them to a total counter that will be returned
    for square in temp_board:
        if square == -1:
            continue
        correct_row = goal_board.index(square) // 3
        correct_col = goal_board.index(square) % 3
        current_row = temp_board.index(square) // 3
        current_col = temp_board.index(square) % 3
        total += (abs(current_row-correct_row) + abs(current_col-correct_col))
    total += depth
    heapq.heappush(priority_queue,(total,temp_board,depth))

#determines the best move to be made by using A* 
def choose_best_move(adjacent_squares):
    global depth
    global squares
    #priority queue to determine the best move to be made
    for square in adjacent_squares:
        calculate_total_manhattan_distance(square)      
    smallest = heapq.heappop(priority_queue)
    _ , best_board, current_depth = smallest
    depth = current_depth
    squares = copy.deepcopy(best_board)
    

def main():
    global depth
    #set up the graphical interface
    pygame.init()
    screen = pygame.display.set_mode((900,900))
    text = pygame.font.Font(None,100)
    pygame.display.set_caption("Puzzle Project")
    running = True
    make_move = True
    #loop that continues running until the goal state is achieved
    while running:
        depth+=1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        grid_size = 300      
        color = (230, 230, 250)
        screen.fill(color)  

        #Finds all of the squares that are adjacent to the empty square (-1)
        empty_square = squares.index(-1)
        empty_row = empty_square // 3
        empty_column = empty_square % 3
        adjacent_squares = []
        if empty_row > 0:
            adjacent_squares.append(squares[empty_square-3])
        if empty_row < 2:
            adjacent_squares.append(squares[empty_square+3])
        if empty_column > 0:
            adjacent_squares.append(squares[empty_square-1])
        if empty_column < 2:
            adjacent_squares.append(squares[empty_square+1])

        #draws the rectangles and places the tile numbers inside of them
        for i, square in enumerate(squares):
            row = i // 3
            col = i % 3
            x = col * grid_size
            y = row * grid_size
            pygame.draw.rect(screen, (0,0,0), (x, y, grid_size, grid_size), 2)  
            if square != -1:
                text_screen = text.render(str(square), True, (0, 0, 0))
                text_rect = text_screen.get_rect(center=(x + grid_size // 2, y + grid_size // 2))
                screen.blit(text_screen, text_rect.topleft)
        pygame.display.flip()
        if make_move:
            choose_best_move(adjacent_squares)
        #time.sleep(.1)
        if squares == goal_board:
            make_move = False
  
if __name__ == '__main__': 
    main()
