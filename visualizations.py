import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Optional, Union, Any

def create_time_series(df: pd.DataFrame, 
                      title: str, 
                      x_col: str = 'Year', 
                      y_col: str = 'Value',
                      color_col: Optional[str] = None) -> go.Figure:
    """
    Create a time series line chart.
    
    Args:
        df: DataFrame containing the data
        title: Chart title
        x_col: Column name for x-axis (default: 'Year')
        y_col: Column name for y-axis (default: 'Value')
        color_col: Optional column name for color differentiation
        
    Returns:
        Plotly figure object
    """
    if color_col:
        fig = px.line(df, x=x_col, y=y_col, color=color_col, title=title)
    else:
        fig = px.line(df, x=x_col, y=y_col, title=title)
    
    # Customize the layout
    fig.update_layout(
        xaxis_title=x_col,
        yaxis_title=y_col,
        template="plotly_white",
        hovermode="x unified"
    )
    
    # Add markers to the lines
    fig.update_traces(mode="lines+markers")
    
    return fig

def create_comparison_chart(df: pd.DataFrame, 
                          title: str,
                          categories: List[str],
                          x_col: str = 'Year') -> go.Figure:
    """
    Create a bar chart for comparing multiple categories.
    
    Args:
        df: DataFrame containing the data
        title: Chart title
        categories: List of column names to compare
        x_col: Column name for x-axis (default: 'Year')
        
    Returns:
        Plotly figure object
    """
    # Melt the DataFrame to get it in the right format for plotting
    melted_df = df.melt(id_vars=[x_col], value_vars=categories, var_name='Category', value_name='Value')
    
    # Create the bar chart
    fig = px.bar(melted_df, x=x_col, y='Value', color='Category', barmode='group', title=title)
    
    # Customize the layout
    fig.update_layout(
        xaxis_title=x_col,
        yaxis_title="Value",
        template="plotly_white",
        hovermode="x unified"
    )
    
    return fig

def create_growth_chart(df: pd.DataFrame, 
                       title: str,
                       x_col: str = 'Year', 
                       y_col: str = 'Growth Rate (%)') -> go.Figure:
    """
    Create a bar chart for growth rates.
    
    Args:
        df: DataFrame containing the data
        title: Chart title
        x_col: Column name for x-axis (default: 'Year')
        y_col: Column name for y-axis (default: 'Growth Rate (%)')
        
    Returns:
        Plotly figure object
    """
    # Create the bar chart
    fig = px.bar(df, x=x_col, y=y_col, title=title)
    
    # Customize the layout
    fig.update_layout(
        xaxis_title=x_col,
        yaxis_title=y_col,
        template="plotly_white",
        hovermode="x unified"
    )
    
    # Color bars based on positive/negative values
    fig.update_traces(
        marker_color=df[y_col].apply(lambda x: 'green' if x >= 0 else 'red')
    )
    
    return fig

def create_forecast_chart(df: pd.DataFrame, 
                         title: str,
                         x_col: str = 'Year', 
                         y_col: str = 'Value',
                         type_col: str = 'Type') -> go.Figure:
    """
    Create a chart showing historical data and forecast.
    
    Args:
        df: DataFrame containing historical and forecast data
        title: Chart title
        x_col: Column name for x-axis (default: 'Year')
        y_col: Column name for y-axis (default: 'Value')
        type_col: Column name indicating data type (default: 'Type')
        
    Returns:
        Plotly figure object
    """
    # Create a combined line and scatter plot
    fig = go.Figure()
    
    # Add historical data as a solid line
    historical_df = df[df[type_col] == 'Historical']
    fig.add_trace(go.Scatter(
        x=historical_df[x_col],
        y=historical_df[y_col],
        mode='lines+markers',
        name='Historical',
        line=dict(color='blue')
    ))
    
    # Add forecast data as a dashed line
    forecast_df = df[df[type_col] == 'Forecast']
    fig.add_trace(go.Scatter(
        x=forecast_df[x_col],
        y=forecast_df[y_col],
        mode='lines+markers',
        name='Forecast',
        line=dict(color='red', dash='dash')
    ))
    
    # Customize the layout
    fig.update_layout(
        title=title,
        xaxis_title=x_col,
        yaxis_title=y_col,
        template="plotly_white",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    return fig

def create_regional_comparison(df: pd.DataFrame, 
                             title: str,
                             region_col: str = 'Region', 
                             value_col: str = 'Value') -> go.Figure:
    """
    Create a bar chart comparing values across different regions.
    
    Args:
        df: DataFrame containing the data
        title: Chart title
        region_col: Column name for regions (default: 'Region')
        value_col: Column name for values (default: 'Value')
        
    Returns:
        Plotly figure object
    """
    # Sort the DataFrame by value
    sorted_df = df.sort_values(by=value_col, ascending=False)
    
    # Create the bar chart
    fig = px.bar(sorted_df, x=region_col, y=value_col, title=title)
    
    # Customize the layout
    fig.update_layout(
        xaxis_title=region_col,
        yaxis_title=value_col,
        template="plotly_white",
        hovermode="x unified"
    )
    
    # Rotate x-axis labels if there are many regions
    if len(df) > 5:
        fig.update_layout(xaxis_tickangle=-45)
    
    return fig

def create_sector_comparison(df: pd.DataFrame, 
                           title: str,
                           sector_col: str = 'Sector', 
                           value_col: str = 'Value') -> go.Figure:
    """
    Create a bar chart comparing values across different sectors.
    
    Args:
        df: DataFrame containing the data
        title: Chart title
        sector_col: Column name for sectors (default: 'Sector')
        value_col: Column name for values (default: 'Value')
        
    Returns:
        Plotly figure object
    """
    # Sort the DataFrame by value
    sorted_df = df.sort_values(by=value_col, ascending=False)
    
    # Create the bar chart
    fig = px.bar(sorted_df, x=sector_col, y=value_col, title=title)
    
    # Customize the layout
    fig.update_layout(
        xaxis_title=sector_col,
        yaxis_title=value_col,
        template="plotly_white",
        hovermode="x unified"
    )
    
    # Rotate x-axis labels if there are many sectors
    if len(df) > 5:
        fig.update_layout(xaxis_tickangle=-45)
    
    return fig

def create_heatmap(df: pd.DataFrame, 
                  title: str,
                  x_col: str, 
                  y_col: str,
                  value_col: str) -> go.Figure:
    """
    Create a heatmap for visualizing data across two dimensions.
    
    Args:
        df: DataFrame containing the data
        title: Chart title
        x_col: Column name for x-axis
        y_col: Column name for y-axis
        value_col: Column name for values (color intensity)
        
    Returns:
        Plotly figure object
    """
    # Pivot the DataFrame to get it in the right format for a heatmap
    pivot_df = df.pivot(index=y_col, columns=x_col, values=value_col)
    
    # Create the heatmap
    fig = px.imshow(
        pivot_df,
        labels=dict(x=x_col, y=y_col, color=value_col),
        x=pivot_df.columns,
        y=pivot_df.index,
        title=title,
        color_continuous_scale="Viridis"
    )
    
    # Customize the layout
    fig.update_layout(
        template="plotly_white",
    )
    
    # Add value annotations
    fig.update_traces(text=pivot_df.values, texttemplate="%{text:.1f}")
    
    return fig

def create_dashboard(data_dict: Dict[str, pd.DataFrame], 
                    region: str, 
                    sector: str,
                    data_type: str) -> Dict[str, go.Figure]:
    """
    Create a complete dashboard with multiple visualizations.
    
    Args:
        data_dict: Dictionary containing various DataFrames
        region: The selected region/county
        sector: The selected industry sector
        data_type: The type of salary data
        
    Returns:
        Dictionary containing Plotly figure objects
    """
    # Extract the DataFrames
    base_df = data_dict['base_data']
    growth_df = data_dict['growth_rates']
    comparison_df = data_dict['comparison']
    forecast_df = data_dict['forecast']
    
    # Create the visualizations
    time_series = create_time_series(
        df=base_df,
        title=f"{data_type} in {region} for {sector} (Time Series)"
    )
    
    growth_chart = create_growth_chart(
        df=growth_df,
        title=f"Annual Growth Rate of {data_type} in {region} for {sector}"
    )
    
    # Create comparison chart if we have comparison data
    if 'National Average' in comparison_df.columns:
        comparison_chart = create_comparison_chart(
            df=comparison_df,
            title=f"Comparison with National Average: {data_type} for {sector}",
            categories=['Selected', 'National Average'],
            x_col='Year'
        )
    else:
        comparison_chart = None
    
    # Create forecast chart
    forecast_chart = create_forecast_chart(
        df=forecast_df,
        title=f"Historical and Forecasted {data_type} in {region} for {sector}"
    )
    
    # Return all visualizations in a dictionary
    return {
        'time_series': time_series,
        'growth_chart': growth_chart,
        'comparison_chart': comparison_chart,
        'forecast_chart': forecast_chart
    }