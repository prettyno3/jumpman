from datetime import datetime
import os
import csv
import pandas as pd
import numpy as np
import datetime, pytz
import folium
import folium.plugins as plugins

df= pd.read_csv('/Users/Shiyun/Desktop/Jumpman23_Analysis/Jumpman23/analyze_me.csv')


folium_map = folium.Map(location=[40.738, -73.98],
                        zoom_start=12)

locations = df[['pickup_lat', 'pickup_lon']].values

# plot heatmap
folium_map.add_child(plugins.HeatMap(locations, radius=15))
folium_map.save('heatmap.html')