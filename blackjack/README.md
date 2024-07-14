# [pwnable.kr] blackjack

> Hey! check out this C implementation of blackjack game!
> I found it online
> * http://cboard.cprogramming.com/c-programming/114023-simple-blackjack-program.html
>
> I like to give my flags to millionares.
> how much money you got?
>
> Running at : nc pwnable.kr 9009

## Bug

```c
/* blackjack.c */

//Global Variables
...
int bet;
...

int betting() //Asks user amount to bet
{
 printf("\n\nEnter Bet: $");
 scanf("%d", &bet);

 if (bet > cash) //If player tries to bet more money than player has
 {
		printf("\nYou cannot bet more money than you have.");
		printf("\nEnter Bet: ");
        scanf("%d", &bet);
        return bet;
 }
 else return bet;
} // End Function
```

`bet`은 `int`형 변수이기 때문에 음수를 넣어도 된다.

```c
/* blackjack.c */

         if(p>21) //If player total is over 21, loss
         {
             printf("\nWoah Buddy, You Went WAY over.\n");
             loss = loss+1;
             cash = cash - bet;
             printf("\nYou have %d Wins and %d Losses. Awesome!\n", won, loss);
             dealer_total=0;
             askover();
         }
```

지면 `cash`에서 `bet`을 빼는데, `bet`이 음수이면 졌을 때 오히려 돈이 늘어나게 된다.

## Exploit

![image](https://github.com/user-attachments/assets/8edebc85-0baa-482c-8212-5981700ed17d)

![image](https://github.com/user-attachments/assets/4480a0d6-9a0b-460b-a124-6c8c80b8e4d1)

![image](https://github.com/user-attachments/assets/f2dc4163-9df6-4452-9af0-7dc7377d56fe)
