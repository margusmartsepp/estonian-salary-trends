import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Union, Any, Tuple
from stat_estonia_api import StatEstoniaAPI

class DataProcessor:
    """
    Handles data processing, transformation, and analysis for the Estonian salary data.
    """
    
    def __init__(self, stat_api: StatEstoniaAPI):
        """
        Initialize the data processor.
        
        Args:
            stat_api: Instance of the Statistics Estonia API client
        """
        self.stat_api = stat_api
        self.data_cache = {}  # Simple cache to store fetched data
    
    def get_salary_data(self, 
                       region: str, 
                       sector: str, 
                       start_year: int, 
                       end_year: int,
                       data_type: str) -> pd.DataFrame:
        """
        Get salary data based on the specified parameters.
        
        Args:
            region: The selected region/county
            sector: The selected industry sector
            start_year: The starting year
            end_year: The ending year
            data_type: The type of salary data (average, median, etc.)
            
        Returns:
            DataFrame with the requested salary data
        """
        # Create a cache key
        cache_key = f"{region}_{sector}_{start_year}_{end_year}_{data_type}"
        
        # Check if data is in cache
        if cache_key in self.data_cache:
            return self.data_cache[cache_key]
        
        try:
            # In a real implementation, this would call the actual API
            # For now, we'll use the mock data method
            df = self.stat_api.get_mock_salary_data(
                region=region,
                sector=sector,
                start_year=start_year,
                end_year=end_year,
                data_type=data_type
            )
            
            # Store in cache
            self.data_cache[cache_key] = df
            
            return df
            
        except Exception as e:
            # Log the error and raise it
            print(f"Error fetching salary data: {str(e)}")
            raise
    
    def calculate_growth_rates(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate year-over-year growth rates for salary data.
        
        Args:
            df: DataFrame containing salary data with 'Year' and 'Value' columns
            
        Returns:
            DataFrame with growth rates added
        """
        # Make a copy to avoid modifying the original
        result_df = df.copy()
        
        # Calculate year-over-year percentage change
        result_df['Growth Rate (%)'] = result_df['Value'].pct_change() * 100
        
        # First year will have NaN growth rate
        result_df['Growth Rate (%)'] = result_df['Growth Rate (%)'].fillna(0)
        
        # Round to 2 decimal places
        result_df['Growth Rate (%)'] = result_df['Growth Rate (%)'].round(2)
        
        return result_df
    
    def compare_with_national_average(self, 
                                    df: pd.DataFrame, 
                                    region: str, 
                                    sector: str,
                                    data_type: str) -> pd.DataFrame:
        """
        Compare the given salary data with the national average.
        
        Args:
            df: DataFrame containing salary data for a specific region/sector
            region: The selected region/county
            sector: The selected industry sector
            data_type: The type of salary data
            
        Returns:
            DataFrame with comparison data
        """
        years = df['Year'].tolist()
        start_year = min(years)
        end_year = max(years)
        
        # If already national data, compare with all sectors
        if region == "All of Estonia":
            if sector == "All sectors":
                # Nothing to compare with
                return df
            
            # Get data for all sectors
            national_df = self.get_salary_data(
                region="All of Estonia",
                sector="All sectors",
                start_year=start_year,
                end_year=end_year,
                data_type=data_type
            )
        else:
            # Get national average for the same sector
            national_df = self.get_salary_data(
                region="All of Estonia",
                sector=sector,
                start_year=start_year,
                end_year=end_year,
                data_type=data_type
            )
        
        # Merge the data
        comparison_df = pd.merge(
            df.rename(columns={'Value': 'Selected'}),
            national_df.rename(columns={'Value': 'National Average'}),
            on='Year'
        )
        
        # Calculate the difference as a percentage
        comparison_df['Difference (%)'] = ((comparison_df['Selected'] / comparison_df['National Average']) - 1) * 100
        comparison_df['Difference (%)'] = comparison_df['Difference (%)'].round(2)
        
        return comparison_df
    
    def forecast_salary_trend(self, 
                            df: pd.DataFrame, 
                            forecast_years: int = 3) -> pd.DataFrame:
        """
        Generate a simple forecast of future salary trends based on historical data.
        
        Args:
            df: DataFrame containing historical salary data
            forecast_years: Number of years to forecast
            
        Returns:
            DataFrame with historical and forecasted data
        """
        # Make a copy to avoid modifying the original
        historical_df = df.copy()
        
        # Get the years and values
        years = historical_df['Year'].values
        values = historical_df['Value'].values
        
        # Calculate the average annual growth rate
        if len(years) >= 2:
            # Compound Annual Growth Rate (CAGR)
            start_value = values[0]
            end_value = values[-1]
            num_years = years[-1] - years[0]
            cagr = (end_value / start_value) ** (1 / num_years) - 1
        else:
            # Default growth rate if not enough data
            cagr = 0.05  # 5% annual growth
        
        # Generate forecast years
        last_year = years[-1]
        forecast_years_list = list(range(last_year + 1, last_year + forecast_years + 1))
        
        # Generate forecasted values
        last_value = values[-1]
        forecast_values = [last_value * (1 + cagr) ** i for i in range(1, forecast_years + 1)]
        
        # Create forecast DataFrame
        forecast_df = pd.DataFrame({
            'Year': forecast_years_list,
            'Value': forecast_values,
            'Type': 'Forecast'
        })
        
        # Add type column to historical data
        historical_df['Type'] = 'Historical'
        
        # Combine historical and forecast data
        combined_df = pd.concat([historical_df, forecast_df], ignore_index=True)
        
        # Round values to 2 decimal places
        combined_df['Value'] = combined_df['Value'].round(2)
        
        return combined_df
    
    def prepare_data_for_export(self, 
                              region: str, 
                              sector: str, 
                              start_year: int, 
                              end_year: int,
                              data_type: str) -> Dict[str, pd.DataFrame]:
        """
        Prepare a comprehensive data package for export.
        
        Args:
            region: The selected region/county
            sector: The selected industry sector
            start_year: The starting year
            end_year: The ending year
            data_type: The type of salary data
            
        Returns:
            Dictionary containing various DataFrames for export
        """
        # Get the base salary data
        base_df = self.get_salary_data(
            region=region,
            sector=sector,
            start_year=start_year,
            end_year=end_year,
            data_type=data_type
        )
        
        # Calculate growth rates
        growth_df = self.calculate_growth_rates(base_df)
        
        # Compare with national average
        comparison_df = self.compare_with_national_average(
            df=base_df,
            region=region,
            sector=sector,
            data_type=data_type
        )
        
        # Generate forecast
        forecast_df = self.forecast_salary_trend(base_df)
        
        # Return all DataFrames in a dictionary
        return {
            'base_data': base_df,
            'growth_rates': growth_df,
            'comparison': comparison_df,
            'forecast': forecast_df
        }
    
    def prepare_data_for_ai_analysis(self, 
                                   region: str, 
                                   sector: str, 
                                   start_year: int, 
                                   end_year: int,
                                   data_type: str) -> Dict[str, Any]:
        """
        Prepare data in a format suitable for AI analysis.
        
        Args:
            region: The selected region/county
            sector: The selected industry sector
            start_year: The starting year
            end_year: The ending year
            data_type: The type of salary data
            
        Returns:
            Dictionary containing data for AI analysis
        """
        # Get all the processed data
        data_dict = self.prepare_data_for_export(
            region=region,
            sector=sector,
            start_year=start_year,
            end_year=end_year,
            data_type=data_type
        )
        
        # Extract key metrics
        base_df = data_dict['base_data']
        growth_df = data_dict['growth_rates']
        comparison_df = data_dict['comparison']
        forecast_df = data_dict['forecast']
        
        # Calculate average growth rate
        avg_growth_rate = growth_df['Growth Rate (%)'].mean()
        
        # Calculate latest value and its year-over-year change
        latest_value = base_df.iloc[-1]['Value']
        if len(base_df) > 1:
            previous_value = base_df.iloc[-2]['Value']
            latest_yoy_change = ((latest_value / previous_value) - 1) * 100
        else:
            latest_yoy_change = 0
        
        # Calculate comparison with national average
        if 'Difference (%)' in comparison_df.columns:
            avg_diff_from_national = comparison_df['Difference (%)'].mean()
        else:
            avg_diff_from_national = 0
        
        # Prepare the data for AI analysis
        ai_data = {
            'region': region,
            'sector': sector,
            'data_type': data_type,
            'time_period': f"{start_year}-{end_year}",
            'years': base_df['Year'].tolist(),
            'values': base_df['Value'].tolist(),
            'growth_rates': growth_df['Growth Rate (%)'].tolist(),
            'avg_growth_rate': round(avg_growth_rate, 2),
            'latest_value': latest_value,
            'latest_yoy_change': round(latest_yoy_change, 2),
            'avg_diff_from_national': round(avg_diff_from_national, 2),
            'forecast_years': forecast_df[forecast_df['Type'] == 'Forecast']['Year'].tolist(),
            'forecast_values': forecast_df[forecast_df['Type'] == 'Forecast']['Value'].tolist()
        }
        
        return ai_data