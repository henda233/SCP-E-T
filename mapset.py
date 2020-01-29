from random import randint
import os

NowPass=""
UpPass=""
NextPass=""
DataRoad="save/"
Maps=[]
#读取模板
file = open("data/mapdata/a_data.ini", "r")
Data_A = file.readlines()
file2=open("data/mapdata/b_data.ini","r")
Data_B=file2.readlines()
file3=open("data/mapdata/c_data.ini","r")
Data_C=file3.readlines()
file4=open("data/mapdata/d_data.ini","r")
Data_D=file4.readlines()
file5=open("data/mapdata/f_data.ini","r")
Data_F=file5.readlines()
print("读取地图模板成功..."+"\n")

#开始函数
def Main_MapSet(Name):
    global DataRoad
    DataRoad="data/save/"+Name+"/maps/"
    FileList = os.listdir(("data\save\ " + Name + "\maps").replace(" ", ""))
    FileName = ("data\save\ " + Name + "\maps\ ").replace(" ", "")
    for File in FileList:
        os.remove(FileName + File)
    print("成功删除上次的地图数据.")
    Data=Start()
    return Data

def YesOrNot():
    C=randint(0,1)
    return C

def RantNum():
    Num=randint(0,99999)
    return Num

def NowPassSet():
    File=open("data/mapdata/f_data.ini","r")
    Pass=File.readlines()
    C=randint(0,2)
    Data=Pass[C]+"^"+str(RantNum())
    NowPass=Data.strip("\n")
    return NowPass

def WFile(Mode,FileName,Text):
    if Mode==1:
        File=open(DataRoad+FileName.replace("\n","")+".ini","w+")
        File.writelines(str(Text).replace("\n",""))
        Maps.append(str(Text).replace("\n",""))



def NextPassSet(UpPassAndNowPass):
    global NowPass
    global UpPass
    global NextPass
    if "直路" in UpPassAndNowPass:
        NextPass=NowPassSet()
        AllPass=UpPassAndNowPass+"#"+NextPass
        WFile(1,NowPass,AllPass)
        UpPass = NowPass

        NowPass=NextPass
    elif "右路" in UpPassAndNowPass:
        NextPass = NowPassSet()
        AllPass = UpPassAndNowPass + "#" + NextPass
        WFile(1, NowPass, AllPass)
        UpPass = NowPass

        NowPass = NextPass
    elif "左路" in UpPassAndNowPass:
        NextPass = NowPassSet()
        AllPass = UpPassAndNowPass + "#" + NextPass
        WFile(1, NowPass, AllPass)
        UpPass = NowPass

        NowPass = NextPass

def MapModeSet(Fisrt):
    global NowPass
    global UpPass
    while len(Data_A)!=0:
        if Fisrt==0:
            if YesOrNot()==0:
                N=len(Data_A)-1
                C=randint(0,N)
                UpPassAndNowPass=NowPass+"."+Data_A[C]
                Data_A.remove(Data_A[C])
                NextPassSet(UpPassAndNowPass)
                return
            elif YesOrNot()==1:
                UpPassAndNowPass = NowPass + ".0"
                NextPassSet(UpPassAndNowPass)
        elif Fisrt==1:
            if YesOrNot()==0:
                N=len(Data_A)-1
                C=randint(0,N)
                UpPassAndNowPass=UpPass+"#"+NowPass+"."+Data_A[C]
                Data_A.remove(Data_A[C])
                NextPassSet(UpPassAndNowPass)
            elif YesOrNot()==1:
                UpPassAndNowPass=UpPass+"#"+NowPass+".0"
                NextPassSet(UpPassAndNowPass)
    print("A区域生成完毕，正在生成B区域地图...")
    while len(Data_B)!=0:
        if YesOrNot() == 0:
            N = len(Data_B) - 1
            C = randint(0, N)
            UpPassAndNowPass = UpPass+"#"+NowPass + "." + Data_B[C]
            Data_B.remove(Data_B[C])
            NextPassSet(UpPassAndNowPass)
        elif YesOrNot() == 1:
            UpPassAndNowPass = UpPass+"#"+NowPass + ".0"
            NextPassSet(UpPassAndNowPass)
    print("B区域生成完毕，正在生成C区域地图...")
    while len(Data_C)!=0:
        if YesOrNot() == 0:
            N = len(Data_C) - 1
            C = randint(0, N)
            UpPassAndNowPass = UpPass+"#"+NowPass + "." + Data_C[C]
            Data_C.remove(Data_C[C])
            NextPassSet(UpPassAndNowPass)
        elif YesOrNot() == 1:
            UpPassAndNowPass = UpPass+"#"+NowPass + ".0"
            NextPassSet(UpPassAndNowPass)
    print("C区域生成完毕，正在生成D区域地图...")
    while len(Data_D)!=0:
        if YesOrNot() == 0:
            N = len(Data_D) - 1
            C = randint(0, N)
            UpPassAndNowPass = UpPass+"#"+NowPass + "." + Data_D[C]
            Data_D.remove(Data_D[C])
            NextPassSet(UpPassAndNowPass)
        elif YesOrNot() == 1:
            UpPassAndNowPass = UpPass+"#"+NowPass + ".0"
            NextPassSet(UpPassAndNowPass)
    print("所有地图生成完毕(save/)，正在调试中...")



def Start():
    global Data_A
    global NowPass
    global Maps
    MaxMapMode=len(Data_F)-1
    C=randint(0,MaxMapMode)
    Pass=NowPassSet()
    UPassAndNowPass=Data_F[C]+"#"+Pass
    NowPass=UPassAndNowPass
    MapModeSet(0)
    MapModeSet(1)
    print("地图生成完毕,一共有 "+str(len(Maps))+" 块区域。")
    return Maps

