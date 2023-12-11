import requests
from bs4 import BeautifulSoup
import csv

def parse_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status() 

        soup = BeautifulSoup(response.text, 'html.parser')
        
        cars = soup.find('div', class_='catalog-list').find_all('a')

        for car in cars:
            try:
                title = car.find('span', class_='catalog-item-caption').text.strip()
            except AttributeError:
                title = ''

            try:
                price = car.find('span', class_='catalog-item-price').text.strip()
            except AttributeError:
                price = ''

            try:
                desc = car.find('span', class_='catalog-item-descr').text.strip()
            except AttributeError:
                desc = ''

            img = car.find('img')
            if img:
                img = img.get('src', '')
            else:
                img = ''

            data = {
                'title': title,
                'price': price,
                'desc': desc,
                'img': img
            }

            write_to_csv(data)

    except requests.RequestException as e:
        print(f"Ошибка запроса: {e}")

def write_to_csv(data):
    with open('data.csv', 'a', newline='', encoding='utf-8') as file:
        write = csv.writer(file)
        write.writerow((data['title'], data['price'], data['img'], data['desc']))

base_url = 'https://cars.kg/offers?page='

for page_number in range(1, 100):
    url = f'{base_url}{page_number}'
    parse_page(url)
