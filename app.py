import pygame
import random
import heapq

all_squares = [1,2,3,4,5,6,7,8]
squares = []
while all_squares:
    choice = random.randint(0,len(all_squares)-1)
    squares.append(all_squares[choice])
    all_squares.remove(all_squares[choice])
random_insert = random.randint(0,len(squares))
squares.insert(random_insert,-1)
original = all_squares

goal_board = [1,2,3,4,5,6,7,8,-1]


def calculate_priority():
    return

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
        empty_square = squares.index(-1)
        empty_row = empty_square // 3
        empty_column = empty_square % 3
        adjacent_squares = []
        if empty_row < 2:
            adjacent_squares.append(empty_square-3)
        if empty_row > 0:
            adjacent_squares.append(empty_square+3)
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
    pygame.quit()
  



if __name__ == '__main__': 
    main()
