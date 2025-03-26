from bot import bot
from scraper import find_prof_name
from dotenv import load_dotenv
import os



load_dotenv()

MSN_URL = os.environ.get('MSN_FACULTY_PAGE')

surfer = bot()
surfer.create_driver()
surfer.get_prof_site(MSN_URL)
# surfer.testground(MSN_URL)