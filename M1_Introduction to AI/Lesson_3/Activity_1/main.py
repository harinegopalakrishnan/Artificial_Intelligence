'''
Title
Rule based Chatbot
Short description:
Create an rule-based chatbot using Python.
'''

import re,random
from colorama import Fore, init

init(autoreset=True) #Print resets after use

destination={"beaches": ["Goa", "Maldives", "Pondicherry"],
             "mountains": ["Himalayas", "Everest", "Dodabetta"],
             "cities": ["Shimla", "Manali", "Kashmir"]}

jokes=["Why was the computer cold? It left its Windows open.",
       "Why did the smartphone need glasses? It lost all its contacts.",
       "Why was the keyboard always tired? It had too many shifts."]


def normalize_input(text):
    return re.sub(r"\s+", " ", text.strip().lower()) #removes extra spaces & converts to lower case

def recommendation_system():
    print(Fore.BLUE + "TBot: Beaches, Mountains or Cities?")
    preferred_choice = input(Fore. WHITE + "You:")
    preferred_choice = normalize_input(preferred_choice)

    if preferred_choice in destination:
        suggested = random.choice(destination[preferred_choice])
        print(Fore.CYAN+ f"TBot: How about {suggested}?")
        print(Fore.YELLOW+"TBot: Do you like this?(yes/no)")
        feedback = input(Fore.GREEN+"You: ").lower()

        if feedback == 'yes':
            print(Fore.GREEN+f"TBot: Enjoy at {suggested}!")
            helper()

        elif feedback == 'no':
            print(Fore.RED+"TBot: Let's try some other place")
            recommendation_system()

        else:
            print(Fore.RED+"TBot: I will suggest a new place")
            recommendation_system()

    else:
         print(Fore.RED + "TBot: Sorry, I don't have what you are looking for. Try again!!!")
         recommendation_system()


def package_helper():
    print(Fore.BLUE + "TBot: Give me the location?")
    location = normalize_input(input(Fore.MAGENTA + "You: "))
    print(Fore.BLUE + "TravelBot: Please share the number of days?")
    days = input(Fore.MAGENTA + "You: ")

    print(Fore.GREEN + f"TBot: Packing tips for {days} days in {location}:")
    print(Fore.GREEN + "Pack your clothes.")
    print(Fore.GREEN + "Take all your electronic gadgets.")
    print(Fore.GREEN + "Take your toiletteries.")
    print(Fore.GREEN + "Take some chocolates.")
    helper()

def joking_system():
    print(Fore.MAGENTA+f"TBot: {random.choice(jokes)}")
    helper()

def helper():
    print(Fore.YELLOW+"to proceed further please choose one among the following:")
    print(Fore.WHITE+"1)For travel spots (Type: recommend)")
    print(Fore.WHITE+"2)For packing tips (Type: packing)")
    print(Fore.WHITE+"3)For jokes (Type: joke)")
    print(Fore.WHITE+"4)To end conversation(Type: Bye)")

def chatbot():
    print(Fore.GREEN +"Hi, I am TBot")
    name = input("What is you name: ")
    print(f"Nice to meet you {name}")

    helper()

    while True:
        user = input(Fore.BLUE + f"{name}: ")
        user = normalize_input(user)

        if "recommend" in user:
            recommendation_system()
        elif "packing" in user:
            package_helper()
        elif "joke" in user:
            joking_system()
        elif "help" in user:
            helper()
        elif "bye" in user:
            print(Fore.MAGENTA + "Bye, Have a nice day")
            break
        else:
            print("Please rephrase ")

if __name__=="__main__":
    chatbot()

