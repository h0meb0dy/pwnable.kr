# [pwnable.kr] random

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> Daddy, teach me how to use random value in programming!
>
> ssh random@pwnable.kr -p2222 (pw:guest)
>
> Release: [random.zip](https://github.com/h0meb0dy/pwnable.kr/files/9080247/random.zip)

## Mitigation

![image](https://user-images.githubusercontent.com/104156058/178171269-3696fc60-0f58-4adf-9a5a-a00c1368895a.png)

## Analysis

```c
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

`rand()`의 반환값을 `random()`에 넣고, `key`를 입력받아서 `key`와 `random`을 xor한 결과가 `0xdeafbeef`이면 플래그를 준다.

## Exploit

랜덤 시드를 설정하지 않으면 `rand()`의 반환값은 프로그램을 실행할 때마다 항상 같다. GDB에서 `rand()`의 반환값을 보면 `0x6b8b4567`인데, 이 값과 `0xdeadbeef`를 xor한 결과를 `key`에 넣어주면 된다.

![image](https://user-images.githubusercontent.com/104156058/178172639-70219549-97c9-4e83-888c-098e44e53c17.png)

```
random@pwnable:~$ ./random
-1255736440
Good!
Mommy, I thought libc random is unpredictable...
```