# This is a program for "UniBuddy," a chatbot designed to assist freshmen in universities.
# It collects Information, such as a user's name, favorite color, age and country.
# It gives personalized responses based on the information collected.
# It answers predefined questions about sports, student support, libraries, restaurants and clubs.

def collect_information():
    user_info = {}
    user_info['name'] = input("What's your name? ")
    user_info['favourite_color'] = input("What's your favorite color? ")
    user_info['age'] = input("How old are you? ")
    user_info['country'] = input("Which country are you from? ")
    return user_info

def give_personalised_response(user_info):
    print(f"Welcome to university, {user_info['name']} from {user_info['country']}!")
    print(f"Ah, {user_info['favourite_color']} is a great color. You'll find many such vibrant colors around campus.")
    if int(user_info['age']) < 20:
        print("You're quite young, you have a lot of exciting experiences ahead of you in university!")
    else:
        print("A great age to start your university journey. There's so much to explore and learn!")

def answer_questions():
    print("I can answer some basic questions about university life. Ask me something!")
    while True:
        question = input("Your question (type 'exit' to quit): ").lower()
        if question == 'exit':
            break
        elif 'library' in question:
            print("The library is at the center of the campus and is open from 8 am to 10 pm.")
        elif 'restaurant' in question:
            print("There are various restaurants and cafes on campus, offering a range of cuisines.")
        elif 'clubs' in question:
            print("There are over 20 clubs and societies. You can join them during the club week or contact the student union.")
        elif 'sports' in question:
            print("Our university has a variety of sports teams and facilities. You can join a team or just enjoy the facilities for fitness.")
        elif 'support' in question:
            print("The student support center offers counseling, academic advice, and other assistance. They're here to help you settle in.")
        else:
            print("I'm not sure about that, but I can find out more for you.")

# Main Program
user_info = collect_information()
give_personalised_response(user_info)
answer_questions()