from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from engine.financial_math import (
    get_base_costs, 
    calculate_future_cost, 
    calculate_monthly_investment, 
    evaluate_feasibility
)

app = FastAPI(title="Financial Dream Planner API")

class PlannerRequest(BaseModel):
    name: str
    age: int
    city: str
    salary: float = Field(..., gt=0)
    saving_percentage: float = Field(..., ge=0, le=100)
    marriage_years: int = Field(default=0, ge=0)
    car_years: int = Field(default=0, ge=0)
    home_years: int = Field(default=0, ge=0)

@app.post("/calculate-plan")
def calculate_plan(request: PlannerRequest):
    try:
        base_costs = get_base_costs(request.city)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
        
    goals = {
        "Marriage": request.marriage_years,
        "Car": request.car_years,
        "Home": request.home_years
    }
    
    plan_details = {}
    total_required_sip = 0.0
    
    for goal, years in goals.items():
        if years > 0:
            current_cost = base_costs[goal]
            future_cost = calculate_future_cost(current_cost, years)
            monthly_inv = calculate_monthly_investment(future_cost, years)
            
            plan_details[goal] = {
                "timeline_years": years,
                "current_estimated_cost": current_cost,
                "future_estimated_cost": future_cost,
                "required_monthly_investment": monthly_inv
            }
            total_required_sip += monthly_inv
            
    feasibility = evaluate_feasibility(request.salary, request.saving_percentage, total_required_sip)
    
    return {
        "user": request.name,
        "goal_breakdown": plan_details,
         "feasibility_analysis": feasibility }