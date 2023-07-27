import socket 
import threading

class ChatServer:
    clients_list = []
    last_received_message = ""

    def __init__(self):
        self.server_socket = None
        self.create_listening_server()

    #listen for incoming connection
    def create_listening_server(self):
        local_ip = '127.0.0.1'
        local_port = 10319

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # this will allow you to immediately restart a TCP server
        self.server_socket.bind((local_ip, local_port))
        print("Server啟動，正在監聽用戶請求...")

        self.server_socket.listen(5) #listen for incomming connections / max 5 clients
        self.receive_messages_in_a_new_thread()
    
    def receive_messages_in_a_new_thread(self):
        while True:
            client = _socket, (ip, port) = self.server_socket.accept() #有新用戶就會從這裡觸發
            self.add_to_clients_list(client)
            print(f'Connected to {ip}:{str(port)}')
            t = threading.Thread(target=self.receive_messages, args=(_socket,))
            t.start()

    def receive_messages(self, so):
        while True:
            incoming_buffer = so.recv(256) #initialize the buffer
            if not incoming_buffer:
                break
            self.last_received_message = incoming_buffer.decode('utf-8')
            self.broadcast_to_all_clients(so)  # send to all clients
        so.close()
    
    def broadcast_to_all_clients(self, senders_socket):
        for client in self.clients_list:
            socket, (ip, port) = client
            if socket is not senders_socket:
                socket.sendall(self.last_received_message.encode('utf-8'))

    def add_to_clients_list(self, client):
        if client not in self.clients_list:
            print(f'add client={client} to clients_list')
            self.clients_list.append(client)

if __name__ == "__main__":
    ChatServer()