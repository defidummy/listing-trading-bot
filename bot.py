"""
 * ------------------------------------------------------------
 * "THE BEERWARE LICENSE" (Revision 42):
 * Onat Deniz Dogan <oddogan@protonmail.com> wrote this code. As long as you retain this 
 * notice, you can do whatever you want with this stuff. If we
 * meet someday, and you think this stuff is worth it, you can
 * buy me a beer in return.
 * ------------------------------------------------------------
"""

import gateio, time
from get_news import get_news
from utils.telegram_bot import post_message

url = "https://www.binance.com/en/support/announcement/c-48?navId=48"
sleep_time = 10
latest_news = 'POLS'

post_message('Bot started!')

while True:
    """
     Get the new announcements from Binance all the time.
     If a new coin listing is announced, immediately buy the coin on GateIO during pumping.
     When the pumping ends, sell the coin and take the profit.
    """
    news = get_news(url)

    # If there is no announcements
    if len(news) == 0:
        time.sleep(sleep_time)
        continue

    # If there is a new coin listing!
    if news[0] != latest_news:
        try:
            latest_news = news[0]
            message = "News! " + latest_news + " will be listed!"
            print(message)
            post_message(message)

            symbol = latest_news+'/USDT'
            if gateio.symbol_check(symbol):
                gateio.buy(symbol)
                gateio.sellBearish(symbol)
            
        except Exception as e:
            message = f'Error: {str(e)}'
            print(message)
            post_message(message)
    
    time.sleep(sleep_time)