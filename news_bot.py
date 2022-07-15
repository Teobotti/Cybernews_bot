TOKEN = "5518157517:AAGds-vbZRJU4W9m4SKUxSQaG3D69hu4GPo"
global chat_id 


#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.
# ! pip install beautifulsoup4
# ! pip install requests
# ! pip install urllib

"""Simple inline keyboard bot with multiple CallbackQueryHandlers.
This Bot uses the Application class to handle the bot.
First, a few callback functions are defined as callback query handler. Then, those functions are
passed to the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot that uses inline keyboard that has multiple CallbackQueryHandlers arranged in a
ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line to stop the bot.
"""
from cgitb import text
from email.mime import application
import logging
from math import prod
import string
from traceback import print_last
import requests
from bs4 import BeautifulSoup
from pprint import pprint

from zmq import Message


# importing the necessary packages for web scraping
#import requests
#from bs4 import BeautifulSoup

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Stages
START_ROUTES, END_ROUTES = range(2)
# Callback data
ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE, TEN, ELEV, TWELVE, TREDICI, QUATTORDICI , QUINDICI, SED, DICIA, DICIOTT, DICIANN, VENTI, VENTUNO= range(21)



def getlinksRansom(site):
    "This function gets the site to scrap. Then search for the 2 latest articles and pass them to sendsite() function."
	# create url
    if(site==1):
        url = "https://www.cybersecurity360.it/tag/ransomware/"
    elif(site==2):
        url = "https://www.redhotcyber.com/post/category/incidenti-ransomware/"
    elif(site==3):
        url = "https://www.cshub.com/tag/ransomware"

	# define headers
    headers = { 'User-Agent': 'Generic user agent' }
    # get page
    page = requests.get(url, headers=headers)
	# let's soup the page
    if(site==1 or site==2):
        soup = BeautifulSoup(page.text, 'html.parser')
    elif(site==3):
        soup = BeautifulSoup(page.text, 'lxml')
        #print(soup)

    links = []

    if(site==1):
        #working
        productDivs = soup.findAll('div', attrs={'class' : 'card-large card-large-home p-relative SHAD_flat2'})
        for div in productDivs:
            links.append(div.a['href'])
        others = soup.find('a', attrs={'class' : 'flex-column growFlex'}).get('href')
        links.append(others)

    elif(site==2):
        #working
        pops = soup.find_all('a', attrs={'class' : 'elementor-post__thumbnail__link'}, href=True, limit=2)
        for i in pops:
            links.append((i['href']))

    elif(site==3):
        #TODO non trova gli elementi della pagina
        temp = soup.find("div", attrs={'class' :'my-4 row no-gutters px-3'})
        #print(temp)
        temp2 = temp.find('div', attrs={ 'class' : 'col-12 col-lg-8 pr-3 page-content'})
        #print(temp2)
        temp3 = temp2.find('div', id='infinite-scroll')
        print(temp3)
        temp4 = temp3.find('div')
        print(temp4)

        productDivs = temp2.findAll('h3', attrs={ 'class" : "article-title'}, limit=2)

        print(productDivs)
        for div in productDivs: 
            temp = "https://www.cshub.com" + div.a['href']
            print(temp)
            links.append(temp)
        
        

        #url = "https://www.cshub.com/tag/ransomware"
        
    #print(links)
    return links

def getlinksIntel(site):

    if(site==1):
        url = "https://www.redhotcyber.com/post/category/intelligence/"
    elif(site==2):
        url = "https://securityaffairs.co/wordpress/category/intelligence"
    elif(site==3):
        url = "https://securityintelligence.com/category/security-intelligence-analytics/"

    # define headers
    headers = { 'User-Agent': 'Generic user agent' }
    # get page
    page = requests.get(url, headers=headers)
	# let's soup the page
    soup = BeautifulSoup(page.text, 'html.parser')

    links=[]

    if(site==1):

        #working
        pops = soup.find_all('a', attrs={'class' : 'elementor-post__thumbnail__link'}, href=True, limit=2)
        for i in pops:
            links.append((i['href']))

    elif(site==2):
        productDivs = soup.findAll('h3',limit=2)
        for div in productDivs:
            links.append(div.a['href'])
        
        #others = soup.find('a', attrs={'class' : 'flex-column growFlex'}).get('href')
        #links.append(others)
    elif(site==3):
        productDivs = soup.findAll('a', attrs={'class' : 'article__content_link'}, limit=2)
        for div in productDivs:
            links.append(div['href'])

    
    return links

def getlinksItaly(site):
    
    if(site==1):
        url = "https://www.redhotcyber.com/post/category/attacchi-informatici-italiani/"
    elif(site==2):
        url = "https://www.cybersecurity360.it/cybersecurity-nazionale/"
    

    # define headers
    headers = { 'User-Agent': 'Generic user agent' }
    # get page
    page = requests.get(url, headers=headers)
	# let's soup the page
    soup = BeautifulSoup(page.text, 'html.parser')

    links=[]

    if(site==1):

        #working
        pops = soup.find_all('a', attrs={'class' : 'elementor-post__thumbnail__link'}, href=True, limit=2)
        for i in pops:
            links.append((i['href']))
    elif(site==2):
        #working
        productDivs = soup.findAll('div', attrs={'class' : 'card-large card-large-home p-relative SHAD_flat2'})
        for div in productDivs:
            links.append(div.a['href'])
        others = soup.find('a', attrs={'class' : 'flex-column growFlex'}).get('href')
        links.append(others)
    
    return links

def getlinksData(site):

    if(site==1):
        url = "https://www.redhotcyber.com/post/category/data-breach/"
    elif(site==2):
        url = "https://securityaffairs.co/wordpress/category/data-breach"
    elif(site==3):
        url = "https://www.infosecurity-magazine.com/data-breaches/"

    # define headers
    headers = { 'User-Agent': 'Generic user agent' }
    # get page
    page = requests.get(url, headers=headers)
	# let's soup the page
    soup = BeautifulSoup(page.text, 'html.parser')

    links =[]

    if(site==1):

        #working
        pops = soup.find_all('a', attrs={'class' : 'elementor-post__thumbnail__link'}, href=True, limit=2)
        for i in pops:
            links.append((i['href']))
    elif(site==2):
        productDivs = soup.findAll('h3',limit=2)
        for div in productDivs:
            links.append(div.a['href'])
    elif(site==3):
        pops = soup.find_all('a', attrs={'class': 'webpage-link'},href=True, limit=2)
        for p in pops:
            links.append(p['href'])

    return links

    
def findLatestVuln() :

    limit = 240000
    
    base_url = "https://exchange.xforce.ibmcloud.com/vulnerabilities/"


    # define headers
    headers = { 'User-Agent': 'Generic user agent' }
    
    links=[]
    
    while(limit > 0):
        url = base_url + str(limit)
        #print(url)
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.text, 'lxml')
        flag = soup.find('meta', {'content': 'IBM X-Force Exchange'}, {'property': 'og:title'})
        if(flag==None):
            print("found!")
            links.append(base_url+str(limit))
            links.append(base_url+str(limit-1))
            links.append(base_url+str(limit-2))
            break
        limit = limit - 1
    
    
    #print(links)

    return links

    





async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Send message on `/start`."""
    # Get user that sent /start and log his name
    user = update.message.from_user
    global chat_id
    chat_id = update.message.from_user.id
    print(chat_id)

    logger.info("User %s started the conversation. Chat id= %s", user.first_name, chat_id)
    # Build InlineKeyboard where each button has a displayed text
    # and a string as callback_data
    # The keyboard is a list of button rows, where each row is in turn
    # a list (hence `[[...]]`).
    keyboard = [
        [
            InlineKeyboardButton("Send News", callback_data=str(ONE)) 
        ], 
        [
            InlineKeyboardButton("Latest Tweets", callback_data=str(QUINDICI))
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send message with text and appended InlineKeyboard
    await update.message.reply_text("What you want me to do?", reply_markup=reply_markup)
    # Tell ConversationHandler that we're in state `FIRST` now
    return START_ROUTES

async def one(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int: #select the topic
    """Shows the various topics from which choose."""
    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Ransomware", callback_data=str(THREE)),
            InlineKeyboardButton("Data Breach", callback_data=str(FOUR)),
        ],
        [
            InlineKeyboardButton("ITALY", callback_data=str(FIVE)),
            InlineKeyboardButton("Intelligence", callback_data=str(SIX)),
        ], 
        [
            InlineKeyboardButton("Close", callback_data=str(TWO)),
        ]
        
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="Choose a topic!", reply_markup=reply_markup
    )
    return START_ROUTES



def getTweet(num):
    
    if(num == 1):
        url = "https://twitter.com/hashtag/ransomware"
    elif(num == 2):
        url = "https://twitter.com/hashtag/databreach"

    headers = { 'User-Agent': 'Generic user agent' }

    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'lxml')

    links = []

    pops = soup.findAll('div', attrs={'class' : 'css-4rbku5 css-18t94o4 css-901oao r-1bwzh9t r-1loqt21 r-1q142lx r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-3s2u2q r-qvutc0'}, href=True, limit=2)
    for i in pops:
        links.append((i['href']))


    print(links)
    return links




async def sendTweetsRans(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    "Sends the articles with a POST request"
    links = getTweet(1)
    sender(links)

async def sendTweetsData(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    "Sends the articles with a POST request"
    links = getTweet(2)
    sender(links)
    
def sender(links):
    global chat_id
    for l in links:
        url = "https://api.telegram.org/bot5518157517:AAGds-vbZRJU4W9m4SKUxSQaG3D69hu4GPo/sendMessage?chat_id=" + str(chat_id) + "&text=" + l
        requests.post(url)

async def pickTweets(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    keyboard = [
            [
              InlineKeyboardButton("Data Breach", callback_data=str(VENTI)),
              
            ],
            [
              InlineKeyboardButton("Ransomware", callback_data=str(VENTUNO))
            ],
            [
              InlineKeyboardButton("Close", callback_data=str(TWO))
            ]
        
            ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text="Choose the website:", reply_markup=reply_markup) 
    #appare o solo la inline message o solo il messaggio mandato
    
    return START_ROUTES

async def sendsiteDataRedHot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int: #ransomware articles
    "Sends the articles with a POST request"
    links = getlinksData(1)
    sender(links)
    
    

async def sendsiteDataSecAff(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int: #ransomware articles
    "Sends the articles with a POST request"
    links = getlinksData(2)
    sender(links)

   

async def sendsiteDataInfosec(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int: #ransomware articles
    "Sends the articles with a POST request"
    links = getlinksData(3)
    sender(links)

   


async def sendsiteIntelRedHot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int: #ransomware articles
    "Sends the articles with a POST request"
    links = getlinksIntel(1)
    global chat_id
    sender(links)
    
async def sendsiteIntelSecAff(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int: #ransomware articles
    "Sends the articles with a POST request"
    links = getlinksIntel(2)
    sender(links)
   

async def sendsiteIntelSecInt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int: #ransomware articles
    "Sends the articles with a POST request"
    links = getlinksIntel(3)
    sender(links)
   


async def sendsiteRansomC360(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int: #ransomware articles
    "Sends the articles with a POST request"
    links = getlinksRansom(1)
    sender(links)
   

async def sendsiteRansomRedHot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int: #ransomware articles
    "Sends the articles with a POST request"
    links = getlinksRansom(2)
    sender(links)
    

async def sendsiteRansomCShub(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int: #ransomware articles
    "Sends the articles with a POST request"
    
    links = getlinksRansom(3)
    sender(links)
    

async def sendsiteItalyRedHot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int: #ransomware articles
    "Sends the articles with a POST request"
    
    links = getlinksItaly(1)
    sender(links)
    

async def sendsiteItalyC360(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int: #ransomware articles
    "Sends the articles with a POST request"
    
    links = getlinksItaly(2)
    sender(links)
   


async def picksiteRansom(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int: #ransomware topic
    
    """Show sites for Ransomware themed news"""
    query = update.callback_query
    await query.answer()
    keyboard = [
            [
              InlineKeyboardButton("Cyber360 ", callback_data=str(SEVEN)),
              InlineKeyboardButton("RedHotCyber ", callback_data=str(EIGHT))
            ],
            [
               InlineKeyboardButton("TODO_CyberSecurityHub ", callback_data=str(NINE))
            ],

            [
              InlineKeyboardButton("Back to topic choice", callback_data=str(ONE))
            ]
        
            ]
        

    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text="Choose website:", reply_markup=reply_markup)
    

    return START_ROUTES

async def picksiteData(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int: #
    #TODO
    """Show sites for Cybercrime themed news"""
    query = update.callback_query
    await query.answer()
    keyboard = [
            [
              
              InlineKeyboardButton("RedHotCyber", callback_data=str(SED)),
              InlineKeyboardButton("SecurityAffairs", callback_data=str(DICIA))

            ],
            [
               InlineKeyboardButton("InfoSec Magazine", callback_data=str(DICIOTT)),
               #InlineKeyboardButton("corrierecomunicazioni", url="https://www.corrierecomunicazioni.it/tag/cybercrime/")
            ],

            [
              InlineKeyboardButton("Back to topic choice", callback_data=str(ONE))
            ]
        
            ]
    
   
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text="Choose the website:", reply_markup=reply_markup) 
    #appare o solo la inline message o solo il messaggio mandato
    
    return START_ROUTES

async def picksiteItaly(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int: #
    

    """Show sites for italy themed news"""
    query = update.callback_query
    await query.answer()
    keyboard = [
            [
              InlineKeyboardButton("Cyber360 ", callback_data=str(QUATTORDICI)),
              InlineKeyboardButton("RedHotCyber ", callback_data=str(TREDICI))
            ],
            [
              InlineKeyboardButton("Back to topic choice", callback_data=str(ONE))
            ]
        
            ]
    
   
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text="Choose the website:", reply_markup=reply_markup) 
    #appare o solo la inline message o solo il messaggio mandato
    
    return START_ROUTES

async def picksiteIntel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int: #
    # https://www.cybersecurity360.it/tag/cybercrime/
    # https://www.redhotcyber.com/post/category/incidenti-ransomware/

    """Show sites for Intelligence themed news"""
    query = update.callback_query
    await query.answer()
    keyboard = [
            [
              InlineKeyboardButton("RedHotCyber ", callback_data=str(TEN)),
              InlineKeyboardButton("SecurityAffairs ", callback_data=str(ELEV))
            ],
            [
              
              InlineKeyboardButton("Security Intelligence", callback_data=str(TWELVE))

            ],
            [
              InlineKeyboardButton("Back to topic choice", callback_data=str(ONE))
            ]
        
            ]
    
   
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text="Choose the website:", reply_markup=reply_markup) 
    #appare o solo la inline message o solo il messaggio mandato
    
    return START_ROUTES


async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over.
    """
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="See you next time!")
    return ConversationHandler.END

def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # Setup conversation handler with the states FIRST and SECOND
    # Use the pattern parameter to pass CallbackQueries with specific
    # data pattern to the corresponding handlers.
    # ^ means "start of line/string"
    # $ means "end of line/string"
    # So ^ABC$ will only allow 'ABC'
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            START_ROUTES: [
                CallbackQueryHandler(one, pattern="^" + str(ONE) + "$"),
                CallbackQueryHandler(pickTweets, pattern="^" + str(QUINDICI) + "$"),
                CallbackQueryHandler(picksiteRansom, pattern="^" + str(THREE) + "$"),
                CallbackQueryHandler(picksiteData, pattern="^" + str(FOUR) + "$"),
                CallbackQueryHandler(picksiteItaly, pattern="^" + str(FIVE) + "$"),
                CallbackQueryHandler(picksiteIntel, pattern="^" + str(SIX) + "$"),
                CallbackQueryHandler(end, pattern="^" + str(TWO) + "$"),
                CallbackQueryHandler(sendsiteRansomC360, pattern="^" + str(SEVEN) + "$"),
                CallbackQueryHandler(sendsiteRansomRedHot, pattern="^" + str(EIGHT) + "$"),
                CallbackQueryHandler(sendsiteRansomCShub, pattern="^" + str(NINE) + "$"),
                CallbackQueryHandler(sendsiteIntelRedHot, pattern="^" + str(TEN) + "$"),
                CallbackQueryHandler(sendsiteIntelSecAff, pattern="^" + str(ELEV) + "$"),
                CallbackQueryHandler(sendsiteItalyRedHot, pattern="^" + str(TREDICI) + "$"),
                CallbackQueryHandler(sendsiteItalyC360, pattern="^" + str(QUATTORDICI) + "$"),
                CallbackQueryHandler(sendsiteIntelSecInt, pattern="^" + str(TWELVE) + "$"),
                CallbackQueryHandler(sendsiteDataRedHot, pattern="^" + str(SED) + "$"),
                CallbackQueryHandler(sendsiteDataSecAff, pattern="^" + str(DICIA) + "$"),
                CallbackQueryHandler(sendsiteDataInfosec, pattern="^" + str(DICIOTT) + "$"),
                CallbackQueryHandler(start, pattern="^" + str(DICIANN) + "$"),
                CallbackQueryHandler(sendTweetsData, pattern="^" + str(VENTI) + "$"),
                CallbackQueryHandler(sendTweetsRans, pattern="^" + str(VENTUNO) + "$")
            ],
            END_ROUTES: [
                CallbackQueryHandler(one, pattern="^" + str(ONE) + "$"),
                CallbackQueryHandler(end, pattern="^" + str(TWO) + "$"),
            ],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    # Add ConversationHandler to application that will be used for handling updates
    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()

if __name__ == "__main__":
    main()

