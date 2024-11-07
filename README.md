# Sales Data Project

## Overview

This Streamlit application, developed within Snowflake, allows users to fetch, analyze, and visualize sales data from the Audiohouse database. The app provides an interactive interface for querying data based on various parameters and offers data export functionality.

## Features

1. **Data Retrieval**: Fetches data from the Snowflake table
2. **Interactive Filters**: Users can select and filter data based on:
   - Stichtag (Date)
   - Vertreter (Representatives)
   - Gebiet/Produckt (Area/Product)
   - Leistungsart (Service Type)
3. **Data Comparison**: Allows comparison between two selected dates.
4. **Data Visualization**: Displays a bar chart comparing revenue by year.
5. **Data Export**: Enables downloading of filtered data as Excel files.

## Requirements

- Snowflake account 
- Streamlit
- Python packages:
  - snowflake-snowpark-python
  - pandas
  - plotly
  - openpyxl (for Excel export functionality)

## Installation

1. Ensure you have a Snowflake account with the necessary permissions.
2. Install required Python packages:
   ```
   pip install streamlit snowflake-snowpark-python pandas plotly openpyxl
   ```

## Usage

1. Run the Streamlit app within your Snowflake environment.
2. Use the dropdown menus and multi-select boxes to filter data:
   - Select Stichtag (Date)
   - Choose Vertreter (Representatives)
   - Select Gebiet/Produckt (Area/Product)
   - Choose Leistungsart (Service Type)
3. Click the "Submit" button to retrieve and display the filtered data.
4. View the resulting data table and download it as an Excel file if needed.
5. For date comparisons, select a Vergleichsstichtag (Comparison Date) to see data from both periods.
6. Analyze the bar chart showing revenue comparison by year.

## Key Components

1. **Data Fetching**: Uses Snowflake's Snowpark to query the database.
2. **Caching**: Implements `@st.cache_data` for efficient data retrieval.
3. **User Interface**: Utilizes Streamlit's form, columns, and input widgets for a user-friendly interface.
4. **Data Processing**: Filters and processes data based on user inputs.
5. **Visualization**: Creates a bar chart using Plotly Express for revenue comparison.
6. **Data Export**: Provides functionality to download data as Excel files.

## Notes

- The app includes error handling for scenarios like no data available or incorrect date selections.
- The visualization is customized for better readability, including formatted y-axis labels and adjusted layout.

## Future Enhancements

- Implement additional visualization types
- Add more advanced filtering options
- Integrate with other Snowflake databases or tables

---

## Author 

Khushi Kala
