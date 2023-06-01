#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(){

    printf("This game is called guess the number!\nKeep in mind, numbers range only from 1-20!\n");

    time_t t;
    srand ((unsigned)time(&t));
    int randomNumber = rand() % 21;
    int userNumber;
    int triesLeft = 5;
    while ( triesLeft >= 1 )
    {
        printf("You have %d tries left.\n", triesLeft);
        printf("Enter your number: ");
        scanf("%d", &userNumber);
        if( userNumber <= 20 && userNumber >= 1 )
            {
            if( userNumber == randomNumber )
                {
                    printf("You've guessed the number!\n");
                    exit(0);
                }
                else
                {
                    if(userNumber < randomNumber)
                        printf("Wrong number! My number is higher.\n\n");

                    else
                        printf("Wrong number! My number is lower.\n\n");
                }
        --triesLeft;
            }
        else
            printf("The number you've entered is not between 1 and 20!\n\n");
    }
    printf("You've ran out of tries!\n");
return 0;
}