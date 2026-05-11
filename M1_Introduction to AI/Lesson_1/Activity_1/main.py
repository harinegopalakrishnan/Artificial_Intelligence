#Title: Hello AI

name = input("Hello! I am AI Bot, Please enter you name: ")
print(f"Nice to meet you,{name} !!!")
print("How are you feeling today (Good/Bad)?: ")
mood = input().lower()

if mood == "good":
    print("That's great")
elif mood == "bad":
    print("I am sorry to hear that !!!")
else:
    print("Please try again later")

print(f"It is nice chatting with you {name}, Bye!!!")