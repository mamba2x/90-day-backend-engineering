def greet_developer(name,language):
    return f"Good afternoon {name}, please Keep building with {language}?"

names = input("enter your name:")
language = input("enter the language you are familiar with:")

print(greet_developer(names,language))