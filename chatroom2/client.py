import socket
import tkinter as tk
from threading import Thread
from tkinter import scrolledtext, simpledialog

host = '192.168.1.108'
port = 8080
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #創建
s.connect((host, port))

def login_in(window_welcome, username):
    s.send(username.encode())
    window_welcome.destroy()
    chat_view()

def welcome_view():
    window_welcome = tk.Tk()
    window_welcome.title('聊天室-登入畫面')
    window_welcome.geometry('520x350')
    window_welcome.resizable(False, False)
    window_welcome.iconbitmap('chat.ico')

    # label_users = tk.Label(window_welcome, text="目前總用戶數")
    label_name = tk.Label(window_welcome, justify=CENTER, text="請輸入用戶名字: ")
    input_text = tk.Entry(window_welcome, textvariable="username")
    btn = tk.Button(window_welcome, text="登入", command=lambda: login_in(window_welcome, input_text.get()))
    
    label_name.pack()
    input_text.pack()    
    btn.pack()
    window_welcome.mainloop()

def chat_view():
    window_chat = tk.Tk()
    window_chat.title('聊天室-聊天畫面')
    window_chat.geometry('520x350')
    window_chat.iconbitmap('chat.ico')

    data = s.recv(1024)
    listbox = tk.Listbox(window_chat)
    listbox.insert(tk.END, f'-----用戶列表-----')
    for user in data.decode().split(','):
        listbox.insert(tk.END, user)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH)

    chat_box = scrolledtext.ScrolledText(window_chat, wrap=tk.WORD)
    chat_box.pack(expand=True, fill=tk.BOTH)

    input_frame = tk.Frame(window_chat)
    input_frame.pack()
    input_entry = tk.Entry(input_frame)
    input_entry.pack(side=tk.LEFT)
    send_button = tk.Button(input_frame, text="傳送訊息") #, command=send_message
    send_button.pack(side=tk.LEFT)

    # receive_thread = Thread(target=receive_messages, args=(s,listbox))
    # receive_thread.start()

    window_chat.mainloop()


if __name__ == '__main__':
    # from PIL import Image
    # img = Image.open('chat.png')
    # img.save('chat.ico')

    welcome_view()
    
