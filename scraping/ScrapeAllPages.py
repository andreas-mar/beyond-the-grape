import os
import json
import time
import datetime as dt
import random
import numpy as np
from Scraper.utils import dict_to_json, Selenium_Scraper

start = dt.datetime.now()

stop_after_n = None # ONLY SET WHEN TESTING CODE. OTHERWISE SET TO NONE
save_after_j_iterations = 50
sleep_after_j_iterations= 500
folder_name = './Data/Selenium_data'
file_name = 'scraped_data_andreesen'
wine_id_file = './Data/wine_ids_andreesen.json'


wine_dict = dict()
vintage_list = list()
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0"}

with open(wine_id_file, 'r') as f:
    json_file = json.load(f)
    vintage_id_list = np.array(list(json_file.values()) )[:,0].tolist()
    wine_id_list = list(json_file.keys())
    # Remove unnecesary stuff and convert to int
    wine_id_list = [int(id_[: id_.find('?year=')]) if id_.find('?year=') != -1 else int(id_) for id_ in wine_id_list]

# initiating the scraper
scraper = Selenium_Scraper()


# Change path
if os.path.exists(os.path.join(os.getcwd(), folder_name)):
    os.chdir(os.path.join(os.getcwd(), folder_name))
else:
    os.mkdir(os.path.join(os.getcwd(), folder_name))
    os.chdir(os.path.join(os.getcwd(), folder_name))

sleep_tracker = 0

for n, (vin_id, wine_id) in enumerate(zip(vintage_id_list[430:], wine_id_list[430:])):
    if n % 10 == 0: print(f'Now pulling wine_id: {wine_id}, Iteration: {n+430}. Timestamp: ' , dt.datetime.now())

    if (n + 1) % save_after_j_iterations == 0:
        # Dump current results into JSON
        dict_to_json(wine_dict, filename=file_name, version=1)
        # Print progress
        progress = round((n + 1+430) / len(wine_id_list), 4)
        try:
            print(f'''
            {n+4300} iterations done. Pct. Done: {progress}
            Currently at wine_id no: {n + 1+430} out of {len(wine_id_list)}.
            ''', '-' * 50)
        except:
            pass

    if (n + 1) % sleep_after_j_iterations == 0:
        sleep_time = random.randint(120, 180)
        print(f'Sleeping for  {sleep_time} seconds...')
        time.sleep(sleep_time)  # Every 1000 iteration sleep between 1-2 min.

    # Get new url each loop
    url = f'https://www.vivino.com/wines/{vin_id}'


    try:
        scraper.parse_page(url, wine_dict, wine_id, vin_id, n)

    except ConnectionResetError:
        print('ConnectionResetError')
        sleep_tracker += 1
        print(f'Sleeping {sleep_tracker} times')
        time.sleep(random.randint(180, 240))  # Sleep 3-4 min
        continue
    except ConnectionError:
        print('ConnectionError')
        sleep_tracker += 1
        print(f'Sleeping {sleep_tracker} times')
        time.sleep(random.randint(180, 240))  # Sleep 3-4 min
        continue

    except:
        print('Other error')
        sleep_tracker += 1
        print(f'Sleeping {sleep_tracker} times')
        time.sleep(10)  # Sleep 10 sec

    if n == stop_after_n: break


scraper.close_driver()
finish = dt.datetime.now()
print('Script runtime:', finish - start)
dict_to_json(wine_dict, filename=file_name, version=1)