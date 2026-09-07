import streamlit as st
import requests

st.set_page_config(page_title="Financial Dream Planner", layout="wide", page_icon="✨")

st.markdown("""
    <style>
    /* Add subtle shadows and rounded corners to metrics */
    div[data-testid="metric-container"] {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        padding: 15px 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    /* Style the main title */
    h1 {
        color: #1e3a8a;
        font-family: 'Helvetica Neue', sans-serif;
    }
    /* Add some breathing room to the top */
    .block-container {
        padding-top: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

st.title("✨ AI-Powered Financial Dream Planner")
st.markdown("### *Plan your future. Calculate the costs. Achieve your dreams.*")
st.divider()

st.sidebar.header("👤 Your Profile")
name = st.sidebar.text_input("Name", value="Sampurna Das")
age = st.sidebar.number_input("Age", min_value=18, max_value=60, value=21)
city = st.sidebar.selectbox("City", ["Kolkata", "Bangalore", "Delhi", "Mumbai", "Hyderabad", "Chennai", "Pune"])

st.sidebar.header("💼 Financials")
salary = st.sidebar.number_input("Monthly Salary (₹)", min_value=10000, value=40000, step=5000)
saving_percentage = st.sidebar.slider("Saving Target (%)", 5, 100, 20)

st.sidebar.header("🎯 Goal Timelines (Years)")
marriage_years = st.sidebar.slider("💍 Marriage", 0, 15, 5)
car_years = st.sidebar.slider("🚗 New Car", 0, 15, 4)
home_years = st.sidebar.slider("🏡 New Home", 0, 30, 10)

if st.sidebar.button("🚀 Calculate My Plan", use_container_width=True, type="primary"):
    payload = {
        "name": name,
        "age": age,
        "city": city,
        "salary": salary,
        "saving_percentage": saving_percentage,
        "marriage_years": marriage_years,
        "car_years": car_years,
        "home_years": home_years
    }

    with st.spinner("Crunching the numbers and analyzing feasibility..."):
        try:
            response = requests.post("http://127.0.0.1:8000/calculate-plan", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                feasibility = data["feasibility_analysis"]
                goals = data["goal_breakdown"]
                
                st.success(f"Welcome, {data['user']}! Here is your personalized financial blueprint.")
                
                # 5. Interactive Tabs for Organization
                tab1, tab2 = st.tabs(["📊 Feasibility Dashboard", "🎯 Goal Breakdown"])
                
                with tab1:
                    st.subheader("Monthly Cash Flow Analysis")
                    
                    # Top-level metrics
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Available Capacity", f"₹{feasibility['available_monthly_capacity']:,.2f}")
                    col2.metric("Total Required SIP", f"₹{feasibility['total_required_monthly']:,.2f}")
                    
                    gap = feasibility['shortfall_surplus']
                    gap_label = "Surplus" if gap >= 0 else "Shortfall"
                    # Streamlit handles color automatically based on positive/negative delta
                    col3.metric(f"Monthly {gap_label}", f"₹{abs(gap):,.2f}", delta=float(gap))
                    
                    st.markdown("---")
                    st.subheader("Plan Status")
                    
                    status = feasibility['status']
                    if status == "Achievable":
                        st.info("✅ **Achievable:** Your current savings plan easily covers your future goals!")
                        # Visual progress bar showing how much of the budget is used
                        ratio = feasibility['total_required_monthly'] / feasibility['available_monthly_capacity']
                        st.progress(min(ratio, 1.0))
                        
                    elif status == "Challenging":
                        st.warning("⚠️ **Challenging:** Your budget is very tight. You might want to push out a goal timeline by 1-2 years.")
                        st.progress(1.0)
                        
                    else:
                        st.error(f"🚨 **Highly Challenging:** You have a monthly shortfall of ₹{abs(gap):,.2f}. Consider increasing your savings percentage or extending your timelines.")
                        
                with tab2:
                    st.subheader("Future Cost Estimates (Assuming 6% Annual Inflation)")
                    
                    if not goals:
                        st.info("No goals selected. Adjust the sliders in the sidebar.")
                        
                    # Dynamically create columns based on the number of selected goals
                    cols = st.columns(len(goals) if len(goals) > 0 else 1)
                    
                    for idx, (goal_name, details) in enumerate(goals.items()):
                        with cols[idx]:
                            st.markdown(f"### {goal_name}")
                            st.markdown(f"**Target:** {details['timeline_years']} years")
                            st.metric("Current Cost", f"₹{details['current_estimated_cost']:,.0f}")
                            st.metric("Future Cost", f"₹{details['future_estimated_cost']:,.0f}")
                            st.metric("Required SIP", f"₹{details['required_monthly_investment']:,.0f}")
                            
            else:
                st.error("There was an issue calculating your plan. Please check your inputs.")
                
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the backend. Please ensure your FastAPI server (`uvicorn api.main:app --reload`) is running in another terminal.")
else:
    
    st.info("👈 Adjust your profile and goal timelines in the sidebar, then click **Calculate My Plan** to begin.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Why Plan Now?")
        st.markdown("""
        * **Beat Inflation:** At 6% inflation, costs double roughly every 12 years.
        * **Compound Interest:** The earlier you start your SIP, the less you have to invest out of pocket.
        * **Financial Clarity:** Know exactly what percentage of your salary needs to be locked away.
        """)