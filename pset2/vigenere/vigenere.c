#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
int main(int argc,string argv[]){
    
    if(argc == 2){
        bool success = true;
        string k = argv[1];
        int lenofk = strlen(k);
        for(int i = 0;i < lenofk;i++){
            if(!isalpha(k[i])){
                success = false;
                break;
            }
        }
        
        if(success == true){
            printf("plaintext: ");
            string input = get_string();
            
            // Check if Null or not
            if (input != NULL){
                printf("ciphertext: ");
                // Traverse Over and Check
                // index stores current character of key to be added
                int index = 0;
                int shift = 0;
                for(int i = 0,n = strlen(input); i < n; i++){
                    char c = input[i];
                    
                    if(index == strlen(k)){
                        index = 0;
                    }
                    // Find the shift value 
                    shift = toupper(k[index]) - 65;
                    if(c >= 'A' && c <= 'Z'){
                        c = (c-65+shift)%26;
                        printf("%c",(c+65));
                        index++;
                    }else if(c >= 'a' && c <= 'z'){
                        c = (c-97+ shift)%26;
                        printf("%c",(c+97));
                        index++;
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
            printf("Usage: ./vigenere k\n");
            return 1;
        }
    }
    else{
        printf("Usage: ./vigenere k\n");
        return 1;
    }
    
    return 0;
}