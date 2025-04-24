import os
from pymongo import MongoClient



class mongo_base:
    def __init__(self):
        self.uri = os.getenv('MONGO_URI')
        self.papers = os.getenv('PAPER_COLLECTION')
        self.prof_db = os.getenv('PROFESSOR_DB')
        self.paper_pool = os.getenv('PAPER_POOL')
        self.client = MongoClient(self.uri)
        self.temp_pool = os.getenv('TEMP_POOL')
        self.tables = {'papers':self.papers,'paper_pool':self.paper_pool,'temp_pool':self.temp_pool}
        
    def sample_documents(self,sample_size,table_name):
        pipeline = [
        {
            '$sample': {
                'size': sample_size
            }
        }
        ]
        return list(self.client[self.prof_db][self.tables[table_name]].aggregate(pipeline))
    
    def delete_paper_from_pool(self,id):
        self.client[self.prof_db][self.paper_pool].delete_one({"_id":id})
    
    def populate_temp_pool(self):

        self.client[self.prof_db][self.paper_pool].aggregate([{
            
                '$project': {
                    '_id': 1, 
                    'passage': {
                        '$concat': [
                            '$title', ' ', '$description'
                        ]
                    }
                }
            },
            {
                '$match': {
                    'passage': {
                        '$ne': ' '
                    }
                }
            },
            {
                "$out":self.temp_pool
                }
            ])
        return list(self.client[self.prof_db][self.temp_pool].aggregate([{"$count":"total_documents"}]))[0]['total_documents']
    
    def get_total_count(self,table_name):
        cur = self.client[self.prof_db][self.tables[table_name]].aggregate([{"$count":"total_documents"}])
        res = list(cur)
        if len(res) == 0:
            return 0
        else:
            return res[0]['total_documents']
  
        

class mongo_bot_helper(mongo_base):
    def __init__(self):
        super().__init__()
        
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
    
    def get_prof_list(self):
        return list(self.client[self.prof_db][self.papers].find())
        
    def close_connection(self):
        self.client.close()