//Module to practice using struct data type in C.

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main ()
{
    struct personal_data
    {
        char name[100];
        char address[1000];
        int year_of_birth;
        int month_of_birth;
        int day_of_birth;
    };

    struct personal_data_extended
    {
        char name[100];
        char address[1000];
        char contact[10];
        int year_of_birth;
        int month_of_birth;
        int day_of_birth;
    };
    
    
    //Initialize variables of type personal_data at compile time.
    struct  personal_data person1 = 
    {
        "Zwima, Mudau",
        "Rivonia, Sandton",
        1993,
        9, 
        16
    };
    
    struct personal_data person2 = 
    {
        "Ele, Mudau",
        "Braam, Joburg",
        1992, 
        3,
        2
    };
    
    //Now we perform dynamical allocation of variables.
    struct personal_data* person_ptr1;
    struct personal_data* person_ptr2;

    person_ptr1 = (struct personal_data*) malloc (sizeof (struct personal_data));

    strcpy (person_ptr1->name, "Zwi, Tshuvhere");
    strcpy (person_ptr1->address, "Hamashau");
    person_ptr1->year_of_birth = 1993;
    person_ptr1->month_of_birth = 9;
    person_ptr1->day_of_birth = 15;

    person_ptr2 = (struct personal_data*) malloc (sizeof (struct personal_data));
    
    strcpy (person_ptr2->name, "Ele, Tshuvhere");
    strcpy (person_ptr2->address, "Hamashau");
    person_ptr2->year_of_birth = 1992;
    person_ptr2->month_of_birth = 4;
    person_ptr2->day_of_birth = 5;

    //free(person_ptr2);

    puts ("Data contained:");
    puts (person1.name);
    puts (person2.name);
    puts (person_ptr1->name);
    puts (person_ptr2->name);

    struct personal_data_extended* person_ptr3;
     

    return 0;
}