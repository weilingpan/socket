import socket

HOST = '192.168.1.108'
PORT = 5000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #創建
s.connect((HOST, PORT))

# 使用者輸入的訊息給伺服器
try:
    while True:
        msg = input("client send: ")
        #print(f'client send: {msg}')
        s.send(msg.encode())
        
        data = s.recv(1024)#接收伺服器訊息
        print(f'receive from server: {data.decode()}\n')
except Exception as e:
    print(e)
    s.close()