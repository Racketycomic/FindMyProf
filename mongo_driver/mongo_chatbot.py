from mongo_driver.mongo_driver import mongo_base
from pymongo import UpdateOne


class mongo_chat(mongo_base):
    
    def __init__(self):
        super().__init__()
        
    
    def bulk_update_embeddings(self,embedding_list,model_name):
        update_query = [
            UpdateOne(
                {"_id": paper['_id']},
                {'$set':{model_name:paper[model_name]}}
            )
             for paper in embedding_list
        ]
        self.client[self.prof_db][self.temp_pool].delete_many({'_id':{'$in':[paper['_id'] for paper in embedding_list]}})
        self.client[self.prof_db][self.paper_pool].bulk_write(update_query)
