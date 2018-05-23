import requests
import json
import sys
import re

file = sys.argv[1]

URL = 'https://lookup.binlist.net/'

bank_set = set()


def card_request(card_number):
    r = requests.get(URL + card_number, headers={'Accept-Version':"3"})
    if 200 <= r.status_code <= 299:
        card_dict = r.json()
        if card_dict['bank']:
            bank_set.add(card_dict['bank']['name'])

with open(file) as f:
    file_json = json.load(f)
    for card in file_json:
        card_number = re.search(r'^(\d{8})\d+', str(card['CreditCard']['CardNumber'])).group(1)
        card_request(card_number)


bank_list = sorted(bank_set)
for bank in bank_list:
    print(bank)