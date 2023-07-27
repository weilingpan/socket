import socket

HOST = '192.168.1.108'
PORT = 7000

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#socket.AF_INET 表示使用 Internet Protocol 的通訊協定，而 socket.SOCK_DGRAM 表示傳輸方式為 UDP
s.bind((HOST, PORT))

print('server start at: %s:%s' % (HOST, PORT))
print('wait for connection...\n')

while True:
    indata, addr = s.recvfrom(1024)
    print(f'recvfrom {str(addr)}: {indata.decode()}')

    outdata = f'[echo]{indata.decode()}'
    s.sendto(outdata.encode(), addr)
s.close()