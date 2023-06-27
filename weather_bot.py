import requests
import spacy
import sys
import time


nlp = spacy.load("en_core_web_md")

api_key = ""
#Enter your OpenWeather API key in the line above.


def menu():
    while True:
        print('''
              \r--- MENU ---
              \rInteract with the Chatbot (Enter a)
              \rEnd the program (Enter b)''')
        choice = input("\nWhat would you like to do? ")
        if choice in ['a', 'b']:
            return choice
        else:
            input('''
                  \rPlease only choose one of the options above.
                  \rEither the letter a or b (in lowercase.)
                  \nPress enter to try again. ''')


def get_weather(city_name):
    api_url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={}".format(city_name, api_key)
    response = requests.get(api_url)
    response_dict = response.json()
    weather = response_dict['weather'][0]["description"]
    if response.status_code == 200:
        return weather
    else:
        print('[!] HTTP {0} calling [{1}]'.format(response.status_code, api_url))
        return None


def chatbot():
    while True:
        user_statement = input('''
                        \rAsk the chatbot what the weather is in any city.
                        \rExample: What is the weather like in Atlanta today?
                        \r\nEnter your question: ''')
        weather = nlp("Current weather in a city")
        statement = nlp(user_statement)
        min_similarity = 0.71
        if weather.similarity(statement) >= min_similarity:
            for ent in statement.ents:
                if ent.label_ == "GPE": # Geopolitical Entity
                    city = ent.text
                    break
                else:
                    return "You need to tell me a city to check."
            city_weather = get_weather(city)
            if city_weather is not None:
                return "In " + city + ", the current weather is: " + city_weather + "."
            else:
                return "Something went wrong."
        else:
            print("Sorry, I don't understand that. Please rephrase your statement.")
            continue
    
    
def app():
    app_running = True
    while app_running:
        choice = menu()
        if choice == "a":
            result = chatbot()
            print(result)
            time.sleep(1.5)
            continue
        elif choice == "b":
            print("Goodbye! The program will close down now.")
            sys.exit()
            
            
def main():
    app()