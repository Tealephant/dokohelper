import pygame as p
from dokoengine import *
from gui import *

def main():
    screen = p.display.set_mode((WIDTH, HEIGHT), p.RESIZABLE)
    clock = p.time.Clock()

    game = Game()
    gamegui = GameGUI(game, screen)
    
    running = True
    while running:
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False        
            else:
                gamegui.handleEvents(event)
        gamegui.draw()
        clock.tick(MAX_FPS)
        p.display.flip()


if __name__ == "__main__":
    main()
    p.quit()
