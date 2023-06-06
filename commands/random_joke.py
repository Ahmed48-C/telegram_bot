import requests
import pyjokes
def random_joke():
    try:
        response = requests.get('https://official-joke-api.appspot.com/random_joke')
        response = response.json()
        joke = response["setup"] + response["punchline"]
        return joke
    except:
        # using get_joke() to generate a single joke
        #language is english
        #category is neutral
        joke = pyjokes.get_joke(language="en", category="all")
        return joke
    
random_joke()