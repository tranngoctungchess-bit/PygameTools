from Kernel import kernal_Init
import pygame
kernal_Init.init()
"""Wrap some func from pygame to make it shorter"""
screen = pygame.display.set_mode
get_events = pygame.event.get
draw_rect = pygame.draw.rect
draw_circle = pygame.draw.circle
setscreen_caption = pygame.display.set_caption
