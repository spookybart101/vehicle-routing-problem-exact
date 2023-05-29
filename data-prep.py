import pandas as pd
import math
import itertools

# Settings
maxStoresPerRoute = 3        #Maximum amount of stores per route
maxCapacityperRoute = 100    #Maximum amount of capacity per route 
cost = 1                     #Cost per distance

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
    combinations = list(itertools.combinations
                        
                        (points[1:], i))
    
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
routes_to_remove = []
for j, column in enumerate(storesOnRoute.columns):
    for i, row in enumerate(storesOnRoute.index):
        if storesOnRoute.loc[i][j] == 1:
            demandOnRoute += demand.loc[row].item()
    
    # Remove routes that are not feasable    
    if demandOnRoute > maxCapacityperRoute:
        columns_to_drop.append(column)
        routes_to_remove.append(routes[j])
    demandOnRoute = 0

storesOnRoute = storesOnRoute.drop(columns=columns_to_drop)

for route in routes_to_remove:
    routes.remove(route)

# Compute minimal distance for each route
def compute_distance(route):
    total_distance = 0

    for j in range(len(route) - 1):
        start = route[j]
        end = route[j + 1]
        total_distance += distances[start][end]
    return total_distance

tempDistances = []
tempName = []
totalDistances = []
fastest_perms = []

for i, route in enumerate(routes):
    start_end = route[1:-1]  # Extract the intermediate stops
    permutations = list(itertools.permutations(start_end))

    for perm in permutations:
        perm_route = [0] + list(perm) + [0]  # Add the start and end points (0)
        distance = compute_distance(perm_route) 
        tempDistances.append(distance)
        tempName.append(perm)

    # Save the minimum distance of each permutation
    min_distance = min(tempDistances)
    totalDistances.append(min_distance)

    min_distance_index = tempDistances.index(min_distance)
    fastest_perms.append(str(tempName[min_distance_index]))

    tempDistances = []
    tempName = []

# Compute costs per route
costs = []

for i, totalDistance in enumerate(totalDistances):
    cost_value = totalDistance * cost
    costs.append(cost_value)

# Export Data
other_information = pd.DataFrame({'route' :fastest_perms,  'distance' :totalDistances, 'costs' : costs})
storesOnRoute.to_excel(r'C:\Users\BartO\Desktop\SDVSP\output.xlsx', index=False)
other_information.to_excel(r'C:\Users\BartO\Desktop\SDVSP\output_extra.xlsx', index=False)
