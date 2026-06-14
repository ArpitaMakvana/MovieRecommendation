import random

# Predefined list of horror movies
horror_movies = ["The Shining", "The Exorcist", "Get Out", "Hereditary", "A Nightmare on Elm Street", "Psycho", "The Conjuring"]

# Function to recommend a horror movie
def recommend_horror_movie():
    return random.choice(horror_movies)

# Main loop for interacting with the chatbot
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        print("Chatbot: Goodbye!")
        break
    if "horror" in user_input.lower():
        response = recommend_horror_movie()
        print("Chatbot:", response)
    else:
        print("Chatbot: I recommend horror movies. If you want a horror movie recommendation, just ask!")

