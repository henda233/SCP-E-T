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
import skill_man
import setthing
import admin
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
PushCarImg=pygame.image.load("img/pushcar.jpg")
DeadBodyImg=pygame.image.load("img/deadbody.jpg")
FirstAidImg=pygame.image.load("img/aid.jpg")
BuyBoxImg=pygame.image.load("img/buybox.jpg")
#图片处理
Wall=pygame.transform.scale(Wall,(Game_Size,Game_Size))
PlayerImg=pygame.transform.scale(PlayerImg,(Game_Size,Game_Size))
DoorImg=pygame.transform.scale(DoorImg,(Game_Size,Game_Size))
ModeDoorImg=pygame.transform.scale(ModeDoorImg,(Game_Size,Game_Size))
FirstAidImg=pygame.transform.scale(FirstAidImg,(Game_Size,Game_Size))
PushCarImg=pygame.transform.scale(PushCarImg,(Game_Size,Game_Size))
DeadBodyImg=pygame.transform.scale(DeadBodyImg,(Game_Size,Game_Size))
BuyBoxImg=pygame.transform.scale(BuyBoxImg,(Game_Size,Game_Size))
print("图片载入完成")
#设置字体
MainFont=pygame.font.SysFont('SimHei',40)
ButtonFont=pygame.font.SysFont('SimHei',24)
NormalFont=pygame.font.SysFont('SimHei',24)
Font=pygame.font.SysFont("SimHei",16)
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
Food=1000
#装备
ArmyHead=[0,"None"]#防御值 名称
ArmyBody=[0,"None"]
ArmyHand=[0,"None"]
ArmyFoot=[0,"None"]
#武器
Weapon=[0,0,"None"]#0：类型 0近战 1远程 0:伤害  "None"武器名
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
PassedMap=[]
Door1XY=[0,0]
Door2XY=[0,0]
ModeDoorXY=[0,0]
DeadBodys=[[0,0,0],[0,0,0]]
PushCar=[0,0,0]
FisrtAid=[0,0,0]
#        x  y  物品数量
BuyBox=[0,0]



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


def PrintPlayerMes():
    HPText=ButtonFont.render("HP:"+str(HP),True,Wcolor)
    TimesText=ButtonFont.render("生存回合数:"+str(Times),True,Wcolor)
    PosText=ButtonFont.render("位置:"+MapName,True,Wcolor)
    FootText=ButtonFont.render("饥饿度："+str(Food),True,Wcolor)

    Scr.blit(HPText,(Scr_W-300,0))
    Scr.blit(TimesText,(Scr_W-300,50))
    Scr.blit(PosText, (Scr_W - 300, 100))
    Scr.blit(FootText,(Scr_W - 300, 150))

def PrintSetThings():
    #尸体显示
    #判断尸体数量
    BodyNumber=0
    if DeadBodys[1][0]!=0:
        BodyNumber=2
    elif DeadBodys[0][0]!=0:
        BodyNumber=1
    elif DeadBodys[0][0]==0:
        BodyNumber=0
    #尸体存在检测
    if BodyNumber==1:
        Scr.blit(DeadBodyImg,(DeadBodys[0][0]*Game_Size,DeadBodys[0][1]*Game_Size))
    elif BodyNumber==2:
        Scr.blit(DeadBodyImg, (DeadBodys[0][0] * Game_Size, DeadBodys[0][1] * Game_Size))
        Scr.blit(DeadBodyImg, (DeadBodys[1][0] * Game_Size, DeadBodys[1][1] * Game_Size))
    #推车
    if PushCar[0]!=0:
        Scr.blit(PushCarImg,(PushCar[0]*Game_Size,PushCar[1]*Game_Size))
    #医疗
    if FisrtAid[0]!=0:
        Scr.blit(FirstAidImg,(FisrtAid[0]*Game_Size,FisrtAid[1]*Game_Size))
    #贩卖机
    if BuyBox[0]!=0:
        Scr.blit(BuyBoxImg,(BuyBox[0]*Game_Size,BuyBox[1]*Game_Size))





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
    PrintPlayerMes()
    #显示特殊
    PrintSetThings()
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
    global DeadBodys
    global PushCar
    global FisrtAid
    global BuyBox
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
    #特殊物品生成
    DeadBodys,PushCar,FisrtAid,BuyBox=setthing.MainStart_SetThing(MapName,PassedMap)
    print("特殊物品生成中...")
    print(DeadBodys,PushCar,FisrtAid,BuyBox)
    print("地图数据载入成功。")

def TipsShow():
    #读取文件
    File=open("text_data/tips.txt","r")
    Tips=File.readlines()
    File.close()
    #随机选择
    C=randint(0,len(Tips)-1)
    #显示
    Text=Font.render("Tips: "+Tips[C],True,Wcolor)
    Scr.blit(Text,(Scr_W/2-25,Scr_L/2+50))

def Load():
    Scr.fill(Black)
    LoadText = Font.render("载入中...", True, (255, 255, 255))
    Scr.blit(LoadText, (Scr_W/2,Scr_L/2))
    TipsShow()
    pygame.display.update()
    time.sleep(randint(5,15))
    Scr.fill(Black)
    LoadText = Font.render("按 移动键 继续...", True, (255, 255, 255))
    Scr.blit(LoadText, (Scr_W/2,Scr_L/2))
    pygame.display.update()

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
    #载入特殊玩家数据
    InGameLoadPlayerData()
    #确定身份
    skill_man.MainStart_PlayerSkillC(Name,Scr)
    #停止音乐
    pygame.mixer_music.stop()
    #载入载入画面
    Load()
    #载入地图模型
    PrintMap(0)
    #载入玩家操控
    PlayerContral()

#添加到已经经过的地图
def AddPassedMaps(Map):
    global PassedMap
    PassedMap.append(Map)

def Door(Number):
    global Scr
    global Dir
    #添加到已经经过的地图list中
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
    AddPassedMaps(MapName)
    LoadMap(Data,1)
    PrintMap(1)



#获得物品 Kind:1尸体1 2尸体2 3推车 4医疗 5贩卖机 6看搜索物品
def GetThings_FromThing(Kind):
    global Item
    global DeadBodys
    global PushCar
    global FisrtAid
    global BuyBox
    global GetItem
    global i
    # 读取全物品
    File = open("data/items/item.dat", "r")
    AllItemText = File.readlines()
    File.close()
    GetItem=[]
    if Kind==1:
        #读取文件
        File=open("data/items/get_item/deadbody/item.txt","r")
        DeadBodyItems=File.readlines()
        File.close()
        while DeadBodys[0][2]>0:
            #随机获得物品
            C=randint(0,len(DeadBodyItems)-1)
            GetItem.append(DeadBodyItems[C].strip())
            DeadBodys[0][2]-=1
    elif Kind==2:
        #读取文件
        File=open("data/items/get_item/deadbody/item.txt","r")
        DeadBodyItems=File.readlines()
        File.close()
        while DeadBodys[1][2]>0:
            #随机获得物品
            C=randint(0,len(DeadBodyItems)-1)
            GetItem.append(DeadBodyItems[C].strip())
            DeadBodys[1][2]-=1
    elif Kind==3:
        #读取文件
        File=open("data/items/get_item/pushcar/item.txt","r")
        PushCarItems=File.readlines()
        File.close()
        while PushCar[2]>0:
            #随机获得物品
            C=randint(0,len(PushCarItems)-1)
            GetItem.append(PushCarItems[C].strip())
            PushCar[2]-=1
    elif Kind==4:
        #读取文件
        File=open("data/items/get_item/aid/item.txt","r")
        FisrtAidItems=File.readlines()
        File.close()
        while FisrtAid[2]>0:
            #随机获得物品
            C=randint(0,len(FisrtAidItems)-1)
            GetItem.append(FisrtAidItems[C].strip())
            FisrtAid[2]-=1
    elif Kind==5:
        #读取文件
        File=open("data/items/get_item/buybox/item.txt","r")
        BuyBoxItems=File.readlines()
        File.close()
        while FisrtAid[2]>0:
            #随机获得物品
            C=randint(0,len(BuyBoxItems)-1)
            GetItem.append(BuyBoxItems[C].strip())
            BuyBox[2]-=1
    print("搜索不到更多的东西了。")
    #GetItem int AllItem str
    #添加到玩家背包
    for j in GetItem:
        Item.append(int(j.strip()))
    File = open("data/save/" + Name + "/item.dat", "w")
    for i in range(len(Item)-1):
        File.writelines(str(Item[i]).strip())
    File.close()
    #数字转为文字
    TextItem=[]
    for Number in GetItem:
        TextItem.append(AllItemText[int(Number)].strip())
    #显示
    pygame.draw.rect(Scr,(0,0,0),((400,300),(400,300)))
    TextX=432
    TextY=332
    for i in range(len(TextItem)):
        Text=NormalFont.render("你找到了："+TextItem[i],True,Wcolor)
        Scr.blit(Text,(TextX,TextY+i*64))
    if len(GetItem)==0:
        Text=NormalFont.render("你什么也没有找到。",True,Wcolor)
        Scr.blit(Text,(TextX,TextY))
    pygame.display.update()


#玩家操作


def EDone(EDir):
    #获得目标坐标
    global EAimX
    global EAimY
    EAimX=0
    EAimY=0
    if EDir=="UP":
        EAimY=PlayerY-1
        EAimX=PlayerX
    elif EDir=="DOWN":
        EAimY=PlayerY+1
        EAimX=PlayerX
    elif EDir=="LEFT":
        EAimY=PlayerY
        EAimX=PlayerX-1
    else:
        EAimY=PlayerY
        EAimX=PlayerX+1
    #特殊物品检测
    if EAimX==DeadBodys[0][0] and EAimY == DeadBodys[0][1]:
        GetThings_FromThing(1)
    elif EAimX==DeadBodys[1][0] and EAimY== DeadBodys[1][1]:
        GetThings_FromThing(2)
    elif EAimX==PushCar[0] and EAimY== PushCar[1]:
        GetThings_FromThing(3)
    elif EAimX==FisrtAid[0] and EAimY== FisrtAid[1]:
        GetThings_FromThing(4)
    elif EAimX==BuyBox[0] and EAimY== BuyBox[1]:
        GetThings_FromThing(5)
    #可搜索

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
    if Food<=0:
        print("玩家死亡。")


#人物移动
def PlayerMove(Dir):
    global PlayerY
    global PlayerX
    global Scr
    global Times
    global Food
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
    Food-=2


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


def EDirDone():
    #显示
    Text=NormalFont.render("搜索哪里？[esc退出]",True,Wcolor)
    Scr.blit(Text,(PlayerX*Game_Size,PlayerY*Game_Size))
    pygame.display.update()
    while 1:
        for event in pygame.event.get():
            if event.type==KEYDOWN:
                if event.key==K_UP:
                    EDone("UP")
                if event.key==K_DOWN:
                    EDone("DOWN")
                if event.key==K_RIGHT:
                    EDone("RIGHT")
                if event.key==K_LEFT:
                    EDone("LEFT")
                if event.key==K_ESCAPE:
                    PrintMap(2)
                    return

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
                    backage.back_main(Name,Scr)
                    InGameLoadPlayerData()
                if event.key==K_e:
                    EDirDone()
                if event.key==K_p:
                    admin.Main_Admin()
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
    LV=int(Data[2].strip("\n"))
    XP=int(Data[3].strip("\n"))
    SV=int(Data[4].strip("\n"))
    Power=int(Data[5].strip("\n"))
    Speed=int(Data[6].strip("\n"))
    #读取物品
    File=open(SaveFilePath+Name+"/item.dat","r")
    Item=File.readlines()
    print("数据读取完毕。")
    Start()

#单独读取HP，装备防御，武器并且更改速度
def InGameLoadPlayerData():
    global HP
    global ArmyHead
    global ArmyBody
    global ArmyHand
    global ArmyFoot
    global Weapon
    global Speed
    #读取HP与Speed
    File=open("data/save/"+Name+"/player.dat","r")
    Data=File.readlines()
    HP=int(Data[1].strip())
    Speed=int(Data[6].strip())
    #读取武器
    File=open("data/save/"+Name+"/weapon.dat","r")
    Data=File.readlines()
    Weapon[0]=int(Data[0].strip())#类型
    Weapon[1]=int(Data[1].strip())#伤害
    Weapon[2]=Data[2].strip()#名称
    print("武器读取完毕。")
    #读取装备防御
    #判断是否有装备
    File=open("data/save/"+Name+"/army.dat","r")
    Data=File.readlines()
    if len(Data)==0:
        print("没有装备，读取默认数值。")
    else:
        #读取
        ArmyHead[0]=int(Data[0].strip())
        ArmyHead[1]=Data[1].strip()
        ArmyBody[0]=int(Data[2].strip())
        ArmyBody[1]=Data[3].strip()
        ArmyHand[0]=int(Data[4].strip())
        ArmyHand[1]=Data[5].strip()
        ArmyFoot[0]=int(Data[6].strip())
        ArmyFoot[1]=Data[7].strip()
        print("装备读取完毕。")
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
    N=randint(0,len(MusicNameList)-1)
    pygame.mixer_music.load(MusicFilePath+MusicNameList[N])
    pygame.mixer_music.play(start=0.0)



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