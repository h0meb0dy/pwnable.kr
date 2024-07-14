from pwn import *

# r = remote("pwnable.kr", 9007)
r = remote("0", 9007)  # in pwnable.kr server


# return b'<start> <start + 1> ... <end>'
def gen_payload(start, end):
    payload = b""
    for i in range(start, end):
        payload += str(i).encode() + b" "
    payload += str(end).encode()
    return payload


r.recvuntil(b"- Ready? starting in 3 sec... -")

for i in range(100):
    # receive N and C
    r.recvuntil(b"N=")
    n = int(r.recvuntil(b" ")[:-1])
    r.recvuntil(b"C=")
    c = int(r.recvline()[:-1])

    start = 1
    mid = int(n / 2)
    end = n

    for t in range(c):
        payload = gen_payload(start, mid)  # start with front half
        r.sendline(payload)
        weight = int(r.recvline()[:-1])

        if weight % 10 == 0:
            # counterfeit in back
            start = mid + 1
            mid = start + int((end - start) / 2)
        else:
            # counterfeit in front
            end = mid
            mid = start + int((end - start) / 2)

    r.sendline(str(start).encode())  # submit

r.interactive()
