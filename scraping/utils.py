import os
import json
import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from langdetect import detect

def parse_HTML(html_file:str):
    import bs4 as bs
    import lxml

    with open(html_file, 'r') as f:
        content = f.read()
        soup = bs.BeautifulSoup(content, 'lxml')

    # Saves both a dict and list of links. The list ensures that non-unique wine_ids still store their URLs

    wine_dict = dict()
    links = []
    for s in soup.find_all('div', class_='cleanWineCard__cleanWineCard--tzKxV cleanWineCard__row--CBPRR'):
        link = s.find('a').attrs['href']
        links.append(link)
        id_ = link[link.find('/w/'):][3:][:link[link.find('/w/'):][2:].find('?year') - 1]
        wine_dict[id_] = link

    return wine_dict, links



def dict_to_json(data, filename: str, version: int = 1, indent: int = 4):
    """
    Save a dictionary to .json with specified filename

    :param data: dict
    :param filename: str
    :param version: int
    :param indent: 4
    :return: dumps dict to json
    """
    filename = filename + '_' + str(version) + '.json'

    with open(filename, 'w') as f:  # Write to file
        json.dump(data, f, indent=indent)


def divide_chunks(data_list, n_elements_per_chunk):
    """
    Divide a list into chunks of size n

    :returns generator object
    """
    for i in range(0, len(data_list), n_elements_per_chunk):
        yield data_list[i:i + n_elements_per_chunk]  # Use yield instead of return so function state is saved


def get_prices(vintage_id=3595824):
    """
    Get wine prices

    :parameter vintage_id: int or list
    :return: dict
    """
    r = requests.get(
        "https://www.vivino.com/api/prices",
        params={
            "vintage_ids[]": vintage_id
        },
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0"}
    ).json()

    price_dict = dict()

    for key, val in r['prices']['vintages'].items(): # Loop through dict

        try: price_id = val['price']['id']
        except: price_id= None
        try: price = val['price']['amount']
        except: price = None
        try: price_type = val['price']['type']
        except: price_type = None
        try: price_discount = val['price']['discounted_from']
        except: price_discount = None

        price_payload = {'currency': r['prices']['market']['currency']['code'],
                         'year': val['vintage']['year'],
                         'grapes': val['vintage']['grapes'],
                         'median_price': val['median']['amount'],
                         'median_type': val['median']['type'],
                         'median_discount': val['median']['discounted_from'],
                         'price_id': price_id,
                         'price': price,
                         'price_type': price_type,
                         'price_discount': price_discount,

                        'maybe_this_is_wine_id': val['vintage']['id']
                         }
        price_dict[key] = price_payload
    return price_dict

def get_ids(wine_id=1239186, year=2015):
    """
    Get wine prices

    :parameter vintage_id: int or list
    :return: dict
    """
    r = requests.get(
        f"https://www.vivino.com/api/wines/{wine_id}/reviews",
        params={
            "year": year,
            'per_page': 10000
        },
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0"}
    )
    return r.json()


def get_wines(page_number):
    """
         Get basic wine info and process it

         :param page_num: int
                 pages to iterate over
         :return: dict
         """
    r = requests.get(
            "https://www.vivino.com/api/explore/explore",
            params={
                "country_code": "DK",
                # "country_codes[]":"pt", #Indicates which countries the wines can come from. Blank means all.
                "currency_code": "DKK",
                "grape_filter": "varietal",
                "min_rating": "1",
                "order_by": "ratings_average",  # Can also be 'price'
                "order": "desc",
                "page": page_number,
                "price_range_max": "2500",
                "price_range_min": "0"
                # "wine_type_ids[]":"1"
            },
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0"}
        )

    return r.json()


def process_wines(data, version:int = 1):
    # Create dicts. These are updated along the way, and become the final output
    region_dict = dict()
    country_dict = dict()
    wine_dict = dict()
    vintage_dict = dict()

    for match in data['explore_vintage']['matches']:
        # Vintage specific
        vintage_id = match['vintage']['id']
        vintage_seo_name = match['vintage']['seo_name']
        vintage_name = match['vintage']['name']
        vintage_ratings_count = match['vintage']['statistics']['ratings_count']
        vintage_ratings_average = match['vintage']['statistics']['ratings_average']
        vintage_labels_count = match['vintage']['statistics']['labels_count']

        # Winery specific
        try:
            winery_id = match['vintage']['wine']['winery']['id']
            winery_name = match['vintage']['wine']['winery']['name']
        except TypeError:
            winery_id = None
            winery_name = None
        # Wine specific
        wine_id = match['vintage']['wine']['id']
        wine_name = match['vintage']['wine']['name']
        wine_ratings_count = match['vintage']['wine']['statistics']['ratings_count']
        wine_ratings_average = match['vintage']['wine']['statistics']['ratings_average']
        wine_labels_count = match['vintage']['wine']['statistics']['labels_count']
        wine_structure = match['vintage']['wine']['taste']['structure']
        wine_vintages_count = match['vintage']['wine']['statistics']['vintages_count']
        try:
            flavor_payload = dict()
            for flavor in match['vintage']['wine']['taste']['flavor']:
                flavor_payload[flavor['group']] = flavor['stats']['score']

        except TypeError:
            flavor_payload = dict()


        try:
            food = []
            for item in match['vintage']['wine']['style']['food']:
                food.append(item['name'])
        except TypeError:  # Sometimes missing
            food = None

        try:
            wine_type_id = match['vintage']['wine']['style']['wine_type_id']
        except TypeError:  # Sometimes missing
            wine_type_id = None

        try:
            wine_style_body = match['vintage']['wine']['style']['body']
            wine_style_acidity = match['vintage']['wine']['style']['acidity']
        except TypeError:  # Sometimes missing
            wine_style_body = None
            wine_style_acidity = None

        # Region specific  ---- need to create payload solution like below, once we figure out relevant variables.
        try:
            region_id = match['vintage']['wine']['region']['id']
            region_dict[region_id] = match['vintage']['wine']['region']['name']  # Put name inside id in dict
        except TypeError:
            region_id = 0000 # To prevent crashes

        # Put everything inside name in dict
        try:
            country_name = match['vintage']['wine']['region']['country']['name']
            country_dict.update({'country': {country_name: 'users_count'}})

            country_payload = {'users_count': match['vintage']['wine']['region']['country']['users_count'],
                               'wines_count': match['vintage']['wine']['region']['country']['wines_count'],
                               'wineries_count': match['vintage']['wine']['region']['country']['wineries_count'],
                               'most_used_grapes': [{grape['name']: grape['id']} for grape in
                                                    match['vintage']['wine']['region']['country'][
                                                        'most_used_grapes']]
                               }
        except TypeError:
            country_name = 0000
            country_payload = dict()

        wine_payload = {'name': wine_name,
                        'ratings_count': wine_ratings_count,
                        'ratings_average': wine_ratings_average,
                        'labels_count': wine_labels_count,
                        'vintages_count': wine_vintages_count,
                        'structure': wine_structure,
                        'flavor': flavor_payload,
                        'acidity': wine_style_acidity,
                        'body': wine_style_body,
                        'type_id': wine_type_id,
                        'food': food,
                        'winery_id': winery_id,
                        'winery_name': winery_name,
                        'country_name':country_name, #FOREIGN KEY
                        'region_id': region_id # FOREIGN KEY
                        }

        vintage_payload = {'seo_name': vintage_seo_name,
                           'name': vintage_name,
                           'ratings_count': vintage_ratings_count,
                           'ratings_average': vintage_ratings_average,
                           'labels_count': vintage_labels_count,
                           'wine_id': wine_id #FOREIGN KEY
                           }

        wine_dict.update({wine_id: wine_payload})
        vintage_dict.update({vintage_id: vintage_payload})
        country_dict.update({country_name: country_payload})

    return vintage_dict, wine_dict, country_dict, region_dict


def process_ids(data, version: int = 1):
    # Create dicts. These are updated along the way, and become the final output
    review_dict = dict()
    user_dict = dict()
    region_dict = dict()
    country_dict = dict()
    wine_dict = dict()
    vintage_dict = dict()

    for match in data['reviews']:
        # Review specific
        review_id = match['id']
        review_rating = match['rating']
        review_note = match['note']
        review_language = match['language']
        review_created_at = match['created_at']

        # USer specific
        user_id = match['user']['id']
        user_seo_name = match['user']['seo_name']
        user_is_featured = match['user']['is_featured']
        user_ratings_count = match['user']['statistics']['ratings_count']
        user_reviews_count = match['user']['statistics']['reviews_count']
        user_ratings_sum = match['user']['statistics']['ratings_sum']
        user_followers_count = match['user']['statistics']['followers_count']
        user_followings_count = match['user']['statistics']['followings_count']

        # Vintage specific
        vintage_id = match['vintage']['id']
        vintage_seo_name = match['vintage']['seo_name']
        vintage_name = match['vintage']['name']
        try: vintage_year = match['vintage']['year']
        except: vintage_year = None
        vintage_ratings_count = match['vintage']['statistics']['ratings_count']
        vintage_ratings_average = match['vintage']['statistics']['ratings_average']
        vintage_labels_count = match['vintage']['statistics']['labels_count']
        vintage_reviews_count = match['vintage']['statistics']['reviews_count']
        vintage_certified_biodynamic = match['vintage']['certified_biodynamic']

        # Winery specific
        try:
            winery_id = match['vintage']['wine']['winery']['id']
            winery_name = match['vintage']['wine']['winery']['name']
            winery_ratings_count = match['vintage']['wine']['winery']['statistics']['ratings_count']
            winery_ratings_average = match['vintage']['wine']['winery']['statistics']['ratings_average']
            winery_labels_count = match['vintage']['wine']['winery']['statistics']['labels_count']
            winery_wines_count = match['vintage']['wine']['winery']['statistics']['wines_count']
        except TypeError:
            winery_id = None
            winery_name = None

        # Wine specific
        wine_id = match['vintage']['wine']['id']
        wine_name = match['vintage']['wine']['name']
        wine_type_id = match['vintage']['wine']['type_id']
        wine_is_natural = match['vintage']['wine']['is_natural']
        wine_style = match['vintage']['wine']['style']
        # wine_ratings_count = match['vintage']['wine']['statistics']['ratings_count']
        # wine_ratings_average = match['vintage']['wine']['statistics']['ratings_average']
        # wine_labels_count = match['vintage']['wine']['statistics']['labels_count']
        # wine_vintages_count = match['vintage']['wine']['statistics']['vintages_count']


        try:
            flavor_payload = dict()
            wine_structure = match['vintage']['wine']['taste']['structure']

            for flavor in match['vintage']['wine']['taste']['flavor']:
                flavor_payload[flavor['group']] = flavor['stats']['score']

        except TypeError:
            flavor_payload = None

        except:
            flavor_payload = None

        try:
            food = []
            for item in match['vintage']['wine']['style']['food']:
                food.append(item['name'])
        except TypeError:  # Sometimes missing
            food = None

        try:
            wine_type_id = match['vintage']['wine']['style']['wine_type_id']
        except TypeError:  # Sometimes missing
            wine_type_id = None

        try:
            wine_style_body = match['vintage']['wine']['style']['body']
            wine_style_acidity = match['vintage']['wine']['style']['acidity']
        except TypeError:  # Sometimes missing
            wine_style_body = None
            wine_style_acidity = None

        # Region specific  ---- need to create payload solution like below, once we figure out relevant variables.
        try:
            region_id = match['vintage']['wine']['region']['id']
            region_dict[region_id] = match['vintage']['wine']['region']['name']  # Put name inside id in dict
        except TypeError:
            region_id = 0  # To prevent crashes

        # Put everything inside name in dict
        try:
            country_name = match['vintage']['wine']['region']['country']['name']
            #country_dict.update({'country': {country_name: 'users_count'}})

            country_payload = {'users_count': match['vintage']['wine']['region']['country']['users_count'],
                               'regions_count': match['vintage']['wine']['region']['country']['regions_count'],
                               'wines_count': match['vintage']['wine']['region']['country']['wines_count'],
                               'wineries_count': match['vintage']['wine']['region']['country']['wineries_count'],
                               'most_used_grapes': [{grape['name']: grape['id']} for grape in
                                                    match['vintage']['wine']['region']['country'][
                                                        'most_used_grapes']]
                               }
        except TypeError:
            country_name = 0
            country_payload = dict()

        review_payload = {'id': review_id,
                          'rating': review_rating,
                          'note': review_note,
                          'language': review_language,
                          'created_at': review_created_at,
                          'vintage_id': vintage_id, #FOREIGN KEY
                          'wine_id': wine_id, #FOREIGN KE,
                          'user_id': user_id #FOREIGN KEY
                          }
        user_payload = {'id': user_id,
                        'seo_name': user_seo_name,
                        'ratings_count': user_ratings_count,
                        'reviews_count': user_reviews_count,
                        'ratings_sum': user_ratings_sum,
                        'is_featured': user_is_featured,
                        'followers_count': user_followers_count,
                        'followings_count': user_followings_count,
                        'vintage_id': vintage_id,  # FOREIGN KEY
                        'wine_id': wine_id, # FOREIGN KEY
                        }



        vintage_payload = {'seo_name': vintage_seo_name,
                           'name': vintage_name,
                           'year': vintage_year,
                           'ratings_count': vintage_ratings_count,
                           'ratings_average': vintage_ratings_average,
                           'labels_count': vintage_labels_count,
                           'reviews_count': vintage_reviews_count,
                           'certified_biodynamic': vintage_certified_biodynamic,
                           'wine_id': wine_id  # FOREIGN KEY
                           }

        wine_payload = {'name': wine_name,
                        # 'ratings_count': wine_ratings_count,
                        # 'ratings_average': wine_ratings_average,
                        # 'labels_count': wine_labels_count,
                        # 'vintages_count': wine_vintages_count,
                        # 'structure': wine_structure,
                        'flavor': flavor_payload,
                        'acidity': wine_style_acidity,
                        'body': wine_style_body,
                        'type_id': wine_type_id,
                        'food': food,
                        'is_natural': wine_is_natural,
                        'style': wine_style,
                        'winery_id': winery_id,
                        'winery_name': winery_name,
                        'winery_ratings_count': winery_ratings_count,
                        'winery_ratings_average': winery_ratings_average,
                        'winery_labels_count': winery_labels_count,
                        'winery_wines_count': winery_wines_count,
                        'country_name': country_name,  # FOREIGN KEY
                        'region_id': region_id  # FOREIGN KEY
                        }

        review_dict.update({review_id: review_payload})
        user_dict.update({user_id: user_payload})
        wine_dict.update({wine_id: wine_payload})
        vintage_dict.update({vintage_id: vintage_payload})
        country_dict.update({country_name: country_payload})

    return review_dict, user_dict, vintage_dict, wine_dict, country_dict, region_dict


class Selenium_Scraper:
    def __init__(self):
        # initiating the webdriver. Parameter includes the path of the webdriver.
        options = Options()
        # options.headless = True
        # options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # options.add_experimental_option('useAutomationExtension', False)
        # options.add_argument('--no-sandbox')
        # options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        self.driver = webdriver.Chrome('chromedriver', options=options)

    def parse_page(self,url, wine_dict, wine_id, vin_id, n):
        # Load URL and slowly scroll through page to load its content
        self.driver.get(url)
        scroll_length = 1000
        for i in range(0, 5):
            self.driver.execute_script("window.scrollTo(0, " + str(scroll_length) + ")")
            scroll_length += 1000
            time.sleep(1)  # Sleep to ensure page content loads

        # this renders the JS code and stores all of the information in static HTML code.
        soup = BeautifulSoup(self.driver.page_source, "lxml")

        # Get wine_id
        # link = soup1.find_all('link', attrs={'hreflang': 'x-default'})[0].attrs['href']
        # wine_id = link[link.find('/w/'):][3:]

        # Price
        try:
            price = soup.find('span', class_='purchaseAvailabilityPPC__amount--2_4GT').string
        except AttributeError:
            price = soup.find('span', class_='purchaseAvailability__currentPrice--3mO4u').string
        except:
            price = None

        # Get taste structure
        taste_structure = soup.find_all('span', attrs={'class': 'indicatorBar__progress--3aXLX'})
        taste_structure = [t.attrs['style'][t.attrs['style'].find('left: '):][6:-2] for t in taste_structure]
        taste_structure = dict(zip(['bold', 'tannic', 'sweet', 'acidic'], taste_structure))

        # Get taste flavors
        mentions_class = 'tasteNote__mentions--1Hjv0'
        mentions = soup.find_all('div', mentions_class)
        mentions = [m.contents[0][:-12] for m in mentions]
        flavor_class = "tasteNote__flavorGroup--3J0at"
        flavor = soup.find_all('span', class_=flavor_class)
        flavor = [f.string for f in flavor]
        flavor = dict(zip(flavor, mentions))
        #flavor = [str(f)[str(f).find(flavor_class) + len(flavor_class) + 2:-6] for f in flavor]

        # Get foods
        foods = soup.find_all('a', class_='anchor__anchor--3DOSm foodPairing__imageContainer--2CtYR')
        foods = [f.attrs['href'][f.attrs['href'].find('food-pairing/') + 13:] for f in foods]

        # Get world & region rankings
        rank = soup.find_all('label', class_='WineRanking__rankDescription--18uMM')
        rank = [r.string for r in rank]

        wine_dict[wine_id] = {'vintage_id': vin_id,
                              'price': price,
                              'taste_structure': taste_structure,
                              'flavor': flavor,
                              'foods': foods,
                              'rank': rank,
                              'iterations': n  # Map to vin_id and N_iteration
                              }
        return wine_dict

    def close_driver(self):
        self.driver.close()



def detect_language(file): #CHANGE THIS TO FIT
    with open('reviews_1.json') as f:
        data = json.load(f)
        for i in data:
            try:
                data[i]['lang_new']= detect(data[i]['note'])
            except: #Sometimes LangDetectError, although that is not official py error. Ensures that content exists in 'lang_new' 
                data[i]['lang_new'] = 'unknown'
    return data #Returns same data with new item  
