import pandas as pd
import io
import base64
from datetime import datetime
from typing import Dict, List, Optional, Union, Any
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def generate_csv_download_link(df: pd.DataFrame, filename: str) -> str:
    """
    Generate a download link for a DataFrame as a CSV file.
    
    Args:
        df: DataFrame to export
        filename: Name of the file to download
        
    Returns:
        HTML string with download link
    """
    # Ensure the filename has .csv extension
    if not filename.endswith('.csv'):
        filename += '.csv'
    
    # Convert DataFrame to CSV
    csv = df.to_csv(index=False)
    
    # Create a download link
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">Download CSV File</a>'
    
    return href

def generate_excel_download_link(df: pd.DataFrame, filename: str) -> str:
    """
    Generate a download link for a DataFrame as an Excel file.
    
    Args:
        df: DataFrame to export
        filename: Name of the file to download
        
    Returns:
        HTML string with download link
    """
    # Ensure the filename has .xlsx extension
    if not filename.endswith('.xlsx'):
        filename += '.xlsx'
    
    # Create a BytesIO object to store the Excel file
    output = io.BytesIO()
    
    # Create Excel writer
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        # Write DataFrame to Excel
        df.to_excel(writer, sheet_name='Data', index=False)
        
        # Get the xlsxwriter workbook and worksheet objects
        workbook = writer.book
        worksheet = writer.sheets['Data']
        
        # Add some formatting
        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'top',
            'fg_color': '#D7E4BC',
            'border': 1
        })
        
        # Write the column headers with the defined format
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, header_format)
            
        # Set column widths
        for i, col in enumerate(df.columns):
            column_width = max(df[col].astype(str).map(len).max(), len(col)) + 2
            worksheet.set_column(i, i, column_width)
    
    # Get the Excel file as bytes
    excel_data = output.getvalue()
    
    # Create a download link
    b64 = base64.b64encode(excel_data).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}">Download Excel File</a>'
    
    return href

def generate_pdf_report(data_dict: Dict[str, pd.DataFrame], 
                       region: str, 
                       sector: str,
                       data_type: str,
                       start_year: int,
                       end_year: int,
                       ai_analysis: Optional[str] = None) -> bytes:
    """
    Generate a PDF report with data tables and optional AI analysis.
    
    Args:
        data_dict: Dictionary containing various DataFrames
        region: The selected region/county
        sector: The selected industry sector
        data_type: The type of salary data
        start_year: The starting year
        end_year: The ending year
        ai_analysis: Optional AI-generated analysis text
        
    Returns:
        PDF file as bytes
    """
    # Create a BytesIO object to store the PDF
    buffer = io.BytesIO()
    
    # Create the PDF document
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    
    # Get the default styles
    styles = getSampleStyleSheet()
    
    # Create a custom style for the title
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=12
    )
    
    # Create a custom style for section headings
    section_style = ParagraphStyle(
        'Section',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=8,
        spaceBefore=12
    )
    
    # Create a custom style for normal text
    normal_style = ParagraphStyle(
        'Normal',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6
    )
    
    # Create the content for the PDF
    content = []
    
    # Add the title
    title = Paragraph(f"Estonian Salary Trends Report: {data_type} in {region} for {sector}", title_style)
    content.append(title)
    
    # Add the date
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date = Paragraph(f"Generated on: {date_str}", normal_style)
    content.append(date)
    content.append(Spacer(1, 0.25 * inch))
    
    # Add the parameters section
    content.append(Paragraph("Report Parameters:", section_style))
    params_text = f"""
    Region/County: {region}
    Industry Sector: {sector}
    Data Type: {data_type}
    Time Period: {start_year} - {end_year}
    """
    content.append(Paragraph(params_text, normal_style))
    content.append(Spacer(1, 0.25 * inch))
    
    # Add the data tables
    # Base data
    if 'base_data' in data_dict:
        content.append(Paragraph("Salary Data:", section_style))
        df = data_dict['base_data']
        table_data = [df.columns.tolist()] + df.values.tolist()
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        content.append(table)
        content.append(Spacer(1, 0.25 * inch))
    
    # Growth rates
    if 'growth_rates' in data_dict:
        content.append(Paragraph("Growth Rates:", section_style))
        df = data_dict['growth_rates']
        table_data = [df.columns.tolist()] + df.values.tolist()
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        content.append(table)
        content.append(Spacer(1, 0.25 * inch))
    
    # Comparison with national average
    if 'comparison' in data_dict:
        content.append(Paragraph("Comparison with National Average:", section_style))
        df = data_dict['comparison']
        table_data = [df.columns.tolist()] + df.values.tolist()
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        content.append(table)
        content.append(Spacer(1, 0.25 * inch))
    
    # Forecast
    if 'forecast' in data_dict:
        content.append(Paragraph("Salary Forecast:", section_style))
        df = data_dict['forecast']
        table_data = [df.columns.tolist()] + df.values.tolist()
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        content.append(table)
        content.append(Spacer(1, 0.25 * inch))
    
    # Add AI analysis if provided
    if ai_analysis:
        content.append(Paragraph("AI-Generated Analysis:", section_style))
        content.append(Paragraph(ai_analysis, normal_style))
        content.append(Spacer(1, 0.25 * inch))
    
    # Add a footer
    footer_text = "Generated by Estonian Salary Trends Application | Data source: Statistics Estonia"
    footer = Paragraph(footer_text, normal_style)
    content.append(footer)
    
    # Build the PDF
    doc.build(content)
    
    # Get the PDF as bytes
    pdf_data = buffer.getvalue()
    buffer.close()
    
    return pdf_data

def generate_pdf_download_link(data_dict: Dict[str, pd.DataFrame], 
                             region: str, 
                             sector: str,
                             data_type: str,
                             start_year: int,
                             end_year: int,
                             ai_analysis: Optional[str] = None,
                             filename: str = "salary_report.pdf") -> str:
    """
    Generate a download link for a PDF report.
    
    Args:
        data_dict: Dictionary containing various DataFrames
        region: The selected region/county
        sector: The selected industry sector
        data_type: The type of salary data
        start_year: The starting year
        end_year: The ending year
        ai_analysis: Optional AI-generated analysis text
        filename: Name of the file to download
        
    Returns:
        HTML string with download link
    """
    # Ensure the filename has .pdf extension
    if not filename.endswith('.pdf'):
        filename += '.pdf'
    
    # Generate the PDF
    pdf_data = generate_pdf_report(
        data_dict=data_dict,
        region=region,
        sector=sector,
        data_type=data_type,
        start_year=start_year,
        end_year=end_year,
        ai_analysis=ai_analysis
    )
    
    # Create a download link
    b64 = base64.b64encode(pdf_data).decode()
    href = f'<a href="data:application/pdf;base64,{b64}" download="{filename}">Download PDF Report</a>'
    
    return href