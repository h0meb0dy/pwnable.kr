# [pwnable.kr] fd

> Mommy! what is a file descriptor in Linux?
>
> * try to play the wargame your self but if you are ABSOLUTE beginner, follow this tutorial link:
> https://youtu.be/971eZhMHQQw
>
> ssh fd@pwnable.kr -p2222 (pw:guest)

## Analysis

```c
/* fd.c */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
char buf[32];
int main(int argc, char* argv[], char* envp[]){
        if(argc<2){
                printf("pass argv[1] a number\n");
                return 0;
        }
        int fd = atoi( argv[1] ) - 0x1234;
        int len = 0;
        len = read(fd, buf, 32);
        if(!strcmp("LETMEWIN\n", buf)){
                printf("good job :)\n");
                system("/bin/cat flag");
                exit(0);
        }
        printf("learn about Linux file IO\n");
        return 0;

}
```

`fd`는 `argv[1]`의 값을 조절하여 임의의 값으로 설정할 수 있다. `fd`가 0인 경우 `stdin`으로 `buf`에 최대 32바이트까지 입력할 수 있다.

## Exploit

`argv[1]`에 4660(`== 0x1234`)을 넣어서 `fd`를 0으로 설정하고 `buf`에 LETMEWIN을 입력하면 플래그를 획득할 수 있다.

![image](https://github.com/h0meb0dy/h0meb0dy/assets/104156058/10396f4b-fce8-4ab9-9d3f-113f90289abb)