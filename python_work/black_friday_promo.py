import random 

words_list = ['b', 'l', 'a', 'c', ]
black_friday = 'blackfriday'

word_list = random.sample(black_friday, 6)

word_string = ''.join([elem for elem in word_list])

print(word_string)