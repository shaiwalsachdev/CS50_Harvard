#include <stdio.h>
#include <cs50.h>
#include <math.h>
int main(){
    printf("O hai! How much change is owed?\n");
    float amount_dollars = get_float();
    while(amount_dollars < 0){
        printf("How much change is owed?\n");
        amount_dollars = get_float();
    }
    //Using Round function 
    int amount_cents = (int)round(amount_dollars*100);
    int num_of_coins = 0;
    
    //Quarters(25¢)
    num_of_coins = num_of_coins + (int)(amount_cents/25);
    amount_cents = amount_cents % 25; 
    
    //Dimes (10¢)
    num_of_coins = num_of_coins + (int)(amount_cents/10);
    amount_cents = amount_cents % 10; 
    
    //Nickels (5¢)
    num_of_coins = num_of_coins + (int)(amount_cents/5);
    amount_cents = amount_cents % 5; 
    
    //Pennies (1¢)
    num_of_coins = num_of_coins + (int)(amount_cents/1);
    amount_cents = amount_cents % 1; 
    
    
    printf("%i\n",num_of_coins);
}

