import requests
from bs4 import BeautifulSoup
import csv

def write_to_csv(data_list):
    with open('data.csv', 'a') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(data_list)

def parse_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status() 

        soup = BeautifulSoup(response.text, 'html.parser')
        
        car_list = soup.find('div', class_='catalog-list').find_all('a')

        data = []  

        for car in car_list:
            try:
                car_title = car.find('span', class_='catalog-item-caption').text.strip()
            except AttributeError:
                car_title = ''

            try:
                car_price = car.find('span', class_='catalog-item-price').text.strip()
            except AttributeError:
                car_price = ''

            try:
                car_desc = car.find('span', class_='catalog-item-descr').text.strip()
            except AttributeError:
                car_desc = ''

            car_img = car.find('img')
            if car_img:
                car_img = car_img.get('src', '')
            else:
                car_img = ''

            car_data = [car_title, car_price, car_desc, car_img]
            data.append(car_data)

        write_to_csv(data)

    except requests.RequestException as e:
        print(f"ошибка запроса: {e}")

base_url = 'https://cars.kg/offers?page='

for page_num in range(1, 105):
    url = f'{base_url}{page_num}'
    parse_page(url)
