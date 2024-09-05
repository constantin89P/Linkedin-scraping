import requests
import json
import csv
from itertools import chain
import time
from bs4 import BeautifulSoup
import pandas as pd
import json
import numpy as np
import parameters


# Scraper to get any business link or email and title from database file of profiles


def get_random_ua():
    random_ua = ''
    try:
        with open(parameters.ua_file_constantin, newline='') as check:
            reader = csv.reader(check)
            url_list = reader
            lines = list(chain(*url_list))
        if len(lines) > 0:
            prng = np.random.RandomState()
            index = prng.permutation(len(lines) - 1)
            idx = np.asarray(index, dtype=np.integer)[0]
            random_proxy = lines[int(idx)]
    except Exception as ex:
        print('Exception in random_ua')
        print(str(ex))
    finally:
        return random_proxy
def extract():
    with open(parameters.file_url_constantin, newline='', encoding="utf-8") as check:
        reader = csv.reader(check)
        url_list = reader
        url_list = list(chain(*url_list))   
    company_urls = url_list
    results = []
    count = 1
    for url in company_urls:
        delays = [30, 20, 10, 12, 16, 9]
        delay = np.random.choice(delays)
        time.sleep(delay)
        count += 1
        if count % 50 == 0:
            print(count)
            print("sleeping due to 50 scrape")
            time.sleep(3600)
            scraper(url,results)
        else:
            scraper(url,results)
def scraper(url,results):
    print("scraping", url)
    user_agent = get_random_ua()
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", 
        "Accept-Encoding": "gzip, deflate", 
        "Accept-Language": "en-US,en-US;q=0.9,en;q=0.8", 
        "User-Agent": str(user_agent),
                }
    page = requests.get(url, headers=headers)
    print(page.status_code)
    #print(page.headers)
    print(page)
    print (user_agent)
    soup = BeautifulSoup(page.content, "html.parser")
    if page.status_code == 200:
        for g in soup.find_all('div', class_='r'):
            anchors = g.find_all('a')
            if anchors:
                link = anchors[0]['href']
                title = g.find('h3').text
                item = {
                    "url": url,
                    "title": title,
                    "link": link
                }
                print(item)
                results.append(item)
                f = open(parameters.json_url_constantin, 'a')
                json.dump(item, f, indent=4)
                results = []

    elif page.status_code == 403 or page.status_code == 400:
        print("sleeping 60 secondes due to  403 or 400 response")
        time.sleep(60)

    elif page.status_code != 200:
        print("sleeping")
        time.sleep(3600)

run = extract()