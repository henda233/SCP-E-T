#载入pygame
import pygame
from pygame.locals import *
import sys
import crtplayer
import os
import mapset
import time
from random import randint
import backage
from threading import Thread

#窗口数据
Scr_W=1200
Scr_L=810
Game_Size=32

#初始化
pygame.init()
Scr=pygame.display.set_mode((Scr_W,Scr_L))
#混音初始化
pygame.mixer.init()
#数据载入
BackGround=pygame.image.load("img/background.jpg")
BackGround=pygame.transform.scale(BackGround,(Scr_W,Scr_L))
Wall=pygame.image.load("img/wall.jpg")
PlayerImg=pygame.image.load("img/man.jpg")
DoorImg=pygame.image.load("img/door.jpg")
ModeDoorImg=pygame.image.load("img/modedoor.JPG")
#图片处理
Wall=pygame.transform.scale(Wall,(Game_Size,Game_Size))
PlayerImg=pygame.transform.scale(PlayerImg,(Game_Size,Game_Size))
DoorImg=pygame.transform.scale(DoorImg,(Game_Size,Game_Size))
ModeDoorImg=pygame.transform.scale(ModeDoorImg,(Game_Size,Game_Size))

print("图片载入完成")
#设置字体
MainFont=pygame.font.SysFont('SimHei',40)
ButtonFont=pygame.font.SysFont('SimHei',24)
NormalFont=pygame.font.SysFont('SimHei',24)

#设置颜色
Wcolor=(255,255,255)
Black=(0,0,0)
Red=(255,0,0)
#玩家数据
Name=""
HP=100
Power=0
Speed=0
LV=1
XP=0
SV=0
Item=[]
PlayerX=0
PlayerY=0
Dir=0
Times=0
#玩家目录相关
SaveFilePath="data/save/"
#地图数据
MapY=0
MapX=0
Map=[]
MapName=""
MapCode=""
UpMap=""
NextMap=""
MapMode=""
Door1XY=[0,0]
Door2XY=[0,0]
ModeDoorXY=[0,0]



#50%的随机
def HalfC():
    R=randint(1,2)
    return R

#获得玩家的坐标
def GetPlayerXY(Mode=0):
    global PlayerX
    global PlayerY
    global Dir
    global Scr
    #模式0 first 1 loop
    if Mode==0:
        Dir = HalfC()
    elif Mode==1:
        pass
    #检测CODE并设置玩家坐标
    if "F-1" in MapCode:
        if Dir==1:
            PlayerX=Door2XY[0]
            PlayerY=Door2XY[1]-1
        else:
            PlayerX=Door1XY[0]
            PlayerY=Door1XY[1]+1
    elif "F-2" in MapCode:
        if Dir == 1:
            PlayerX = Door2XY[0]
            PlayerY = Door2XY[1] -1
        else:
            PlayerX = Door1XY[0]-1
            PlayerY = Door1XY[1]
    elif "F-3" in MapCode:
        if Dir == 1:
            PlayerX = Door2XY[0]
            PlayerY = Door2XY[1] -1
        else:
            PlayerX = Door1XY[0]+1
            PlayerY = Door1XY[1]



#载入地图模型
def PrintMap(Mode):#mode 0 first 1 move to new map 2 loop
    global MapY
    global MapX
    global Map
    global Door1XY
    global Door2XY
    global ModeDoorXY
    global Scr
    #读取地图设定
    File=open("data/mapdata/"+MapCode+"/"+MapCode+"-S.txt","r")
    MapSet=File.readlines()
    MapX=int(MapSet[0].replace("\n",""))
    MapY=int(MapSet[1].replace("\n",""))
    #读取地图文件
    File=open("data/mapdata/"+MapCode+"/"+MapCode+"-M.txt","r")
    Map=File.readlines()
    File=open("data/mapdata/"+MapCode+"/"+MapCode+"-D.txt","r")
    Doors=File.readlines()
    Door1XY[0]=int(Doors[0].replace("\n",""))
    Door1XY[1]=int(Doors[1].replace("\n",""))
    Door2XY[0]=int(Doors[2].replace("\n",""))
    Door2XY[1]=int(Doors[3].replace("\n",""))
    ModeDoorXY[0]=int(Doors[4].replace("\n",""))
    ModeDoorXY[1]=int(Doors[5].replace("\n",""))
    #打印地图到屏幕
    Scr.fill(Black)
    for i_y in range(MapY+1):
        for j_x in range(MapX+1):
            pos=[i_y*32,j_x*32]
            if Map[i_y][j_x]=="W":
                Scr.blit(Wall,(pos[1],pos[0]))
            if Map[i_y][j_x]=="D":
                Scr.blit(DoorImg, (pos[1], pos[0]))
            if Map[i_y][j_x]=="M":
                Scr.blit(ModeDoorImg, (pos[1], pos[0]))
    #获得玩家坐标
    if Mode==0:#Fisrt
        GetPlayerXY(Mode)
        # 打印玩家
        Scr.blit(PlayerImg, (PlayerX * Game_Size, PlayerY * Game_Size))

    elif Mode==1:#to new map
        GetPlayerXY(Mode)
        # 打印玩家
        Scr.blit(PlayerImg, (PlayerX * Game_Size, PlayerY * Game_Size))

    elif Mode==2:#walk
        # 打印玩家
        Scr.blit(PlayerImg, (PlayerX * Game_Size, PlayerY * Game_Size))
    #显示玩家信息
    HPText=ButtonFont.render("HP:"+str(HP),True,Wcolor)
    TimesText=ButtonFont.render("生存回合数:"+str(Times),True,Wcolor)
    PosText=ButtonFont.render("位置:"+MapName,True,Wcolor)
    Scr.blit(HPText,(Scr_W-250,0))
    Scr.blit(TimesText,(Scr_W-250,50))
    Scr.blit(PosText, (Scr_W - 250, 100))
    pygame.display.update()




#载入地图数据
def LoadMap(Maps,Mode):
    global UpMap
    global NextMap
    global MapName
    global MapCode
    global MapMode
    global Data
    global Scr
    #分开模式：0--》第一次 1-->循环
    if Mode==0:
        #随机选择地图
        N=len(Maps)-1
        C=randint(0,N)
        Data=Maps[C]
    elif Mode==1:
        Data=Maps
    #分割Data
    Data_2=str(Data).split("#")
    UpMap=Data_2[0].replace("\n","")
    NextMap=Data_2[2].replace("\n","")
    Data_3=Data_2[1].split(".")
    MapName=Data_3[0].replace("\n","")
    MapMode=Data_3[1].replace("\n","")
    Data_4=Data_3[0].split("%")
    MapCode=Data_4[0].replace("\n","")
    print("地图数据载入成功。")


def Start():
    global Scr
    Scr.fill(Black)
    LoadText=ButtonFont.render("载入中...",True,Wcolor)
    Scr.blit(LoadText,(Scr_L/2,Scr_W/2))
    pygame.display.update()
    #生成地图
    Maps=mapset.Main_MapSet(Name)
    #载入地图
    LoadMap(Maps,0)
    #载入地图模型
    PrintMap(0)
    #载入玩家操控
    PlayerContral()

def Door(Number):
    global Scr
    global Dir
    #提示载入
    Scr.fill(Black)
    LoadText=ButtonFont.render("载入新地图中...",True,Wcolor)
    Scr.blit(LoadText,(Scr_W/2,Scr_L/2))
    #判断门并且设置方向
    Maps=""
    if Number==1:
        Dir=1
        Maps=NextMap
    elif Number==2:
        Dir=2
        Maps=UpMap
    #更换地图并且读取新地图
    #到目录寻找对应的地图数据
    File=open("data/save/"+Name+"/maps/"+Maps+".ini","r")
    Data=File.read()
    LoadMap(Data,1)
    PrintMap(1)



#玩家操作

#移动检测：墙 门 mode 门
def CheckMove(DAimX,DAimY):
    global PlayerY
    global PlayerX
    global AimX
    global AimY
    global Scr
   #获得目标坐标的地图数
    Ojb=Map[DAimY][DAimX]
    AimX=DAimX
    AimY=DAimY
    if Ojb=="W":
        PrintMap(2)
    if Ojb=="N":
        PlayerX = AimX
        PlayerY = AimY
        PrintMap(2)
    if Ojb=="D":
        if AimX==Door1XY[0] and AimY==Door1XY[1]:
            Door(1)
        elif AimX==Door2XY[0] and AimY==Door2XY[1]:
            Door(2)


#人物移动
def PlayerMove(Dir):
    global PlayerY
    global PlayerX
    global Scr
    global Times
    if Dir=="UP":
        AimX=PlayerX
        AimY=PlayerY-1
        CheckMove(AimX,AimY)
    elif Dir=="DOWN":
        AimX=PlayerX
        AimY=PlayerY+1
        CheckMove(AimX,AimY)
    elif Dir=="RIGHT":
        AimX=PlayerX+1
        AimY=PlayerY
        CheckMove(AimX,AimY)
    elif Dir=="LEFT":
        AimX=PlayerX-1
        AimY=PlayerY
        CheckMove(AimX,AimY)
    Times+=1

def PlayerBackage():
    pass


def InGameMain():
    #显示文字
    BackGameText=ButtonFont.render("[1]返回游戏",True,Wcolor)
    ExitGameText=ButtonFont.render("[2]退出游戏(目前不支持保存)",True,Wcolor)
    #to scr
    Scr.blit(BackGameText,(950,600))
    Scr.blit(ExitGameText,(850,650))
    pygame.display.update()
    while 1:
        for event in pygame.event.get():
            if event.type==KEYDOWN:
                if event.key==K_1:
                    PrintMap(2)
                    return
                if event.key==K_2:
                    sys.exit()

#操作主函数
def PlayerContral():
    global Scr
    InGame=True
    while InGame:
        for event in pygame.event.get():
            if event.type==KEYDOWN:
                if event.key==K_UP:
                    PlayerMove("UP")
                if event.key==K_DOWN:
                    PlayerMove("DOWN")
                if event.key==K_RIGHT:
                    PlayerMove("RIGHT")
                if event.key==K_LEFT:
                    PlayerMove("LEFT")
                if event.key==K_TAB:
                    PlayerBackage()
                if event.key==K_ESCAPE:
                    InGameMain()


        pygame.display.update()



def LoadPlayerData(Number,FileList):
    global Name
    global Power
    global Speed
    global LV
    global XP
    global SV
    global Item
    global Scr
    Name=FileList[Number]
    File=open(SaveFilePath+Name+"/player.dat","r")
    #处理普通数据
    Data=File.readlines()
    print(Data)
    LV=int(Data[1].strip("\n"))
    XP=int(Data[3].strip("\n"))
    SV=int(Data[4].strip("\n"))
    Power=int(Data[6].strip("\n"))
    Speed=int(Data[8].strip("\n"))
    #读取物品
    File=open(SaveFilePath+Name+"/item.dat","r")
    Item=File.readlines()
    print("数据读取完毕。")
    Start()



def LoadGame():
    global Scr
    #搜索玩家目录
    FileList=os.listdir("data\save")
    #判断是否存在玩家
    print("23333")
    if len(FileList)==0:
        ErrorText=ButtonFont.render("没有找到玩家存档！请按 1 创建新存档.",True,Wcolor)
        Scr.blit(ErrorText,(200,200))
        pygame.display.update()
    else:
        #读取玩家存档
        for i in range(len(FileList)):
            Text=ButtonFont.render("读取到玩家存档：",True,Wcolor)
            Scr.blit(Text,(0,230))
            LoadText=ButtonFont.render("["+str(i)+"]"+FileList[i],True,Wcolor)
            Scr.blit(LoadText,(i*100,i*100+250))
        pygame.display.update()
        while 1:
            for event in pygame.event.get():
                if event.type==KEYDOWN:
                    if event.key==K_0:
                        LoadPlayerData(0,FileList)
                    if event.key==K_1:
                        LoadPlayerData(1,FileList)
            pygame.display.update()



def StartGame():
    global Scr
    #创建角色
    print("start game")
    StartText = ButtonFont.render("请查看控制台", True, Wcolor)
    Scr.blit(StartText, (0, 170))
    pygame.display.update()
    crtplayer.Main_CrtPlayer()
    Start()



def PlayMusic():
    global Scr
    #读取音乐列表
    MusicFilePath="data/music/"
    MusicNameList=os.listdir(MusicFilePath)
    #初始化
    pygame.mixer.init()
    pygame.mixer_music.set_volume(0.2)
    #随机选择&loop播放
    while 1:
        N=randint(0,len(MusicNameList)-1)
        pygame.mixer_music.load(MusicFilePath+MusicNameList[N])
        pygame.mixer_music.play(start=0.0)
        time.sleep(300)
        pygame.mixer_music.stop()





def GameMain():
    global Scr
    global i
    # 载入背景
    Scr.blit(BackGround, (0, 0))
    #载入新闻
    File=open("text_data/news.txt","r")
    Data=File.readlines()
    i=0
    N=len(Data)-1
    while i<=N:
        NewsText=NormalFont.render(Data[i].strip(),True,Wcolor)
        Scr.blit(NewsText,(500,i*50+50))
        i+=1
    #载入文字
    GameNameText=MainFont.render("SCP-E-T 0.6B",True,Wcolor)
    StartText=ButtonFont.render("Start[1]",True,Wcolor)
    LoadText=ButtonFont.render("Load Game[2]",True,Wcolor)
    ExitText=ButtonFont.render("Exit Game[3]",True,Wcolor)
    Scr.blit(LoadText,(0,200))
    Scr.blit(GameNameText,(0,90))
    Scr.blit(StartText,(0,150))
    Scr.blit(ExitText,(0,350))
    #载入音乐
    Th=Thread(target=PlayMusic)
    Th.start()
    pygame.display.update()


def main():
    global Scr
    #主界面
    pygame.display.set_caption("SCP-E-T 0.6B")
    #载入菜单
    GameMain()
    #loop
    Running=True
    while Running:
        for Event in pygame.event.get():
            if Event.type==QUIT:
                sys.exit()
            if Event.type==KEYDOWN:
                if Event.key==K_1:
                    StartGame()
                if Event.key==K_2:
                    print("载入Game")
                    LoadGame()
                if Event.key==K_3:
                    print("exit")
                    sys.exit()
        pygame.display.update()


main()

