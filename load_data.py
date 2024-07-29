import json
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'otomoto_project.settings')
django.setup()

from car_listing.models import Car

def load_cars_from_json():
    with open('otomoto_project/all_cars.json', 'r', encoding='utf-8') as f:
        cars = json.load(f)

    for car in cars:
        try:
            Car.objects.create(
                name=car.get('name', 'Brak nazwy'),
                link=car.get('link', 'Brak linku'),
                price=car.get('price', 'Brak ceny'),
                price_currency=car.get('price_currency', 'Brak waluty'),
                mileage=car.get('mileage', 'Brak przebiegu'),
                fuel_type=car.get('fuel_type', 'Brak paliwa'),
                year=car.get('year', 'Brak roku produkcji'),
                gearbox=car.get('gearbox', 'Brak'),
                horsepower=car.get('horsepower', 'Brak'),
                location=car.get('location', 'Brak'),
                image_url=car.get('image_url', 'Brak zdjęcia',),
                engine_capacity=car.get('engine_capacity', 'Brak')
            )
        except Exception as e:
            print("Błąd przy dodawaniu samochodu")

    print("Dane zostały załadowane do bazy danych.")

if __name__ == "__main__":
    load_cars_from_json()