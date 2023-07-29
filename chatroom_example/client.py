from tkinter import Tk, Frame, Scrollbar, Label, END, Entry, Text, VERTICAL, Button, messagebox #Tkinter Python Module for GUI  
import tkinter as tk
import socket
import threading
import datetime

class ChatGUI:
    client_socket = None
    last_received_message = None
    
    def __init__(self, master):
        self.root = master
        self.chat_transcript_area = None
        self.user_list_area = None
        self.name_widget = None
        self.enter_text_widget = None
        self.join_button = None
        
        self.initialize_socket()
        self.initialize_gui()
        self.listen_for_incoming_messages_in_a_thread()

    def initialize_socket(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_ip = '127.0.0.1'
        remote_port = 10319
        self.client_socket.connect((remote_ip, remote_port)) #connect to the remote server

    def initialize_gui(self): # GUI initializer
        self.root.title("我的聊天室") 
        self.root.resizable(0, 0)
        self.root.iconbitmap('chat.ico')
        self.display_name_section()
        self.name_widget.focus() #預設游標位置
        
    def listen_for_incoming_messages_in_a_thread(self):
        thread = threading.Thread(target=self.receive_message_from_server, args=(self.client_socket,)) # Create a thread for the send and receive in same time 
        thread.start()

    def receive_message_from_server(self, so):
        try:
            while True:
                buffer = so.recv(256)
                if not buffer:
                    break
                message = buffer.decode('utf-8')
                print(f'[client get] {message}')

                if "user_list" in message:
                    lst = message.split(':')[-1].strip()
                    self.user_list_area.delete("1.0", tk.END)
                    self.user_list_area.insert('end', lst)
                else:
                    self.chat_transcript_area.insert('end', message + '\n')
                    self.chat_transcript_area.yview(END)
            so.close()
        except ConnectionAbortedError:
            print(f"quit")

    def display_user_list(self):
        frame = Frame()
        self.user_list_area = Text(frame, width=20)
        self.user_list_area.bind('<KeyPress>', lambda e: 'break')
        self.user_list_area.pack(side='left')
        frame.pack(side='left')

    def display_name_section(self):
        frame = Frame()
        Label(frame, text='Enter Your Name: ', font=("arial", 13,"bold")).pack(side='left', pady=20)
        self.name_widget = Entry(frame, width=60, font=("arial", 13))
        self.name_widget.pack(side='left', anchor='e', pady=15)
        self.join_button = Button(frame, text="Join", width=10, command=self.on_join)
        self.join_button.pack(side='right', padx=5, pady=15)
        frame.pack(side='top', anchor='nw')

    def display_chat_box(self):
        frame = Frame()
        Label(frame, text='Chat History', font=("arial", 12,"bold")).pack(side='top')
        self.chat_transcript_area = Text(frame, width=60, height=13, font=("arial", 12))
        scrollbar = Scrollbar(frame, command=self.chat_transcript_area.yview, orient=VERTICAL)
        self.chat_transcript_area.config(yscrollcommand=scrollbar.set)
        self.chat_transcript_area.bind('<KeyPress>', lambda e: 'break')
        self.chat_transcript_area.pack(side='left', padx=15, pady=10)
        scrollbar.pack(side='right', fill='y')
        frame.pack()

    def display_chat_input_box(self):   
        frame = Frame()
        Label(frame, text='Enter Your Message', font=("arial", 12, "bold")).pack(side='top')
        self.enter_text_widget = Text(frame, width=62, height=3, font=("arial", 12))
        self.enter_text_widget.pack(side='top', padx=15, pady=(0, 10))
        self.enter_text_widget.bind('<Return>', self.on_enter_key_pressed)
        frame.pack()

    def on_join(self):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        #TODO: 確認暱稱是否重複
        if len(self.name_widget.get()) == 0:
            messagebox.showerror(
                "登入錯誤", "請輸入暱稱")
            return

        self.name_widget.config(state='disabled')
        self.join_button.config(state='disabled')

        self.display_user_list()
        self.display_chat_box()
        self.display_chat_input_box()
        self.enter_text_widget.focus_set() #預設游標位置
        self.client_socket.send((f"[{now}] {self.name_widget.get()} 加入聊天室").encode('utf-8'))

    def on_enter_key_pressed(self, event):
        self.send_chat()
        self.clear_text()
        return 'break'  # 阻止預設換行行為
        
    def clear_text(self):
        self.enter_text_widget.delete(1.0,'end')

    def send_chat(self):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        senders_name = self.name_widget.get().strip()
        data = self.enter_text_widget.get(1.0, 'end-1c').strip() #使用 end-1c 表示取得倒數第二個字元 ( 因為最後一個字元是換行符 )
        message = f'[{now}] {senders_name}: {data}'.encode('utf-8')
        self.client_socket.send(message)
        self.clear_text()        

    def on_close_window(self):
        if messagebox.askokcancel("離開視窗", "確定要離開嗎?"):
            self.root.destroy()
            self.client_socket.close()
            exit(0)

if __name__ == '__main__':
    root = Tk()
    gui = ChatGUI(root)
    root.protocol("WM_DELETE_WINDOW", gui.on_close_window)
    root.mainloop()
