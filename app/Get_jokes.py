import requests
import random
from bs4 import BeautifulSoup

# фунцция для получения анекдота
def get_joke() -> BeautifulSoup:
    url = "https://anekdotov.net/anekdot/black/index-page-" + \
        str(random.randint(1, 35)) + ".html"
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    jokes = soup.find_all("div", class_="anekdot")
    joke = random.choice(jokes)
    return joke.text
