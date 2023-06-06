import requests

def random_quote():
    url = "https://quotes15.p.rapidapi.com/quotes/random/"

    querystring = {"language_code":"en"}

    headers = {
        "X-RapidAPI-Key": "9d3bd00d0fmsh299ee009acda650p1f6768jsn691079464863",
        "X-RapidAPI-Host": "quotes15.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    quote = response.json()["content"]

    return quote