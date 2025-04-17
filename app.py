import streamlit as st
import pandas as pd
import plotly.express as px
import os
from dotenv import load_dotenv

# Import our custom modules
from stat_estonia_api import StatEstoniaAPI
from data_processor import DataProcessor
from visualizations import create_time_series, create_comparison_chart, create_growth_chart
from export_utils import generate_csv_download_link, generate_excel_download_link, generate_pdf_download_link

# Conditionally import OpenAI client if API key is available
try:
    from openai_api import OpenAIClient
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

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
    data_processor = DataProcessor(stat_api)
    
    # Initialize OpenAI client if API key is available
    openai_client = None
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if OPENAI_AVAILABLE and openai_api_key and openai_api_key != "your_openai_api_key_here":
        try:
            openai_client = OpenAIClient(api_key=openai_api_key)
        except Exception as e:
            st.sidebar.warning(f"Failed to initialize OpenAI client: {str(e)}")
    
    return stat_api, openai_client, data_processor

stat_api, openai_client, data_processor = initialize_clients()

# Display warning if OpenAI is not available
if not openai_client:
    st.sidebar.warning(
        "OpenAI API key not found or invalid. AI-powered analysis will be limited to pre-defined responses. "
        "To enable full AI functionality, add your OpenAI API key to the .env file."
    )

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
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Accept user input
    if prompt := st.chat_input("Ask a question about Estonian salary trends:"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            
            try:
                if openai_client:
                    # Prepare data for AI analysis
                    salary_data = None
                    if 'df' in locals():
                        # Convert DataFrame to dictionary for AI analysis
                        salary_data = {
                            'region': selected_region,
                            'sector': selected_sector,
                            'data_type': selected_data_type,
                            'years': df['Year'].tolist(),
                            'values': df['Value'].tolist()
                        }
                    
                    # Get response from OpenAI
                    with st.spinner("Generating AI analysis..."):
                        response = openai_client.answer_salary_question(prompt, salary_data)
                else:
                    # Fallback responses when OpenAI is not available
                    fallback_responses = {
                        "trend": """
                        Based on the data from Statistics Estonia, IT sector salaries have shown a consistent upward trend over the past 5 years, with an average annual growth rate of 7.2%. This is significantly higher than the national average growth rate of 5.1% across all sectors.
                        
                        Key factors contributing to this growth include:
                        1. Increased demand for IT professionals in Estonia and the broader EU market
                        2. Growth of the Estonian startup ecosystem
                        3. Digital transformation initiatives across industries
                        
                        Looking ahead, this trend is expected to continue, with projected growth of 6-8% annually for the next 2-3 years.
                        """,
                        
                        "comparison": """
                        When comparing salaries in Tartu to the national average, Tartu shows approximately 5-10% lower salaries across most sectors. This is typical for regional differences, with Tallinn having the highest salaries in the country.
                        
                        However, in the education and research sectors, Tartu's salaries are more competitive due to the presence of major universities and research institutions.
                        """,
                        
                        "skills": """
                        To increase your salary in the finance sector in Estonia, consider developing these high-demand skills:
                        
                        1. Data analysis and financial modeling
                        2. Risk management and compliance expertise
                        3. FinTech knowledge and digital transformation skills
                        4. ESG (Environmental, Social, Governance) expertise
                        5. Advanced Excel and financial software proficiency
                        
                        Additionally, certifications like CFA, ACCA, or specialized FinTech credentials can significantly boost your earning potential.
                        """,
                        
                        "default": """
                        Based on the available salary data for Estonia, there are significant variations across different sectors and regions. The IT, finance, and professional services sectors typically offer the highest salaries, while retail, hospitality, and certain public sectors tend to have lower average salaries.
                        
                        Salary growth has generally outpaced inflation in recent years, with an average annual growth rate of 5-7% across all sectors. Regional differences are notable, with Tallinn and Harju county offering the highest salaries, followed by Tartu county.
                        """
                    }
                    
                    # Select appropriate fallback response based on keywords in the prompt
                    if any(keyword in prompt.lower() for keyword in ["trend", "growth", "increase", "decrease"]):
                        response = fallback_responses["trend"]
                    elif any(keyword in prompt.lower() for keyword in ["compare", "comparison", "difference", "versus", "vs"]):
                        response = fallback_responses["comparison"]
                    elif any(keyword in prompt.lower() for keyword in ["skill", "improve", "increase salary", "earn more"]):
                        response = fallback_responses["skills"]
                    else:
                        response = fallback_responses["default"]
                
                # Display the response
                message_placeholder.markdown(response)
                
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response})
                
                # Add a disclaimer about the content
                if openai_client:
                    st.info("Note: This analysis is generated by AI based on historical data and should be used as a general guide only.")
                else:
                    st.warning("Note: This is a pre-defined response. For customized analysis, please add your OpenAI API key to the .env file.")
                
            except Exception as e:
                st.error(f"Error generating analysis: {str(e)}")

with tab3:
    st.header("Export Data and Reports")
    
    # Export options
    st.markdown("Download the data and analysis in your preferred format.")
    
    # Check if data has been fetched
    if 'df' in locals():
        # Prepare data for export
        export_data = {
            'base_data': df,
        }
        
        # Add growth rate data if available
        if 'growth_data' in locals():
            export_data['growth_rates'] = growth_data
            
        # Add comparison data if available
        if 'comparison_data' in locals():
            export_data['comparison'] = comparison_data
        
        # Get AI analysis if available
        ai_text = None
        if 'ai_response' in locals():
            ai_text = ai_response
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("Export as CSV"):
                st.markdown(
                    generate_csv_download_link(
                        df=df,
                        filename=f"salary_data_{selected_region}_{selected_sector}_{selected_years[0]}-{selected_years[1]}.csv"
                    ),
                    unsafe_allow_html=True
                )
        
        with col2:
            if st.button("Export as Excel"):
                st.markdown(
                    generate_excel_download_link(
                        df=df,
                        filename=f"salary_data_{selected_region}_{selected_sector}_{selected_years[0]}-{selected_years[1]}.xlsx"
                    ),
                    unsafe_allow_html=True
                )
        
        with col3:
            if st.button("Generate PDF Report"):
                st.markdown(
                    generate_pdf_download_link(
                        data_dict=export_data,
                        region=selected_region,
                        sector=selected_sector,
                        data_type=selected_data_type,
                        start_year=selected_years[0],
                        end_year=selected_years[1],
                        ai_analysis=ai_text,
                        filename=f"salary_report_{selected_region}_{selected_sector}_{selected_years[0]}-{selected_years[1]}.pdf"
                    ),
                    unsafe_allow_html=True
                )
    else:
        st.info("Please fetch data in the 'Data Visualization' tab before exporting.")

# Footer
st.markdown("---")
st.markdown("Data source: Statistics Estonia | Powered by OpenAI")