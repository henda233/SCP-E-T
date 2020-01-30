from os import mkdir
import pygame
from pygame.locals import *
import msvcrt

pygame.init()
Font=pygame.font.SysFont("SimHei",16)
#玩家数据
Name=""
HP=100
LV=1
XP=0
SV=100
Power=0
Speed=1


def SavePlayer():
    #创建玩家目录
    mkdir("data/save/"+Name+"/")
    mkdir('data/save/'+Name+"/maps/")
    File=open("data/save/"+Name+"/army.dat","w+")
    File=open("data/save/"+Name+"/weapon.dat","w+")
    #写入武器
    File.writelines("0\n")
    File.writelines("1\n")
    File.writelines("拳头\n")
    File=open("data/save/"+Name+"/player.dat","w+")

    #写入数据
    File.writelines(Name+"\n")
    File.writelines(str(HP)+"\n")
    File.writelines(str(LV) + "\n")
    File.writelines(str(XP) + "\n")
    File.writelines(str(SV) + "\n")
    File.writelines(str(Power) + "\n")
    File.writelines(str(Speed) + "\n")
    File=open("data/save/"+Name+"/item.dat","w+")
    print("玩家数据保存成功！")


def Main_CrtPlayer():
    global Name
    Name="Player"
    SavePlayer()