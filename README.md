# Vehicle Routing Problem

This repository contains a solution for the Vehicle Routing Problem, which is a combinatorial optimization problem in the field of logistics. The goal is to determine the optimal routes for a fleet of vehicles to serve a set of customers, minimizing the total distance traveled.

## Features

- The program considers the three following constraints: maximum capacity per vehicle, the maximum number of stores visited per route and maximum amount of vehicles.
- The constraints are incorporated in the generation of feasible routes.
- You can adjust parameters such as costs per distance, maximum capacity, maximum stores per route, and the maximum number of vehicles in the respective files: `data-prep.py` and `solver.py`.

## Usage
  1. Set the demand and coordinates for each customer in the respective Excel files named `demand.xlsx` and `coords.xlsx`. Ensure that customer 0 is designated as the depot, and the remaining customers are defined accordingly.
  2. Modify the parameters in the `data-prep.py` file to set the maximum capacity per vehicle, maximum number of stores per route, and other relevant data for the problem.
  3. Run the `data-prep.py` script to prepare the input data.
  4. Modify the `max_vehicles` parameter in the `solver.py` file to set the maximum number of vehicles available for the routing problem.
  5. Run the `solver.py` script to find the optimal routes and generate the output.
  6. After running the solver, the output will be visualized to provide a clear representation of the computed routes.

- Please note that this solution is suitable for small-scale problems where an exact solution is feasible. For larger problems, finding an optimal solution becomes computationally challenging or infeasible.

## Visualization

After running the solution, you can visualize the generated routes on a graph to gain insights into the optimal solution. The visualization plots the store locations and the routes taken by the vehicles.

## License

This project is licensed under the MIT License. You are free to use, modify, and distribute the software under the terms of the MIT License. Refer to the [LICENSE](LICENSE) file for more information.

