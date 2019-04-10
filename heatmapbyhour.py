from datetime import datetime
import os
import csv
import pandas as pd
import numpy as np
import datetime, pytz
import folium
import folium.plugins as plugins

df= pd.read_csv('/Users/Shiyun/Desktop/Jumpman23_Analysis/Jumpman23/analyze_me.csv')
for dt_col in df.columns.tolist()[-4:]:
    df[dt_col]=pd.to_datetime(df[dt_col])
    df[dt_col].apply(lambda t: t.replace(microsecond =0))
df['weight'] = 1
folium_map = folium.Map(location=[40.738, -73.98],
                        zoom_start=12)

locations = df[['pickup_lat', 'pickup_lon']].values
# plot heatmap
# folium_map.add_child(plugins.HeatMap(locations, radius=15))
# folium_map.save('heatmap.html')

def getHours(row):
    return row.hour
df['hour'] = df.when_the_delivery_started.apply(getHours)
# hour_15D = df.loc[df.hour ==15] 
# hour_15 = folium.Map([40.744607, -73.990742], zoom_start=12)
# stationArr = hour_15D[['pickup_lat', 'pickup_lon']].values
# # plot heatmap
# hour_15.add_child(plugins.HeatMap(stationArr, radius=15))
# folium_map.save('heatmapbyhours.html')

df_hour_list = []
for hour in df.hour.sort_values().unique():
    loc_data_hourly = df.loc[df.hour == hour, ['pickup_lat', 'pickup_lon', 'weight']]
    grouped_loc_data_hourly = loc_data_hourly.groupby(['pickup_lat', 'pickup_lon']).sum().reset_index().values.tolist()
    df_hour_list.append(grouped_loc_data_hourly)
# print(len(df_hour_list))

from folium.plugins import HeatMapWithTime

time_index = [_ for _ in range(23)]
HeatMapWithTime(df_hour_list, min_opacity=0.3, max_opacity=0.8).add_to(folium_map)
folium_map.save('heatmapbyhours.html')