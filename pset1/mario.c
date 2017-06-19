#include <stdio.h>
#include <cs50.h>

int main(void)
{
    printf("Height: ");
    int height = get_int();
    while(height < 0 || height > 23)
    {
        printf("Height: ");
        height = get_int();
    }
    
    //Outer Loop for Number of Lines (Height)
    for(int i = 1;i <= height; i++){
        //Printing Spaces
        for(int j = height - i;j > 0; j--)
            printf(" ");
        //Printing Hash
        for(int k = i + 1; k > 0; k--)
            printf("#");
        
        printf("\n");
    }
    
}