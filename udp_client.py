import socket

HOST = '192.168.1.108'
PORT = 7000

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #創建
#socket.AF_INET 表示使用 Internet Protocol 的通訊協定，而 socket.SOCK_DGRAM 表示傳輸方式為 UDP

# 使用者輸入的訊息給伺服器
while True:
    msg = input("Please input message: ")
    print(f'client send: {msg}')
    s.sendto(msg.encode(), (HOST, PORT))
    
    data, addr = s.recvfrom(1024)#接收伺服器訊息
    print(f'receive from server: {data.decode()}\n')

s.close()