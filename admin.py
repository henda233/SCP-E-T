
AdminPassWord="zxc123"

def AdminMode():
    File=open("text_data/admin.txt","r")
    Text=File.read()
    File.close()
    Act=input(Text)
    if Act=="6":
        return
    elif Act=="1":
        pass

def Main_Admin():
    Pass=input("你即将进入管理员模式（调试模式），请输入密码：")
    if AdminPassWord==Pass:
        print("Login!")
        AdminMode()
    else:
        print("错误密码！")
        return