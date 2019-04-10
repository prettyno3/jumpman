import os
import csv
import pandas as pd
import numpy as np
import datetime, pytz

######
#ReadData
######
df= pd.read_csv('/Users/Shiyun/Desktop/Jumpman23_Analysis/Jumpman23/analyze_me.csv')
# print(df.info())
# print(df.isnull().sum())

######
#cleardata
######
ids=df['delivery_id']
#print(ids)
#check repeat delivery_id and each other categories, and we find there are the same
repeat=df[ids.isin(ids[ids.duplicated()])].sort_values('delivery_id')
# print(repeat.head(),repeat.tail())

# dataframe with no repeat value
df=df.drop_duplicates(['delivery_id'], keep='first')
# print(df.info())


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


# distance: The distance between pickup places and the dropoff places.
from geographiclib.geodesic import Geodesic
import math
geod = Geodesic.WGS84 

def distance(data):
    g = geod.Inverse(data['pickup_lon'],data['pickup_lat'],data['dropoff_lon'],data['dropoff_lat'])
    return g['s12']*0.000621371
df['distance']= df.apply(lambda row: distance(row), axis=1)
# print(df['distance'].mean())

# Deliver_speed
# print(df[['transit_time','distance']])
df['delivery_speed']=round(df['distance']/df['transit_time'],2)

# print([df['delivery_speed']])
# print(df.info())

#######
#Analysis
#######

# ###overall analysis On KPIs###
# print('Total Order Deliveries: {0} '.format(len(df.delivery_id)))
# print('Total Customer: {0} '.format(len(df['customer_id'].value_counts())))
# print('Total Marchant: {0} '.format(len(df['pickup_place'].value_counts())))
# print('Total delivery_man: {0} '.format(len(df['jumpman_id'].value_counts())))
# print('Return customer: {0}'.format(len(df['jumpman_id'].value_counts())))
# t=len(df['customer_id'].value_counts())
# r=sum(i>1 for i in df['customer_id'].value_counts())
# print('Return customer ratio :{:.3%}'.format((r/t)))

####average distancex###
# avg_distance=df.groupby(['vehicle_type']).distance.mean()
# print('Total avgerage distance :{:.2f} miles'.format((df['distance'].mean())))
# for i, k in enumerate(avg_distance.to_dict()):
#     print('Average Dilivery distance {0}: {1:.2f} miles'.format(k, avg_distance[k]))

# # Average Delivery time
# print('Total avgerage dlivery time :{:.2f} mins'.format(df['total_time'].mean()))
# avg_deliverytime=df.groupby(['vehicle_type']).total_time.mean()
# for i, k in enumerate(avg_deliverytime.to_dict()):
#     print('Average Dilivery Times for {0}: {1:.2f} mins'.format(k, avg_deliverytime[k]))


# # # Average Transit time
# print('Total avgerage transit time :{:.2f} mins'.format((df['transit_time'].mean())))
# avg_transittime=df.groupby(['vehicle_type']).transit_time.mean()
# for i, k in enumerate(avg_transittime.to_dict()):
#     print('Average Transit Times for {0}: {1:.2f} mins'.format(k, avg_transittime[k]))

# # # average prepare time
# print('Total avgerage prepare time :{:.2f} mins'.format((df['prepare_time'].mean())))
# avg_prepare=df.groupby(['place_category']).transit_time.mean()
# print('Top 10 longest prepare time Place ',avg_prepare.sort_values(ascending=False)[:10])
# print('Top 10 fast prepare time Place',avg_prepare.sort_values(ascending=True)[:10])

# # # average delivery speed
# print('Total avgerage delivery speed time :{0:.3f}mph'.format((df['delivery_speed'].mean())))
# avg_delivery_speed=df.groupby(['vehicle_type']).delivery_speed.mean()
# for i, k in enumerate(avg_delivery_speed.to_dict()):
#     print('Average Transit Times for {0}: {1:.3f} mph'.format(k, avg_delivery_speed[k]))


######
#DATA Visualization 
######
import matplotlib.pyplot as plt

#Customer Order Frequency#
# print(df['customer_id'].value_counts())
# ax=df['customer_id'].value_counts().plot(kind='hist',title='Customer Order Distrubution',bins=20)
# ax.set_ylabel('Mumber of Customers')
# ax.set_xlabel('Orders per customer')
# plt.show()

###plot hourly, daily, weekly consumer Demand###


def date(row, prop):
    return getattr(row, prop)

# demand_hours= df.when_the_delivery_started.apply(date, prop = 'hour').value_counts()
# demand_hours=demand_hours.append(pd.Series([0], index=[5])).sort_index()
# HourlyDemand=demand_hours.plot(kind = 'bar', title = 'Hourly Demand')
# HourlyDemand.set_xlabel('Hour of Day')
# HourlyDemand.set_ylabel('Number of delivery')
# plt.show()


# demand_day= df.when_the_delivery_started.apply(date, prop = 'day').value_counts().sort_index()
# dailydemand=demand_day.plot(kind = 'line', title = 'Daily Demand')
# dailydemand.set_xlabel('Date')
# dailydemand.set_ylabel('Number of delivery')
# plt.show()

# demand_weeks= df.when_the_delivery_started.apply(date, prop = 'dayofweek').value_counts().sort_index()
# # print(demand_weeks)
# weeklyDemand=demand_weeks.plot(kind = 'bar', title = 'Customer Demand day of week')
# plt.xticks(demand_weeks.index, ('Mon', 'Tue', 'Wed', 'Thr', 'Fri','Sat','Sunday'),rotation=0)
# weeklyDemand.set_xlabel('Day of Week')
# weeklyDemand.set_ylabel('Number of delivery')
# plt.show()


###Merchant###

# ### plot most popular restaurant
# p_restaurants = df.groupby('pickup_place').sum()
# # print(p_restaurants.item_quantity.sort_values(ascending=False)[:30])
# ax=p_restaurants.item_quantity.sort_values(ascending=False)[:30].plot(kind='barh',title='Top 30 Restraurants in NYC',fontsize=10,color='c')
# ax.set_ylabel('Restaurant Name')
# ax.set_xlabel('Number of order')
# ax.invert_yaxis() 
# plt.show()

# ### plot most popular catrgories
# p_categories = df.groupby('place_category').sum()
# ax=p_categories.item_quantity.sort_values(ascending=False)[:30].plot(kind='barh', title='Top 30 Categories in NYC',color='c')
# ax.set_ylabel('Category Name')
# ax.set_xlabel('Number of order')
# ax.invert_yaxis() 
# plt.show()

# ### plot number of marchant preparetime
# p_restaurants_prep = (df.groupby('pickup_place').mean())
# # print(p_restaurants_prep['prepare_time'])
# ax=p_restaurants_prep['prepare_time'].plot(kind='hist',title='Merchant Prepare time distrubution')
# ax.set_ylabel('Mumber of Merchants')
# ax.set_xlabel('Prepare Time')
# plt.show()

## Plot Jumpman ###

# trans = df.vehicle_type.value_counts()
# # print(type(trans))
# fig1, ax1 = plt.subplots()
# ax1.pie(trans, startangle=90,labeldistance=1.05)
# plt.title('Most popular model of transport for Jumpman')
# tlabels = []
# tsum = sum(trans)
# for i in range(len(trans.index)):
#     tlabels.append(trans.index[i] + ': ' + str(round(trans[i]/tsum*100,2))+ '%')

# plt.legend(labels=tlabels, bbox_to_anchor=(0.85,1.025), loc="upper left")
# plt.tight_layout()
# plt.show()


### boxplot on distance###
# df.boxplot(column='distance',by='vehicle_type')
# plt.title('Distance by vehicle type')
# plt.xlabel('Vehicle_type')
# plt.ylabel('Distance')
# plt.show()


###plot on delivery_speed ###
df.boxplot(column='delivery_speed',by='vehicle_type')
plt.title('delivery_speed by vehicle_type')
plt.xlabel('Vehicle_type')
plt.ylabel('delivery_speed')
plt.show()

