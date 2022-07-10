# [pwnable.kr] collision

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> Daddy told me about cool MD5 hash collision today.
> I wanna do something like that too!
>
> ssh col@pwnable.kr -p2222 (pw:guest)
>
> Release: [collision.zip](https://github.com/h0meb0dy/pwnable.kr/files/9079385/collision.zip)

## Mitigation

![image](https://user-images.githubusercontent.com/104156058/178152328-f4b63fbe-c33e-4f4d-8a11-ac674adaa3c9.png)

## Analysis

### `main()`

```c
	if(argc<2){
		printf("usage : %s [passcode]\n", argv[0]);
		return 0;
	}
```

`argv[1]`에 `passcode`를 입력해야 한다.

```c
	if(strlen(argv[1]) != 20){
		printf("passcode length should be 20 bytes\n");
		return 0;
	}
```

`passcode`의 길이는 20바이트여야 한다.

```c
	if(hashcode == check_password( argv[1] )){
		system("/bin/cat flag");
		return 0;
	}
```

전역 변수 `hashcode`의 값이 `check_password(passcode)`의 반환값과 같으면 플래그를 획득할 수 있다.

### `check_password()`

```c
unsigned long check_password(const char* p){
	int* ip = (int*)p;
	int i;
	int res=0;
	for(i=0; i<5; i++){
		res += ip[i];
	}
	return res;
}
```

인자로 받는 `p`(`passcode`)의 길이는 20바이트인데, 4바이트씩 나누어 정수 5개를 만든다. 이 정수 5개를 모두 합한 결과를 반환한다.

## Exploit

모두 더해서 `hashcode`의 값(`0x21dd09ec`)이 되는 5개의 정수를 문자열 형태로 이어붙여서 입력하면 된다.

![image](https://user-images.githubusercontent.com/104156058/178152573-502ead87-dc9c-40d3-8bef-0cef742367f1.png)

### Full exploit

```python
from pwn import *

LOCAL = False

passcode = p32(0x6c5cec8) + p32(0x6c5cec9) * 4

if LOCAL:
    r = process(['./release/col', passcode])
else:
    s = ssh('col', 'pwnable.kr', 2222, 'guest')
    r = s.process(['./col', passcode])

r.interactive()
```

```
$ python3 ex.py
[+] Connecting to pwnable.kr on port 2222: Done
[*] col@pwnable.kr:
    Distro    Ubuntu 16.04
    OS:       linux
    Arch:     amd64
    Version:  4.4.179
    ASLR:     Enabled
[+] Starting remote process bytearray(b'./col') on pwnable.kr: pid 154179
[*] Switching to interactive mode
daddy! I just managed to create a hash collision :)
```