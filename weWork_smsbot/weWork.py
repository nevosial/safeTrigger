# encoding: utf-8


#css_selector ='.flight-low-fare-matrix'
# url = https://www.studentuniverse.co.uk/flights/1/SJC/BOM/2018-12-18/BOM/SJC/2019-01-17?flexible=true&premiumCabins=false&source=productHome

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from twilio.rest import Client
import requests
import json
import logging
import os
import errno
import config
from bs4 import BeautifulSoup



client = Client(config.twilio['account_sid'], config.twilio['auth_token'])

# message = client.messages \
#                 .create(
#                      body="nevillem",
#                      from_=config.twilio['from_phone'],
#                      to='+15304436088'
#                  )
#
# print(message.sid)

def send_message(message):
    sent_message = client.messages.create(
        body=message,
        from_=config.twilio['from_phone'],
        to='+15304436088'
    )



def login_portal(web_url):
    print(web_url)
    # Initialize headless browser
    # options = Options()
    # options.set_headless(headless=True)
    # driver = webdriver.Firefox(firefox_options=options, executable_path='/home/nev/PyCharmProjects/ImageScraper/drivers/geckodriver')

    driver = webdriver.Firefox(executable_path='/home/nev/PyCharmProjects/ImageScraper/drivers/geckodriver')

    try:
        driver.get(web_url)
        driver.implicitly_wait(30)
        driver.find_element_by_id('username').send_keys(config.w2w['username'])
        driver.find_element_by_id('password').send_keys(config.w2w['password'])
        driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div/form/div/button').click()
        driver.implicitly_wait(10)

        # send me text message about next shift.
        shift = driver.find_element_by_xpath('/html/body/div[2]/table/tbody/tr/td[3]/table/tbody/tr[2]/td')
        # print(shift.text)
        send_message(shift.text)

        # check who is on now
        driver.find_element_by_xpath('/html/body/div[1]/div/table/tbody/tr/td[9]').click()
        on_now = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/table').get_attribute('outerHTML')
        # print(on_now)
        soup = BeautifulSoup(on_now, 'html.parser')
        table = soup.find("table", attrs={"class": "modwide"})
        # headings = [th.get_text().strip() for th in table.find("tr").find_all("th")]
        rows = table.find_all('tr')
        print(rows[4])
        for i in rows:
            print(rows[4])
            print('===')

        # click to view upcoming trades.
        # driver.find_element_by_xpath('/html/body/div[2]/table/tbody/tr/td[2]/table/tbody/tr[6]/td').click()

        # signout
        driver.find_element_by_xpath('//*[@id="SingleUserMenu"]').click()

        driver.quit()
    except Exception as e:
        logging.exception("Action incomplete.")


def main():
    url = 'https://whentowork.com/logins.htm'
    response = requests.get(url)
    print(response.status_code)

    if response.status_code == 200:
        web_response = response.text
        #print(web_response)
        login_portal(url)
        # m = u"""
        # Next shift 🕯
        # Thu Aug 30, 2018
        # 10pm-2am
        # Office Assistant"""
        # send_message(m)
    else:
        logging.exception('Failed to reach remote url.')


if __name__ == "__main__":
    main()
