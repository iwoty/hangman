import datetime  # for time counting
import random

font_green = ('\033[1;32;40m')  # changing font colors
font_blue = ('\033[1;37;44m')
font_red = ('\033[1;37;41m')
font_normal = ('\033[1;37;0m')


def make_it_short(word, length):
    '''Make length of the word equal to chosen length and returns it'''
    if len(str(word)) <= length:
        word = (length - len(str(word))) * " " + str(word)
        return str(word)
    elif len(str(word)) > length:
        word = str(word)[0:length]
        return str(word)


def split_names(from_index, to_index, line_to_split):
    '''Split names by '|' to list and join them to string and returns it'''
    name = []
    for i in range(from_index, to_index):
        name.append(line_to_split[i])
    name = (" ".join(name))
    return name


def add_spaces_between(word, is_underlined):
    '''Adding spaces between letters and returns it'''
    splitted_word = []
    for i in range(len(word)):
        if word[i] == (" "):
            splitted_word.append("    ")
        elif is_underlined is True:
            splitted_word.append("_")
        elif is_underlined is False:
            splitted_word.append(word[i])
    splitted_word = (" ".join(splitted_word))
    return splitted_word


def print_ascii_arts(i):
    '''Create list with ASCII arts, print with life_points'''
    ascii_art_list = []
    try:
        ascii_art_list.append(open('hangman5.txt', 'r'))  # open txt files with ASCII arts and create list with them
        ascii_art_list.append(open('hangman4.txt', 'r'))
        ascii_art_list.append(open('hangman3.txt', 'r'))
        ascii_art_list.append(open('hangman2.txt', 'r'))
        ascii_art_list.append(open('hangman1.txt', 'r'))
    except FileNotFoundError:
        print(font_red, 'Missing some of ASCII arts files :( Bye!', font_normal)
        exit()
    print(ascii_art_list[i].read())


def print_line(n):
    '''Printing line with lower dash at n-length'''
    print('_'*n)


def main():
    wrong_word = []  # list of wrong guessed whole words
    wrong_letter = []  # list of wrong guessed letters

    print_line(88)
    print("Welcome to ***The Hangman 4.20 Game***")
    name = input("Enter your name: ")
    print_line(88)
    print("Now we will choose name of a capital for you!")
    print("You have 5 lifes, you will lose 1 for wrong answer!")

    # random choice of line from txt file, making it upper, split to list with country, '|' and capital
    try:
        random_line = random.choice(list(open('capitals_list.txt'))).upper().split()
    except FileNotFoundError:
        print(font_red, 'Missing capital_list.txt file :( Bye!', font_normal)
        exit()

    country = split_names(0, random_line.index("|"), random_line)
    capital = split_names(random_line.index("|")+1, len(random_line), random_line)
    print(capital)
    capital_underlined = add_spaces_between(capital, True)
    capital_splitted = add_spaces_between(capital, False)
    # game
    time_start = datetime.datetime.today()  # set stopwatch on
    life_points = 5  # number of lifes
    tries = 0  # counter of tries

    while life_points > 0:  # game (loop) is working only if you have at least 1 life point

        print_line(88)
        print(font_green, "Your number of lifes is:", life_points, font_normal, "\n")  # life_points
        print(font_blue, "Your name of the capital to guess is:", capital_underlined, font_normal)  # _ _ _ _ _ _ _
        print_line(50)
        print("Wrong letters guesses are:", ", ".join(wrong_letter))  # join to list of wrong guessed letters
        print("Wrong words guesses are:", ", ".join(wrong_word))  # join to list of wrong guessed words
        print_line(50)

        stage = input("Do you want to guess ONE LETTER (enter L) or WHOLE WORD (enter W)? ")

        if stage.upper() == "W":  # guessing whole word
            guess_word = input("Enter word: ")

            if guess_word.upper() == capital:  # CORRECT ANSWER - exit from loop - goes to 'You win'
                break
            else:
                life_points -= 2  # wrong answer = -2 life points
                print("Wrong guess! You lose 2 life points!")
                print_ascii_arts(life_points)
                wrong_word.append(guess_word.upper())

        elif stage.upper() == "L":  # guessing one letter
            guess_letter = input("Enter letter: ")
            try:
                # locating index of a guessed letter(s) #zwraca error
                guess_letter_id = capital_splitted.index(guess_letter.upper())

                guess_letter_id = [i for i, v in enumerate(capital_splitted)
                                   if v == guess_letter.upper()]  # same as one line up for multiple words names

                capital_underlined = list(capital_underlined)

                for i in range(len(guess_letter_id)):
                    capital_underlined[guess_letter_id[i]] = guess_letter.upper()

                capital_underlined = ("".join(capital_underlined))

                if capital_underlined == capital_splitted:
                    break  # exit from try

            except ValueError:
                life_points -= 1
                print("Wrong letter!")
                print_ascii_arts(life_points)
                wrong_letter.append(guess_letter.upper())
        tries += 1

        if life_points == 1:  # if you have left with 1 life point - you're getting a hint
            print_line(88)
            print(font_green, "You have left with only 1 life point!", font_normal)
            print(font_green, "We have a hint for you!", font_normal)
            print(font_green, "Name of a country is:", country, font_normal)
            print_line(88)

    if life_points < 1:
        print(font_green, "You lose!!!!!!", font_normal)
        print(font_green, "The name of a capital was:", capital, font_normal)
        result = "lose"
    else:
        print(font_green, "You win!!!!!!!", font_normal)
        result = "win"

    # HIGHSCORE
    time_end = datetime.datetime.today()  # set stopwatch off
    gamedate = datetime.date.today()  # date of game
    player_time = (time_end - time_start).seconds  # how long did player play
    points = int(tries) * int(player_time)

    players_score = [make_it_short(i, 16) for i in [name, gamedate, player_time, tries, capital, points, result]]
    with open('highscores.txt', 'a') as highscore_add:  # opens and adds
        highscore_add.write(" | ".join(players_score) + "\n")

    # highscore highscore_sorted
    highscore = []
    with open('highscores.txt', 'r') as read:  # opens highscores.txt in read mode
        for i in range(sum(1 for line in open('highscores.txt'))):
            highscore.append(read.readline().split("|"))    # rozjebujemy liste zeby dostac sie do punktow

    highscore = sorted(highscore, key=lambda y: y[int(5)])    # sortujemy wg punktow

    print_line(129)
    print("You guessed (or not ;) ) after", int(tries), "tries. It took you", player_time, "seconds.")
    print(font_green, "So far highscores (less points is better): ", font_normal, "\n")
    print("      Name       |       Date       |      Time        |      Tries       |   Guessed word   |"
          "      Points      | Result")
    print_line(129)

    for i in range(len(highscore)):
        highscore[i] = ("|".join(highscore[i]))
    print("".join(highscore[0:10]))
    print_line(129)


if __name__ == '__main__':
    main()
