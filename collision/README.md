# [pwnable.kr] collision

> Daddy told me about cool MD5 hash collision today.
> I wanna do something like that too!
>
> ssh col@pwnable.kr -p2222 (pw:guest)

## Analysis

```c
/* col.c */

#include <stdio.h>
#include <string.h>
unsigned long hashcode = 0x21DD09EC;
unsigned long check_password(const char* p){
        int* ip = (int*)p;
        int i;
        int res=0;
        for(i=0; i<5; i++){
                res += ip[i];
        }
        return res;
}

int main(int argc, char* argv[]){
        if(argc<2){
                printf("usage : %s [passcode]\n", argv[0]);
                return 0;
        }
        if(strlen(argv[1]) != 20){
                printf("passcode length should be 20 bytes\n");
                return 0;
        }

        if(hashcode == check_password( argv[1] )){
                system("/bin/cat flag");
                return 0;
        }
        else
                printf("wrong passcode.\n");
        return 0;
}
```

`check_password()`는 `p`에 저장된 문자열을 앞에서부터 4바이트씩 잘라서 5개의 정수를 만들고 모두 더한 결과를 반환한다.

`check_password(argv[1])`의 값이 `hashcode`와 같으면 플래그를 획득할 수 있다.

## Exploit

```python
from pwn import *

hashcode = 0x21DD09EC
passcode = b""

# generate passcode
for i in range(5):
    passcode_int = int(hashcode / (5 - i))
    hashcode -= passcode_int
    for j in range(4):
        passcode += bytes([passcode_int % 0x100])
        passcode_int = passcode_int >> 8

s = ssh("col", "pwnable.kr", 2222, "guest")
p = s.process(["./col", passcode])
p.interactive()
```

![image](https://github.com/h0meb0dy/h0meb0dy/assets/104156058/31b01b0a-a268-4ac7-a65a-63bddeb19796)
