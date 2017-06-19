import cs50
import sys

def main():
    if len(sys.argv) == 2:
        k = int(sys.argv[1])
        print("plaintext: ",end ="")
        input = cs50.get_string();
        
        if input != None:
            print("ciphertext: ",end ="")
            #Traverse Over and Check
            for i in range(len(input)):
                
                c = ord(input[i])
                if c >= (65) and c <= (65+26):
                    c = (c-65+k) % 26
                    print(chr(c+65),end="")
                elif c >= (97)  and c <= (97+26):
                    c = (c-97+k) % 26
                    print(chr(c+97),end="")
                else:
                    print(chr(c),end="")
        
            print()
            exit(0)
        
        else:
            exit(1)
                    
    else:
        print("Usage: ./caesar k")
        exit(1)
        
    exit(0)
if __name__ == "__main__":
    main()
            