import socket 
import threading
import re
import datetime

class ChatServer:
    socket_list = []
    user_list = {} #socket:name
    received_message = ""

    def __init__(self):
        self.server_socket = None
        self.create_listening_server()

    #listen for incoming connection
    def create_listening_server(self):
        local_ip = '127.0.0.1'
        local_port = 10319

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
        # 當socket關閉後，本地端用於該socket的端口號立刻就可以被重用。value設置為1 ，表示將SO_REUSEADDR標記為TRUE 
        # this will allow you to immediately restart a TCP server
        self.server_socket.bind((local_ip, local_port))
        print("Server啟動，正在監聽用戶請求...")

        self.server_socket.listen(5) #listen for incomming connections / max 5 clients
        self.receive_messages_in_a_new_thread()
    
    # 有新用戶就會從這裡觸發
    def receive_messages_in_a_new_thread(self):
        while True:
            socket, (ip, port) = self.server_socket.accept() #有新用戶就會從這裡觸發，client is tuple
            print(f'Connected to {ip}:{str(port)}')
            self.add_to_socket_list(socket)

            # 當start()方法被呼叫時，將在新的執行緒中執行target內的函數
            t = threading.Thread(target=self.receive_messages, args=(socket,))
            t.start()

    # 偵聽器
    def receive_messages(self, socket):
        try:
            while True:
                incoming_buffer = socket.recv(256) #等待 #數字 256 是指要接收的資料的最大大小，以位元組 (bytes) 為單位。
                if not incoming_buffer:
                    break
                self.received_message = incoming_buffer.decode('utf-8')

                if "joined" in self.received_message:
                    user = re.findall(r"] (\w+) joined", self.received_message)[0]
                    self.user_list[socket] = user
                    msg = '------用戶列表------\n'+'\n'.join(self.user_list.values())
                    # print(msg)
                    self.broadcast_to_all_clients(f'user_list: {msg}')
                
                print(f'[server get] {self.received_message}')
                self.broadcast_to_all_clients(self.received_message)  # send to all clients
            socket.close()
        except ConnectionResetError:
            self.socket_list.remove(socket)
            name_quit = self.user_list[socket]
            print(f'{name_quit} quit')
            del self.user_list[socket]

            msg = '------用戶列表------\n'+'\n'.join(self.user_list.values())
            self.broadcast_to_all_clients(f'user_list: {msg}')
            self.broadcast_to_all_clients(f'[{datetime.datetime.now()}] {name_quit} 離開了聊天室')
            
    
    def broadcast_to_all_clients(self, message):
        for socket in self.socket_list:
            socket.sendall(message.encode('utf-8'))

    def add_to_socket_list(self, socket):
        if socket not in self.socket_list:
            print(f'add new socket')
            self.socket_list.append(socket)

if __name__ == "__main__":
    ChatServer()