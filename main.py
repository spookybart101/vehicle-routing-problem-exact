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

# Find all possible routes and their distances
permutations = list(itertools.permutations(points, maxStoresPerRoute))
storesOnRoute = pd.DataFrame(0, index = range(lengthCoords), columns=[])

totalDistances = [0] * (len(permutations))
routes = []

for i in range(len(permutations)):
    perm = permutations[i]
    route = (0,) + perm + (0,)
    
    totalDistance = 0
    storesOnRouteList = [0] * lengthCoords

    # Calculate the total distance of the route
    for j in range(len(route) - 1):
        start = route[j]
        end = route[j + 1]
        totalDistance += distances[start][end]
        storesOnRouteList[start] = 1

    # If the route already exists, check if this solution has a shorter distance
    exists = False
    for idx, existing_route in enumerate(routes):
        if set(existing_route) == set(route):
            exists = True
            duplicate_index = idx 

            if totalDistance < totalDistances[idx]:
                totalDistances[i] = totalDistance
            break

    # If the route does not exist yet, add it to the results
    if not exists:
        storesOnRoute[i] = storesOnRouteList
        totalDistances[i]= (totalDistance)
        routes.append(route)

# Trim storesOnRoute back to ordered columns 
storesOnRoute = storesOnRoute.iloc[:, :(len(routes) + 1)]
storesOnRoute.columns = range(1, len(storesOnRoute.columns) + 1)

# Remove zero values for totalDistances
totalDistances = [distance for distance in totalDistances if distance != 0]

# Check if the route is feasable with the demand of the customers, save routes that are feasable
