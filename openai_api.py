import logging
from typing import Dict, List, Optional, Union, Any
from openai import OpenAI

class OpenAIClient:
    """
    Client for interacting with the OpenAI API.
    This class handles generating salary trend summaries, forecasts, and recommendations.
    """
    
    def __init__(self, api_key: str):
        """
        Initialize the OpenAI API client.
        
        Args:
            api_key: OpenAI API key
        """
        self.logger = logging.getLogger(__name__)
        self.client = OpenAI(api_key=api_key)
    
    def generate_salary_trend_analysis(self, 
                                      salary_data: Dict[str, Any], 
                                      region: str, 
                                      sector: str) -> str:
        """
        Generate a summary of salary trends based on the provided data.
        
        Args:
            salary_data: Dictionary containing salary data
            region: The region/county for the analysis
            sector: The industry sector for the analysis
            
        Returns:
            String containing the generated analysis
        """
        try:
            # Prepare the prompt with context
            prompt = self._create_trend_analysis_prompt(salary_data, region, sector)
            
            # Call the OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert economist specializing in salary trends and labor markets in Estonia. Provide clear, data-driven analysis of salary trends."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800,
                temperature=0.5
            )
            
            # Extract and return the generated text
            return response.choices[0].message.content
            
        except Exception as e:
            self.logger.error(f"Error generating salary trend analysis: {str(e)}")
            return "Sorry, I couldn't generate an analysis at this time. Please try again later."
    
    def generate_salary_forecast(self, 
                               salary_data: Dict[str, Any], 
                               region: str, 
                               sector: str,
                               forecast_years: int = 3) -> str:
        """
        Generate a forecast of future salary trends.
        
        Args:
            salary_data: Dictionary containing historical salary data
            region: The region/county for the forecast
            sector: The industry sector for the forecast
            forecast_years: Number of years to forecast
            
        Returns:
            String containing the generated forecast
        """
        try:
            # Prepare the prompt with context
            prompt = self._create_forecast_prompt(salary_data, region, sector, forecast_years)
            
            # Call the OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert economist specializing in salary forecasting and labor market trends in Estonia. Provide clear, data-driven forecasts of future salary trends."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=600,
                temperature=0.5
            )
            
            # Extract and return the generated text
            return response.choices[0].message.content
            
        except Exception as e:
            self.logger.error(f"Error generating salary forecast: {str(e)}")
            return "Sorry, I couldn't generate a forecast at this time. Please try again later."
    
    def generate_career_recommendations(self, 
                                      sector: str, 
                                      current_role: Optional[str] = None) -> str:
        """
        Generate career growth recommendations for achieving salary growth.
        
        Args:
            sector: The industry sector
            current_role: Optional current job role
            
        Returns:
            String containing career growth recommendations
        """
        try:
            # Prepare the prompt with context
            prompt = self._create_recommendations_prompt(sector, current_role)
            
            # Call the OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert career coach specializing in the Estonian job market. Provide clear, actionable recommendations for career growth and salary advancement."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=700,
                temperature=0.7
            )
            
            # Extract and return the generated text
            return response.choices[0].message.content
            
        except Exception as e:
            self.logger.error(f"Error generating career recommendations: {str(e)}")
            return "Sorry, I couldn't generate recommendations at this time. Please try again later."
    
    def answer_salary_question(self,
                             question: str,
                             salary_data: Optional[Dict[str, Any]] = None) -> str:
        """
        Answer a specific question about salary trends using the OpenAI API.
        
        Args:
            question: The user's question
            salary_data: Optional dictionary containing relevant salary data
            
        Returns:
            String containing the answer to the question
        """
        try:
            # Prepare the prompt with context
            prompt = self._create_question_prompt(question, salary_data)
            
            # Call the OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert economist specializing in Estonian salary trends and labor markets. Provide clear, accurate answers to questions about salaries in Estonia."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800,
                temperature=0.7
            )
            
            # Extract and return the generated text
            return response.choices[0].message.content
            
        except Exception as e:
            self.logger.error(f"Error answering salary question: {str(e)}")
            return "Sorry, I couldn't answer your question at this time. Please try again later."
    
    def stream_salary_question(self,
                              question: str,
                              salary_data: Optional[Dict[str, Any]] = None):
        """
        Stream the answer to a specific question about salary trends using the OpenAI API.
        
        Args:
            question: The user's question
            salary_data: Optional dictionary containing relevant salary data
            
        Returns:
            A streaming response from the OpenAI API
        """
        try:
            # Prepare the prompt with context
            prompt = self._create_question_prompt(question, salary_data)
            
            # Call the OpenAI API with streaming enabled
            stream = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert economist specializing in Estonian salary trends and labor markets. Provide clear, accurate answers to questions about salaries in Estonia."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800,
                temperature=0.7,
                stream=True
            )
            
            # Return the streaming response
            return stream
            
        except Exception as e:
            self.logger.error(f"Error streaming salary question answer: {str(e)}")
            raise
    
    def _create_trend_analysis_prompt(self, 
                                    salary_data: Dict[str, Any], 
                                    region: str, 
                                    sector: str) -> str:
        """
        Create a prompt for salary trend analysis.
        
        Args:
            salary_data: Dictionary containing salary data
            region: The region/county for the analysis
            sector: The industry sector for the analysis
            
        Returns:
            String containing the prompt
        """
        # Convert salary data to a string representation
        data_str = self._format_data_for_prompt(salary_data)
        
        prompt = f"""
        Please analyze the following salary data for {sector} in {region}:
        
        {data_str}
        
        Provide a comprehensive analysis including:
        1. Overall trend (increasing, decreasing, stable)
        2. Average annual growth rate
        3. Comparison with inflation rates if possible
        4. Key factors that might be influencing these trends
        5. How these trends compare to other sectors or regions in Estonia
        
        Your analysis should be clear, data-driven, and focused on the most important insights.
        """
        
        return prompt
    
    def _create_forecast_prompt(self, 
                              salary_data: Dict[str, Any], 
                              region: str, 
                              sector: str,
                              forecast_years: int) -> str:
        """
        Create a prompt for salary forecast.
        
        Args:
            salary_data: Dictionary containing historical salary data
            region: The region/county for the forecast
            sector: The industry sector for the forecast
            forecast_years: Number of years to forecast
            
        Returns:
            String containing the prompt
        """
        # Convert salary data to a string representation
        data_str = self._format_data_for_prompt(salary_data)
        
        prompt = f"""
        Based on the following historical salary data for {sector} in {region}:
        
        {data_str}
        
        Please provide a forecast for the next {forecast_years} years, including:
        1. Projected salary levels for each year
        2. Expected growth rates
        3. Factors that might influence these projections
        4. Level of confidence in the forecast
        5. Potential risks or opportunities that could affect the forecast
        
        Your forecast should be data-driven and consider both historical trends and current economic conditions in Estonia.
        """
        
        return prompt
    
    def _create_recommendations_prompt(self, 
                                     sector: str, 
                                     current_role: Optional[str]) -> str:
        """
        Create a prompt for career growth recommendations.
        
        Args:
            sector: The industry sector
            current_role: Optional current job role
            
        Returns:
            String containing the prompt
        """
        role_context = f" for someone currently working as a {current_role}" if current_role else ""
        
        prompt = f"""
        Please provide specific recommendations for achieving salary growth in the {sector} sector in Estonia{role_context}.
        
        Include:
        1. In-demand skills that can lead to higher salaries
        2. Educational qualifications or certifications that are valued
        3. Career paths or roles that offer the best salary progression
        4. Industry trends that might affect future salary potential
        5. Specific companies or types of organizations that typically offer higher salaries
        
        Your recommendations should be practical, actionable, and specific to the Estonian job market.
        """
        
        return prompt
    
    def _create_question_prompt(self, 
                              question: str, 
                              salary_data: Optional[Dict[str, Any]]) -> str:
        """
        Create a prompt for answering a specific question.
        
        Args:
            question: The user's question
            salary_data: Optional dictionary containing relevant salary data
            
        Returns:
            String containing the prompt
        """
        # Convert salary data to a string representation if provided
        data_context = ""
        if salary_data:
            data_str = self._format_data_for_prompt(salary_data)
            data_context = f"""
            Here is some relevant salary data that might help you answer the question:
            
            {data_str}
            """
        
        prompt = f"""
        Please answer the following question about Estonian salary trends:
        
        "{question}"
        
        {data_context}
        
        Provide a clear, informative answer based on the data and your knowledge of the Estonian labor market.
        """
        
        return prompt
    
    def _format_data_for_prompt(self, data: Dict[str, Any]) -> str:
        """
        Format data dictionary for inclusion in a prompt.
        
        Args:
            data: Dictionary containing data to format
            
        Returns:
            String representation of the data
        """
        # This is a simple implementation - you might want to customize this
        # based on the actual structure of your data
        formatted_str = ""
        
        if "years" in data and "values" in data:
            for year, value in zip(data["years"], data["values"]):
                formatted_str += f"{year}: {value}\n"
        else:
            # Just convert the dictionary to a string
            for key, value in data.items():
                formatted_str += f"{key}: {value}\n"
        
        return formatted_str