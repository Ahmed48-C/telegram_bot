import pyshorteners

def url_shortner(url):
    s = pyshorteners.Shortener()
    short_url = s.tinyurl.short(url)
    return short_url