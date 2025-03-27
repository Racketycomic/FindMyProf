from bot import bot,scholar_bot
from scraper import find_prof_name
from dotenv import load_dotenv
import os



load_dotenv()

MSN_URL = os.environ.get('MSN_FACULTY_PAGE')
GOOGLE= os.environ.get('GOOGLE')
GSCHOLAR = os.environ.get('GOOGLE_SCHOLAR')

# surfer = bot()
# prof_list = surfer.get_prof_site(MSN_URL)
# print(prof_list)
firstName = "Thomas"
lastName = "Sugar"
url = f""

scholar = scholar_bot(GOOGLE,GSCHOLAR,firstName,lastName)
# fn,ln = prof_list[0].split(' ')
scholar.get_single_prof_Detail()
# scholar.testground()
# surfer.testground(MSN_URL)