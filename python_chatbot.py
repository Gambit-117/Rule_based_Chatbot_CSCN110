#Import resources, and download library resources for talking like normal
import random
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
from nltk.tokenize import word_tokenize
from nltk import pos_tag

#Make reponses for AI
responses = {
    "greeting": ["Hello!", "Hi there!", "Hey!"],
    "farewell": ["Goodbye!", "Bye!", "See you later!"],
    "thanks": ["You're welcome!", "No problem!", "Anytime!"],
    "default": ["I'm not sure I understand.", "Could you please rephrase that?", "Sorry, I don't understand."]
    }

#Function to generate a response based on user input
def generate_response(user_input):

    #Tokenize user input for sending to AI
    tokens = word_tokenize(user_input.lower())

    #Perform part-of-speech tagging
    tagged_tokens = pos_tag(tokens)

    #Check for specific patterns in tagged tokens
    if any(tag in tagged_tokens for tag in ['NN', 'VB', 'JJ']):
        #If nouns, verbs, or adjectives are present, generate a response based on input
        return "I see you're talking about something interesting!"
    
    #Check for specific words in user input
    user_input = user_input.lower()
    if "hello" in user_input or "hi" in user_input:
        return random.choice(responses["greeting"])
    elif "bye" in user_input or "goodbye" in user_input:
        return random.choice(responses["farewell"])
    elif "thanks" in user_input or "thank you" in user_input:
        return random.choice(responses["thanks"])
    else:
        return random.choice(responses["default"])
    
#Main function to handle user interaction
def chat():
    print("Chatbot: Hello! How can I assist you today?")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "exit":
            print("Chatbot: Goodbye!")
            break
        response = generate_response(user_input)
        print("Chatbot:", response)

#Start the conversation
chat()

