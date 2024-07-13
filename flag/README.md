# [pwnable.kr] flag

> Papa brought me a packed present! let's open it.
>
> Download : http://pwnable.kr/bin/flag
>
> This is reversing task. all you need is binary

![image](https://github.com/user-attachments/assets/174b90e5-297f-4e33-9352-fc40b873160a)

바이너리에 포함된 문자열을 확인해 보면 [UPX](https://upx.sf.net)로 패킹된 바이너리임을 알 수 있다.

```bash
wget https://github.com/upx/upx/releases/download/v4.2.4/upx-4.2.4-amd64_linux.tar.xz
ls
tar -xvf upx-4.2.4-amd64_linux.tar.xz
rm upx-4.2.4-amd64_linux.tar.xz
ls upx-4.2.4-amd64_linux
upx-4.2.4-amd64_linux/upx -d flag
```

![image](https://github.com/user-attachments/assets/2242bffb-69f9-402a-929e-d87cdfc3d5a6)

패킹이 해제된 바이너리로부터 플래그를 획득할 수 있다.

![image](https://github.com/user-attachments/assets/ddd9fee3-8b0c-4b4b-be6a-458e427f09bc)

![image](https://github.com/user-attachments/assets/0f7e9375-737e-4971-be8f-4187c4c918e9)