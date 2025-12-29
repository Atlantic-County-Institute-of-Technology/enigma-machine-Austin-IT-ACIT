import os
import inquirer3

example = "soething.txt"
file_sentence = 'text.txt'
file_KEY = 'KEY.txt'

encode = False
stringing = True
keying = True

encrypted = ""
upper_encrypted = ""
vig_cipher = ""
final = ""
string = ""
key = ""


def prompt_list_message(in_message, in_choices):
    # prompt question from input
    question = [
        inquirer3.List(
            "choice",
            message=in_message,
            choices=in_choices,
        ),
    ]
    # parse and return the response
    answer = inquirer3.prompt(question)
    # clears the terminal on both windows and linux
    os.system('cls' if os.name == 'nt' else 'clear')
    return answer["choice"]


def get_string():
    global stringing, string

    try:
        string = ""
        with open(file_sentence, 'r+') as file:
            string = file.read()
            print(f"your string is {string}")
            response = prompt_list_message("Please choose an option (string / sentence):", ["See File Text",
                                           "Change File Text", "Key"])
            if response == "See File Text":
                print(string)
                get_string()
            elif response == "Change File Text":
                print(f"The File says {string}")
                file.seek(0)
                file.truncate()
                content = input("What is the Sentence wanted to be shown? - ")
                file.write(content)
                os.system('cls' if os.name == 'nt' else 'clear')
            elif response == "Key":
                stringing = False
        return string

    except FileNotFoundError as e:
        print(e)
        print("Would you like to create or restart the code")
        response = prompt_list_message("Please choose an option (string / sentence):", ["Create File", "Restart Code",
                                       "Exit"])
        if response == "Create File":
            file_name = file_sentence
            content = input("What is the text wanted to be said?")

            # Open the file in write mode ('w')
            with open(file_name, 'w') as file:
                file.write(content)

            print(f"File '{file_name}' created and content written.")

        elif response == "Restart Code":
            pass
        elif response == "Exit":
            stringing = False
        return stringing


def get_key():
    global keying, key, temp_key
    key = ""
    try:
        with open(file_KEY, 'r+') as file:
            key = file.read()
            temp_key = key.upper()
            response = prompt_list_message("Please choose an option (key):", ["See File Text", "Change File Text",
                                           "Cypher"])
            if response == "See File Text":
                print(key)
                get_key()
            elif response == "Change File Text":
                print(f"The File says {key}")
                file.seek(0)
                file.truncate()
                content = input("What is the Key wanted to be shown? - ")
                file.write(content)
            elif response == "Cypher":
                keying = False
        return key, temp_key

    except FileNotFoundError as e:
        print(e)
        print("Would you like to create or restart the code")
        response = prompt_list_message("Please choose an option (key):", ["Create File", "Restart Code", "Exit"])
        if response == "Create File":

            file_name = file_KEY
            content = input("What is the text wanted to be said?")

            # Open the file in write mode ('w')
            with open(file_name, 'w') as file:
                file.write(content)

            print(f"File '{file_name}' created and content written.")

        elif response == "Restart Code":
            # main()
            pass
        elif response == "Exit":
            keying = False
    return keying


def vigenere_cipher():
    global string, key, final
    final = ''
    string = get_string()
    key = get_key()
    key_letters = [c.upper() for c in key if c.isalpha()]
    if not key_letters:
        print("No valid alphabetic key found. Aborting cipher operation.")
        return string, string

    key_index = 0
    if encode:
        for ch in string:
            if ch.isalpha():
                shift = ord(key_letters[key_index % len(key_letters)]) - ord('A')
                if ch.isupper():
                    final += chr((ord(ch) + shift - ord('A')) % 26 + ord('A'))
                else:
                    final += chr((ord(ch) + shift - ord('a')) % 26 + ord('a'))
                key_index += 1
            else:
                final += ch
        return string, final
    else:
        for ch in string:
            if ch.isalpha():
                shift = ord(key_letters[key_index % len(key_letters)]) - ord('A')
                if ch.isupper():
                    final += chr((ord(ch) - shift - ord('A')) % 26 + ord('A'))
                else:
                    final += chr((ord(ch) - shift - ord('a')) % 26 + ord('a'))
                key_index += 1
            else:
                final += ch
        return final, string

def main_menu():
    global encode, string, key, final, encrypted, stringing, keying
    response = prompt_list_message("Please choose an option:", ["See Files", "Encode", "Decode", "Exit"])
    if response == "See Files":
        print(f"files for phrases / sentences - ({file_sentence}), files for keys - ({file_KEY})")
        main_menu()

    elif response == "Encode":
        encode = True
        encrypted, final = vigenere_cipher()
        print(f"The normal phrase '{encrypted}' || and the Encoded phrase '{final}'")
        response = prompt_list_message("Please choose an option:", ["Restart", "Quit"])
        if response == "Restart":
            stringing = True
            keying = True
            main_menu()

        elif response == "Quit":
            exit()
    elif response == "Decode":
        encrypted, final = vigenere_cipher()
        print(f"The normal phrase '{encrypted}' || and the Decoded phrase '{final}'")
        response = prompt_list_message("Please choose an option:", ["Restart", "Quit"])
        if response == "Restart":
            stringing = True
            keying = True
            main_menu()

        elif response == "Quit":
            exit()
    elif response == "Exit":
        exit()


if __name__ == "__main__":
    main_menu()
