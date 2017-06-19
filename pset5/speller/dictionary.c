/**
 * Implements a dictionary's functionality.
 */

#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include "dictionary.h"
int get_index(char c);
/**
 * Returns true if word is in dictionary else false.
 */
int wordcounter = 0; // count theno of words
node *root = NULL; // stores the trie tree
bool check(const char *word)
{
    // checking for existence of word in the dictionary
    node *ptr = root;
    // Traverse over each letter
    for(int i = 0,n = strlen(word);i < n; i++){
        int index = get_index(word[i]);
        
        // if node not present , word is not present
        if(ptr->child[index] == NULL)
            return false;
            
        ptr = ptr->child[index];
    }
    
    // if word present hence return true
    if(ptr != NULL && ptr->is_word == true)
        return true;
    
    return false;
}

node *getnode(){
    // Make a new node
    node * new_node = (node *)malloc(sizeof(struct node));
    
    for(int i = 0;i < MAXCHILD; i++)
        new_node->child[i] = NULL;
        
    new_node->is_word = false;
    
    return new_node;
}

int get_index(char c){
    
    //Get the index for each letter
    if(c >= 'a' && c <= 'z'){
        return (int)(c-'a');
    }
    
    if(c >= 'A' && c <= 'Z'){
        return (int)(c-'A');
    }
    // for apostrophe
    return 26;
}


void insert(node *root,char *word){
    node *ptr = root;
    
    // insert the word into trie tree
    for(int i = 0,n = strlen(word);i < n; i++){
        int index = get_index(word[i]);
        
        // if node not present create it
        if(ptr->child[index] == NULL)
            ptr->child[index] = getnode();
            
        ptr = ptr->child[index];
    }
    ptr->is_word = true;
}

/**
 * Loads dictionary into memory. Returns true if successful else false.
 */
bool load(const char *dictionary)
{
    // TODO
    root = getnode();
    //Get the word array
    //char *word = malloc((LENGTH+1) * sizeof(char));
    char word[LENGTH + 1];
    FILE * dict = fopen(dictionary,"r");
    if(dict == NULL){
        return false;
    }
    int read = 0;
    
    // read line by line
    read = fscanf(dict,"%s",word);
    while(read != EOF){
        insert(root,word);
       
        wordcounter++;
        read = fscanf(dict,"%s",word);
    }
    fclose(dict);
    //free(word);
    //EOF reached done!! loading
    if(read == EOF)
        return true;
    else
        return false;
}

/**
 * Returns number of words in dictionary if loaded else 0 if not yet loaded.
 */
unsigned int size(void)
{
    // returns the no of words that is wordcounter
    if(wordcounter == 0)
        return 0;
    else
        return wordcounter;
}





void freeNode(node *root)
{
    
    //delete node
    for (int i=0;i<27;i++)
    {
        if (root->child[i] != NULL)  // it has children which are not null   
            freeNode(root->child[i]);  // move to the children
    }
    free(root); //delete them
 }



/**
 * Unloads dictionary from memory. Returns true if successful else false.
 */
bool unload(void)
{
    
    // for each children of root
    for (int i=0;i<27;i++)           
    {
        // if root not null delete it
        if (root->child[i] != NULL)  
            freeNode(root->child[i]);
    }
    return true;         
}
