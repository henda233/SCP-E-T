from os import mkdir


#玩家数据
Name=""
LV=1
XP=0
SV=100
Power=0
Speed=0


def SavePlayer():
    #创建玩家目录
    mkdir("data/save/"+Name+"/")
    mkdir('data/save/'+Name+"/maps")
    File=open("data/save/"+Name+"/player.dat","w+")

    #写入数据
    File.writelines(Name+"\n")
    File.writelines(str(LV) + "\n")
    File.writelines(str(XP) + "\n")
    File.writelines(str(SV) + "\n")
    File.writelines(str(Power) + "\n")
    File.writelines(str(Speed) + "\n")
    File=open("data/save/"+Name+"/item.dat","w+")
    print("玩家数据保存成功！")


def Main_CrtPlayer():
    global Name
    print("创建角色：")
    File=open("text_data/crtplayer.txt","r")
    Text=File.read()
    Data=input(Text)
    if Data=="":
        print("请输入合法的名称！")
        Main_CrtPlayer()
    else:
        Name=Data
        SavePlayer()
        print("返回游戏")
