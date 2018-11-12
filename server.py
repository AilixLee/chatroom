# server.py
#!/usr/bin/env python3
#coding=utf-8
'''
name:
email:
date:2018-9
class:AID
introduce:Chatroom server
env:python3.5
'''
from socket import *
import os,sys

#登录判断
def do_login(s,user,name,addr):
    if (name in user) or name == '管理员':
        s.sendto("该用户已存在".encode(),addr)
        return
    s.sendto(b'OK',addr)

    #通知其他人
    msg = "\n欢迎%s进入聊天室"%name
    for i in user:
        s.sendto(msg.encode(),user[i])

    #插入用户
    user[name] = addr

#转发聊天消息
def do_chat(s,user,name,text):
    msg = "\n%s 说:%s"%(name,text)
    for i in user:
        if i != name:
            s.sendto(msg.encode(),user[i])
#退出聊天室
def do_quit(s,user,name):
    msg = '\n' + name + "退出了聊天室"
    for i in user:
        if i == name:
            s.sendto(b'EXIT',user[i])
        else:
            s.sendto(msg.encode(),user[i])

    #从字典中删除用户
    del user[name]

#接收客户端请求
def do_parent(s):
    #存储结构{'zhangsan':('127.0.0.1')}
    user = {}
    while True:
        msg,addr = s.recvfrom(1024)
        msgList = msg.decode().split(' ')

        #区分请求类型
        if msgList[0] == 'L':
            do_login(s,user,msgList[1],addr)
        elif msgList[0] == 'C':
            do_chat(s,user,msgList[1],' '.join(msgList[2:]))
        elif msgList[0] == 'Q':
            do_quit(s,user,msgList[1])


#做管理员喊话
def do_child(s,addr):
    while True:
        msg = input("管理员消息:")
        msg = 'C 管理员 ' + msg
        s.sendto(msg.encode(),addr)

#创建网络，创建进程，调用功能函数
def main():
    #server address
    ADDR = ('0.0.0.0',8888)

    #创建套接字
    s = socket(AF_INET,SOCK_DGRAM)
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(ADDR)

    #创建一个单独的进程处理管理员喊话功能
    pid = os.fork()
    if pid < 0:
        sys.exit("创建进程失败")
    elif pid == 0:
        do_child(s,ADDR)
    else:
        do_parent(s)
if __name__ == "__main__":
    main()