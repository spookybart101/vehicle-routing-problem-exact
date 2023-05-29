import pandas as pd
from ortools.sat.python import cp_model

# Load Data
routes = pd.read_excel(r'C:\Users\BartO\Desktop\SDVSP\output.xlsx')
costs = pd.read_excel(r'C:\Users\BartO\Desktop\SDVSP\costs_output.xlsx')
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
        optimal_vehicles = len(optimal_routes)

        return optimal_objective, optimal_routes, optimal_route_costs, optimal_vehicles
        

    
    return 'inf', None, None, None


# Start solver
optimal_objective, optimal_routes, optimal_route_costs, optimal_vehicles = solve_vrp(routes, costs, maxVehicles)

# Give output
if optimal_routes:
    print("The following routes are driven: ")
    for route in optimal_routes:
        print(f"{route}: ", end="")
        store_indices = [i for i in range(len(stores)) if routes.iloc[i, route] == 1]
        print(" > ".join([str(i) for i in store_indices]), end=" > 0\n")

    print("Total costs:", optimal_objective)
    print("Amount of vehicles:", optimal_vehicles)
else:
    print("No feasible solution found.")



