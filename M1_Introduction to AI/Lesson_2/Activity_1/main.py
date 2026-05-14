'''
Title:
Sentiment Spy
Short description:
In this activity, you will interact with an AI-powered "Sentiment Spy" chatbot, which uses Textblob a natural language processing Library to analyze the emotions in their text messages (positive, neutral, or negative). You will explore how AI detects sentiment in real time and receive mission-themed feedback, making learning fun and engaging!
Pre-requisite:
pip install textblob colorama
python -m textblob.download_corpora
'''


import colorama

from colorama import Fore, Style

from textblob import TextBlob

colorama.init()

print(f"{Fore.CYAN} Welcome to spy !!!{Style.RESET_ALL}")

user_name = input(f"{Fore.MAGENTA} Please enter your name: {Style.RESET_ALL}").strip()

if not user_name:

    user_name = "Mystery Agent"

conversation_history = []

print(f"\n {Fore.CYAN}Hello, Agent {user_name}!")

print("Type a sentence, I will analyze your sentences with Textblob and show the sentiment ")

print(f"Type {Fore.YELLOW}'reset'{Fore.CYAN}, {Fore.YELLOW}'history'{Fore.CYAN}, "

      f"or {Fore.YELLOW}'exit'{Fore.CYAN} to quit.{Style.RESET_ALL}\n")

while True:
    user_input = input(f"{Fore.GREEN}>>{Style.RESET_ALL}").strip()
    if not user_input:
        print(f"{Fore.RED} Please enter some text or a valid command {Style.RESET_ALL}")
        continue

    if user_input.lower() == "exit":
        print(f"\n{Fore.BLUE} Exiting Sentiment Spy. Good Bye, Agent {user_name} ! {Style.RESET_ALL}")
        break

    elif user_input.lower() == "reset":
        conversation_history.clear()
        print(f"{Fore.CYAN} All conversation history cleared! {Style.RESET_ALL}")
        continue

    elif user_input.lower() == "history":
        if not conversation_history:
            print(f"{Fore.YELLOW} No conversational history yet. {Style.RESET_ALL}")

        else:
            print(f"{Fore.CYAN} Conversation History: {Style.RESET_ALL}")

            for idx, (text, polarity, sentiment_type) in enumerate(conversation_history, start=1):
                if sentiment_type == "Positive":
                    color = Fore.GREEN
                    emoji = "🌸"

                elif sentiment_type == "Negative":
                    color = Fore.RED
                    emoji = "😿"

                else:
                    color = Fore.YELLOW
                    emoji = "😐"

                print(f"{idx}.{color}{emoji} {text}" f"(Polarity: {polarity:.2f}), {sentiment_type} {Style.RESET_ALL}")

        continue

    polarity = TextBlob(user_input).sentiment.polarity
    if polarity > 0.25:
        sentiment_type = "Positive"
        color = Fore.GREEN
        emoji = "🌸"

    elif polarity < -0.25:
        sentiment_type = "Negative"
        color = Fore.RED
        emoji = "😿"

    else:
        sentiment_type = "Neutral"
        color = Fore.YELLOW
        emoji = "😐"

    conversation_history.append((user_input,polarity,sentiment_type))

    print(f"{color} {emoji} {sentiment_type} sentiment detected! "f"Polarity: {polarity:.2f}")



