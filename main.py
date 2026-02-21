import requests
import logging

from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="ridenow-car-finder")
logger = logging.getLogger(__name__)

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

API_URL = 'https://ridenow3.ct.ms/api/v2/cars'


def fetch_info() -> dict:
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as error:
        logger.warning(f"An error has occurred: {response.status_code}")


def find_car(CAR_TYPE_ID, data: dict) -> tuple[bool, float | None, float | None]:
    cars = data["cars"]

    for car in cars:
        if car[1] == CAR_TYPE_ID:
            return True, float(car[2]), float(car[3])
    
    return False, None, None


def find_car_location(lat, lon) -> str:
    try:
        location = geolocator.reverse((lat,lon), language='en', timeout=10)
        return location.address
    
    except Exception as error:
        logger.warning("Reverse geolocator failed")
        return None

def user_input() -> int:
    while True:
        try:
            return int(input("Enter specified car (1-8): "))
        except ValueError:
            continue


def main():
    while True:
        data = fetch_info()

        car_type_id = user_input()
        found, lat, lon = find_car(car_type_id, data)

        if found:
            car_location = find_car_location(lat, lon)
            logger.info(f"Specified car found at {car_location}")
        else:
            logger.info(f"Specified car is not available right now")


if __name__ == "__main__":
    main()