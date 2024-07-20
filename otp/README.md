# [pwnable.kr] otp

> I made a skeleton interface for one time password authentication system.
> I guess there are no mistakes.
> could you take a look at it?
>
> hint : not a race condition. do not bruteforce.
>
> ssh otp@pwnable.kr -p2222 (pw:guest)

## Analysis

```c
/* otp.c */

    int fd = open("/dev/urandom", O_RDONLY);
    if(fd==-1) exit(-1);

    if(read(fd, otp, 16)!=16) exit(-1);
    close(fd);

    sprintf(fname, "/tmp/%llu", otp[0]);
    FILE* fp = fopen(fname, "w");
    if(fp==NULL){ exit(-1); }
    fwrite(&otp[1], 8, 1, fp);
    fclose(fp);
```

`/dev/urandom`으로부터 가져온 난수를 `/tmp` 디렉토리에 파일을 만들어서 저장한다. 이 파일의 내용과 `argv[1]`이 같으면 플래그를 획득할 수 있다.

## Exploit

`ulimit`의 옵션 중에 프로세스에서 생성하는 파일의 최대 크기를 지정하는 옵션이 있다.

![image](https://github.com/user-attachments/assets/34823227-983e-47de-90a0-ebd9ac7e5010)

이 값을 0으로 바꾸면 `/tmp` 디렉토리에 만들어지는 파일에 값을 쓸 수 없기 때문에 `passcode`가 난수의 역할을 하지 못하게 된다.

![image](https://github.com/user-attachments/assets/97651e7b-d863-4647-9d13-7aabd56261b5)

하지만 실행해 보면 에러가 발생한다. 로컬에서 똑같이 실행했을 때 `core` 파일을 통해 file size가 한계에 도달하여 `SIGXFSZ` signal이 발생한 것을 확인할 수 있다. `otp`를 실행할 때 `SIGXFSZ` signal을 무시하도록 설정하면 플래그를 획득할 수 있다.

`SIGXFSZ`의 경우 Python에서 subprocess를 실행했을 때 기본적으로 무시하도록 설정되어 있다.

![image](https://github.com/user-attachments/assets/12e1c662-01c0-4f6b-8f64-be495ba0d967)

`subprocess` 모듈의 `Popen()` 함수의 매개변수 중 `restore_signals`의 값이 `True`이면 `SIG_IGN`로 설정된 signal들이 `SIG_DFL`로 복원된다. 기본값이 `True`이므로 `restore_signals=False`를 인자로 전달하면 `SIGXFSZ` signal이 그대로 무시된다.

![image](https://github.com/user-attachments/assets/c0a7020f-300f-481e-ab1a-9e6b4aa01a1f)
