import pygame
from pygame.locals import *
from random import randint
from time import sleep
import os

#初始化
pygame.init()
#大小
W=680
L=510
#位置
X=300
Y=200
#颜色
B=(0,0,0)
#字体
Font=pygame.font.SysFont("SimHei",16)
#返回的值
Data=["None","None","None","None"]#技能 身份 身份描述 技能描述
#点数
Point=10
#玩家名称
Name=""
#身份标志符
Man=0#0随机 1保安 2科学家 3D级 4清洁工
#力量
Power=0
#字距
TextLong=30

def PrintToScr(Scr):
    #分成LIST
    Scr.fill((0,0,0))
    ManTexts=Data[2].split("\n")
    SkillTexts=Data[3].split("\n")
    #身份描述
    TextX=X+30
    TextY=Y+30
    for i in range(len(ManTexts)):
        MText=Font.render(ManTexts[i],True,(255,255,255))
        Scr.blit(MText,(TextX,TextY+i*TextLong))
    #技能描述
    TextY=Y+150
    for j in range(len(SkillTexts)):
        SText=Font.render(SkillTexts[j],True,(255,255,255))
        Scr.blit(SText,(TextX,TextY+j*TextLong))
    Text=Font.render("技能:"+Data[0],True,(255,255,255))
    Scr.blit(Text,(TextX,TextY+100))
    Text=Font.render("力量:"+str(Power),True,(255,255,255))
    Scr.blit(Text,(TextX,TextY+150))
    #显示文字
    cText=Font.render("按 TAB 继续...",True,(255,255,255))
    Scr.blit(cText,(TextX,TextY+250))
    pygame.display.update()


#完成Data数据
def GetDataDone():
    global Data
    global ManText
    #处理身份
    if Man==1:
        ManText="安保人员"
        Data[1]=ManText
    elif Man==2:
        ManText="科研人员"
        Data[1]=ManText
    elif Man==3:
        ManText="D级人员"
        Data[1]=ManText
    elif Man==4:
        ManText="清洁工"
        Data[1]=ManText
    #处理描述
    File=open("text_data/man_text/"+ManText+".txt","r",encoding='utf-8')
    ManText=File.read()
    File.close()
    File=open("text_data/skill_text/"+Data[0]+".txt","r",encoding='utf-8')
    SkillText=File.read()
    Data[2]=ManText
    Data[3]=SkillText
    File.close()


#玩家力量加点（自动）
def PlayerPower():
    global Power
    Power=Point
    #读取玩家数据
    File=open("data/save/"+Name+"/player.dat","r",encoding='utf-8')
    PlayerData=File.readlines()
    AddPower=Point
    PlayerData[5] = str(int(PlayerData[5].strip()) + AddPower) + "\n"
    #写回
    File=open("data/save/"+Name+"/player.dat","w")
    File.writelines(PlayerData)
    File.close()
    GetDataDone()

#角色选择
def PlayerManC():
    global Man
    #判断是否有技能
    if Man==0:
        #随机选择
        C=randint(1,4)
        Man=C
    PlayerPower()
#实现技能
def DoneSkill(Kind):
    global Point
    global Data
    global Man
    global PlayerData
    #读取玩家数据
    File=open("data/save/"+Name+"/player.dat","r")
    PlayerData=File.readlines()
    if Kind==1:
        AddHP=int(int(PlayerData[1].strip())*0.5)
        PlayerData[1]=str(int(PlayerData[1].strip())+AddHP)+"\n"
        #减去点数
        Point-=8
        Data[0]="强化人"
    elif Kind==2:
        AddHP=int(int(PlayerData[1].strip())*0.5)
        PlayerData[1]=str(int(PlayerData[1].strip())-AddHP)+"\n"
        PlayerData[6] = str(int(PlayerData[6].strip()) + 2) + "\n"
        #减去点数
        Point-=7
        Data[0] = "914实验体"
    elif Kind==3:
        Man=1
        #减去点数
        Point-=6
        Data[0] = "保安"
    elif Kind==4:
        Man=2
        #减去点数
        Point-=5
        Data[0] = "科学家"
    elif Kind==5:
        Data[0]="5"
    #写回
    File=open("data/save/"+Name+"/player.dat","w+")
    File.writelines(PlayerData)
    File.close()
    PlayerManC()


#选择技能
def MainStart_PlayerSkillC(Data_Name,Scr):
    global Name
    Name=Data_Name
    #显示背景
    pygame.draw.rect(Scr,B,((X,Y),(W,L)))
    #读取技能文件
    File=open("text_data/skills.txt","r",encoding='utf-8')
    SkillTexts=File.readlines()
    #显示
    TextX=X+30
    TextY=Y+30
    for i in range(len(SkillTexts)-1):
        SkillText=Font.render(SkillTexts[i].strip(),True,(255,255,255))
        Scr.blit(SkillText,(TextX,TextY+i*30))
    pygame.display.update()
    #检测输入
    while 1:
        for event in pygame.event.get():
            if event.type==KEYDOWN:
                if event.key==K_1:
                    DoneSkill(1)
                if event.key == K_2:
                    DoneSkill(2)
                if event.key==K_3:
                    DoneSkill(3)
                if event.key==K_4:
                    DoneSkill(4)
                if event.key==K_5:
                    DoneSkill(5)
                if event.key==K_TAB:
                    return Data
                PrintToScr(Scr)
                pygame.display.update()
