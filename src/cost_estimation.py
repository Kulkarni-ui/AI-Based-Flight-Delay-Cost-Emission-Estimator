import yaml

def calculate_cost(delay_minutes, config_file="config.yaml"):
    with open(config_file, "r") as f:
        config = yaml.safe_load(f)

    fuel_cost = delay_minutes * config["costs"]["fuel_per_minute"]
    crew_cost = delay_minutes * config["costs"]["crew_per_minute"]
    compensation_cost = config["costs"]["compensation_per_flight"]

    total_cost = fuel_cost + crew_cost + compensation_cost

    return {
        "FuelCost": fuel_cost,
        "CrewCost": crew_cost,
        "CompensationCost": compensation_cost,
        "TotalCost": total_cost
    }
