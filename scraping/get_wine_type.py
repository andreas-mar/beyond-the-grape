import requests
import bs4 as bs
import time
import lxml
import datetime as dt
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import os

#os.chdir('./Scraper')
print(os.getcwd())

output_file_name = 'wine_types.csv'

wines = pd.read_csv('wine_ids.csv', index_col='vintage_id')[::-1]

options = Options()
options.add_argument('--window-size=1920,1080')
driver = webdriver.Chrome('./chromedriver', options=options)

wines['types'] = None

for i, vintage_id in enumerate(wines.index):
    if i %10 == 0: print(f'Now pulling wine_id: {vintage_id}, Iteration: {i} out of {len(wines)}. Timestamp: ' , dt.datetime.now())
    if (i+1) % 50==0: wines.to_csv(output_file_name)
    if (i+1) % 200 ==0: time.sleep(120)

    try:
        driver.get(f'https://www.vivino.com/wines/{vintage_id}')
        time.sleep(5)
        soup = bs.BeautifulSoup(driver.page_source, 'lxml')
        wine_type = soup.find('span', attrs={'class': 'wineLocationHeader__wineType--14nrC'}).string

        wines.loc[vintage_id, 'types'] = wine_type

    except:
        wines.loc[vintage_id, 'types'] = 'error'
        print(f'error in {vintage_id}, iteration: {i}')

driver.close()
wines.to_csv(output_file_name)