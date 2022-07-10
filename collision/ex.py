from pwn import *

LOCAL = False

passcode = p32(0x6c5cec8) + p32(0x6c5cec9) * 4

if LOCAL:
    r = process(['./release/col', passcode])
else:
    s = ssh('col', 'pwnable.kr', 2222, 'guest')
    r = s.process(['./col', passcode])

r.interactive()