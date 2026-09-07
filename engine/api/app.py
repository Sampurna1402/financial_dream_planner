import os

import streamlit as st
import requests

API_URL = os.getenv("FINANCIAL_PLANNER_API_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="Financial Dream Planner", layout="wide", page_icon="🎓")

st.title("🎓 AI-Powered Financial Dream & Goal Planner")
st.write("Plan Your Dreams. Calculate. Analyse. Achieve.")

# Sidebar Inputs
st.sidebar.header("Your Profile")
name = st.sidebar.text_input("Name", "Sampurna Das")
age = st.sidebar.number_input("Age", min_value=18, max_value=100, value=21)
city = st.sidebar.selectbox("City", ["Kolkata", "Bangalore", "Delhi", "Mumbai", "Hyderabad", "Chennai", "Pune", "Ahmedabad", "Jaipur", "Lucknow"])
salary = st.sidebar.number_input("Expected Monthly Salary (₹)", min_value=1000, value=35000, step=1000)
saving_percent = st.sidebar.slider("Saving Percentage (%)", 0, 100, 25)

st.sidebar.header("Goal Timelines (Years)")
marriage_years = st.sidebar.slider("Marriage", 0, 20, 5)
car_years = st.sidebar.slider("New Car", 0, 20, 3)
home_years = st.sidebar.slider("New Home", 0, 30, 8)

if st.sidebar.button("Calculate My Plan", type="primary"):
    payload = {
        "name": name,
        "age": age,
        "city": city,
        "salary": salary,
        "saving_percentage": saving_percent,
        "marriage_years": marriage_years,
        "car_years": car_years,
        "home_years": home_years
    }

    with st.spinner("Calculating future costs and checking feasibility..."):
        try:
            # Connect to local FastAPI server
            response = requests.post(f"{API_URL}/calculate-plan", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                st.success(f"Financial plan generated successfully for {data['user']}!")
                
                # Feasibility Analysis
                st.subheader("📊 Feasibility Analysis")
                feasibility = data["feasibility_analysis"]
                
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Available Capacity/Month", f"₹{feasibility['available_monthly_capacity']:,.2f}")
                col2.metric("Total Required/Month", f"₹{feasibility['total_required_monthly']:,.2f}")
                
                gap = feasibility['shortfall_surplus']
                gap_label = "Surplus" if gap >= 0 else "Shortfall"
                col3.metric(f"Monthly {gap_label}", f"₹{abs(gap):,.2f}")
                
                status_color = "🟢" if feasibility['status'] == "Achievable" else "🟡" if feasibility['status'] == "Challenging" else "🔴"
                col4.metric("Status", f"{status_color} {feasibility['status']}")
                
                st.divider()
                
                # Goal Breakdown
                st.subheader("🎯 Goal Breakdown")
                goals = data["goal_breakdown"]
                
                if not goals:
                    st.info("No future goals selected. Adjust the sliders on the left.")
                
                for goal, details in goals.items():
                    with st.expander(f"{goal} (in {details['timeline_years']} years)", expanded=True):
                        gc1, gc2, gc3 = st.columns(3)
                        gc1.metric("Current Baseline Cost", f"₹{details['current_estimated_cost']:,.2f}")
                        gc2.metric("Future Cost (6% inflation)", f"₹{details['future_estimated_cost']:,.2f}")
                        gc3.metric("Required SIP/Month", f"₹{details['required_monthly_investment']:,.2f}")
                        
            else:
                st.error(f"Error from API: {response.json().get('detail', 'Unknown Error')}")
                
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the backend API. Please ensure the FastAPI server is running in another terminal on port 8000.")