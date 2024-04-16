#Import resources, and download library resources for talking like normal
import random
import nltk
import requests
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from bs4 import BeautifulSoup

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
    
    #Check for specific words in user input
    if "hello" in tokens or "hi" in tokens:
        return random.choice(responses["greeting"])
    elif "bye" in tokens or "goodbye" in tokens:
        return random.choice(responses["farewell"])
    elif "thanks" in tokens or "thank you" in tokens:
        return random.choice(responses["thanks"])
    elif "wikipedia" in tokens:
        return handle_wikipedia_search(user_input)
        if resopnse:
            return response
        else:
            return random.choice(responses["default"])
    else:
        return random.choice(responses["default"])
    
#Function to search Wikipedia articles
def search_wikipedia(query):
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": query,
        "utf8": 1
    }
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            search_results = data.get('query', {}).get('search', [])
            return search_results
        else:
            print("Failed to retrieve search results from Wikipedia.")
            return None
    except Exception as e:
        print(f"Error searching Wikipedia: {e}")
        return None
    
#Function to retrieve content of a Wikipedia article by title
def get_wikipedia_article(title, chunk_size=500):
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "prop": "extracts",
        "titles": title,
        "utf8": 1
    }

    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            pages = data.get('query', {}).get('pages', {})
            if pages:
                page_id = list(pages.keys())[0]
                page = pages[page_id]

                if 'extract' in page:
                    article_content = page['extract']
                    soup = BeautifulSoup(article_content, 'html.parser')
                    text_content = soup.get_text()
                    paginated_content = paginate_text(text_content, chunk_size)
                    return paginated_content
                else:
                    print("Article content not found in Wikipedia API")
                    return None
            else:
                print("Article not found on Wikipedia.")
                return None
        else:
            print("Failed to retrieve Wikipedia article.")
            return None
    except Exception as e:
        print(f"Error retrieving Wikipedia article: {e}")
        return None

def handle_wikipedia_search(query):
    # Search Wikipedia for articles related to the query
    search_results = search_wikipedia(query)
    if search_results:
        print(f"Search results for '{query}':")
        for idx, result in enumerate(search_results, start=1):
            print(f"{idx}. {result['title']}")
        
        # Ask the user if they want to learn more about a specific article
        user_choice = input("Enter the number of the article you want to learn more about (or type 'exit' to exit): ").strip()
        if user_choice.lower() == 'exit':
            print("Exiting Wikipedia search.")
            return None
        try:
            article_index = int(user_choice) - 1
            if 0 <= article_index < len(search_results):
                article_title = search_results[article_index]['title']
                article_content = get_wikipedia_article(article_title)
                if article_content:
                    print(f"Content of '{article_title}' article:")
                    print(article_content)  # Print the article content for debugging
                    return article_content  # Return the article content
                else:
                    print("Failed to retrieve article content.")
                    return None
            else:
                print("Invalid choice. Please enter a valid number.")
                return None
        except ValueError:
            print("Invalid input. Please enter a number.")
            return None
    else:
        print(f"No search results found for '{query}'.")
        return None

def paginate_text(text, chunk_size=500):
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i+chunk_size])
    return chunks

#Main function to handle user interaction
def chat():
    print("Chatbot: Hello! How can I assist you today?")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "exit":
            print("Chatbot: Exiting chat")
            break
        response = generate_response(user_input)
        print("Chatbot:", response)

#Start the conversation
chat()

