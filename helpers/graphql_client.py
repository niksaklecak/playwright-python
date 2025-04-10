import requests
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

class GraphQLClient:
    

    def __init__(self):
        self.url = os.getenv("API_BASE_URL")
        self.session = requests.Session()
        
    
    def execute_query(self, query, variables=None):    
        headers = {'Content-Type': 'application/json'}
        payload = {'query': query, 'variables': variables}
        response = self.session.post(self.url, json=payload, headers=headers)
        return response.json()

    
    def close(self):
        self.session.close()
    


        

    



    