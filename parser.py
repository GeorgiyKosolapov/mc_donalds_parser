import requests
import json
from bs4 import BeautifulSoup

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
url = 'https://www.mcdonalds.com/ua/uk-ua/eat/fullmenu.html'
tags_to_find = ['h1', 'span', 'li', 'div']


def links_scraper(url, header):
    response = requests.get(url, headers=header)
    soup = BeautifulSoup(response.text, 'html.parser')
    if response.status_code == 200:
        links = []
        for link in soup.find_all('a', class_='cmp-category__item-link'):
            links.append(link.get('href'))
        return links
    else:
        return f"Error: {response.status_code}"
    
def name_searcher(soup):
    header = soup.find('h1')
    name = header.find('span', class_="cmp-product-details-main__heading-title").text
    return name

def description_searcher(soup):
    description_block = soup.find('div', class_="cmp-product-details-main__description")
    description_text = description_block.find('span', class_='body').text.replace('\xa0', '')
    return description_text

def nutrition_primary_searcher(soup):
    primary_nutrition_table = soup.find_all('ul', class_='cmp-nutrition-summary__heading-primary')
    nutrients = [nutrient.text for nutrient in primary_nutrition_table.find_all('li', class_='cmp-nutrition-summary__heading-primary-item')]
    print(nutrients)
    return nutrients

def products_parser(links):
    result_json = {}
    for link in links:
        response = requests.get(f'https://www.mcdonalds.com{link}', headers=header)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            result_json[link] = {
                'name': name_searcher(soup),
                'description': description_searcher(soup),
                'calories': 'N/A',
                'fats': 'N/A',
                'carbs': 'N/A',
                'proteins': 'N/A',
                'unsaturated_fats': 'N/A',
                'sugar': 'N/A',
                'salt': 'N/A',
                'portion': 'N/A',
                'nutrients': nutrition_primary_searcher(soup)
            }
            print(result_json)
        else:
            print(f"Error: {response.status_code}")
        break

links = links_scraper(url, header)
products_parser(links)

