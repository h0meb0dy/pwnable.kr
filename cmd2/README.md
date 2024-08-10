# [pwnable.kr] cmd2

> Daddy bought me a system command shell.
> but he put some filters to prevent me from playing with it without his permission...
> but I wanna play anytime I want!
>
> ssh cmd2@pwnable.kr -p2222 (pw:flag of cmd1)
>
> [Attachment](./attachment)

```c
/* cmd2.c */

#include <stdio.h>
#include <string.h>

int filter(char* cmd){
	int r=0;
	r += strstr(cmd, "=")!=0;
	r += strstr(cmd, "PATH")!=0;
	r += strstr(cmd, "export")!=0;
	r += strstr(cmd, "/")!=0;
	r += strstr(cmd, "`")!=0;
	r += strstr(cmd, "flag")!=0;
	return r;
}

extern char** environ;
void delete_env(){
	char** p;
	for(p=environ; *p; p++)	memset(*p, 0, strlen(*p));
}

int main(int argc, char* argv[], char** envp){
	delete_env();
	putenv("PATH=/no_command_execution_until_you_become_a_hacker");
	if(filter(argv[1])) return 0;
	printf("%s\n", argv[1]);
	system( argv[1] );
	return 0;
}
```

`PATH`가 초기화되고 `/`가 필터링되어 있어서 일반적인 방법으로 명령어를 실행할 수 없다.

![image](https://github.com/user-attachments/assets/813faeaf-edaf-4286-a7a6-b13c482fb8df)

내장 명령어인 `command`의 `-p` 옵션을 사용하면 환경 변수가 기본값인 상태로 명령어를 실행할 수 있다.

![image](https://github.com/user-attachments/assets/2bc35999-fd51-47d2-a484-168703d19a91)
