from random import randint

DeadBodys=[[0,0,0],[0,0,0]]
PushCar=[0,0,0]
FisrtAid=[0,0,0]
BuyBox=[0,0,0]

def SetBox():
    global BuyBox
    #随机几率
    C=randint(1,10)
    if C in range(5):
        #随机坐标
        BoxX=randint(1,10)
        BoxY=1
        BuyBox[0]=BoxX
        BuyBox[1]=BoxY
    else:
        BuyBox[0]=0
        BuyBox[1]=0


def SetFisrtAid():
    global FisrtAid
    #随机几率
    C=randint(1,10)
    if C in range(4):
        #随机坐标
        AidX=randint(1,10)
        AidY=randint(1,5)
        #写入
        FisrtAid[0]=AidX
        FisrtAid[1]=AidY
        # 设置物品数量
        ItemNumber = randint(1, 2)
        FisrtAid[2]=ItemNumber
    else:
        FisrtAid[0]=0
        FisrtAid[1]=0
def SetPushCar():
    global PushCar
    #随机几率
    C=randint(1,10)
    if C in range(2):
        #随机坐标
        PushCarX=randint(1,10)
        PushCarY=randint(1,5)
        #写入
        PushCar[0]=PushCarX
        PushCar[1]=PushCarY
        # 设置物品数量
        ItemNumber = randint(1, 2)
        PushCar[2]=ItemNumber
    else:
        PushCar[0]=0
        PushCar[1] = 0

def SetDeadBody():
    global DeadBodys
    #随机几率
    C=randint(1,10)
    if C in range(3):
        # 随机数量
        Number = randint(1, 2)
        if Number==1:
            #随机坐标
            BodyX=randint(1,10)
            BodyY=randint(1,5)
            #写入
            DeadBodys[0][0]=BodyX
            DeadBodys[0][1]=BodyY
        else:
            #随机坐标
            BodyX=randint(1,10)
            BodyY=randint(1,5)
            #写入
            DeadBodys[0][0]=BodyX
            DeadBodys[0][1]=BodyY
            #随机坐标
            BodyX=randint(1,10)
            BodyY=randint(1,5)
            #写入
            DeadBodys[1][0]=BodyX
            DeadBodys[1][1]=BodyY
        #设置物品数量
        ItemNumber=randint(1,2)
        DeadBodys[0][2]=ItemNumber
        DeadBodys[1][2]=ItemNumber

    else:
        DeadBodys[0][0]=0
        DeadBodys[0][1]=0
        DeadBodys[0][2]=0
        DeadBodys[1][0]=0
        DeadBodys[1][1]=0
        DeadBodys[1][2]=0


def MainStart_SetThing(NowMap,PassedMaps):
    global DeadBodys
    global PushCar
    global FisrtAid
    global BuyBox
    #判断是否经过
    if NowMap in PassedMaps:
        print("你之前来过这里")
        return [[0,0,0],[0,0,0]],[0,0,0],[0,0,0],[0,0,0]

    else:
        c=randint(1,4)
        if c==1:
            SetDeadBody()
        elif c==2:
            SetPushCar()
        elif c==3:
            SetFisrtAid()
        SetBox()
        return DeadBodys, PushCar, FisrtAid, BuyBox
