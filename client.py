# client.py

from socket import *
import sys,os

def send_msg(s,name,addr):
    while True:
        text = input("发言:")
        #如果输入quit退出
        if text.strip() == 'quit':
            msg = 'Q ' + name
            s.sendto(msg.encode(),addr)
            sys.exit("退出聊天室")

        msg = 'C %s %s'%(name,text)
        s.sendto(msg.encode(),addr)

def recv_msg(s):
    while True:
        data,addr = s.recvfrom(2048)
        if data.decode() == 'EXIT':
            sys.exit(0)
        print(data.decode() + "\n发言:",end = '')


#创建套接字登录，如果登录成功，创建子进程
def main():
    #从命令行获取服务端地址
    if len(sys.argv) < 3:
        print("argv is error")
        return
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    ADDR = (HOST,PORT)

    #创建套接字
    s = socket(AF_INET,SOCK_DGRAM)

    while True:
        name = input("请输入姓名:")
        msg = "L " + name
        #发送登录请求
        s.sendto(msg.encode(),ADDR)
        #等待服务器回复
        data,addr = s.recvfrom(1024)
        if data.decode() == 'OK':
            print("您已进入聊天室")
            break
        else:
            #不成功，服务器会回复不允许登录原因
            print(data.decode())

    #创建父子进程
    pid = os.fork()
    if pid < 0:
        sys.exit("创建子进程失败")
    elif pid == 0:
        send_msg(s,name,ADDR)
    else:
        recv_msg(s)



if __name__ == "__main__":
    main()