import pygame
import random

all_squares = [1,2,3,4,5,6,7,8]
squares = [-1]
while all_squares:
    choice = random.randint(0,len(all_squares)-1)
    squares.append(all_squares[choice])
    all_squares.remove(all_squares[choice])

def main():
    #set up the graphical interface
    pygame.init()
    screen = pygame.display.set_mode((900,900))
    pygame.display.set_caption("Puzzle Project")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    
        grid_size = 300      
        color = (230, 230, 250)
        screen.fill(color)  
        for i, item in enumerate(squares):
            row = i // 3
            col = i % 3
            x = col * grid_size
            y = row * grid_size
            pygame.draw.rect(screen, (0,0,0), (x, y, grid_size, grid_size), 2)  
            
        pygame.display.flip()
 
    pygame.quit()
  



if __name__ == '__main__': 
    main()
