import pygame

# general setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption('Tong777')
running = True

while running:
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # draw the game
    background = "/Users/kung/Intro to programming_Python/Fay_Python/Module 5/Tong777_V2/images/tong777_pic.png"
    screen.fill('white')
    pygame.display.update()

pygame.quit()
