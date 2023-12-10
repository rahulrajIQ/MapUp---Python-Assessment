import pandas as pd
import datetime as dt
import json
import os

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
    json_files = list(filter(lambda f: f.endswith('.json'), all_files))            
else:
    folder_path = "evaluation_data/output/process2"
    all_files = os.listdir(folder_path)    
    json_files = list(filter(lambda f: f.endswith('.json'), all_files))


def check_null(x):
    if x is None:
        return ''
    else:
        return x


df=pd.DataFrame()

for i in json_files:
    unit= i.split('.')[0].split('_')[0]
    trip_id= i.split('.')[0].split('_')[1]

    file_path = folder_path +'/'+ i
    f = open(file_path)
    data = json.load(f)
    f.close()

    if 'route' in data.keys():
        if 'tolls' in data['route'].keys():
            for j in data['route']['tolls']:
                toll_system_type = check_null(j['type'])
                tag_cost = check_null(j['tagCost'])
                cash_cost= check_null(j.get('cashCost'))
                license_plate_cost = check_null(j['licensePlateCost'])

                toll_loc_id_start = check_null(j['start']['id'])
                toll_loc_id_end = check_null(j['end']['id'])
                toll_loc_name_start = check_null(j['start']['name'])
                toll_loc_name_end = check_null(j['end']['name'])
                entry_time= check_null(j['start']['arrival']['time'])
                exit_time= check_null(j['end']['arrival']['time'])

                dictionary={
                    'unit':unit,
                    'trip_id': trip_id,
                    'toll_loc_id_start': toll_loc_id_start,
                    'toll_loc_id_end': toll_loc_id_end,
                    'toll_loc_name_start': toll_loc_name_start,
                    'toll_loc_name_end': toll_loc_name_end,
                    'toll_system_type': toll_system_type,
                    'entry_time': entry_time,
                    'exit_time': exit_time,
                    'tag_cost': tag_cost,
                    'cash_cost': cash_cost,
                    'license_plate_cost': license_plate_cost
                }
                df_dictionary = pd.DataFrame([dictionary])
                df = pd.concat([df, df_dictionary], ignore_index=True)


filename_to_save= '/'+  'transformed_data.csv'
if args.output_dir:
    df.to_csv(str(args.output_dir) + filename_to_save, index= False)
else:
    df.to_csv('evaluation_data/output/process3'+ filename_to_save, index= False)