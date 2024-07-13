from pwn import *

hashcode = 0x21DD09EC
passcode = b""

# generate passcode
for i in range(5):
    passcode_int = int(hashcode / (5 - i))
    hashcode -= passcode_int
    for j in range(4):
        passcode += bytes([passcode_int % 0x100])
        passcode_int = passcode_int >> 8

s = ssh("col", "pwnable.kr", 2222, "guest")
p = s.process(["./col", passcode])
p.interactive()
