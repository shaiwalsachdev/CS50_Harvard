#include <stdio.h>
#include <cs50.h>

int main(void)
{
    printf("Minutes: ");
    int min = get_int();
    int bottles = (128 * (1.5* min) )/ 16;
    printf("Bottles: %i\n",bottles);
}


