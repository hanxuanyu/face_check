import socket
import json
DATA = '{{"cmd": "{}", "info": "{}"}}'
IP = '47.93.128.120'
# IP = '127.0.0.1'


def saveName(userName):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 建立连接:
    s.connect((IP, 7777))
    # 接收欢迎消息:
    print(s.recv(1024).decode('utf-8'))

    # 存入数据
    s.send(DATA.format('save', userName).encode('utf-8'))
    result = json.loads(s.recv(1024).decode('utf-8'))
    isSaved = result['info']
    # 退出系统
    s.send(DATA.format('exit', 'exit').encode('utf-8'))
    s.close()
    return isSaved

def getNames():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 建立连接:
    s.connect((IP, 7777))
    # 接收欢迎消息:
    print(s.recv(1024).decode('utf-8'))
    # 获取数据
    s.send(DATA.format('get_names', 'name').encode('utf-8'))
    result = json.loads(s.recv(1024).decode('utf-8'))
    names = result['info']
    # 退出系统
    s.send(DATA.format('exit', 'exit').encode('utf-8'))
    s.close()
    result = []
    for name in names:
        result.append(name['name'])
    return result

def doSign(name, date):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 建立连接:
    s.connect((IP, 7777))
    # 接收欢迎消息:
    print(s.recv(1024).decode('utf-8'))
    # 获取数据
    signDate = {'cmd': 'sign', 'info': [name, date]}
    s.send(json.dumps(signDate).encode('utf-8'))
    result = json.loads(s.recv(1024).decode('utf-8'))
    result = result['info']
    # 退出系统
    s.send(DATA.format('exit', 'exit').encode('utf-8'))
    s.close()
    return result


if __name__ == '__main__':
    print(saveName('hxuanyu'))
    names = getNames()
    print(names)
