import re
from bs4 import BeautifulSoup
import requests
import sys

try:
    if len(sys.argv) < 2:
        throw

    req = requests.get(sys.argv[1])

    soup = BeautifulSoup(req.text, 'html.parser')

    list_of_links = list(
        map(lambda x: str(x), soup.find_all(class_="dropdown-item")))

    reg = re.compile(r"/deck/download")

    res = list(filter(reg.search, list_of_links))

    deck_id = res[0].split("\"")[3].split("/")[-1]

    req_deck_info = requests.get(
        f'https://www.mtggoldfish.com/deck/arena_download/{deck_id}')

    deck_soup = BeautifulSoup(req_deck_info.text, 'html.parser')

    print(deck_soup.find("textarea").text)
except:
    print("Something happened")
