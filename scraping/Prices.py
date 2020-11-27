import os
import json
import time
import random
import datetime as dt
from Scraper.utils import get_prices, dict_to_json, divide_chunks

start = dt.datetime.now()
print('script started at: ', start)

base_filename = 'prices'
vin_id_file = './Data/All_review_data/vintages_1.json'
folder_name = './Data/price_data'
save_after_j_iterations = 50
sleep_after_j_iterations = 500
size_chunks = 250

# Needs to be updated once we have a file with all vintage ids
with open(vin_id_file, 'r') as f:
    vin_id_list = list(json.load(f).keys())  # Get values from dict and slice it with numpy.

# Change path to price data
if os.path.exists(os.path.join(os.getcwd(), folder_name)):
    os.chdir(os.path.join(os.getcwd(), folder_name))
else:
    os.mkdir(os.path.join(os.getcwd(), folder_name))

# Loop through chunks and for each chunk, get the data and write it to a file
price_dict = dict()
sleep_tracker = 0
vin_id_list = divide_chunks(vin_id_list, size_chunks)  # Divide it into smaller pieces


for n, chunk_vintages in enumerate(vin_id_list):
    if n % 10 == 0: print(f'Now pulling vin_id: {chunk_vintages[0]}, Iteration: {n}. Timestamp: ', dt.datetime.now())

    if (n + 1) % save_after_j_iterations == 0:
        # Dump current results into JSON
        dict_to_json(price_dict, filename=base_filename, version=1)

    if (n + 1) % sleep_after_j_iterations == 0:
        sleep_time = random.randint(120, 180)
        print(f'Sleeping for  {sleep_time} seconds...')
        time.sleep(sleep_time)  # Every 1000 iteration sleep between 1-2 min.

    try:
        price_dict.update(get_prices(chunk_vintages))

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
        time.sleep(random.randint(180, 240))  # Sleep 3-4 min

dict_to_json(price_dict, filename=base_filename)

finish = dt.datetime.now()
dict_to_json(price_dict, filename=base_filename, version=1)
print('Script runtime:', finish - start)
