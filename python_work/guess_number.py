import random 

number_guessed = input('Guess a number from 0 to 10: ')

random_number = random.randint(0, 10)

if number_guessed == random_number:
    print('Correct')
else:
    print('Incorrect')