//Memory allocation module.

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main ()
{
    char *my_string;
    size_t number = (size_t) 3;
    my_string = (char *) malloc(1);

    *my_string = "z";

    printf("%s\n", my_string);  



    return 0;
}