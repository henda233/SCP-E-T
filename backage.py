import pygame
from pygame.locals import *
import sys

pygame.init()
#大小
W=480
L=420
#背包界面位置
BackX=400
BackY=300
#物品显示大小
ItemSize=64
#图片载入
BackageImg=pygame.image.load("img/backage.jpg")
#修改图片大小
BackageImg=pygame.transform.scale(BackageImg,(W,L))
#字体
NormalFont=pygame.font.SysFont("SimHei",24)
#颜色
WColor=255,255,255
#物品
Name=""
Item=[]
PlayerItem=[]


def DropItem(DropNumber):
    global PlayerItem
    #读取
    File=open("data/save/"+Name+"/item.dat","r")
    Data=File.readlines()
    #删除
    PlayerItem.pop(DropNumber)
    Data.pop(DropNumber)
    #写回
    File=open("data/save/"+Name+"/item.dat","w")
    File.writelines(Data)
    print("成功使用或者删除物品："+PlayerItem[DropNumber])

def AddWeapon(WeaponName):
    #读取文件
    File=open("data/items/weapons/"+WeaponName+".txt","r")
    Data=File.readlines()
    Kind=Data[0].strip()
    Hurt=Data[1].strip()
    #写入玩家武器数据
    File=open("data/save/"+Name+"/weapon.dat","w+")
    File.writelines(Kind+"\n")
    File.writelines(Hurt+"\n")
    File.writelines(WeaponName+"\n")
    print("装备武器： "+WeaponName)


def AddHP(AddNumber):
    File = open("data/save/" + Name + "/player.dat", "r")
    Data = File.readlines()
    Data[1] = str(int(Data[1].strip()) + int(AddNumber)) + "\n"
    # 返回
    File = open("data/save/" + Name + "/player.dat", "w")
    File.writelines(Data)
    print("HP+"+str(AddNumber))

#丢弃或者使用物品
def UseItem(UseNumber,Scr):
    global PlayerItem
    #合法性检测
    #是否超出
    Max=len(PlayerItem)
    if UseNumber>Max:
        print("你没有这个东西！")
        return
    else:
        #读取物品使用信息
        ItemName=PlayerItem[UseNumber]
        File=open("data/items/use_item/"+ItemName+".txt","r")
        Data=File.readlines()
        ItemKind=Data[0].strip()
        #检测类型
        if "教程" in ItemKind:
            File=open("text_data/playerhelp.txt","r")
            print(File.read())
        if "HP" in ItemKind:
            ItemDo=int(Data[1].strip())
            #更改HP
            AddHP(ItemDo)
            #删除物品
            DropItem(UseNumber)
            print("使用物品，成功删除物品： "+ItemName)
        if "武器" in ItemKind:
            #添加武器
            AddWeapon(ItemName)
            #不删除
    PrintItemToScr(Scr)



#将物品打印到屏幕
def PrintItemToScr(Scr):
    global ItemY
    global ItemX
    #数字转为文本
    NumberToText()
    ListNumber=1
    ItemX=BackX+32
    ItemY=BackY+32
    for i in range(len(PlayerItem)):
        if ListNumber==4:
            ItemX = BackX + 32
            ItemY+=90
        #读取图片
        ItemImg=pygame.image.load("data/items/item_img/"+PlayerItem[i]+".jpg")
        #调整大小
        ItemImg=pygame.transform.scale(ItemImg,(128,128))
        Scr.blit(ItemImg,(ItemX,ItemY))
        #打印文字
        ItemText=NormalFont.render(str(i)+PlayerItem[i],True,(0,0,0))
        #显示文字
        Scr.blit(ItemText,(ItemX,ItemY))
        pygame.display.update()
        ItemX+=128
        ListNumber+=1



#玩家物品数字转为具体的物品文字
def NumberToText():
    global Item
    global PlayerItem
    Item=[]
    PlayerItem=[]
    #读取玩家物品数字
    File=open("data/save/"+Name+"/item.dat","r")
    PlayerNumber=File.readlines()
    #读取全物品
    File=open("data/items/item.dat","r")
    Item=File.readlines()
    #与玩家物品数字进行匹配
    for i in range(len(PlayerNumber)):
        PlayerItem.append(Item[int(PlayerNumber[i].strip())].strip())


#主运行函数
def back_main(Data_Name,Scr):
    global Name
    #载入名称
    Name=Data_Name
    #显示背包背景
    Scr.blit(BackageImg,(BackX,BackY))
    #显示文字
    PrintItemToScr(Scr)
    pygame.display.update()
    while 1:
        for event in pygame.event.get():
            if event.type==KEYDOWN:
                if event.key==K_TAB:
                    pygame.draw.rect(Scr,(0,0,0),((BackX,BackY),(W,L)))
                    print("返回游戏")
                    return
                if event.key==K_0:
                    UseItem(0,Scr)
                if event.key==K_1:
                    UseItem(1,Scr)
                if event.key==K_2:
                    UseItem(2,Scr)
                if event.key==K_3:
                    UseItem(3,Scr)
                if event.key==K_4:
                    UseItem(4,Scr)
                if event.key==K_5:
                    UseItem(5,Scr)
                if event.key==K_6:
                    UseItem(6,Scr)
                if event.key==K_7:
                    UseItem(7,Scr)
                if event.key==K_8:
                    UseItem(8,Scr)
        pygame.display.update()
