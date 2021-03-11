import socket
import threading
import time
import json
import server.DataBaseUtils as db

DATA = '{{"cmd": "{}", "info": "{}"}}'


def tcplink(sock_C, address):
    print('Accept new connection from %s:%s...' % address)
    sock_C.send(b'Welcome!')
    while True:

        data = json.loads(sock_C.recv(1024).decode('utf-8'))
        print("收到请求:", data)
        time.sleep(1)
        if not data or data['cmd'] == 'exit':
            break
        if data['cmd'] == 'save':
            result = db.saveData(data['info'])
            sock_C.send(DATA.format('back', result).encode('utf-8'))
        elif data['cmd'] == 'get_names':
            result = db.getAllData()
            data = {'cmd': 'back', 'info': result}
            sock_C.send(json.dumps(data).encode('utf-8'))
        elif data['cmd'] == 'sign':
            result = db.doSign(data['info'][0], data['info'][1])
            data = {'cmd': 'back', 'info': result}
            sock_C.send(json.dumps(data).encode('utf-8'))
    sock_C.close()
    print('Connection from %s:%s closed.' % address)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 监听端口:
s.bind(('localhost', 7777))
s.listen(5)
print('Waiting for connection...')
while True:
    # 接受一个新连接:
    sock, addr = s.accept()
    # 创建新线程来处理TCP连接:
    t = threading.Thread(target=tcplink, args=(sock, addr))
    t.start()
