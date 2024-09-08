import pygame
import heapq
import copy
import time
import sys

#priority_queue that holds board states and their priority
priority_queue = []

#original board state
test_board = [1,2,3,-1,4,6,7,5,8]
test_board2 = [4,1,3,-1,2,6,7,5,8]
test_board3 = [1,8,2,-1,4,3,7,6,5]
test_board4 = [7,2,4,5,-1,6,8,3,1]
test_board5 = [8,6,7,2,5,4,3,-1,1]

squares = test_board5
#chooses board based on command line arguement
if len(sys.argv)>1:
    if sys.argv[1] == "3":
        squares = test_board
    elif sys.argv[1] == "5":
        squares = test_board2
    elif sys.argv[1] == "9":
        squares = test_board3
    elif sys.argv[1] == "20":
        squares = test_board4
    elif sys.argv[1] == "31":
        pass
    

#goal state
goal_board = [1,2,3,4,5,6,7,8,-1]

#depth of the search tree
depth = 0

#keeps track of visited boards so they are not revisited
visited = []

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
    return total

#determines the best move to be made by using A* 
def choose_best_move(adjacent_squares):
    global depth
    global squares
    #priority queue to determine the best move to be made
    for square in adjacent_squares:
        calculate_total_manhattan_distance(square)      
    smallest = heapq.heappop(priority_queue)
    _ , best_board, current_depth = smallest
    while best_board in visited:
        smallest = heapq.heappop(priority_queue)
        _ , best_board, current_depth = smallest
    depth = current_depth
    visited.append(best_board)
    squares = copy.deepcopy(best_board)
    
move = 0
def main():
    global move
    global depth
    #set up the graphical interface
    pygame.init()
    screen = pygame.display.set_mode((1500,900))
    text = pygame.font.Font(None,100)
    pygame.display.set_caption("Puzzle Project")
    running = True
    make_move = True
    #loop that continues running until the goal state is achieved
    while running:
        if make_move:
            depth+=1
            move += 1
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
        font = pygame.font.Font(None, 70)
        text1 = font.render(f"Number of moves: {move}", True, (0, 0, 0))
        text2 = font.render(f"Depth of solution: {depth}", True, (0, 0, 0))
        text1_rect = text1.get_rect(center=(1200, 350))
        text2_rect = text2.get_rect(center=(1200, 450))
        screen.blit(text1, text1_rect)
        screen.blit(text2, text2_rect)
        pygame.display.flip()
        if len(sys.argv) > 2 and sys.argv[2] == "slow":
            time.sleep(1)
        if make_move:
            choose_best_move(adjacent_squares)
        if squares == goal_board:
            make_move = False

if __name__ == '__main__': 
    main()
