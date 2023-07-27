import socket

HOST = '192.168.1.108'
PORT = 7000

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((HOST, PORT))

print('server start at: %s:%s' % (HOST, PORT))
print('wait for connection...\n')

while True:
    indata, addr = s.recvfrom(1024)
    print(f'recvfrom {str(addr)}: {indata.decode()}')

    outdata = f'[echo]{indata.decode()}'
    s.sendto(outdata.encode(), addr)
s.close()