""" 
 * ------------------------------------------------------------
 * "THE BEERWARE LICENSE" (Revision 42):
 * Onat Deniz Dogan <oddogan@protonmail.com> wrote this code. As long as you retain this 
 * notice, you can do whatever you want with this stuff. If we
 * meet someday, and you think this stuff is worth it, you can
 * buy me a beer in return.
 * ------------------------------------------------------------
"""

import requests, sys
from lxml import html

def get_news(url):
    try:
        response = requests.get(url)
    except Exception as e:
        print(str(e))
        sys.exit(2)

    if response.status_code != 200:
        print('Sorry, invalid response ' + str(response.status_code))
        sys.exit(2)

    tree = html.fromstring(response.text)

    extracteditems = tree.xpath('//a[@class="css-1ej4hfo"]/text()')

    listing_news = []

    for index, news in enumerate(extracteditems):
        if "WILL LIST" in news.upper():
            news = news.upper().split("WILL LIST ", 1)[1]
            news = news[news.find('(')+1:news.find(')')]
            listing_news.append(news)

    return(listing_news)