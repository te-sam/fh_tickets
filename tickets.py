import requests

from bs4 import BeautifulSoup

def get_tickets():
    response = requests.get("https://market.fitnesshouse.ru/jar")

    soup =  BeautifulSoup(response.text, 'html.parser')
    cards = soup.find_all(class_='card')
    tickets = []

    for card in cards:
        ticket ={}

        name = card.find(class_='card-title')
        price = card.find(class_='product-price-sm')
        subtitles = card.find_all(class_='card-subtitle')
        
        for subtitle in subtitles:
            text = subtitle.get_text()
            if ("год" in text) or ("месяц" in text):
                ticket['name'] = name.get_text().strip()
                ticket['price']  = int(price.get_text().replace(" ", ""))
                ticket['time'] = text

                if 'год' in text:
                    ticket['price_on_month'] = ticket['price'] / 12 / int(text.split()[0])
                if 'месяц' in text:
                    ticket['price_on_month'] = ticket['price'] / int(text.split()[0])

                tickets.append(ticket)
    return tickets


