import socket

HOST = '192.168.1.108'
PORT = 5000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #創建
s.bind((HOST, PORT)) #綁定
s.listen(5) #監聽

print('server start at: %s:%s' % (HOST, PORT))
print('wait for connection...\n')

# 等待客戶端連線
try:
    while True:
        conn, addr = s.accept()
        print(f'connected by {str(addr)}')

        while True:
            #連線成功後，接收並印出資料
            indata = conn.recv(1024)
            data = indata.decode()
            print(f'receive from client: {data}')

            msg = input("server send: ")
            conn.send(msg.encode())
        conn.close()
except Exception as e:
    print(e)
    s.close()