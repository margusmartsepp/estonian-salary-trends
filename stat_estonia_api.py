import requests
import pandas as pd
import json
import logging
from typing import Dict, List, Optional, Union, Any

class StatEstoniaAPI:
    """
    Client for interacting with the Statistics Estonia API.
    This class handles fetching data from various tables in the Statistics Estonia database.
    """
    
    BASE_URL = "https://andmed.stat.ee/api"
    
    def __init__(self):
        """Initialize the Statistics Estonia API client."""
        self.logger = logging.getLogger(__name__)
        self.session = requests.Session()
    
    def get_table_data(self, table_id: str, params: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
        """
        Fetch data from a specific table in the Statistics Estonia database.
        
        Args:
            table_id: The ID of the table (e.g., 'PA107', 'PA51', etc.)
            params: Optional parameters for filtering the data
            
        Returns:
            DataFrame containing the requested data
        """
        url = f"{self.BASE_URL}/v1/et/stat/{table_id}"
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            # Parse the JSON response
            data = response.json()
            
            # Convert to DataFrame
            df = pd.DataFrame(data)
            
            return df
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error fetching data from table {table_id}: {str(e)}")
            raise
    
    def get_salary_data_by_county(self, county: str, start_year: int, end_year: int) -> pd.DataFrame:
        """
        Get salary data for a specific county within a time range.
        
        Args:
            county: The name of the county
            start_year: The starting year for the data
            end_year: The ending year for the data
            
        Returns:
            DataFrame with salary data for the specified county and time range
        """
        # For PA107 table: Average monthly gross wages, median and number of employees by county
        params = {
            "county": county,
            "year": f"{start_year}-{end_year}"
        }
        
        return self.get_table_data("PA107", params)
    
    def get_salary_data_by_sector(self, sector: str, start_year: int, end_year: int) -> pd.DataFrame:
        """
        Get salary data for a specific industry sector within a time range.
        
        Args:
            sector: The industry sector
            start_year: The starting year for the data
            end_year: The ending year for the data
            
        Returns:
            DataFrame with salary data for the specified sector and time range
        """
        # We'll need to identify the appropriate table and parameters for sector-based data
        # This is a placeholder implementation
        params = {
            "sector": sector,
            "year": f"{start_year}-{end_year}"
        }
        
        # Assuming there's a table for sector-based data
        return self.get_table_data("PA_SECTOR", params)
    
    def get_available_counties(self) -> List[str]:
        """
        Get a list of available counties in the database.
        
        Returns:
            List of county names
        """
        # This would typically fetch the list from the API
        # For now, we'll return a hardcoded list
        return [
            "All of Estonia", "Harju county", "Tartu county", "Ida-Viru county", 
            "Pärnu county", "Lääne-Viru county", "Viljandi county", "Rapla county", 
            "Võru county", "Saare county", "Jõgeva county", "Järva county", 
            "Valga county", "Põlva county", "Lääne county", "Hiiu county"
        ]
    
    def get_available_sectors(self) -> List[str]:
        """
        Get a list of available industry sectors in the database.
        
        Returns:
            List of sector names
        """
        # This would typically fetch the list from the API
        # For now, we'll return a hardcoded list
        return [
            "All sectors", "Information and communication", "Finance and insurance", 
            "Professional, scientific and technical activities", "Manufacturing", 
            "Construction", "Wholesale and retail trade", "Transportation and storage", 
            "Accommodation and food service", "Education", "Healthcare"
        ]
    
    def get_mock_salary_data(self, region: str, sector: str, start_year: int, end_year: int, 
                            data_type: str) -> pd.DataFrame:
        """
        Generate mock salary data for development and testing.
        
        Args:
            region: The selected region/county
            sector: The selected industry sector
            start_year: The starting year
            end_year: The ending year
            data_type: The type of salary data (average, median, etc.)
            
        Returns:
            DataFrame with mock salary data
        """
        years = list(range(start_year, end_year + 1))
        
        # Base values and growth rates for different sectors
        sector_base = {
            "All sectors": 1200,
            "Information and communication": 2200,
            "Finance and insurance": 1900,
            "Professional, scientific and technical activities": 1700,
            "Manufacturing": 1300,
            "Construction": 1400,
            "Wholesale and retail trade": 1100,
            "Transportation and storage": 1250,
            "Accommodation and food service": 950,
            "Education": 1150,
            "Healthcare": 1350
        }
        
        sector_growth = {
            "All sectors": 5.0,
            "Information and communication": 7.2,
            "Finance and insurance": 6.5,
            "Professional, scientific and technical activities": 6.0,
            "Manufacturing": 4.5,
            "Construction": 4.8,
            "Wholesale and retail trade": 4.2,
            "Transportation and storage": 4.5,
            "Accommodation and food service": 3.8,
            "Education": 4.0,
            "Healthcare": 5.2
        }
        
        # Region adjustments (percentage of the sector base)
        region_factor = {
            "All of Estonia": 1.0,
            "Harju county": 1.15,
            "Tartu county": 0.95,
            "Ida-Viru county": 0.85,
            "Pärnu county": 0.9,
            "Lääne-Viru county": 0.88,
            "Viljandi county": 0.87,
            "Rapla county": 0.89,
            "Võru county": 0.86,
            "Saare county": 0.88,
            "Jõgeva county": 0.85,
            "Järva county": 0.87,
            "Valga county": 0.84,
            "Põlva county": 0.83,
            "Lääne county": 0.86,
            "Hiiu county": 0.85
        }
        
        # Data type adjustments
        data_type_factor = {
            "Average monthly gross wages": 1.0,
            "Median monthly gross wages": 0.85,
            "Average hourly gross wages": 1/168,  # Approximate hours per month
            "Median hourly gross wages": 0.85/168
        }
        
        # Generate the data
        base_value = sector_base.get(sector, 1200)
        growth_rate = sector_growth.get(sector, 5.0) / 100
        region_multiplier = region_factor.get(region, 1.0)
        data_type_multiplier = data_type_factor.get(data_type, 1.0)
        
        # Calculate salaries with compound growth
        salaries = []
        for i, year in enumerate(years):
            # Apply compound growth
            value = base_value * (1 + growth_rate) ** i
            # Apply region and data type adjustments
            value = value * region_multiplier * data_type_multiplier
            # Add some random variation (±2%)
            variation = 0.98 + 0.04 * (hash(f"{region}-{sector}-{year}") % 1000) / 1000
            value = value * variation
            salaries.append(round(value, 2))
        
        # Create DataFrame
        df = pd.DataFrame({
            'Year': years,
            'Value': salaries
        })
        
        return df