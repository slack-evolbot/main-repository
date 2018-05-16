import pygame
import sys
from pygame.locals import *

WDTH = 50  # width of tile
TNUM = 6   # number of tiles

SCR_W = WDTH * TNUM
SCR_H = WDTH * TNUM
WPOS = WDTH*(TNUM-1)

komacolor = [[0 for x in range(TNUM)] for x in range(TNUM)]
    
def main():
    pygame.init()
    screen = pygame.display.set_mode( (SCR_W, SCR_H) )
    screen.fill((0,0,0))
    pygame.display.set_caption('Mini Othello')

    image1 = pygame.image.load('tile.jpg')
    image2 = pygame.image.load('black.jpg')
    image3 = pygame.image.load('white.jpg')
    image1 = image1.convert()
    image2 = image2.convert()
    image3 = image3.convert()
    ckey2 = image2.get_at((0,0))
    ckey3 = image3.get_at((0,0))
    image2.set_colorkey(ckey2)
    image3.set_colorkey(ckey3)
    imagerect1 = image1.get_rect()
    imagerect2 = image2.get_rect()
    imagerect3 = image3.get_rect()

    pygame.mouse.set_visible(True)
    whoturn = 0

    """ showing background tiles """
    for i in xrange(0, WPOS+1, WDTH):
        for j in xrange(0, WPOS+1, WDTH):
            screen.blit(image1, imagerect1.move(i,j))
    screen.blit(image2, imagerect2.move(WDTH*TNUM/2,WDTH*TNUM/2))
    screen.blit(image2, imagerect2.move(WDTH*(TNUM/2-1),WDTH*(TNUM/2-1)))
    screen.blit(image3, imagerect3.move(WDTH*(TNUM/2-1),WDTH*TNUM/2))
    screen.blit(image3, imagerect3.move(WDTH*TNUM/2,WDTH*(TNUM/2-1)))
    komacolor[TNUM/2][TNUM/2] = 1
    komacolor[TNUM/2-1][TNUM/2-1] = 1
    komacolor[TNUM/2-1][TNUM/2] = 2
    komacolor[TNUM/2][TNUM/2-1] = 2
    pygame.display.flip()

    while 1:

        for event in pygame.event.get():
            if (event.type == KEYDOWN and
                event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                whoturn += 1
                xpos = int(pygame.mouse.get_pos()[0]/WDTH)
                ypos = int(pygame.mouse.get_pos()[1]/WDTH)
                if komacolor[xpos][ypos] == 0:
                    if whoturn%2 == 0:
                        screen.blit(image2, imagerect2.move(WDTH*xpos,WDTH*ypos))
                        komacolor[xpos][ypos] = 1
                        if ypos-2 >= 0:
                            for i in range(ypos-2, 0, -1):
                                if komacolor[xpos][i] == komacolor[xpos][ypos]:
                                    screen.blit(image2,
                                                imagerect2.move(WDTH*xpos,WDTH*(i+1)))
                    else:
                        screen.blit(image3, imagerect3.move(WDTH*xpos,WDTH*ypos))
                        komacolor[xpos][ypos] = 2
                        if ypos-2 >= 0:
                            for i in range(ypos-2, 0, -1):
                                if komacolor[xpos][i] == komacolor[xpos][ypos]:
                                    screen.blit(image3,
                                                imagerect3.move(WDTH*xpos,WDTH*(i+1)))
                        
                pygame.display.flip()

if __name__ == '__main__':
    main()
