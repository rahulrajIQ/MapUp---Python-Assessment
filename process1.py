#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import datetime as dt

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
    dff=pd.read_parquet(args.to_process, engine='auto')
            
else:
    dff=pd.read_parquet('evaluation_data/input/raw_data.parquet', engine='auto')


# In[97]:


def trip(z):
    global trip_no
    if z>= pd.Timedelta('0 days 07:00:00'):
        trip_no += 1
        return trip_no
    else:
        return trip_no
    
    

def process_1(df,vehicle_code):
    df['time'] = pd.to_datetime(df.timestamp)
    df['time_diff']= df.time.diff().abs()
    df['trip']= df['time_diff'].apply(lambda x: trip(x))
    
    for j in df.trip.unique():
        filename= '/'+str(vehicle_code) +'_'+str(j) +'.csv'
        if args.output_dir:
            df[df.trip==j][dff.columns].to_csv(str(args.output_dir) + filename, index= False)
        else:
            df[df.trip==j][dff.columns].to_csv('evaluation_data/output/process1'+filename, index= False)
        
    


for i in dff.unit.unique():
    trip_no=0
    process_1(dff[dff.unit==i],i)





