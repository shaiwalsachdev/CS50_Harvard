#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <string.h>

int main(void){
    
    // Get input
    string name = get_string();
   
    if(name != NULL){
        // Traverse Over String
        // First Letter
        printf("%c",toupper(name[0]));
        
        // Other Letters
        for(int i = 0,n = strlen(name);i < n-1;i++){
            if(name[i] == ' '){
                printf("%c",toupper(name[i+1]));
            }
        }
        printf("\n");
    }
    return 0;
}