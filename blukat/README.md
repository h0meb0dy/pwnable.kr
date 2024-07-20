# [pwnable.kr] blukat

> Sometimes, pwnable is strange...
> hint: if this challenge is hard, you are a skilled player.
>
> ssh blukat@pwnable.kr -p2222 (pw: guest)

![image](https://github.com/user-attachments/assets/2183017a-2cfb-4750-a874-6af572a62d00)

서버에 접속해 보면 `blukat_pwn` group에 속해 있고, `password` 파일은 group에 읽기 권한이 있다. 그래서 그냥 `password` 파일을 읽을 수 있다.

![image](https://github.com/user-attachments/assets/603d491b-7d48-4997-bf1c-c10c2fdbbba6)

파일 내용은 낚시다.

![image](https://github.com/user-attachments/assets/e0237d58-4810-46d4-bc3d-ad4fe07740da)
