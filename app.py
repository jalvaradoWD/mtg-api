import re
from bs4 import BeautifulSoup
import requests
import sys
import urllib.parse as url_parse
import json
import time

# TEST URL
# "https://www.mtggoldfish.com/archetype/standard-esper-midrange-mid#paper"

scryfall_api = "https://api.scryfall.com"
app_args = sys.argv


def card_format(card_name):
    if "\r" in card_name:
        card_name = card_name[0:-1]

    card_name_split = card_name.split(" ")

    card_amount = card_name_split[0]
    card_text_name = " ".join(card_name_split[1:])

    return {"card_amount": card_amount, "card_name": card_text_name}


def get_deck_url(url: str):
    base_url = url[0:28]
    req = requests.get(url)

    soup = BeautifulSoup(req.text, 'html.parser')

    list_of_links = list(
        map(lambda x: str(x), soup.find_all(class_="dropdown-item")))

    reg = re.compile(r"/deck/download")

    res = list(filter(reg.search, list_of_links))

    download_link = res[0].split("\"")[3]

    deck_text = requests.get(f"{base_url}{download_link}", stream=True)

    return list(map(card_format, deck_text.text.split("\n")))


def get_deck_json_data(deck_list):
    base_url_api = "https://api.scryfall.com/cards/named?exact="

    api_call_card_list = []
    json_data = []

    for card in deck_list:
        api_call_card_list.append(
            f"{base_url_api}{url_parse.quote(card['card_name'])}")

    for req in api_call_card_list:
        api_req = requests.get(req).text
        json_data.append(json.loads(api_req))
        time.sleep(0.1)

    return json_data


precious_data = get_deck_json_data(get_deck_url(app_args[1]))

with open("deck.json", "w+") as f:
    f.write(json.dumps(precious_data))
    f.close()
