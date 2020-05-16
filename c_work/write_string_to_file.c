#include <stdio.h>

int main ()
{
    int index;
    FILE *my_stream;
    my_stream = fopen("test.txt", "w");

    fprintf(my_stream, "Head1 Head2 Head3\n"); 
    for (index = 0; index < 4; index++)
    {
        fprintf(my_stream, "%f %f %f\n", 1.0, 1.0, 1.0);
    }
    fclose(my_stream);
}