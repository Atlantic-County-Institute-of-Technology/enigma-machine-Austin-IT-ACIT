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
            match response:
                case "See File Text":
                    print(string)
                    get_string()
                case "Change File Text":
                    print(f"The File says {string}")
                    file.seek(0)
                    file.truncate()
                    content = input("What is the Sentence wanted to be shown? - ")
                    file.write(content)
                    os.system('cls' if os.name == 'nt' else 'clear')
                case "Key":
                    stringing = False
        return string

    except FileNotFoundError as e:
        print(e)
        print("Would you like to create or restart the code")
        response = prompt_list_message("Please choose an option (string / sentence):", ["Create File", "Restart Code",
                                       "Exit"])
        match response:
            case "Create File":

                file_name = file_sentence
                content = input("What is the text wanted to be said?")

                # Open the file in write mode ('w')
                with open(file_name, 'w') as file:
                    file.write(content)

                print(f"File '{file_name}' created and content written.")

            case "Restart Code":
                pass
            case "Exit":
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
            match response:
                case "See File Text":
                    print(key)
                    get_key()
                case "Change File Text":
                    print(f"The File says {key}")
                    file.seek(0)
                    file.truncate()
                    content = input("What is the Key wanted to be shown? - ")
                    file.write(content)
                case "Cypher":
                    keying = False
        return key, temp_key

    except FileNotFoundError as e:
        print(e)
        print("Would you like to create or restart the code")
        response = prompt_list_message("Please choose an option (key):", ["Create File", "Restart Code", "Exit"])
        match response:
            case "Create File":

                file_name = file_KEY
                content = input("What is the text wanted to be said?")

                # Open the file in write mode ('w')
                with open(file_name, 'w') as file:
                    file.write(content)

                print(f"File '{file_name}' created and content written.")

            case "Restart Code":
                # main()
                pass
            case "Exit":
                keying = False
    return keying


def vigenere_cipher():
    global encrypted, upper_encrypted, final, vig_cipher, string, key, temp_key
    encrypted = ""
    upper_encrypted = ""
    temp_key = ""
    key = ""
    final = ""
    upper_pass = 0
    while stringing:
        string = get_string()
    while keying:
        key, temp_key = get_key()

    os.system('cls' if os.name == 'nt' else 'clear')

    for letter in string:

        if letter.isalpha():
            encrypted += letter
            if letter.islower():
                print(ord(letter))
                upper_encrypted += letter.upper()
                # ordinal_letter = ord(letter) - 32
                # print(letter, ord(letter))
                # print(chr(ordinal_letter), ordinal_letter)
                # upper_encrypted += ord(letter) - 32

            else:
                upper_encrypted += letter
        else:
            encrypted += letter
            upper_encrypted += letter
    for i in upper_encrypted[upper_pass]:
        for k in temp_key:
            # print(k)
            if i.isalpha():
                if encode:
                    combined_ordi = ord(k.upper()) - ord("A")
                    final_ordi = chr((ord(i) - 65 + combined_ordi) % 26 + 65)
                    print( i, combined_ordi, final_ordi, upper_encrypted, k,  key, temp_key)
                    vig_cipher += final_ordi
                    upper_pass += 1

                else:
                    combined_ordi = ord(k) - ord("A")
                    final_ordi = chr((ord(i) - 65 - combined_ordi) % 26 + 65)
                    vig_cipher += final_ordi
                    upper_pass += 1

            else:
                vig_cipher += i
    for j in encrypted:
        for r in vig_cipher:
            if j.isalpha():
                if j.islower():
                    final += chr(ord(r.lower()))
            else:
                final += j
    return encrypted, final


def main_menu():
    global encode, string, key, final, encrypted, stringing, keying
    response = prompt_list_message("Please choose an option:", ["See Files", "Encode", "Decode", "Exit"])
    match response:
        case "See Files":
            print(f"files for phrases / sentences - ({file_sentence}), files for keys - ({file_KEY})")
            main_menu()

        case "Encode":
            encode = True
            encrypted, final = vigenere_cipher()
            print(f"The normal phrase '{encrypted}' || and the Encoded phrase '{final}'")
            response = prompt_list_message("Please choose an option:", ["Restart", "Quit"])
            match response:
                case "Restart":
                    stringing = True
                    keying = True
                    main_menu()

                case "Quit":
                    exit()
        case "Decode":
            encrypted, final = vigenere_cipher()
            print(f"The normal phrase '{encrypted}' || and the Decoded phrase '{final}'")
            response = prompt_list_message("Please choose an option:", ["Restart", "Quit"])
            match response:
                case "Restart":
                    stringing = True
                    keying = True
                    main_menu()

                case "Quit":
                    exit()
        case "Exit":
            exit()


if __name__ == "__main__":
    main_menu()
