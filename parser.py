import requests
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import re

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
url = 'https://www.mcdonalds.com/ua/uk-ua/eat/fullmenu.html'

def click_on_page(link):
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    full_url = f'https://www.mcdonalds.com{link}'
    driver.get(full_url)
    try:
        try:
            # Wait for the button with the specific class and title text
            button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//button[contains(@class, 'cmp-accordion__button') and .//span[text()='Енергетична цінність та вміст поживних речовин']]"
                ))
            )
            button.click()
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "cmp-nutrition-summary__heading-primary-item"))
            )
        except Exception as e:
            print(f"Accordion button not found or not clickable: {e}")
        selenium_content = driver.page_source
        return selenium_content

    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        driver.quit()


def links_scraper(url, header):
    response = requests.get(url, headers=header)
    content_html = BeautifulSoup(response.text, 'html.parser')
    if response.status_code == 200:
        links = []
        for link in content_html.find_all('a', class_='cmp-category__item-link'):
            links.append(link.get('href'))
        return links
    else:
        return f"Error: {response.status_code}"
    
def name_searcher(content_html):
    header = content_html.find('h1')
    name = header.find('span', class_="cmp-product-details-main__heading-title").text
    return name

def description_searcher(content_html):
    description_block = content_html.find('div', class_="cmp-product-details-main__description")
    description_text = description_block.find('span', class_='body').text.replace('\xa0', ' ')
    return description_text

def nutrition_primary_searcher(content_html):
    target_li = list(content_html.find_all('li', class_='cmp-nutrition-summary__heading-primary-item'))
    nutrition_dict = {}
    for li in target_li:
        value_span = li.find('span', class_='value')
        value = value_span.find('span', attrs={'aria-hidden': 'true'})
        value_text = value.get_text(strip=True) if value else ''

        metric_span = li.find('span', class_='metric')
        metric_name = ''
        if metric_span:
            metric_name = metric_span.find('span', attrs={'aria-hidden': 'true'})
            metric_name = metric_name.get_text(strip=True).split('(')[0].strip() if metric_name else ''

        daily_value = ''
        if metric_span:
            metric_text = metric_span.find('span', attrs={'aria-hidden': 'true'})
            if metric_text:
                match = re.search(r'\((\d+\s*%)', metric_text.get_text())
                if match:
                    daily_value = match.group(1)

        nutrition_dict[metric_name] = f'{value_text}, {daily_value} DV'
    return nutrition_dict

def nutrition_secondary_searcher(content_html):
    nutrition_dict = {}
    target_li = content_html.find_all('li', class_='label-item')
    
    for li in target_li:
        metric_span = li.find('span', class_='metric')
        metric_name = metric_span.get_text(strip=True).replace(':', '') if metric_span else ''
        value_span = li.find('span', class_='value')
        visible_value_tag = value_span.find('span', attrs={'aria-hidden': 'true'}) if value_span else None
        if visible_value_tag:
            raw_value = visible_value_tag.get_text(strip=True)
            match = re.search(r'([\d.,]+[г\w/]+)?\s*(\([\d\s\w/]+\))?', raw_value)
            
            if match:
                value = match.group(1) or ''.replace('/g', '')
                dv = match.group(2) or ''
            else:
                value = raw_value
                dv = ''
                
            if metric_name:
                nutrition_dict[metric_name] = f'{value} {dv}'.strip()

    return nutrition_dict


def products_parser(links):
    result_json = {}
    for link in links:
        content_html = click_on_page(link)
        if content_html:
            content_html = BeautifulSoup(content_html, 'html.parser')
            name_and_description = {
                'name': name_searcher(content_html), 
                'description': description_searcher(content_html)
                }
            nutrients = {
                **nutrition_primary_searcher(content_html),
                **nutrition_secondary_searcher(content_html)
            }
            result_json[link] = { **name_and_description, **nutrients }
            print(result_json)
        else:
            print(f"Error: ")
        break

links = links_scraper(url, header)
products_parser(links)

