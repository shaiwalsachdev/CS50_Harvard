/**
 * helpers.c
 *
 * Helper functions for Problem Set 3.
 */
 
#include <cs50.h>

#include "helpers.h"

/**
 * Returns true if value is in array of n values, else false.
 */
bool search(int value, int values[], int n)
{
    // TODO: implement a searching algorithm
    //Your implementation must return false immediately if n is non-positive.
    if(n < 0)
        return false;
    
    int low = 0;
    int high = n - 1;
    // Low pointer, High Pointer
    while(low <= high){
        // While we have elements
        int middle = (low + high)/2;
        if(values[middle] == value)
            return true;
        else if(value > values[middle])
                low = middle + 1;
        else
            high = middle - 1;
    }
    return false;
}

/**
 * Sorts array of n values.
 */
void sort(int values[], int n)
{
    // TODO: implement a sorting algorithm
    // Selection Sort
    for(int i = 0;i < n-1; i++){
        int mini = i;
        // Pick Minimum and Swap it along to the front
        for(int j = i + 1;j < n; j++){
            if(values[j] < values[mini]){
                mini = j;
            }
        }
        if(mini != i){
            int t = values[mini];
            values[mini] = values[i];
            values[i] = t;
        }
    }
    return;
}
