import os
import time
import random
import json
from Scraper.utils import process_ids, get_ids, dict_to_json

start = time.time()

# Set dir and filenames
folder_name = 'Data/review1_data'
save_after_j_iterations = 50
sleep_after_j_iterations= 500

with open('wines_ids_1.json', 'r') as f:
    wine_id_list = list(json.load(f).keys())
    # Remove unnecesary stuff and convert to int
    wine_id_list = [int(id_[: id_.find('?year=')]) if id_.find('?year=') != -1 else int(id_) for id_ in wine_id_list]

# Change path
if os.path.exists(os.path.join(os.getcwd(), folder_name)):
    os.chdir(os.path.join(os.getcwd(), folder_name))
else:
    os.mkdir(os.path.join(os.getcwd(), folder_name))
    os.chdir(os.path.join(os.getcwd(), folder_name))


# Loop through chunks and for each chunk, get the data and write it to a file
sleep_tracker = 0  # Track if connection breaks
review_dict, user_dict, vintage_dict, wine_dict, country_dict, region_dict = dict(), dict(), dict(), dict(), dict(), dict()
track_wines_out_range = dict()
iterations = 1

for j, wine_id in enumerate(wine_id_list[9450:]):
    print(f'Now pulling wine_id: {wine_id}, No: {j+9450}. Script runtime: ' , time.time()-start)

    for y in [2015]: # Could be expanded later if we want to check other dates
        if (iterations+1) % save_after_j_iterations == 0:
            # Dump current results into JSON
            dict_to_json(review_dict, filename='reviews', version=1)
            dict_to_json(user_dict, filename='users', version=1)
            dict_to_json(vintage_dict, filename='vintages', version=1)
            dict_to_json(wine_dict, filename='wines', version=1)
            dict_to_json(country_dict, filename='countries', version=1)
            dict_to_json(region_dict, filename='regions', version=1)
            dict_to_json({wine_id: [j, y]},
                         filename='Wine_ID_No')  # If timeout track which page you are approximately at

            progress = round((j+1+3000) / len(wine_id_list), 4)
            try:
                print(f'''
                {iterations} iterations done. Pct. Done: {progress}
                Currently at wine_id no: {j+1} out of {len(wine_id_list)}.
                Number of unique vintages: {len(vintage_dict)}
                ''','-'*50)
            except:
                pass

        if (iterations+1) % sleep_after_j_iterations==0:
            sleep_time = random.randint(60, 120)
            print(f'Sleeping for  {sleep_time} seconds...')
            time.sleep(sleep_time)  # Every 1000 iteration sleep between 1-2 min.

        try:
            data = get_ids(wine_id = wine_id, year = y)
            review_temp, user_temp, vintage_temp, wine_temp, country_temp, region_temp = process_ids(data)

            review_dict.update(review_temp)
            user_dict.update(user_temp)
            vintage_dict.update(vintage_temp)
            wine_dict.update(wine_temp)
            country_dict.update(country_temp)
            region_dict.update(region_temp)

            '''
            elif vintage_temp['year'] < 1990:
                track_wines_out_range['wine_id'] = vintage_temp['wine_id']
                track_wines_out_range['vintage_id'] = vintage_temp['vintage_id']
                track_wines_out_range['year'] = vintage_temp['year']
            '''

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

        iterations += 1
    #if iterations == 10: break
    time.sleep(random.randint(4,10))

# Dump results into JSON
dict_to_json(review_dict, filename='reviews', version=1)
dict_to_json(user_dict, filename='users', version=1)
dict_to_json(vintage_dict, filename='vintages', version=1)
dict_to_json(wine_dict, filename='wines', version=1)
dict_to_json(country_dict, filename='countries', version=1)
dict_to_json(region_dict, filename='regions', version=1)
dict_to_json({'Wine_ID_No': [j, wine_id]},
             filename='Wine_ID_No')  # If timeout track which page you are approximately at

finish = time.time()
print(f'Time taken to execute script is {(finish - start) / 60} minutes')













