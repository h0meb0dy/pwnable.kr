# [pwnable.kr] shellshock

> Mommy, there was a shocking news about bash.
> I bet you already know, but lets just make it sure :)
>
> ssh shellshock@pwnable.kr -p2222 (pw:guest)
>
> [Attachment](./attachment)

## Bug

Shellshock 취약점(CVE-2014-6271)은 `bash` 쉘이 실행될 때 환경 변수를 초기화하는 과정에서 발생하는 취약점이다.

![image](https://github.com/user-attachments/assets/09dbb632-d1c5-4e7d-95c5-8f6a2675ae5b)

정상적인 `bash`에서는 위와 같이 문자열의 형태에 관계없이 그대로 문자열로 등록되는데,

![image](https://github.com/user-attachments/assets/b37d6d53-16f8-4b26-89e7-ee3d974e1007)

취약점이 존재하는 `bash`를 실행하면 함수 형태의 문자열을 함수로 바꿔서 등록하는 것을 확인할 수 있다.

만약 함수 정의 뒤에 다른 명령어를 추가하면 함수를 등록한 후 그 명령어까지 이어서 실행하게 된다.

![image](https://github.com/user-attachments/assets/0bf1d5de-408f-4dac-9a3a-c419f11fd36d)

즉, `bash`가 실행됨과 동시에 원하는 명령어를 실행할 수 있다.

```
/* shellshock.c */

#include <stdio.h>
int main(){
        setresuid(getegid(), getegid(), getegid());
        setresgid(getegid(), getegid(), getegid());
        system("/home/shellshock/bash -c 'echo shock_me'");
        return 0;
}
```

`shellshock.c`에서 `bash`를 실행하는데 `shellshock` 바이너리에 setgid가 걸려 있기 때문에 `bash`에서 `flag`를 읽을 수 있다.

## Exploit

![image](https://github.com/user-attachments/assets/d7972ba0-4b77-42a5-a8b0-5e1ccd01e8cc)
