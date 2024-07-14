# [pwnable.kr] mistake

> We all make mistakes, let's move on.
> (don't take this too seriously, no fancy hacking skill is required at all)
>
> This task is based on real event
> Thanks to dhmonkey
>
> hint : operator priority
>
> ssh mistake@pwnable.kr -p2222 (pw:guest)

## Bug

```c
/* mistake.c */

int main(int argc, char* argv[]){
	
	int fd;
	if(fd=open("/home/mistake/password",O_RDONLY,0400) < 0){
		printf("can't open password %d\n", fd);
		return 0;
	}

	printf("do not bruteforce...\n");
	sleep(time(0)%20);

	char pw_buf[PW_LEN+1];
	int len;
	if(!(len=read(fd,pw_buf,PW_LEN) > 0)){
		printf("read error\n");
		close(fd);
		return 0;		
	}
...
}
```

`password` 파일을 열 때 `open()`의 return value를 `fd`에 넣고 이 값을 0과 비교하는 것을 의도한 것 같지만, 실제로는 `<`의 연산자 우선순위가 `=`보다 높기 때문에 `open()`의 return value를 0과 비교한 결과가 `fd`에 들어가게 된다. `open()`은 `password` 파일을 성공적으로 열었다면 0 이상의 값을 반환하기 때문에 0과 비교한 결과는 false가 되고, 따라서 `fd`에 0이 들어가게 된다.

결론적으로, `password` 파일로부터 읽어와야 할 password에 stdin으로 임의의 문자열을 넣을 수 있다.

## Exploit

`pw_buf`와 `pw_buf2`의 각 문자를 xor했을 때 `XORKEY`(1)가 나오도록 입력하면 플래그를 획득할 수 있다.

![image](https://github.com/user-attachments/assets/83b6ddf3-3147-48ae-a1ad-b9ea00fbc8d9)
