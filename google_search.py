# gets the next 100 results not done in the excel file
import json
import requests
import pandas as pd
import logging

API_KEY = '' # put Google Custom Search API key here
# create a google programmable search engine that excludes "www.puc.texas.gov/*" 
SEARCH_ENGINE_ID = '' # search engine id should be available to copy after creating the search engine


logging.basicConfig(filename='google_search.log', level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("-------- RUNNING PROGRAM --------")

def build_params(query):
    return {
        'key' : API_KEY,
        'q' : query,
        'cx' : SEARCH_ENGINE_ID,
    }
 
def request(params):
    response = requests.get('https://customsearch.googleapis.com/customsearch/v1', params=params)  
    if response.status_code != 200: 
        logger.error(response.status_code)
        logger.error(response.headers)
        raise Exception(response.status_code)
    logger.info(response.json())
    return response.json()
   
# beginning process: get current json data 
with open('outfile.json', 'r') as file:
    outdata = json.load(file)
    
# load excel table of companies
names_excel = pd.ExcelFile("./PUCT_drinking_water_directory.xlsx")
names_df = names_excel.parse("WaterDB_WaterUtilities_List_Exc")

for i in range(len(outdata['data']), len(outdata['data']) + 100):
    query = names_df.loc[i]['Utility Name'] + " texas water utility website"
    params = build_params(query)
    results = request(params)
    # 'items' contains the search result data 
    outdata['data'].append(results['items'])
    
# finally: write search data to json
with open('outfile.json', 'w') as file:
    file.write(json.dumps(outdata))