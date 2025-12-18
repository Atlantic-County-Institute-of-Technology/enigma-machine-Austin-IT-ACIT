# developer - Austin Vaneman
# date - 12/2/25
# name - enigma machine
# about - create an “enigma machine” that will allow us to encode and decode messages using a simple rotational cipher. 
# program will be able to encrypt a message from text or file, and decrypt a file into text with the following behavior.

import os
import inquirer3

ROTATION = 3

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


def generate_number_list():
    WORD_LIST = []
    with open('assets/words_alpha.txt', 'r') as dictionary:
        for word in dictionary.readlines():
            WORD_LIST.append(word.strip())
    return WORD_LIST


def decode():
    global ROTATION
    encrypted = caesar_cipher_decode(message_file, ROTATION)
    print(f"The Rotation is {ROTATION}")
    print(encrypted)
    response = prompt_list_message("Please choose an option:", ["Increase Rotation", "Decrease Rotation", "Menu"])
    match response:
        case "Increase Rotation":
            encrypted = ""
            increase_rotation()
            decode()
        case "Decrease Rotation":
            encrypted = ""
            decrease_rotation()
            decode()
        case "Menu":
            main()


def encode():
    global ROTATION
    WORD_LIST = generate_number_list()
    encrypted = caesar_cipher(message_file, ROTATION)
    print(f"The Rotation is {ROTATION}")
    print(encrypted)
    response = prompt_list_message("Please choose an option:", ["Increase Rotation", "Decrease Rotation", "Auto", "Menu"])
    match response:
        case "Increase Rotation":
            encrypted = ""
            increase_rotation()
            encode()
        case "Decrease Rotation":
            encrypted = ""
            decrease_rotation()
            encode()
        case "Auto":
            auto = True
            while auto:
                if encrypted in WORD_LIST:
                    auto = False
                    encrypted = ""
                    increase_rotation()
                    encode()
                else:
                    auto = False
        case "Menu":
            main()


def increase_rotation():
    global message_file
    global ROTATION
    ROTATION += 1
    encrypted = ""
    encrypted = caesar_cipher_decode(message_file, ROTATION)
    return ROTATION, encrypted


def decrease_rotation():
    global message_file
    global ROTATION
    ROTATION -= 1
    encrypted = ""
    encrypted = caesar_cipher(message_file, ROTATION)
    return ROTATION, encrypted


def caesar_cipher(message_file, rotation):
    encrypted = ""
    for letter in message_file:
        if letter.isalpha():
            charset = (65 if letter.isupper() else 97)
            encrypted += chr((ord(letter) - charset - rotation) % 26 + charset)
        else:
            encrypted += letter
    return encrypted


def caesar_cipher_decode(message_file, rotation):
    encrypted = ""
    for letter in message_file:
        if letter.isalpha():
            charset = (65 if letter.isupper() else 97)
            encrypted += chr((ord(letter) - charset + rotation) % 26 + charset)
        else:
            encrypted += letter
    return encrypted


def remove_file():
    os.remove(message_file)

message_file = 'text.txt'

def main():
    while True:
        with open("text.txt", 'r+') as f:
            try:
                print("Text file is already created")
                response = prompt_list_message("Please choose an option:", ["Remove", "Change Content", "See Content", "Exit", "Encode", "Decode"])
                match response:
                    case "Exit":
                        print("Goodbye!")
                        exit()
                    case "Remove":
                        f.close()
                        os.remove(f)
                        print("Message file has been removed")
                    case "Change Content":
                        print("Changing Content")
                        content = input("What is the text wanted to be said?")
                        # Open the file in write mode ('w')
                        file.write(content)
                    case "Encode":
                        encode()
                    case "Decode":
                        decode()
                    case "See Content":
                        message_test = open('text.txt', 'r')
                        content = message_test.read()
                        print(content)
                        message_test.close()
            except FileNotFoundError:
                message_file = 'text.txt'
                print("Error: The file 'non_existent_file.txt' was not found.")
                print(f)
                # You could also create the file here, or prompt the user for a valid path.
                response = prompt_list_message("Please choose an option:", ["Create one", "Leave"])
                match response:
                    case "Create one":
                        file_name = "text.txt"
                        content = input("What is the text wanted to be showed?")

                        # Open the file in write mode ('w')
                        with open(file_name, 'w') as file:
                            file.write(content)
                        print(f"File '{file_name}' created and content written.")
                    case "Leave":
                        exit()


if __name__ == "__main__":
    main()