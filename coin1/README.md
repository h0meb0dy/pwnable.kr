# [pwnable.kr] coin1

> Mommy, I wanna play a game!
> (if your network response time is too slow, try nc 0 9007 inside pwnable.kr server)
>
> Running at : nc pwnable.kr 9007
>
> [Attachment](./attachment)

![image](https://github.com/user-attachments/assets/413d269f-cbdc-4aed-97cd-ee1b18b5557c)

N개의 코인 중에서 C번의 기회 안에 무게가 다른 한 개의 코인을 찾는 문제다.

전체 코인을 절반으로 나눠서 한쪽의 무게를 재면 둘 중 어느 쪽에 무게가 다른 코인이 섞여 있는지 알 수 있고, 이 과정을 코인 한 개만 남을 때까지 반복하면 정답을 맞출 수 있다.

```python
# ex.py

from pwn import *

# r = remote("pwnable.kr", 9007)
r = remote("0", 9007)  # in pwnable.kr server


# return b'<start> <start + 1> ... <end>'
def gen_payload(start, end):
    payload = b""
    for i in range(start, end):
        payload += str(i).encode() + b" "
    payload += str(end).encode()
    return payload


r.recvuntil(b"- Ready? starting in 3 sec... -")

for i in range(100):
    # receive N and C
    r.recvuntil(b"N=")
    n = int(r.recvuntil(b" ")[:-1])
    r.recvuntil(b"C=")
    c = int(r.recvline()[:-1])

    start = 1
    mid = int(n / 2)
    end = n

    for t in range(c):
        payload = gen_payload(start, mid)  # start with front half
        r.sendline(payload)
        weight = int(r.recvline()[:-1])

        if weight % 10 == 0:
            # counterfeit in back
            start = mid + 1
            mid = start + int((end - start) / 2)
        else:
            # counterfeit in front
            end = mid
            mid = start + int((end - start) / 2)

    r.sendline(str(start).encode())  # submit

r.interactive()
```

![image](https://github.com/user-attachments/assets/7b88dad8-d2ce-43d4-a635-1bbe144c189b)
