import pandas as pd
import math
import itertools

# Settings
maxStoresPerRoute = 3; #Maximum amount of stores per route
maxCapacityperRoute = 100; #Maximum amount of capacity per route 

# Read the Excel files
coords = pd.read_excel(r'C:\Users\BartO\Desktop\SDVSP\coords.xlsx')
points = coords["Points"]
lengthCoords = len(coords)

demand = pd.read_excel(r'C:\Users\BartO\Desktop\SDVSP\demand.xlsx')

# Compute distances
distances = pd.DataFrame(index=range(lengthCoords), columns=range(lengthCoords))

for i in range(lengthCoords):
    for j in range(lengthCoords):
       distances[i][j] = (math.sqrt((coords.iloc[i][1] - coords.iloc[j][1])**2 + (coords.iloc[i][2] - coords.iloc[j][2])**2))

# Find all possible routes and their distances
permutations = list(itertools.permutations(points, maxStoresPerRoute))

totalDistances = [None] * len(permutations)
storesOnRoute = pd.DataFrame(0, index = range(lengthCoords), columns=range(len(permutations)))

for i in range(len(permutations)):
    perm = permutations[i]
    route = (0,) + perm + (0,)
    
    totalDistance = 0
    for j in range(len(route) - 1):
        start = route[j]
        end = route[j + 1]
        totalDistance = totalDistance + distances[start][end]

        storesOnRoute.loc[start][i] = 1
    totalDistances[i] = totalDistance

print(storesOnRoute)

# Compare routes
