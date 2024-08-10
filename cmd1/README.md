# [pwnable.kr] cmd1

> Mommy! what is PATH environment in Linux?
>
> ssh cmd1@pwnable.kr -p2222 (pw:guest)
>
> [Attachment](./attachment)

```c
/* cmd1.c */

#include <stdio.h>
#include <string.h>

int filter(char* cmd){
	int r=0;
	r += strstr(cmd, "flag")!=0;
	r += strstr(cmd, "sh")!=0;
	r += strstr(cmd, "tmp")!=0;
	return r;
}
int main(int argc, char* argv[], char** envp){
	putenv("PATH=/thankyouverymuch");
	if(filter(argv[1])) return 0;
	system( argv[1] );
	return 0;
}
```

`PATH` 환경 변수가 초기화되기 때문에 `cat`의 full path인 `/bin/cat`을 사용해야 하고, `flag` 필터링은 `fla*`로 우회할 수 있다.

![image](https://github.com/user-attachments/assets/68d26159-7f22-4a76-babc-d006524bef2d)
