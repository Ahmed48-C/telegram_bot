import requests

def youtube_search(search):
    url = "https://simple-youtube-search.p.rapidapi.com/search"
    

    querystring = {"query": search, "type": "video", "safesearch": "false"}

    headers = {
        "X-RapidAPI-Key": "9d3bd00d0fmsh299ee009acda650p1f6768jsn691079464863",
        "X-RapidAPI-Host": "simple-youtube-search.p.rapidapi.com"
    }
    try:
        response = requests.get(url, headers=headers, params=querystring)
        
        urls = []
        
        result = []

        results = response.json()["results"]

        for video in results:
            url = video["url"]
            urls.append(url)
        
        for link in urls[0:5]:
            result.append(link)
        return result
    except:
        return "Failed to search, try again later."
    
youtube_search("python gui tutorial")