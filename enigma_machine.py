# developer - Austin Vaneman
# date - 12/2/25
# name - enigma machine
# about - create an “enigma machine” that will allow us to encode and decode messages using a simple rotational cipher. 
# program will be able to encrypt a message from text or file, and decrypt a file into text with the following behavior.

import os
import inquirer3

file_sentence = 'text.txt'
file_KEY = 'KEY.txt'

encode = False
stringing = True
keying = False

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

def change_string():
    with open(file_sentence, 'r+') as file:
        file.seek(0)
        file.truncate()
        content = input("What is the Sentence wanted to be shown? - ")
        file.write(content)
        os.system('cls' if os.name == 'nt' else 'clear')

def change_key():
    with open(file_KEY, 'r+') as file:
        file.seek(0)
        file.truncate()
        content = input("What is the Key wanted to be shown? - ")
        file.write(content)
        os.system('cls' if os.name == 'nt' else 'clear')

def get_string():
    global stringing, string, keying
    while stringing:
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
                    change_string()
                    get_string()
                elif response == "Key":
                    stringing = False
                    keying = True
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

    while keying:
        try:
            key = ""
            temp_key = ""
            with open(file_KEY, 'r+') as file:
                key = file.read()
                temp_key = key.upper()
                print(f"your Key is {key}")
                response = prompt_list_message("Please choose an option (key):", ["See File Text", "Change File Text",
                                               "Cypher"])
                if response == "See File Text":
                    print(key)
                    get_key()
                elif response == "Change File Text":
                    print(f"The File says {key}")
                    change_key()
                    get_key()
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
    global string, key, final, temp_key
    final = ''
    string = get_string()
    key, temp_key = get_key()
    key_letters = [c.upper() for c in key if c.isalpha()]
    if not key_letters:
        print("No valid alphabetic key found. Aborting cipher operation.")
        return string, string

    key_index = 0
    if encode:
        for ch in string:
            if ch.isalpha():
                shift = ord(temp_key[key_index % len(key_letters)]) - ord('A')
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
                shift = ord(temp_key[key_index % len(key_letters)]) - ord('A')
                if ch.isupper():
                    final += chr((ord(ch) - shift - ord('A')) % 26 + ord('A'))
                else:
                    final += chr((ord(ch) - shift - ord('a')) % 26 + ord('a'))
                key_index += 1
            else:
                final += ch
        return string, final

def main_menu():
    global encode, string, key, final, encrypted, stringing, keying
    response = prompt_list_message("Please choose an option:", ["See Files", "Encode", "Decode", "Exit"])
    if response == "See Files":
        print(f"files for phrases / sentences - ({file_sentence}), files for keys - ({file_KEY})")
        main_menu()

    elif response == "Encode":
        encode = True
        string, final = vigenere_cipher()
        print(f"The beginning phrase '{string}' || and the Ending phrase '{final}'")
        response = prompt_list_message("Please choose an option:", ["Restart", "Quit"])
        if response == "Restart":
            stringing = True
            keying = True
            encode = False
            main_menu()

        elif response == "Quit":
            exit()
    elif response == "Decode":
        string, final = vigenere_cipher()
        print(f"The Beginning phrase '{string}' || and the Ending phrase '{final}'")
        response = prompt_list_message("Please choose an option:", ["Restart", "Quit"])
        if response == "Restart":
            stringing = True
            keying = True
            encode = False
            main_menu()

        elif response == "Quit":
            exit()
    elif response == "Exit":
        exit()


if __name__ == "__main__":
    main_menu()
