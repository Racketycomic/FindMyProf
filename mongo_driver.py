from dotenv import load_dotenv
import os
from pymongo import MongoClient

load_dotenv()

class mongo_helper:
    def __init__(self):
        self.uri = os.getenv('MONGO_URI')
        self.papers = os.getenv('PAPER_COLLECTION')
        self.prof_db = os.getenv('PROFESSOR_DB')
        self.paper_pool = os.getenv('PAPER_POOL')
        self.client = MongoClient(self.uri)
        

    def insert_profs(self,document):
        self.client[self.prof_db][self.papers].insert_one(document)
        
    def check_prof_exists(self,prof_name):
        return self.client[self.prof_db][self.papers].find({prof_name:{"$exists":True}})
    
    def insert_prof_names(self,documents):
        self.client[self.prof_db][self.papers].insert_many(documents)
    
    def insert_papers(self,papers):
        self.client[self.prof_db][self.paper_pool].insert_many(papers)
        
    def insert_paper_by_prof(self,id,paper):
        pipe = [
    {
        "$set": {
            "details": {
                "$concatArrays": [
                    {"$ifNull": ["$details", []]},
                    [paper]
                ]
            }
        }
    }
]
        self.client[self.prof_db][self.papers].update_one({"_id":id},pipe)
    
    
    def get_papers_from_pool(self):
        pipeline = [
     {
        '$sample': {
            'size': 5
        }
    }
    ]
        return list(self.client[self.prof_db][self.paper_pool].aggregate(pipeline))
    
    def delete_paper_from_pool(self,id):
        self.client[self.prof_db][self.paper_pool].delete_one({"_id":id})
        
    def get_prof_list(self):
        return list(self.client[self.prof_db][self.papers].find())
        
    def close_connection(self):
        self.client.close()