""" 
 * ------------------------------------------------------------
 * "THE BEERWARE LICENSE" (Revision 42):
 * Onat Deniz Dogan <oddogan@protonmail.com> wrote this code. As long as you retain this 
 * notice, you can do whatever you want with this stuff. If we
 * meet someday, and you think this stuff is worth it, you can
 * buy me a beer in return.
 * ------------------------------------------------------------
"""

import telegram
from . import config

def post_message(message):
    """
    post_message posts the given message on Telegram Bot.

    Args:
        message (string): The message to be sent on Telegram
    """
    
    try:
        bot = telegram.Bot(token=config.TOKEN)
        for id in config.CHAT_IDS:
            bot.send_message(id,message)
    except Exception as e:
        print(e)
    return