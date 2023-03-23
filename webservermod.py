import socket
import threading

IP = socket.gethostbyname(socket.gethostname())
PORT = 5050
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((IP,PORT))

def handle_client(conn,addr):
    print(f'{addr} connected \n')
    req = conn.recv(1024).decode(FORMAT)
    reqPath = req.split('\n')[0].split()[1]
    if reqPath == '/':
        reqPath = '/index.html'
    print(reqPath)

    try:
        with open(reqPath) as f:
            cont = f.read()
            res = f'HTTP/1.1 200 OK\n\n{cont}'
    except FileNotFoundError:
        try:
            with open('404.html') as f:
                cont = f.read()
                res = f'HTTP/1.1 404 NOT FOUND\n\n{cont}'
        except FileNotFoundError:
            cont = 'File not found'
            res = f'HTTP/1.1 404 NOT FOUND\n\n{cont}'
    
    conn.send(res.encode(FORMAT))
    conn.close()

def start():
    server.listen()
    print(f"Server running at {IP}:{PORT}")

    while True:
        conn,addr = server.accept()
        thread = threading.Thread(target=handle_client,args=(conn,addr))
        thread.start()
        print(f'Active Clients = {threading.active_count()-1}')

start()
