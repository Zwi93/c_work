/* Module to test malloc and realloc functions in C */

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main ()
{
    char *ptr_string;
    size_t nbytes = 10;
    ssize_t no_of_characters;
    char *input_string;

    printf("To end chat, type Enter!\n");
    input_string = "Hi User!";
    puts(input_string);

    do 
    {
        
        ptr_string = (char *) malloc (nbytes + 1);
        no_of_characters = getline (&ptr_string, &nbytes, stdin);
        puts(ptr_string);
        free(ptr_string);
        
    }

    while ( no_of_characters != 1);
    
    return 0;    
}