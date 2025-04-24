import os
from openai import OpenAI
from mongo_driver.mongo_chatbot import mongo_chat
import time
from langchain_text_splitters import RecursiveCharacterTextSplitter
import numpy as np

class Embed_client:
    def __init__(self):
        self.client = OpenAI(
        api_key=os.getenv('NVIDIA_API_KEY'),
        base_url="https://integrate.api.nvidia.com/v1"
        )
        self.mongo_client = mongo_chat()
        self.total_doc = 0
        self.sample_size = 25
        self.model_key = None
        self.model_value = None
        
    def teardown(self):
        self.client.close()
        self.mongo_client.client.close()
        self.total_doc = 0       
        
    
    
    def get_embeddings(self,text_list,model_name):
        
        response = self.client.embeddings.create(
        input=text_list,
        model=model_name,
        encoding_format="float",
        extra_body={"input_type": "passage", "truncate": "NONE"}
        )
        return response
    
    def create_embeddings(self,model_list):
        for model_key,model_value in model_list.items():
            self.model_key = model_key
            self.model_value = model_value
            self.total_doc = self.mongo_client.get_total_count('temp_pool')
            if self.total_doc <= 0 :
                self.total_doc = self.mongo_client.populate_temp_pool()
            while self.total_doc > 0:
                mongo_document =self.mongo_client.sample_documents(self.sample_size,'temp_pool')
                text_list = [i['passage'] for i in mongo_document]
                response= None
                try:
                    response = self.get_embeddings(text_list,model_value)
                except Exception as e:
                    print("errorred: ",e)
                    if self.mongo_client.get_total_count('temp_pool') <= 25:
                        for idx,text in enumerate(text_list):
                            try:
                                response = self.get_embeddings(text,model_value)
                                self.update_embeddings(response,[mongo_document[idx]])
                            except Exception as e:
                                self.split_meanpool_embed(text,[mongo_document[idx]])
                    # tl,md = self.binary_search_embed(text_list,mongo_document)
                    # self.split_meanpool_embed(tl,md)
                    continue
                # result = [{'_id':mongo_document[idx]['_id'],model_key:embedding.embedding} for idx,embedding in enumerate(response.data)]
                # self.mongo_client.bulk_update_embeddings(result,model_key)
                # total_doc -= sample_size
                self.update_embeddings(response,mongo_document)
                time.sleep(2)
        self.teardown()
        
    
    def update_embeddings(self,response,mongo_document):
        result = [{'_id':mongo_document[idx]['_id'],self.model_key:embedding.embedding} for idx,embedding in enumerate(response.data)]
        self.mongo_client.bulk_update_embeddings(result,self.model_key)
        self.total_doc -= len(result)
        print(len(result))
        

    def split_meanpool_embed(self,text_list,mongo_document):
        print("Inside split meanpool")
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=30)
        texts = text_splitter.split_text(text_list[0])
        response = self.get_embeddings(texts,self.model_value)
        chunk_embedding  = np.mean(np.array([embedding.embedding for embedding in response.data]),axis=0).tolist()
        response = {'data':[{'embedding':chunk_embedding}]}
        result = [{'_id':mongo_document[idx]['_id'],self.model_key:embedding['embedding']} for idx,embedding in enumerate(response['data'])]
        self.mongo_client.bulk_update_embeddings(result,self.model_key)
        self.total_doc -= len(result)
        print(len(result))
        # self.update_embeddings(response,mongo_document)
                

