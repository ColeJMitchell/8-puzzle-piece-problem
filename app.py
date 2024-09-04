import pygame
import random
import heapq

#list that shrinks after each tile is randomly added to the squares list
all_squares = [1,2,3,4,5,6,7,8]
squares = []

while all_squares:
    choice = random.randint(0,len(all_squares)-1)
    squares.append(all_squares[choice])
    all_squares.remove(all_squares[choice])

random_insert = random.randint(0,len(squares))
squares.insert(random_insert,-1)
original = squares

goal_board = [1,2,3,4,5,6,7,8,-1]

prior_tile = None
#determines the best move to be made by using A* 
def calculate_priority(adjacent_squares):
    global prior_tile
    #priority queue to determine the best move to be made
    priority_queue = []
    for square in adjacent_squares:
        current_index = squares.index(square)
        goal_index = goal_board.index(square)
        original_index = original.index(square)
        h = abs(current_index-goal_index)
        g = abs(current_index-original_index)
        f = g + h
        heapq.heappush(priority_queue,(-f,square))
    smallest = heapq.heappop(priority_queue)
    _ , best = smallest
    if prior_tile is not None and prior_tile == best:
        smallest = heapq.heappop(priority_queue)
        _ , best = smallest
    prior_tile = best
    swap(best)

#swaps the squares
def swap(best):      
    empty_index = squares.index(-1)
    best_index = squares.index(best)
    squares[empty_index] = best
    squares[best_index] = -1



def main():
    #set up the graphical interface
    pygame.init()
    screen = pygame.display.set_mode((900,900))
    text = pygame.font.Font(None,100)
    pygame.display.set_caption("Puzzle Project")
    running = True
    
    #loop that continues running until the goal state is achieved
    while running:
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

        calculate_priority(adjacent_squares)

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
        if squares == goal_board:
            pygame.quit()

    pygame.quit()
  
if __name__ == '__main__': 
    main()
