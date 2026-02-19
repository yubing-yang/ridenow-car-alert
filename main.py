import requests
import time
import logging
import os
import sys

from dotenv import load_dotenv

from geopy.geocoders import Nominatim

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes


#---

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_URL = 'https://ridenow3.ct.ms/api/v2/cars'
POLL_INTERVAL = 60

BRAND_MODEL_INDEX = 1 # Index in full JSON file
LATITUDE_INDEX = 2 # Index in full JSON file
LONGITUDE_INDEX = 3 # Index in full JSON file
BMW_TYPE_ID = 8

TUPLE_LATITUDE_INDEX = 1 # Index in returned tuple
TUPLE_LONGITUDE_INDEX = 2 # Index in returned tuple

geolocator = Nominatim(user_agent="bmw-finder")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)


#---


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.application.bot_data["chat_id"] = update.effective_chat.id
    await update.message.reply_text("Saved")


async def check_cars(context: ContextTypes.DEFAULT_TYPE):

    chat_id = context.application.bot_data.get("chat_id")
    if not chat_id:
        return


def fetch_info() -> dict | None:

    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as error:
        logger.warning(f"An error has occurred: {response.status_code}")
        return None


def find_bmw(data: dict) -> tuple[bool, float | None, float | None]:
    
    cars = data["cars"]

    for car in cars:
        if car[BRAND_MODEL_INDEX] == BMW_TYPE_ID:
            return True, float(car[LATITUDE_INDEX]), float(car[LONGITUDE_INDEX])
    
    return False, None, None


def find_bmw_location(bmw_information) -> str:
    try:
        return geolocator.reverse((bmw_information[TUPLE_LATITUDE_INDEX], bmw_information[TUPLE_LONGITUDE_INDEX]), language='en')
    except Exception as error:
        logger.warning("Reverse geolocator failed")
        return None


#--


def main():

    """
    if not BOT_TOKEN:
        print("Missing Bot Token")
        sys.exit(1)
    
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    application.run_polling()
    """

    while True:
        
        local_time = time.strftime("%H:%M %p", time.localtime())

        data = fetch_info()

        bmw_information = find_bmw(data)
        bmw_location = find_bmw_location(bmw_information)

        print(f"{bmw_information} at: {bmw_location}")

        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    main()
