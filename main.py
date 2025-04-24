from driver.bot import scholar_bot
from driver.bot import prof_bot
from mongo_driver.mongo_driver import mongo_bot_helper
from rag.embedder import Embed_client


from dotenv import load_dotenv
import random
import os
import time
import argparse
import datetime


parser = argparse.ArgumentParser()
parser.add_argument("-n","--number",help="Number of times to run the Paper details scraper")
args = parser.parse_args()



load_dotenv()

print("Start time:",datetime.datetime.now())

MSN_URL = os.environ.get('MSN_FACULTY_PAGE')
GOOGLE= os.environ.get('GOOGLE')
GSCHOLAR = os.environ.get('GOOGLE_SCHOLAR')

def scrape_prof_names():
    surfer = prof_bot()
    prof_list = surfer.get_prof_site(MSN_URL)
    print(prof_list)

def scrape_paper_list():
    mc = mongo_bot_helper()
    scholar = scholar_bot(GOOGLE,GSCHOLAR,mc)
    scholar.insert_paper_links()
    
# scrape_paper_list()
def scrape_paper_details():
    mc = mongo_bot_helper()
    scholar = scholar_bot(GOOGLE,GSCHOLAR,mc)
    for i in range(int(args.number)):
        x = scholar.random_paper_insert()
        if x == False:
            break
        time.sleep(random.uniform(120,180))
    mc.client.close()
    scholar.driver.quit()
# scrape_paper_details()

def create_embeddings():
    model_list = {
        'MISTRALV2_7B':os.getenv('MISTRALV2_7B'),
        }
    e = Embed_client()
    e.create_embeddings(model_list)
    
create_embeddings()
    

print("End time:",datetime.datetime.now())
# scholar.testground()
# surfer.testground(MSN_URL)