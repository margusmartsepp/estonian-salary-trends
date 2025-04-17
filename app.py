import streamlit as st
import pandas as pd
import plotly.express as px
import os
from dotenv import load_dotenv

# Import our custom modules
from stat_estonia_api import StatEstoniaAPI
from openai_api import OpenAIClient
from data_processor import DataProcessor
from visualizations import create_time_series, create_comparison_chart, create_growth_chart

# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="Estonian Salary Trends",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize API clients
@st.cache_resource
def initialize_clients():
    stat_api = StatEstoniaAPI()
    openai_client = OpenAIClient(api_key=os.getenv("OPENAI_API_KEY"))
    data_processor = DataProcessor(stat_api)
    return stat_api, openai_client, data_processor

stat_api, openai_client, data_processor = initialize_clients()

# Application title and description
st.title("Estonian Salary Trends")
st.markdown("""
    Analyze Estonian salary market data and understand trends across various sectors.
    This application uses data from Statistics Estonia and OpenAI to generate insights.
""")

# Sidebar for filters
st.sidebar.header("Data Filters")

# Region/County selection
counties = ["All of Estonia", "Harju county", "Tartu county", "Ida-Viru county", 
            "Pärnu county", "Lääne-Viru county", "Viljandi county", "Rapla county", 
            "Võru county", "Saare county", "Jõgeva county", "Järva county", 
            "Valga county", "Põlva county", "Lääne county", "Hiiu county"]
selected_region = st.sidebar.selectbox("Select Region/County", counties)

# Industry sector selection
# These are example sectors, we'll need to get the actual list from the API
sectors = ["All sectors", "Information and communication", "Finance and insurance", 
           "Professional, scientific and technical activities", "Manufacturing", 
           "Construction", "Wholesale and retail trade", "Transportation and storage", 
           "Accommodation and food service", "Education", "Healthcare"]
selected_sector = st.sidebar.selectbox("Select Industry Sector", sectors)

# Time period selection
years = list(range(2010, 2026))
selected_years = st.sidebar.slider("Select Time Period", min(years), max(years), (2020, 2025))

# Data type selection
data_types = ["Average monthly gross wages", "Median monthly gross wages", 
              "Average hourly gross wages", "Median hourly gross wages"]
selected_data_type = st.sidebar.selectbox("Select Data Type", data_types)

# Main content area with tabs
tab1, tab2, tab3 = st.tabs(["Data Visualization", "AI Analysis", "Export"])

with tab1:
    st.header("Salary Data Visualization")
    
    # Placeholder for when we implement the actual data fetching
    if st.button("Fetch Data"):
        with st.spinner("Fetching data from Statistics Estonia..."):
            try:
                # This will be replaced with actual API calls
                # For now, let's create some dummy data
                years_range = list(range(selected_years[0], selected_years[1] + 1))
                dummy_data = {
                    'Year': years_range,
                    'Salary': [1200 + i * 100 + (0 if selected_region == "All of Estonia" else -200) for i in range(len(years_range))]
                }
                df = pd.DataFrame(dummy_data)
                
                # Display the data
                st.subheader(f"{selected_data_type} in {selected_region} for {selected_sector}")
                st.dataframe(df)
                
                # Create visualizations
                st.subheader("Salary Trend Over Time")
                fig = px.line(df, x='Year', y='Salary', title=f"{selected_data_type} Trend ({selected_years[0]}-{selected_years[1]})")
                st.plotly_chart(fig, use_container_width=True)
                
                # Comparison chart (dummy data for now)
                st.subheader("Comparison with National Average")
                comparison_data = pd.DataFrame({
                    'Year': years_range,
                    'Selected': df['Salary'],
                    'National Average': [1200 + i * 100 for i in range(len(years_range))]
                })
                fig2 = px.bar(comparison_data.melt(id_vars=['Year'], var_name='Category', value_name='Salary'), 
                             x='Year', y='Salary', color='Category', barmode='group',
                             title="Comparison with National Average")
                st.plotly_chart(fig2, use_container_width=True)
                
                # Growth rate visualization
                st.subheader("Annual Growth Rate")
                growth_data = pd.DataFrame({
                    'Year': years_range[1:],
                    'Growth Rate (%)': [5 + i * 0.2 for i in range(len(years_range)-1)]
                })
                fig3 = px.bar(growth_data, x='Year', y='Growth Rate (%)', 
                             title="Annual Salary Growth Rate (%)")
                st.plotly_chart(fig3, use_container_width=True)
                
            except Exception as e:
                st.error(f"Error fetching data: {str(e)}")
    else:
        st.info("Click 'Fetch Data' to load salary information based on your selections.")

with tab2:
    st.header("AI-Powered Salary Analysis")
    
    # Chat interface for AI analysis
    st.markdown("""
        Ask questions about the salary data and get AI-generated insights.
        Examples:
        - What are the trends in IT sector salaries over the last 5 years?
        - How do salaries in Tartu compare to the national average?
        - What skills should I develop to increase my salary in the finance sector?
    """)
    
    user_question = st.text_input("Ask a question about Estonian salary trends:")
    
    if user_question:
        with st.spinner("Generating AI analysis..."):
            try:
                # This will be replaced with actual OpenAI API calls
                # For now, let's return a placeholder response
                ai_response = """
                Based on the data from Statistics Estonia, IT sector salaries have shown a consistent upward trend over the past 5 years, with an average annual growth rate of 7.2%. This is significantly higher than the national average growth rate of 5.1% across all sectors.
                
                Key factors contributing to this growth include:
                1. Increased demand for IT professionals in Estonia and the broader EU market
                2. Growth of the Estonian startup ecosystem
                3. Digital transformation initiatives across industries
                
                Looking ahead, this trend is expected to continue, with projected growth of 6-8% annually for the next 2-3 years. To maximize your earning potential in this sector, focusing on skills in cloud computing, data science, and cybersecurity would be particularly valuable.
                """
                
                st.markdown("### AI Analysis")
                st.write(ai_response)
                
                # Add a disclaimer about the AI-generated content
                st.info("Note: This analysis is generated by AI based on historical data and should be used as a general guide only.")
                
            except Exception as e:
                st.error(f"Error generating AI analysis: {str(e)}")
    else:
        st.info("Enter a question above to get AI-powered insights about Estonian salary trends.")

with tab3:
    st.header("Export Data and Reports")
    
    # Export options
    st.markdown("Download the data and analysis in your preferred format.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Export as CSV"):
            st.info("CSV export functionality will be implemented here.")
    
    with col2:
        if st.button("Export as Excel"):
            st.info("Excel export functionality will be implemented here.")
    
    with col3:
        if st.button("Generate PDF Report"):
            st.info("PDF report generation will be implemented here.")

# Footer
st.markdown("---")
st.markdown("Data source: Statistics Estonia | Powered by OpenAI")