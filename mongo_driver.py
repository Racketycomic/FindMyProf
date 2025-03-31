from dotenv import load_dotenv
import os
from pymongo import MongoClient

load_dotenv()




class mongo_helper:
    def __init__(self):
        self.uri = os.getenv('MONGO_URI')
        self.papers = os.getenv('PAPER_COLLECTION')
        self.prof_db = os.getenv('PROFESSOR_DB')
        self.client = MongoClient(self.uri)
        

    def insert_profs(self,document):
        self.client[self.prof_db][self.papers].insert_one(document)
        
    def check_prof_exists(self,prof_name):
        return self.client[self.prof_db][self.papers].find({prof_name:{"$exists":True}})
        
        
    def close_connection(self):
        self.client.close()