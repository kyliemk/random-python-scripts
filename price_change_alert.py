# !/usr/bin/python

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from twilio.rest import Client
import os

# for more information on how to set up twillio to send sms messages go to https://www.fullstackpython.com/blog/send-sms-text-messages-python.html
# I saved all these values in my .bash_profile
TWILIO_SID = os.getenv('TWILIO_SID')
TWILIO_TOKEN = os.environ.get('TWILIO_TOKEN')
TWILIO_PHONE = os.environ.get('TWILIO_PHONE')
MY_PHONE = os.environ.get('MY_PHONE')

client = Client(TWILIO_SID, TWILIO_TOKEN)

item_list = [
    { "url":"https://www.amazon.com/dp/B07HGZ383D/?coliid=I8EFPFGS2HWND&colid=1BZ6LR2EOXUP8&psc=1&ref_=lv_ov_lig_dp_it", "original_price": "$14.59"},
    { "url":"https://www.amazon.com/dp/B07TRC9CZ7/?coliid=IE65RNGGUNL1Q&colid=1BZ6LR2EOXUP8&psc=1&ref_=lv_ov_lig_dp_it", "original_price": "$14.99"},
    { "url":"https://www.amazon.com/dp/B07S1V238Z/?coliid=I19BE655DL7UX0&colid=1BZ6LR2EOXUP8&psc=1&ref_=lv_ov_lig_dp_it", "original_price": "$23.99"},
    { "url":"https://www.amazon.com/dp/B07F2XFKYV/?coliid=I9AWAVDISD0QJ&colid=1BZ6LR2EOXUP8&psc=1&ref_=lv_ov_lig_dp_it", "original_price": "$26.99"}
    ]
driver = webdriver.Chrome()
for x in item_list:
    driver.get(x["url"])
    item = driver.find_element_by_id("productTitle").text
    try:
        current_price = driver.find_element_by_id("priceblock_ourprice").text
    except:
        current_price = driver.find_element_by_id("priceblock_dealprice").text
    if current_price != x["original_price"]:
        current_price = current_price[1:]
        original_price = x["original_price"][1:]
        if float(current_price) < float(original_price):
            client.messages.create(to=MY_PHONE,
                from_=TWILIO_PHONE,
                body="Price of " + item + " decreased from $" + original_price + " to $" + current_price)
        else:
            client.messages.create(to=MY_PHONE,
                from_=TWILIO_PHONE,
                body="Price of " + item + " increased from $" + current_price + " to $" + original_price)

driver.close()
