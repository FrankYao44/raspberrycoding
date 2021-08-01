import socket,threading,time
def th(sock,addr):
    print('incoming tranmission')
    sock.send(b'commander general')
    while True:
        data = sock.recv(1024)
        time.sleep(1)
        if not data or data.decode('utf-8') == 'exit':
            break
        else:
            print(data.decode('utf-8'))
    sock.close()
    print('Connection from %s:%s closed.' % addr)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1', 2134))
s.listen(5)
print('battle contorl onlined')
while True:
    sock,addr=s.accept()
    t=threading.Thread(target=th,args=(sock,addr))
    t.start()
    
    
