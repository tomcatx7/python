import socket

c = socket.socket()
hostName = socket.gethostname()
port = 123
c.connect(("localhost",port))
c.send("hello".encode("utf-8"))

while True:
    data = c.recv(1024).decode("utf-8")
    print("client 收到",data)
    print("请输入发送内容:")
    str = input()
    if str == "#":
        break
    c.send(str.encode("utf-8"))
    print("发送完毕:", str)

c.close()