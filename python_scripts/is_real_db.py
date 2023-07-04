from array import array
import requests
from pymongo import MongoClient


# Connect to MongoDB
FILES_DIR = 'output'
CONNECTION_STRING =  'mongodb://localhost:27017/'
client = MongoClient(CONNECTION_STRING)
db = client['swaggerhub']
collection = db['api_specs']
db_oas = client['api_ace_db_dev']
commits = db_oas['commits']
bad_sign = ['localhost', 'api.swaggerhub.com', 'petstore.swagger.io','example.com','virtserver.swaggerhub.com']

def is_real(api):
    if api is not None:    
        if 'servers' in api:
            if isinstance(api['servers'], list):
                for server in api['servers']:   
                    return isinstance(server, dict) and is_reachable(server['url'])            
            else:
                return is_reachable(api['servers'])
        else:   
            return False
          
        if 'host' in api:
            return is_reachable(api['host'])       
        else:
            return False
    else:
        return False

def is_reachable(url, path=None):
    def f(url):
        if not list(filter(lambda x: x in url, bad_sign)):
            try:     
                requests.get(url)                
                return True
            except  Exception as e: 
                return False
    return f(url) if path is None else f(url + path)

def  run(e):
    api  = e['api_spec']
    if is_real(api):
        commits.update_one({'sha': e['sha']}, {'$set': {'reachable': True}})
    else:
        commits.update_one({'sha': e['sha']}, {'$set': {'reachable': False}})
    
if __name__ == "__main__":
    total = commits.count_documents({})
    for i in range(1,total):
        c = commits.find().skip(i).limit(1)
        for api in c:
            print(f"|---- {i} out of {total} commits")
            if api is not None:               
                run(api)             
            else:
                print('No more documents')
                break
    

    