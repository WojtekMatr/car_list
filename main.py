import requests
from bs4 import BeautifulSoup
import json
import csv
import time


def fetch(page_number):
    while True:
        url = f'https://www.otomoto.pl/osobowe?page={page_number}'
        try:
            response = requests.get(url)
            response.raise_for_status()
            html_content = response.content
            soup = BeautifulSoup(html_content, 'html.parser')
            car_elements = soup.find_all('article', class_='ooa-yca59n')
            return car_elements
        except (requests.RequestException, Exception) as e:
            print(f'Błąd podczas pobierania strony {page_number}: {e}. Próba ponownie za 5 sekund...')
            time.sleep(5)
def data_save(element):
    name_tag = element.find('h1', class_='e1vic7eh9')
    name = name_tag.get_text() if name_tag else 'Brak nazwy'
    link_tag = name_tag.find('a') if name_tag else None
    link = link_tag.get('href') if link_tag else 'Brak linku'

    img_tag = element.find('img', class_='e17vhtca4 ooa-2zzg2s')
    img_url = img_tag.get('src') if img_tag else 'Brak zdjęcia'

    price_tag = element.find('h3', class_='e1vic7eh16')
    price = price_tag.get_text() if price_tag else 'Brak ceny'
    price_currency_tag = element.find('p', class_='e1vic7eh17')
    price_currency = price_currency_tag.get_text() if price_currency_tag else 'Brak waluty'

    location_tag = element.find('dd', class_='ooa-1jb4k0u e1vic7eh15')
    location = 'Brak lokalizacji'
    if location_tag:
        location_paragraph = location_tag.find('p', class_='ooa-gmxnzj')
        location = location_paragraph.get_text() if location_paragraph else 'Brak lokalizacji'

    details = element.find_all('dd', class_='ooa-1omlbtp')
    mileage = details[0].get_text() if len(details) > 0 else 'Brak przebiegu'
    fuel_type = details[1].get_text() if len(details) > 1 else 'Brak paliwa'
    year = details[3].get_text() if len(details) > 3 else 'Brak roku produkcji'
    gearbox = details[4].get_text() if len(details) > 4 else 'Brak skrzyni biegów'
    horsepower = details[5].get_text() if len(details) > 5 else 'Brak koni mechanicznych'

    engine_and_power_tag = element.find('p', class_='e1vic7eh10 ooa-1tku07r er34gjf0')
    if engine_and_power_tag:
        engine_power_text = engine_and_power_tag.get_text()
        engine_capacity = engine_power_text.split('•')[0].strip()
        horsepower = engine_power_text.split('•')[1].split('KM')[0].strip()

    gearbox_tag = element.find('dd', {'data-parameter': 'gearbox'})
    gearbox_type = 'Brak typu skrzyni biegów'
    if gearbox_tag:
        # Pobranie tekstu po tagu <svg>
        gearbox_type_text = gearbox_tag.get_text(strip=True)
        if 'Manualna' in gearbox_type_text:
            gearbox_type = 'Manualna'
        elif 'Automatyczna' in gearbox_type_text:
            gearbox_type = 'Automatyczna'

    car_data = {
        'name': name,
        'link': link,
        'price': price,
        'price_currency': price_currency,
        'mileage': mileage,
        'fuel_type': fuel_type,
        'year': year,
        'gearbox': gearbox_type,
        'horsepower': horsepower,
        'location': location,
        'image_url': img_url,
        'engine_capacity': engine_capacity
    }
    return car_data

all_cars = []

for page in range(1, 70):
    print(f'Pobieranie danych z strony {page}')
    car_elements = fetch(page)
    if not car_elements:
        print(f'Brak ogłoszeń na stronie {page}, przerywanie.')
        break

    for element in car_elements:
        car_data = data_save(element)
        all_cars.append(car_data)


    time.sleep(1)

with open('otomoto_project/otomoto_project/all_cars.json', 'w', encoding='utf-8') as f:
    json.dump(all_cars, f, ensure_ascii=False, indent=4)

print("Dane zostały zapisane.")

with open('otomoto_project/all_cars.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['name', 'link', 'price', 'price_currency', 'mileage', 'fuel_type', 'year',
                                           'gearbox', 'horsepower', 'location', 'image_url', 'engine_capacity'])
    writer.writeheader()
    writer.writerows(all_cars)

print("Dane zostały zapisane")
