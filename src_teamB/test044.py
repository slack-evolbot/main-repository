from time import sleep
import pygame.mixer

pygame.mixer.init()
pygame.mixer.music.load("./g_string_quartet.mp3")

pygame.mixer.music.play(-1)

sleep(10)
