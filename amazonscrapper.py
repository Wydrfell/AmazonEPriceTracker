#!/usr/local/bin/python3.8
import requests
from bs4 import BeautifulSoup
import smtplib
import time

URL = 'https://www.amazon.ca/perseids-800x480-Resolution-Resistive-Raspberry/dp/B077ZPZPRQ/ref=sr_1_2?crid' \
      '=UTQ72HD4Y37U&keywords=geeekpi+5+inch+hdmi+monitor&qid=1579712238&sprefix=geeekpi+%2Caps%2C151&sr=8-2 '
URL2 = 'https://tinyurl.com/AMD5700XTDriver-Support'
#google search user agent to find your user agent information, your setup may not be the same as mine
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/79.0.3945.117 Safari/537.36"}
subscriber = '<insert target email>'
hostmail = '<insert sender gmail email>'


def TitleandPrice(URL, headers):
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    soupEn = BeautifulSoup(soup.encode("utf-16"), "html.parser")

    title = soupEn.find(id="productTitle").get_text()
    price = soupEn.find(id="priceblock_ourprice").get_text()
    convertedPrice = convertPrice(price)

    print(title.strip(), convertedPrice)

    if convertedPrice < 50.00:
        send_mail(URL, title)


def convertPrice(price):
    newPrice = ''
    for ind in range(len(price)):
        if (price[ind].isdigit()) or price[ind] == '.':
            newPrice = newPrice + price[ind]

    return float(newPrice)


def send_mail(URL, title):
    # must enable 2 factor auth for google
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    #in order for the login process to work user must activate two factor authentication for the hostmail gmail account 
    #after two factor auth has been enabled, user must go and generate a google app password for Gmail 
    server.login(hostmail, '<insert generated google app password>')
    subject = f'The price had dropped for {title}'
    body = f'Check the Amazon link:\n{URL}'

    msg = f'subject: {subject}\n\n{body}'

    server.sendmail(hostmail,
                    subscriber,
                    msg)
    print('EMAIL SENT!')
    server.quit()


while (True):
    TitleandPrice(URL, headers)
    # once a day
    time.sleep(86400)
