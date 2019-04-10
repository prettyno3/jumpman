import os
import csv
import pandas as pd
import numpy as np
import datetime, pytz
import folium
import folium.plugins as plugins

df= pd.read_csv('/Users/Shiyun/Desktop/Jumpman23_Analysis/Jumpman23/analyze_me.csv')


locations = df[['pickup_lat', 'pickup_lon']]
locationlist = locations.values.tolist()
folium_map = folium.Map(location=[40.738, -73.98],
                        zoom_start=13,
                        tiles="CartoDB dark_matter")
marker_cluster = plugins.MarkerCluster().add_to(folium_map)

for point in range(len(locationlist)):
    folium.Marker(locationlist[point], popup=df['pickup_place'][point]).add_to(marker_cluster)

# df['distance']= df.apply(lambda row: distance(row), axis=1)

folium_map.save('cluster.html')

