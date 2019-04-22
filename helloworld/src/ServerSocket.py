import socket

s = socket.socket()
ip_port = ("localhost",123)
s.bind(ip_port)
s.listen(5)

def handleMsg(client):
    try:
        while True:
            data = client.recv(1024)
            msg = data.decode("utf-8")
            print("收到：",msg)
            print("请输入发送内容:")
            str = input()
            client.send(str.encode("utf-8"))
            print("发送完毕:",str)
    except Exception:
        print("socekt error")
    finally:
        client.close()

while True:
    c,addr=s.accept()
    print(addr)
    handleMsg(c)



