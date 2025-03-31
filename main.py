from bot import prof_bot,scholar_bot
from scraper import find_prof_name
from dotenv import load_dotenv
import os



load_dotenv()

MSN_URL = os.environ.get('MSN_FACULTY_PAGE')
GOOGLE= os.environ.get('GOOGLE')
GSCHOLAR = os.environ.get('GOOGLE_SCHOLAR')

surfer = prof_bot()
prof_list = surfer.get_prof_site(MSN_URL)
print(prof_list)


scholar = scholar_bot(GOOGLE,GSCHOLAR,prof_list)
scholar.insert_prof_details()
# scholar.testground()
# surfer.testground(MSN_URL)