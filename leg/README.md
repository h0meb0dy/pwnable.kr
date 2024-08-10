# [pwnable.kr] leg

> Daddy told me I should study arm.
> But I prefer to study my leg!
>
> Download : http://pwnable.kr/bin/leg.c
> Download : http://pwnable.kr/bin/leg.asm
>
> ssh leg@pwnable.kr -p2222 (pw:guest)
>
> [Attachment](./attachment)

## key1

```
(gdb) disass key1
Dump of assembler code for function key1:
   0x00008cd4 <+0>:    push    {r11}        ; (str r11, [sp, #-4]!)
   0x00008cd8 <+4>:    add    r11, sp, #0
   0x00008cdc <+8>:    mov    r3, pc
   0x00008ce0 <+12>:    mov    r0, r3
   0x00008ce4 <+16>:    sub    sp, r11, #0
   0x00008ce8 <+20>:    pop    {r11}        ; (ldr r11, [sp], #4)
   0x00008cec <+24>:    bx    lr
End of assembler dump.
```

`+8`에서 `pc`를 `r3`에 넣고 그 값을 그대로 반환한다. `pc`는 program counter로 현재 실행 중인 명령어의 주소를 의미한다. 하지만 실제로 디버깅해보면 `r3`에는 저 시점에서 두 단계 뒤의 명령어의 주소가 들어가는 것을 확인할 수 있다.

![image](https://github.com/user-attachments/assets/6759c3a4-fc87-40c7-9fa4-4b717b068db9)

그 이유는 [이 링크](https://stackoverflow.com/questions/24091566/why-does-the-arm-pc-register-point-to-the-instruction-after-the-next-one-to-be-e)에 잘 설명되어 있다.

`leg.asm`을 보면 `0x8cdc`에서 `r3`에 `pc`를 넣고 있으므로, `key1()`의 반환값은 `0x8ce4`가 된다.

## key2

```
(gdb) disass key2
Dump of assembler code for function key2:
   0x00008cf0 <+0>:    push    {r11}        ; (str r11, [sp, #-4]!)
   0x00008cf4 <+4>:    add    r11, sp, #0
   0x00008cf8 <+8>:    push    {r6}        ; (str r6, [sp, #-4]!)
   0x00008cfc <+12>:    add    r6, pc, #1
   0x00008d00 <+16>:    bx    r6
   0x00008d04 <+20>:    mov    r3, pc
   0x00008d06 <+22>:    adds    r3, #4
   0x00008d08 <+24>:    push    {r3}
   0x00008d0a <+26>:    pop    {pc}
   0x00008d0c <+28>:    pop    {r6}        ; (ldr r6, [sp], #4)
   0x00008d10 <+32>:    mov    r0, r3
   0x00008d14 <+36>:    sub    sp, r11, #0
   0x00008d18 <+40>:    pop    {r11}        ; (ldr r11, [sp], #4)
   0x00008d1c <+44>:    bx    lr
End of assembler dump.
```

`+20`에서 `r3`에 `pc`를 넣고, 바로 다음에 `r3`에 4를 더한 후 그대로 반환한다.. `+20`에서 `r3`에는 `0x8d08`이 들어가고, 4를 더하면 `key2()`의 반환값은 `0x8d0c`가 된다.

## key3

```
(gdb) disass key3
Dump of assembler code for function key3:
   0x00008d20 <+0>:    push    {r11}        ; (str r11, [sp, #-4]!)
   0x00008d24 <+4>:    add    r11, sp, #0
   0x00008d28 <+8>:    mov    r3, lr
   0x00008d2c <+12>:    mov    r0, r3
   0x00008d30 <+16>:    sub    sp, r11, #0
   0x00008d34 <+20>:    pop    {r11}        ; (ldr r11, [sp], #4)
   0x00008d38 <+24>:    bx    lr
End of assembler dump.
```

`+8`에서 `r3`에 `lr`(return address)을 넣고 그대로 반환한다.

```
(gdb) disass main
Dump of assembler code for function main:
...
   0x00008d7c <+64>:    bl    0x8d20 <key3>
   0x00008d80 <+68>:    mov    r3, r0
...
End of assembler dump.
```

`key3()`가 반환된 후 돌아갈 주소는 `main+68`이다. 따라서 `key3()`의 반환값은 `0x8d80`이 된다.

## Exploit

세 함수의 반환값을 모두 더한 108400을 입력하면 플래그를 획득할 수 있다.

![image](https://github.com/user-attachments/assets/0ba5cec6-e71b-4eae-bf03-fc862c1d8b64)
