import pandas as pd
from ortools.sat.python import cp_model

# Load Data
routes = pd.read_excel(r'C:\Users\BartO\Desktop\SDVSP\output.xlsx')
costs = pd.read_excel(r'C:\Users\BartO\Desktop\SDVSP\costs_output.xlsx')



print(costs)

# Solve problem
def solve_vrp(routes, costs):
    stores = routes.iloc[:, 0].tolist()
    num_stores = len(stores)
    num_routes = len(routes.columns)

    print(routes)
    print(num_routes)
    print(range(num_routes))
    print(range(num_stores))

    model = cp_model.CpModel()
    x = {}
    for i in range(num_routes):
        x[i] = model.NewBoolVar(f'x_{i}')

    print(x)
    # Constraints
    # Make sure every store is visited
    '''
    for j in range(num_stores):
        model.Add(sum(x[i] * routes.iloc[j, i] for i in range(num_routes)) == 1)
        print(j)
    '''
    for j in range(num_stores):
        model.Add(sum(x[i] * routes.iloc[j, i] for i in range(num_routes)) >= 1)

    # Make sure we do not use more than the maximum vehicles

    # Objective function: Minimize costs
    objective = sum(x[i] * costs.iloc[i,0] for i in range(num_routes))
    model.Minimize(objective)

    # Solve the model
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        
        optimal_objective = solver.ObjectiveValue()
        return optimal_objective
        '''
        optimal_routes = []
        for i in range(num_routes):
            if solver.Value(x[i]):
                optimal_routes.append(i)
        
        optimal_route_costs = [costs[i] for i in optimal_routes]

        return optimal_objective, optimal_routes, optimal_route_costs
        '''

    
    return 500000


# Example usage
# optimal_objective, optimal_routes, optimal_route_costs = solve_vrp(routes, costs)

optimal_objective = solve_vrp(routes, costs)
print(optimal_objective)

'''
if optimal_routes:
    for route, cost in zip(optimal_routes, optimal_route_costs):
        print(f"Route {route} is driven with cost {cost}")
else:
    print("No feasible solution found.")
'''
