# developer - Austin Vaneman
# date - 12/2/25
# name - enigma machine
# about - create an “enigma machine” that will allow us to encode and decode messages using a simple rotational cipher. 
# program will be able to encrypt a message from text or file, and decrypt a file into text with the following behavior.

import os
import inquirer3

# Default file names used by the program for message text and key
file_sentence = 'text.txt'
file_KEY = 'KEY.txt'

# Flags used to track program state in the interactive menu
encode = False      # True when performing encryption; False for decryption
stringing = True    # Controls the "get_string" interactive loop
keying = False      # Controls the "get_key" interactive loop

# Working variables used by the cipher functions
encrypted = ""      # placeholder for encrypted output (not heavily used)
upper_encrypted = ""# placeholder for uppercase encrypted (unused here)
vig_cipher = ""     # placeholder for vigenere cipher (unused)
final = ""          # final transformed string returned by cipher
string = ""         # message text read from file
key = ""            # key text read from file


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
    """Replace the contents of the sentence file with user input.

    Opens `file_sentence` for read/write, truncates it, writes the new
    content provided by the user, and clears the terminal.
    """
    with open(file_sentence, 'r+') as file:
        file.seek(0)
        file.truncate()
        content = input("What is the Sentence wanted to be shown? - ")
        file.write(content)
        os.system('cls' if os.name == 'nt' else 'clear')

def change_key():
    """Replace the contents of the key file with user input.

    Mirrors `change_string()` but operates on the `file_KEY` file.
    """
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
            # Read the message text from the sentence file and let the user
            # view or change it. If the user chooses to proceed to the key,
            # exit this loop so `get_key()` can run next.
            string = ""
            with open(file_sentence, 'r+') as file:
                string = file.read()
                print(f"your string is {string}")
                response = prompt_list_message(
                    "Please choose an option (string / sentence):",
                    ["See File Text", "Change File Text", "Key"],
                )
                if response == "See File Text":
                    print(string)
                    get_string()
                elif response == "Change File Text":
                    print(f"The File says {string}")
                    change_string()
                    get_string()
                elif response == "Key":
                    # move on to key selection
                    stringing = False
                    keying = True
            return string

        except FileNotFoundError as e:
            # If the sentence file doesn't exist, offer to create it or exit.
            print(e)
            print("Would you like to create or restart the code")
            response = prompt_list_message(
                "Please choose an option (string / sentence):",
                ["Create File", "Restart Code", "Exit"],
            )
            if response == "Create File":
                file_name = file_sentence
                content = input("What is the text wanted to be said?")

                # Create and write the new file
                with open(file_name, 'w') as file:
                    file.write(content)

                print(f"File '{file_name}' created and content written.")

            elif response == "Restart Code":
                # simply continue looping; main_menu will handle flow
                pass
            elif response == "Exit":
                stringing = False
            return stringing


def get_key():
    global keying, key, temp_key

    while keying:
        try:
            # Read the key file, show the key, and allow user to change it or
            # proceed to ciphering. `temp_key` stores the uppercase key used
            # for computing shifts.
            key = ""
            temp_key = ""
            with open(file_KEY, 'r+') as file:
                key = file.read()
                temp_key = key.upper()
                print(f"your Key is {key}")
                response = prompt_list_message(
                    "Please choose an option (key):",
                    ["See File Text", "Change File Text", "Cypher"],
                )
                if response == "See File Text":
                    print(key)
                    get_key()
                elif response == "Change File Text":
                    print(f"The File says {key}")
                    change_key()
                    get_key()
                elif response == "Cypher":
                    # move on to cipher operation
                    keying = False
            return key, temp_key

        except FileNotFoundError as e:
            # If the key file doesn't exist, offer to create it or exit.
            print(e)
            print("Would you like to create or restart the code")
            response = prompt_list_message(
                "Please choose an option (key):",
                ["Create File", "Restart Code", "Exit"],
            )
            if response == "Create File":
                file_name = file_KEY
                content = input("What is the text wanted to be said?")

                # Create and write the new file
                with open(file_name, 'w') as file:
                    file.write(content)

                print(f"File '{file_name}' created and content written.")

            elif response == "Restart Code":
                # main() could be called here if desired
                pass
            elif response == "Exit":
                keying = False
            return keying


def vigenere_cipher():
    global string, key, final, temp_key
    final = ''
    string = get_string()
    key, temp_key = get_key()
    # Build a list of alphabetic key characters and validate presence
    key_letters = [c.upper() for c in key if c.isalpha()]
    if not key_letters:
        print("No valid alphabetic key found. Aborting cipher operation.")
        return string, string

    # Walk through the input string, applying Vigenère shifts for letters
    key_index = 0
    if encode:
        # Encryption: shift each letter forward by the key letter amount
        for ch in string:
            if ch.isalpha():
                shift = ord(temp_key[key_index % len(key_letters)]) - ord('A')
                if ch.isupper():
                    final += chr((ord(ch) + shift - ord('A')) % 26 + ord('A'))
                else:
                    final += chr((ord(ch) + shift - ord('a')) % 26 + ord('a'))
                key_index += 1
            else:
                # Preserve non-letter characters unchanged
                final += ch
        return string, final
    else:
        # Decryption: shift each letter backward by the key letter amount
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
        # Show the file names used for the sentence and key
        print(f"files for phrases / sentences - ({file_sentence}), files for keys - ({file_KEY})")
        main_menu()

    elif response == "Encode":
        # Set encoding mode and run the cipher
        encode = True
        string, final = vigenere_cipher()
        print(f"The beginning phrase '{string}' || and the Ending phrase '{final}'")
        response = prompt_list_message("Please choose an option:", ["Restart", "Quit"])
        if response == "Restart":
            # reset state to allow another run
            stringing = True
            keying = True
            encode = False
            main_menu()
        elif response == "Quit":
            exit()
    elif response == "Decode":
        # Decode (encryption flag remains False)
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
