import pandas as pd
import math
import itertools

# Settings
maxStoresPerRoute = 2; #Maximum amount of stores per route
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

# Find all possible routes
routes = []
storesOnRoute = pd.DataFrame(0, index = range(lengthCoords), columns=[])
combinations = list(itertools.combinations(points[1:], 1))

storesOnRouteList = [0] * lengthCoords

# Find every combination of possible routes, which satisfy the maxStoresPerRoute constraint 
for i in range(maxStoresPerRoute + 1):
    combinations = list(itertools.combinations(points[1:], i))
    
    for j in range(len(combinations)):
        comb = combinations[j]
        route = (0,) + comb + (0,)

        storesOnRouteList = [0] * lengthCoords
        
        # Find every store on the route, 1 if store is on the route, 0 if store is not on the route
        for k in range(len(route) - 1):
            start = route[k]
            end = route[k + 1]
            storesOnRouteList[start] = 1

        column_name = f"{i}_{j}"
        storesOnRoute[column_name] = storesOnRouteList

        routes.append(route)

# Find feasable routes, which satisfy the demand constraint
demandOnRoute = 0
columns_to_drop = []

for j, column in enumerate(storesOnRoute.columns):
    for i, row in enumerate(storesOnRoute.index):
        if storesOnRoute.loc[i][j] == 1:
            demandOnRoute += demand.loc[row].item()
    
    # Remove routes that are not feasable    
    if demandOnRoute > maxCapacityperRoute:
        columns_to_drop.append(column)
    
    demandOnRoute = 0

storesOnRoute = storesOnRoute.drop(columns=columns_to_drop)
