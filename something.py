import os
import inquirer3

file_sentence = 'text.txt'
file_KEY = 'KEY.txt'


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


# response = prompt_list_message("Please choose an option:", ["Increase Rotation", "Decrease Rotation", "Menu"])
# match response:
#     case "Increase Rotation":
#         pass
#     case "Decrease Rotation":
#         pass
#     case "Menu":
#         pass


def get_string():
    try:
        if os.path.exists(file_sentence):
            sentence = open('text.txt', 'r')
            string = sentence.read()
            return string
    except:
        print('There is no text.txt file available')


def get_key():
    try:
        if os.path.exists(file_KEY):
            sentence = open('KEY.txt', 'r')
            key = sentence.read()
            return key
    except:
        print('There is no KEY.txt file available')


def vigenere_cipher():

    encrypted = ""
    upper_encrypted = ""
    vig_cipher = ""
    final = ""
    inner_pass = 0
    for letter in string:

        if letter.isalpha():
            encrypted += letter
            if letter.islower():

                ordinal_letter = ord(letter) - 32
                # print(letter, ord(letter))
                # print(chr(ordinal_letter), ordinal_letter)
                upper_encrypted += chr(ordinal_letter)

            else:
                upper_encrypted += letter

        else:
            encrypted += letter
            upper_encrypted += letter

    for i in upper_encrypted:
        for k in key[inner_pass]:
            if i.isalpha():
                combined_ordi = ord(k) - ord("A")
                final_ordi = chr((ord(i) - 65 + combined_ordi) % 26 + 65)
                vig_cipher += final_ordi
                inner_pass += 1
                if inner_pass >= len(key):
                    inner_pass = 0
                break

            else:
                vig_cipher += i
                break

    inner_pass = 0
    for i in encrypted:
        for k in vig_cipher[inner_pass]:

            if i.isalpha() and i.islower():
                change_lower = k.lower()
                final += chr(ord(change_lower))
                inner_pass += 1
                break

            else:
                final += i
                break
    return encrypted, vig_cipher, final


key = get_key()
string = get_string()
cipher = vigenere_cipher()
print(cipher)
# print(STRING)


# # def prompt_list_message(in_message, in_choices):
# #     # prompt question from input
# #     question = [
# #         inquirer3.List(
# #             "choice",
# #             message=in_message,
# #             choices=in_choices,
# #         ),
# #     ]
# #     # parse and return the response
# #     answer = inquirer3.prompt(question)
# #     # clears the terminal on both windows and linux
# #     os.system('cls' if os.name == 'nt' else 'clear')
# #     return answer["choice"]

# def decode():
#     global ROTATION
#     encrypted = caesar_cipher_decode(Phrase, ROTATION)
#     print(f"The Rotation is {ROTATION}")
#     print(encrypted)
#     # response = prompt_list_message("Please choose an option:", ["Increase Rotation", "Decrease Rotation", "Menu"])
#     # match response:
#     #     case "Increase Rotation":
#     #         encrypted = ""
#     #         increase_rotation()
#     #         decode()
#     #     case "Decrease Rotation":
#     #         encrypted = ""
#     #         decrease_rotation()
#     #         decode()
#     #     case "Menu":
#     #         main()


# def encode():
#     global ROTATION
#     # WORD_LIST = generate_number_list()
#     encrypted = caesar_cipher(Phrase, ROTATION)
#     print(f"The Rotation is {ROTATION}")
#     print(encrypted)
#     # response = prompt_list_message("Please choose an option:", ["Increase Rotation", "Decrease Rotation", "Auto", "Menu"])
#     # match response:
#     #     case "Increase Rotation":
#     #         encrypted = ""
#     #         increase_rotation()
#     #         encode()
#     #     case "Decrease Rotation":
#     #         encrypted = ""
#     #         decrease_rotation()
#     #         encode()
#     #     case "Auto":
#     #         auto = True
#     #         while auto:
#     #             if encrypted in WORD_LIST:
#     #                 auto = False
#     #                 encrypted = ""
#     #                 increase_rotation()
#     #                 encode()
#     #             else:
#     #                 auto = False
#     #     case "Menu":
#     #         main()


# def increase_rotation():
#     global Phrase
#     global ROTATION
#     ROTATION += 1
#     encrypted = ""
#     encrypted = caesar_cipher_decode(Phrase, ROTATION)
#     return ROTATION, encrypted


# def decrease_rotation():
#     global Phrase
#     global ROTATION
#     ROTATION -= 1
#     encrypted = ""
#     encrypted = caesar_cipher(Phrase, ROTATION)
#     return ROTATION, encrypted


# def caesar_cipher(Phrase, rotation):
#     encrypted = ""
#     for letter in Phrase:
#         if letter.isalpha():
#             charset = (65 if letter.isupper() else 97)
#             encrypted += chr((ord(letter) - charset - rotation) % 26 + charset)
#         else:
#             encrypted += letter
#     return encrypted


# def caesar_cipher_decode(Phrase, rotation):
#     encrypted = ""
#     for letter in Phrase:
#         if letter.isalpha():
#             charset = (65 if letter.isupper() else 97)
#             encrypted += chr((ord(letter) - charset + rotation) % 26 + charset)
#         else:
#             encrypted += letter
#     return encrypted