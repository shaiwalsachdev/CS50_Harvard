import cs50
import math
def main():
    print("O hai! How much change is owed?")
    amount_dollars = cs50.get_float()
    while amount_dollars < 0:
        print("How much change is owed?")
        amount_dollars = cs50.get_float()
    
    #Round Function
    amount_cents = int(round(amount_dollars*100,2))
    num_of_coins = 0
    
    #Quarters
    num_of_coins = num_of_coins + int((amount_cents/25))
    amount_cents = amount_cents % 25
    
    #Dimes
    num_of_coins = num_of_coins + int((amount_cents/10))
    amount_cents = amount_cents % 10
    
    #Nickels
    num_of_coins = num_of_coins + int((amount_cents/5))
    amount_cents = amount_cents % 5
    
    #Pennies
    num_of_coins = num_of_coins + int((amount_cents/1))
    amount_cents = amount_cents % 1
    
    print(num_of_coins)
    
if __name__ == "__main__":
    main()
            