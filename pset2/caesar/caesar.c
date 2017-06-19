#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <stdlib.h>

int main(int argc,string argv[]){
    if(argc == 2){
        // String to Integer
        int k =  atoi(argv[1]);
        printf("plaintext: ");
        string input = get_string();
        
        // Check if Null or not
        if (input != NULL){
            printf("ciphertext: ");
            // Traverse Over and Check
            for(int i = 0,n = strlen(input); i < n; i++){
                char c = input[i];
                if(c >= 'A' && c <= 'Z'){
                    c = (c-65+k) % 26;
                    printf("%c",(c+65));
                }else if (c >= 'a' && c <= 'z' ){
                    c = (c-97+k) % 26;
                    printf("%c",(c+97));
                }else{
                    printf("%c",c);
                }
            }
        printf("\n");
        return 0;
        }
        else{
            return 1;
        }
    }
    else{
        printf("Usage: ./caesar k\n");
        return 1;
    }
    
    return 0;
}