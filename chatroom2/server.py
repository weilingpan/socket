import socket
import datetime
from threading import Thread

host = '192.168.1.108'
port = 8080

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP
s.bind((host, port))

user = {} #存放用戶的數據 conn: name
accept_client_num = 5

def handle_client_in(conn, addr, name):
    welcome = f'[{datetime.datetime.now()}] 歡迎 {name} 加入聊天室'
    user[conn] = name
    print(welcome)
    print(f'目前在聊天室的人數: {len(user)}')

    # 將訊息傳送給所有客戶端
    for client in user:
        print(client)
        client.send(','.join(user.values()).encode())

if __name__ == '__main__':
    s.listen(accept_client_num)
    print('Server啟動，正在監聽用戶請求...')

    while True:         
        conn, address = s.accept()
        print(f'address={address} 已建立連接')

        indata = conn.recv(1024)
        name = indata.decode()

        #多用戶
        client_thread = Thread(target=handle_client_in, args=(conn, address, name))
        client_thread.start() 

        # while True:
        #     try:
        #         msg = conn.recv(1024)
        #         for client in user:
        #             client.send(msg.encode())
        #     except:
        #         conn.close()
