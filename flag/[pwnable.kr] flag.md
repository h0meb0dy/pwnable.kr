# [pwnable.kr] flag

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> Papa brought me a packed present! let's open it.
>
> Download : http://pwnable.kr/bin/flag
>
> This is reversing task. all you need is binary
>
> Release: [flag.zip](https://github.com/h0meb0dy/pwnable.kr/files/9079449/flag.zip)

## Analysis

```
$ strings flag | grep UPX
UPX!
$Info: This file is packed with the UPX executable packer http://upx.sf.net $
$Id: UPX 3.08 Copyright (C) 1996-2011 the UPX Team. All Rights Reserved. $
UPX!
UPX!
```

바이너리에 포함된 문자열들을 확인해보면 UPX로 패킹된 바이너리임을 알 수 있다. 먼저 패킹을 풀고 분석해야 한다.

> https://github.com/upx/upx/releases/download/v3.96/upx-3.96-amd64_linux.tar.xz

```
$ ./upx-3.96-amd64_linux/upx -d flag
                       Ultimate Packer for eXecutables
                          Copyright (C) 1996 - 2020
UPX 3.96        Markus Oberhumer, Laszlo Molnar & John Reiser   Jan 23rd 2020

        File size         Ratio      Format      Name
   --------------------   ------   -----------   -----------
    883745 <-    335288   37.94%   linux/amd64   flag

Unpacked 1 file.
```

### `main()`

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  char *dest; // [rsp+8h] [rbp-8h]

  puts("I will malloc() and strcpy the flag there. take it.", argv, envp);
  dest = (char *)malloc(100LL);
  strcpy(dest, flag);
  return 0;
}
```

전역 변수 `flag`에 있는 데이터를 `dest`로 복사한다.

## Solve

`flag`에 있는 데이터는 아래와 같다.

![image](https://user-images.githubusercontent.com/104156058/178154387-8782e62a-fc6c-4479-91bf-ef2bb246c201.png)

그대로 플래그에 인증하면 된다.

```
UPX...? sounds like a delivery service :)
```