import requests
from bs4 import BeautifulSoup
import csv

def write_to_csv(data_list):
    with open('data.csv', 'a', newline='') as file:
        csv_writer = csv.writer(file)
        for data in data_list:
            csv_writer.writerow(data)

def parse_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status() 

        soup = BeautifulSoup(response.text, 'html.parser')
        
        car_list = soup.find('div', class_='catalog-list').find_all('a')

        data = []  

        for car in car_list:
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

            car_data = [title, price, desc, img]
            data.append(car_data)

        write_to_csv(data)

        return True  

    except requests.RequestException as e:
        print(f"ошибка запроса: {e}")
        return False  

base_url = 'https://cars.kg/offers?page='

page_num = 1
while True:
    url = f'{base_url}{page_num}'
    success = parse_page(url)

    if not success:  
        break
    page_num += 1
