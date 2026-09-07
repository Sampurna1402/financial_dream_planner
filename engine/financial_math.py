import pandas as pd
from pathlib import Path

# Project mandatory assumption
INFLATION_RATE = 0.06  

def get_base_costs(city: str) -> dict:
    csv_path = Path(__file__).parent / 'api' / 'city_goal_costs copy.csv'
    df = pd.read_csv(csv_path)
    
    city_data = df[df['City'].str.lower() == city.lower()]
    if city_data.empty:
        raise ValueError(f"City '{city}' not found in the dataset.")
        
    return {
        "Marriage": float(city_data['Marriage_Cost_Current'].mean()),
        "Car": float(city_data['Car_Cost_Current'].mean()),
        "Home": float(city_data['Home_Cost_Current'].mean())
    }

def calculate_future_cost(current_cost: float, years: int) -> float:
    if years <= 0:
        return 0.0
    # Future Cost = Current Cost * (1 + 0.06) ^ Number of Years
    future_cost = current_cost * ((1 + INFLATION_RATE) ** years)
    return round(future_cost, 2)

def calculate_monthly_investment(future_cost: float, years: int, expected_annual_return: float = 0.10) -> float:
    if years <= 0:
        return 0.0
    months = years * 12
    monthly_rate = expected_annual_return / 12
    sip_amount = (future_cost * monthly_rate) / (((1 + monthly_rate) ** months) - 1)
    return round(sip_amount, 2)

def evaluate_feasibility(salary: float, saving_percentage: float, total_required: float) -> dict:
    capacity = salary * (saving_percentage / 100)
    gap = capacity - total_required
    
    if total_required <= (0.8 * capacity):
        status = "Achievable"
    elif total_required <= capacity:
        status = "Challenging"
    else:
        status = "Highly Challenging"
        
    return {
        "available_monthly_capacity": round(capacity, 2),
        "total_required_monthly": round(total_required, 2),
        "shortfall_surplus": round(gap, 2),
        "status": status
    }