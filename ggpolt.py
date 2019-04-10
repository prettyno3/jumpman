import os
import csv
import pandas as pd
import numpy as np
import datetime, pytz

######
df= pd.read_csv('/Users/Shiyun/Desktop/Jumpman23_Analysis/Jumpman23/analyze_me.csv')
df=df.drop_duplicates(['delivery_id'], keep='first')
### get rid of inapporate timeformat:
for dt_col in df.columns.tolist()[-4:]:
    df[dt_col]=pd.to_datetime(df[dt_col])
    df[dt_col].apply(lambda t: t.replace(microsecond =0))


######
## Data Processing 
######

### pick up wait time 
df['total_time'] = (df.when_the_Jumpman_arrived_at_dropoff - df.when_the_delivery_started)
df['total_time']=df['total_time'].astype('timedelta64[s]')/60
df['prepare_time'] = df.when_the_Jumpman_left_pickup - df.when_the_Jumpman_arrived_at_pickup
df['prepare_time']=df['prepare_time'].astype('timedelta64[s]')/60
df['transit_time']=df.when_the_Jumpman_arrived_at_dropoff - df.when_the_Jumpman_left_pickup
df['transit_time']=df['transit_time'].astype('timedelta64[s]')/60

from geographiclib.geodesic import Geodesic
import math
geod = Geodesic.WGS84 

def distance(data):
    g = geod.Inverse(data['pickup_lon'],data['pickup_lat'],data['dropoff_lon'],data['dropoff_lat'])
    return g['s12']*0.000621371
df['distance']= df.apply(lambda row: distance(row), axis=1)

df['delivery_speed']=round(df['distance']/df['transit_time'],2)

from ggplot import *

# df = pd.melt(df)
g=ggplot(aes(x=df['customer_id']), data=df) + geom_histogram()
# ggplot(aes(x='value', color='variable'), data=df) + \
#     geom_histogram()
print(g)