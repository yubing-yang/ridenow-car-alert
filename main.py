import requests
import time
from geopy.geocoders import Nominatim
from colorama import Fore, Back, Style
from colorama import init

init()

API_URL = 'https://ridenow3.ct.ms/api/v2/cars'
BMW_TYPE_ID = 8
POLL_INTERVAL = 60

bmw_status_original = None

geolocator = Nominatim(user_agent="bmw_finder")

while True:

    local_time = time.strftime("%H:%M %P", time.localtime())

    try:
        response = requests.get(API_URL)

        if response.status_code == 200:

            data = response.json()

            print(f"{Style.DIM}{Fore.LIGHTBLACK_EX}Number of Cars:{Style.RESET_ALL} {Style.BRIGHT}{Fore.WHITE}{len(data['cars'])}{Style.RESET_ALL}", end="  ")

            bmw_status = False
            bmw_location = None

            for i, e in enumerate(data["cars"]):

                if e[1] == BMW_TYPE_ID:
                    bmw_latitude = e[2]
                    bmw_longitude = e[3]

                    bmw_location = geolocator.reverse((bmw_latitude, bmw_longitude), language='en')

                    bmw_status = True
                    break

            if bmw_status_original is None or bmw_status_original != bmw_status:

                if bmw_status:
                    print(f"{Style.BRIGHT}{Fore.GREEN}Found at: {Fore.WHITE}{local_time}{Style.RESET_ALL}", end="  ")
                    print(f"{Style.BRIGHT}Location: {bmw_location.address}{Style.RESET_ALL}")

                else:
                    print(f"{Style.BRIGHT}{Fore.RED}Disappeared at: {Fore.WHITE}{local_time}{Style.RESET_ALL}")
            
                bmw_status_original = bmw_status

        else:
            
            print(f"Unsuccessful: , {response.status_code}")

    except requests.exceptions.RequestException as e:
        print("An error has occured")


    time.sleep(POLL_INTERVAL)