"""The Stigler diet problem.

A description of the problem can be found here:
https://en.wikipedia.org/wiki/Stigler_diet.
"""
from ortools.linear_solver import pywraplp
import json
from pathlib import Path
import nextmv


def main():
    """Entry point of the program."""
    # Instantiate the data problem by loading the nutrients and data from
    # an external input file `inputs/diet_data.json` so the problem data is
    # separated from code.
    # Load data from JSON file
    with open("diet_data.json", "r") as f:
        data_file = json.load(f)

    nutrients = data_file.get("nutrients", [])
    data = data_file.get("data", [])

    # Instantiate a Glop solver and naming it.
    solver = pywraplp.Solver.CreateSolver("GLOP")
    if not solver:
        return

    # Declare an array to hold our variables.
    foods = [solver.NumVar(0.0, solver.infinity(), item[0]) for item in data]

    print("Number of variables =", solver.NumVariables())

    # Create the constraints, one per nutrient.
    constraints = []
    for i, nutrient in enumerate(nutrients):
        constraints.append(solver.Constraint(nutrient[1], solver.infinity()))
        for j, item in enumerate(data):
            constraints[i].SetCoefficient(foods[j], item[i + 3])

    print("Number of constraints =", solver.NumConstraints())

    # Objective function: Minimize the sum of (price-normalized) foods.
    objective = solver.Objective()
    for food in foods:
        objective.SetCoefficient(food, 1)
    objective.SetMinimization()

    print(f"Solving with {solver.SolverVersion()}")
    status = solver.Solve()

    # Check that the problem has an optimal solution.
    if status != solver.OPTIMAL:
        print("The problem does not have an optimal solution!")
        if status == solver.FEASIBLE:
            print("A potentially suboptimal solution was found.")
        else:
            print("The solver could not solve the problem.")
            exit(1)

    # Display the amounts (in dollars) to purchase of each food.
    nutrients_result = [0] * len(nutrients)

    # Write human-readable solution summary to `solution.txt` (appended).
    with open("solution.txt", "a", encoding="utf-8") as f:
        result = "\nAnnual Foods:\n"
        for i, food in enumerate(foods):
            if food.solution_value() > 0.0:
                result += "{}: ${:.4f}\n".format(data[i][0], 365.0 * food.solution_value())
                for j, _ in enumerate(nutrients):
                    nutrients_result[j] += data[i][j + 3] * food.solution_value()

        result += "\nOptimal annual price: ${:.4f}\n".format(365.0 * objective.Value())

        result += "\nNutrients per day:\n"
        for i, nutrient in enumerate(nutrients):
            result += "{}: {:.2f} (min {})\n".format(nutrient[0], nutrients_result[i], nutrient[1])

        # Write to file
        f.write(result)

    print("\nAdvanced usage:")
    print(f"Problem solved in {solver.wall_time():d} milliseconds")
    print(f"Problem solved in {solver.iterations():d} iterations")

    # MODIFIED - write statistics to statistics.json
    statistics_file = "statistics.json"
    with open(statistics_file, "w") as stats_f:
        statistics = nextmv.Statistics(
            result=nextmv.ResultStatistics(
                duration=solver.wall_time(),
                value=objective.Value(),
                custom={
                    "iterations": solver.iterations(),
                    "annual_price": 365.0 * objective.Value()
                },
            ),
        )
        stats_f.write(json.dumps({"statistics": statistics.to_dict()}))

    print(f"Statistics written to {statistics_file}")   


if __name__ == "__main__":
    main()