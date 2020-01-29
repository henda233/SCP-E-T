import pygame
from pygame.locals import *
import sys

#窗口信息
Scr_W=420
Scr_L=540

#初始化
pygame.init()
#字体
NormalFont=pygame.font.SysFont("SimHei",24)
#颜色
W=255,255,255


def NumberToText():
    pass


def back_main():
    B_Scr = pygame.display.set_mode((Scr_W, Scr_L), NOFRAME)
    #显示文字
    TitleText=NormalFont.render("背包:",True,W)
    B_Scr.blit(TitleText,(0,0))
    pygame.display.update()
    while 1:
        for event in pygame.event.get():
            if event.type==QUIT:
                sys.exit()