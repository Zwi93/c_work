import random

def file_reader ():
    "Function to read data from a .txt file and put it in a list"

    with open('dice_roller.txt') as file:
        dice_list = []

        for letter in file.read():
            dice_list.append(letter)

    return dice_list

def welcome_user():
    "Function to welcome the user and set out the rules of the game"

    print("Welcome User xyz, please read the rules carefully \n")
    print("Pick how many dice you would like to roll \n")

    number = input()

    return number

def roll_dice (dices, lines):
    "Function to roll dice (1 or 2) and give the output to screen."

    #Pick one number from the list using the module random;the list is the lines input variable.
    number = random.choice(lines)

    #Now print the number chosen by hte algorithmn.
    print(number)


#welcome_user()
dice_list = file_reader()
roll_dice(1, dice_list)