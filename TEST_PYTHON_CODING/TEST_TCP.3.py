import socket,time
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(('127.0.0.1',2134))
#t=input()
t=1
t='%s'% t
while True:
    s.send(t.encode('utf-8'))
    print(s.recv(1024).decode('utf-8'))
    s.send(b'exit')
    time.sleep(10)
