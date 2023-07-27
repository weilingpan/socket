import socket

HOST = '192.168.1.108'
PORT = 5000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #創建
s.bind((HOST, PORT)) #綁定
s.listen(5) #監聽

print('server start at: %s:%s' % (HOST, PORT))
print('wait for connection...\n')

# 等待客戶端連線
while True:
    conn, addr = s.accept()
    #print('connected by ' + str(addr))

    #連線成功後，接收並印出資料
    indata = conn.recv(1024)
    data = indata.decode()
    print(f'receive from client: {data}')

    outdata = f'[echo]{data}'
    print(f'server send: {outdata}')
    conn.send(outdata.encode())
    conn.close()
s.close()