import pandas as pd
import math
import itertools

# Settings
maxStoresPerRoute = 3; #Maximum amount of stores per route
maxCapacityperRoute = 100; #Maximum amount of capacity per route 

# Read the Excel files
coords = pd.read_excel(r'C:\Users\BartO\Desktop\SDVSP\coords.xlsx')
lengthCoords = len(coords)

demand = pd.read_excel(r'C:\Users\BartO\Desktop\SDVSP\demand.xlsx')

# Compute distances
distances = pd.DataFrame(index=range(lengthCoords), columns=range(lengthCoords))

for i in range(lengthCoords):
    for j in range(lengthCoords):
       distances[i][j] = (math.sqrt((coords.iloc[i][1] - coords.iloc[j][1])**2 + (coords.iloc[i][2] - coords.iloc[j][2])**2))

# Find routes

