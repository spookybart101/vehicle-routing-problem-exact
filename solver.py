import pandas as pd
from ortools.sat.python import cp_model
import matplotlib.pyplot as plt

# Load Data
routes = pd.read_excel(r'C:\Users\BartO\Desktop\SDVSP\output.xlsx')
extra_information = pd.read_excel(r'C:\Users\BartO\Desktop\SDVSP\output_extra.xlsx')

costs = extra_information[['costs']]
distances = extra_information[['distance']]
coords = pd.read_excel(r'C:\Users\BartO\Desktop\SDVSP\coords.xlsx')

stores = routes.iloc[:, 0].tolist()
maxVehicles = 5

# Solve problem
def solve_vrp(routes, costs, maxVehicles):
    num_stores = len(stores)
    num_routes = len(routes.columns)

    model = cp_model.CpModel()
    x = {}
    for i in range(num_routes):
        x[i] = model.NewBoolVar(f'x_{i}')

    # Constraints
    for j in range(num_stores):
        model.Add(sum(x[i] * routes.iloc[j, i] for i in range(num_routes)) >= 1)

    # Make sure we do not use more than the maximum vehicles
    model.Add(sum(x[i] for i in range(num_routes)) <= maxVehicles)

    # Objective function: Minimize costs
    objective = sum(x[i] * costs.iloc[i,0] for i in range(num_routes))
    model.Minimize(objective)

    # Solve the model
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        optimal_objective = solver.ObjectiveValue()
        
        optimal_routes = []
        for i in range(num_routes):
            if solver.Value(x[i]):
                optimal_routes.append(i)
        
        optimal_route_costs = [costs.iloc[i,0]  for i in optimal_routes]
        optimal_route_distances = [distances.iloc[i,0]  for i in optimal_routes]
        optimal_vehicles = len(optimal_routes)

        return optimal_objective, optimal_routes, optimal_route_costs, optimal_route_distances, optimal_vehicles
        

    
    return 'inf', None, None, None


# Start solver
optimal_objective, optimal_routes, optimal_route_costs, optimal_route_distances, optimal_vehicles = solve_vrp(routes, costs, maxVehicles)

# Give output
if optimal_routes:
    print("The following routes are driven: ")
    for route_index in optimal_routes:
        route_name = extra_information.loc[route_index, 'route']
        stores = [0] + [int(store) for store in route_name.strip('()').split(',')]
        print(f"{route_index}: ", end="")
        print(" > ".join([str(i) for i in stores]), end=" > 0\n")


    print("Total costs:", optimal_objective)
    print("Total distance:", sum(optimal_route_distances))
    print("Distance per route:", optimal_route_distances )
    print("Amount of vehicles:", optimal_vehicles)
else:
    print("No feasible solution found.")

# Visualize the solution
if optimal_routes:
    # Extract store coordinates
    x_coords = coords['X'].tolist()
    y_coords = coords['Y'].tolist()

    # Extract the selected routes
    selected_routes = optimal_routes

    # Plot the store locations
    plt.scatter(x_coords, y_coords, marker='o', color='black')

    # Plot the routes
    for route_index in optimal_routes:
        route_name = extra_information.loc[route_index, 'route']
        stores = [0] + [int(store) for store in route_name.strip('()').split(',')] + [0]
        x = [x_coords[i] for i in stores]
        y = [y_coords[i] for i in stores]
        plt.plot(x, y, marker='o')

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Solution Visualization')
    plt.grid(True)
    plt.show()
