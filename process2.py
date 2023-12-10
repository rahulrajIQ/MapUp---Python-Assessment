import pandas as pd
import datetime as dt
import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()



import argparse


# Initialize parser
parser = argparse.ArgumentParser()

# Adding optional argument
parser.add_argument("-i", "--to_process", help = "to_process")
parser.add_argument("-o", "--output_dir", help = "output_dir")

# Read arguments from command line
args = parser.parse_args()


# In[106]:



if args.to_process:
    folder_path = args.to_process
    all_files = os.listdir(args.to_process)    
    csv_files = list(filter(lambda f: f.endswith('.csv'), all_files))            
else:
    folder_path = "evaluation_data/output/process1"
    all_files = os.listdir(folder_path)    
    csv_files = list(filter(lambda f: f.endswith('.csv'), all_files))


url = os.getenv('TOLLGURU_API_URL')
headers = {'x-api-key': os.getenv('TOLLGURU_API_KEY'), 'Content-Type': 'text/csv'}

for i in csv_files:
    file_path = folder_path +'/'+ i
    with open(file_path, 'rb') as file:
        response = requests.post(url, data=file, headers=headers)
        data = json.loads(response.content)
        
    if args.output_dir:
        with open(args.output_dir +'/'+ i[:-4] + '.json', 'w') as f:
            json.dump(data, f)
    else:
        with open("evaluation_data/output/process2/" + i[:-4] + '.json', 'w') as f:
            json.dump(data, f)
            
            

