import cs50

def main():
    print("Height: ",end="")
    height = cs50.get_int()
    while height < 0 or height > 23:
        print("Height: ",end="")
        height = cs50.get_int()
    
    
    for i in range(1,height+1):
        for j in range(height - i,0,-1):
            print(" ",end = "")
        for k in range(i+1,0,-1):
            print("#",end = "")
        
        print()


if __name__ == "__main__":
    main()
            
        
    
    