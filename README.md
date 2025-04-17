# Estonian Salary Trends

A web application for analyzing Estonian salary market data, generating summaries, forecasts, and career growth recommendations using Statistics Estonia and OpenAI APIs.

## Features

- Comprehensive salary data analysis including average salaries, salary ranges, and growth rates by industry and region
- Interactive visualizations with dynamic filtering and comparative charts
- AI-powered analysis using OpenAI to generate insights and answer specific questions
- Data export functionality in various formats

## Prerequisites

- Python 3.8 or higher
- OpenAI API key

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/estonian-salary-trends.git
   cd estonian-salary-trends
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```
   # Copy the example .env file
   cp .env.example .env
   
   # Edit the .env file and add your OpenAI API key
   ```

## Usage

1. Run the Streamlit application:
   ```
   streamlit run app.py
   ```

2. Open your web browser and navigate to:
   ```
   http://localhost:8501
   ```

3. Use the sidebar filters to select:
   - Region/County
   - Industry Sector
   - Time Period
   - Data Type (Average/Median, Monthly/Hourly)

4. Explore the data visualizations, AI analysis, and export options in the respective tabs.

## Project Structure

- `app.py`: Main Streamlit application
- `stat_estonia_api.py`: Client for the Statistics Estonia API
- `openai_api.py`: Client for the OpenAI API
- `data_processor.py`: Data processing and analysis utilities
- `visualizations.py`: Data visualization functions
- `requirements.txt`: Project dependencies
- `.env.example`: Example environment variables file

## Data Sources

This application uses data from the following Statistics Estonia tables:

1. PA107: Average monthly gross wages, median wages, and number of employees by county
2. PA51: Average monthly gross and net wages (2000-2017, monthly data)
3. PA5321: Average monthly gross and net wages by county (2000-2017)
4. PA118: Average hourly gross wages by county (quarterly data)
5. PA22: Average hourly gross wages by county (2000-2018, quarterly data)
6. PA5322: Average hourly gross wages by county (2000-2017)
7. PA5331: Average monthly gross and net wages by kind of owner of an enterprise (2000-2017)

## License

This project is licensed under the MIT License - see the LICENSE file for details.
