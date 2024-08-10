# [pwnable.kr] input

> Mom? how can I pass my input to a computer program?
>
> ssh input2@pwnable.kr -p2222 (pw:guest)
>
> [Attachment](./attachment)

## Stage 1: argv

```c
/* input.c */

// argv
	if(argc != 100) return 0;
	if(strcmp(argv['A'],"\x00")) return 0;
	if(strcmp(argv['B'],"\x20\x0a\x0d")) return 0;
	printf("Stage 1 clear!\n");	
```

```python
# ex.py

from pwn import *

# stage 1
argv = ["" for i in range(100)]
argv[0] = "/home/input2/input"
argv[0x41] = "\x00"
argv[0x42] = "\x20\x0a\x0d"
p = process(argv)

p.interactive()
```

![image](https://github.com/user-attachments/assets/49e6940a-faeb-40e4-943d-7a989dbcc78d)

## Stage 2: stdio

```c
/* input.c */

	// stdio
	char buf[4];
	read(0, buf, 4);
	if(memcmp(buf, "\x00\x0a\x00\xff", 4)) return 0;
	read(2, buf, 4);
        if(memcmp(buf, "\x00\x0a\x02\xff", 4)) return 0;
	printf("Stage 2 clear!\n");
```

`stderr`로부터 입력을 받는 부분은, `"\x00\x0a\x02\xff"`를 파일에 저장해 놓고 그 파일을 `stderr`로 열도록 하면 된다.

```python
from pwn import *

# stage 1
argv = ["" for i in range(100)]
argv[0] = "/home/input2/input"
argv[0x41] = "\x00"
argv[0x42] = "\x20\x0a\x0d"
p = process(argv, stderr=open("/tmp/h0meb0dy/stderr", "rb"))

# stage 2
p.send(b"\x00\x0a\x00\xff")

p.interactive()
```

![image](https://github.com/user-attachments/assets/849b7b83-2d2b-4120-b527-6c99d7f14bec)

## Stage 3: env

```c
/* input.c */

	// env
	if(strcmp("\xca\xfe\xba\xbe", getenv("\xde\xad\xbe\xef"))) return 0;
	printf("Stage 3 clear!\n");
```

```python
p = process(
    argv,
    stderr=open("/tmp/h0meb0dy/stderr", "rb"),
    env={"\xde\xad\xbe\xef": "\xca\xfe\xba\xbe"},
)
```

![image](https://github.com/user-attachments/assets/13d24704-de3c-4d89-b363-449b28f64c48)

## Stage 4: file

```c
/* input.c */

	// file
	FILE* fp = fopen("\x0a", "r");
	if(!fp) return 0;
	if( fread(buf, 4, 1, fp)!=1 ) return 0;
	if( memcmp(buf, "\x00\x00\x00\x00", 4) ) return 0;
	fclose(fp);
	printf("Stage 4 clear!\n");	
```

```python
# ex.py

from pwn import *

# stage 4
with open("\x0a", "wb") as f:
    f.write(b"\x00\x00\x00\x00")

# stage 1
argv = ["" for i in range(100)]
argv[0] = "/home/input2/input"
argv[0x41] = "\x00"
argv[0x42] = "\x20\x0a\x0d"
p = process(
    argv,
    stderr=open("/tmp/h0meb0dy/stderr", "rb"),
    env={"\xde\xad\xbe\xef": "\xca\xfe\xba\xbe"},
)

# stage 2
p.send(b"\x00\x0a\x00\xff")

p.interactive()
```

![image](https://github.com/user-attachments/assets/35e9398e-e32f-4b7a-ab9d-b66b0a9e8fe9)

## Stage 5: network

```c
	// network
	int sd, cd;
	struct sockaddr_in saddr, caddr;
	sd = socket(AF_INET, SOCK_STREAM, 0);
	if(sd == -1){
		printf("socket error, tell admin\n");
		return 0;
	}
	saddr.sin_family = AF_INET;
	saddr.sin_addr.s_addr = INADDR_ANY;
	saddr.sin_port = htons( atoi(argv['C']) );
	if(bind(sd, (struct sockaddr*)&saddr, sizeof(saddr)) < 0){
		printf("bind error, use another port\n");
    		return 1;
	}
	listen(sd, 1);
	int c = sizeof(struct sockaddr_in);
	cd = accept(sd, (struct sockaddr *)&caddr, (socklen_t*)&c);
	if(cd < 0){
		printf("accept error, tell admin\n");
		return 0;
	}
	if( recv(cd, buf, 4, 0) != 4 ) return 0;
	if(memcmp(buf, "\xde\xad\xbe\xef", 4)) return 0;
	printf("Stage 5 clear!\n");
```

```python
# ex.py

from pwn import *
import socket

# stage 4
with open("\x0a", "wb") as f:
    f.write(b"\x00\x00\x00\x00")

# stage 1
argv = ["" for i in range(100)]
argv[0] = "/home/input2/input"
argv[0x41] = "\x00"
argv[0x42] = "\x20\x0a\x0d"

# stage 5
argv[0x43] = "12345"

p = process(
    argv,
    stderr=open("/tmp/h0meb0dy/stderr", "rb"),
    env={"\xde\xad\xbe\xef": "\xca\xfe\xba\xbe"},
)

# stage 2
p.send(b"\x00\x0a\x00\xff")

# stage 5
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
addr = ("localhost", 12345)
sock.connect(addr)
sock.send("\xde\xad\xbe\xef")

p.interactive()
```

![image](https://github.com/user-attachments/assets/b4da6f07-2d34-4d0c-ba00-6b1388ce9164)
