# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
import io
import pandas as pd

import plotly.express as px



try: 
    import openpyxl
except ImportError:
    st.write("Note: Install openpyxl to enable direct Excel export")

# Write directly to the app
st.title("Sales Data Project")
st.write(
    """Fetching Data from Audiohouse Database and Audiohouse Test Data Table"""
)

# CSS to add space between elements
spacing_css = """
    <style>
    .spacer {
        margin-top: 20px;
    }
    </style>
    """

# Get the current credentials
session = get_active_session()

# session.add_import()
data_query = 'select * from Audiohouse.Tests.AUDIOHOUSE_TEST_DATA_CPY'

@st.cache_data
def fetch_data(data_query):
    sql_query = session.sql(data_query)
    # Fetch data from URL here, and then clean it up.
    return sql_query.to_pandas()

@st.experimental_fragment
def download_function_excel(label, data, file_name):
    st.download_button(
    label=label,
    data=data,
    file_name=file_name,
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)



stichtag_list = []
vertreter_list = []
gebiet_list = []
leistungsart_list = []


queried_dataframe = fetch_data(data_query=data_query)

stichtag_values = queried_dataframe['STICHTAG'].unique()
vertreter_values = queried_dataframe['MEDIABERATUNG'].unique()
gebiet_values = queried_dataframe['VK Gebiet'].unique()
leistungsart_values = queried_dataframe['GA'].unique()

for i in stichtag_values:
    if i is not None:
        stichtag_list.append(i)

for i in vertreter_values:
    if i is not None:
        vertreter_list.append(i)

for i in gebiet_values:
    if i is not None:
        gebiet_list.append(i)

for i in leistungsart_values:
    if i is not None:
        leistungsart_list.append(i)
    

with st.form(key= 'ENTRIES_FORM'):

    col1,col2 = st.columns([3,3])
    
    with col1:
        stichtag_selected = st.selectbox('**Stichtag***',stichtag_list, key = 'STICHTAG')
        st.markdown(spacing_css, unsafe_allow_html=True)

        vertreter_selected = st.multiselect('**Vertreter***',vertreter_list, key = 'VERTRETER', default = vertreter_list[0])
        st.markdown(spacing_css, unsafe_allow_html=True)

        gebiet_selected = st.multiselect('**Gebiet/Produckt***',gebiet_list, key = 'GEBIET', default = gebiet_list[0] )
        st.markdown(spacing_css, unsafe_allow_html=True)
        
    with col2:
        vergleichsstichtag_selected = st.selectbox('**Vergleichsstichtag***',stichtag_list, key= 'VERGLEICHSSTICHTAG')
        st.markdown(spacing_css, unsafe_allow_html=True)
       

        leistungsart_selected = st.multiselect('**Leistungsart***',leistungsart_list, key = 'LEISTUNGSART', default = leistungsart_list[0])
        st.markdown(spacing_css, unsafe_allow_html=True)

    
    submit_button = st.form_submit_button("Submit")

if submit_button:
    if stichtag_selected and vertreter_selected and gebiet_selected  and leistungsart_selected:
       st.success("Data Retrieved Successfully!!!")
       st.markdown(spacing_css, unsafe_allow_html=True)

       st.subheader("Data Table")

       result_df = queried_dataframe.copy()

       result_df = queried_dataframe[ (queried_dataframe['STICHTAG'] == stichtag_selected) &
                                       (queried_dataframe['MEDIABERATUNG'].isin(vertreter_selected)) & 
                                       (queried_dataframe['VK Gebiet'].isin(gebiet_selected)) &
                                       (queried_dataframe['GA'].isin(leistungsart_selected))]
       len_result_df = len(result_df.index) 
        
       if len_result_df == 0:
            st.write("**No Records Available**")
       else:
            st.write(f"**Number of Records Fetched: {len_result_df}**")
            st.markdown(spacing_css, unsafe_allow_html=True)
               
            st.dataframe(result_df)
            st.markdown(spacing_css, unsafe_allow_html=True)

            c1,c2 = st.columns([3,3])
            with c1:
                
                st.subheader("**Export Data**")
                st.write("Download the above Table Data")
             
           
            st.markdown(spacing_css, unsafe_allow_html=True)

            with c2:
                buffer_excel = io.BytesIO()
                with pd.ExcelWriter(buffer_excel, engine='openpyxl') as writer:
                    result_df.to_excel(writer, index=False, sheet_name='Sheet1')
                buffer_excel.seek(0)

                download_function_excel(label= 'Download as Excel file (xlsx)', data = buffer_excel, file_name= 'sales_data.xlsx')
            

            if stichtag_selected <= vergleichsstichtag_selected:
                st.write("**For comparison please select correct dates**")
            else:
                comparison_dates = [stichtag_selected,vergleichsstichtag_selected]
                comparison_df = queried_dataframe.copy()

                comparison_df = queried_dataframe[ (queried_dataframe['STICHTAG'].isin(comparison_dates))&
                                       (queried_dataframe['MEDIABERATUNG'].isin(vertreter_selected)) & 
                                       (queried_dataframe['VK Gebiet'].isin(gebiet_selected)) &
                                       (queried_dataframe['GA'].isin(leistungsart_selected))]
                
                st.subheader("Comparison Data")
                st.markdown(spacing_css, unsafe_allow_html=True)
                st.write(f"Number of Records Fetched: {len(comparison_df)}")
                st.markdown(spacing_css, unsafe_allow_html=True)
                st.dataframe(comparison_df)
                column1, column2 = st.columns([3,3])
                with column1:
                    st.subheader("**Export Data**")
                    st.write("Download the above Table Data")
                    
                with column2:

                    buffer_excel_comp = io.BytesIO()
                    with pd.ExcelWriter(buffer_excel_comp, engine='openpyxl') as writer:
                        comparison_df.to_excel(writer, index=False, sheet_name='Sheet1')
                    buffer_excel_comp.seek(0)
    
                    download_function_excel(label= 'Download as Excel file (xlsx)', data = buffer_excel_comp, file_name= 'sales_data_comparison.xlsx')
                
                    st.markdown(spacing_css, unsafe_allow_html=True)
    
                  
                st.subheader("Graphical Analysis")
                grouped_data = comparison_df.groupby('JAHR')['Anteil Vert.'].agg('sum').reset_index()
                
             
                grouped_data['Anteil Vert.'] = grouped_data['Anteil Vert.'].apply(lambda x: f"{x:.2f}")
             
                grouped_data['Anteil Vert.'] = grouped_data['Anteil Vert.'].astype('float') 
                grouped_data['JAHR'] = grouped_data['JAHR'].astype('int')

                max_revenue = grouped_data['Anteil Vert.'].max()
                
                y_max = (max_revenue // 50000 + 1) * 50000
                
            
                fig = px.bar(
                    grouped_data,
                    x='JAHR',
                    y='Anteil Vert.',
                    title='Revenue Comparison by Year',
                    labels={'JAHR': 'Year', 'Anteil Vert.': 'Revenue (€)'},
                    text='Anteil Vert.'  
                )

               
                fig.update_traces(
                    textposition='outside',  
                    marker_color=['#1f77b4', '#2ca02c']  
                )

                fig.update_xaxes(
                    tickmode='array',
                    tickvals=grouped_data['JAHR'].tolist(),  
                    ticktext=grouped_data['JAHR'].tolist() ,
                    type='category',
                )
                
                fig.update_layout(
                 margin=dict(
                            l=80,    # left margin
                            r=40,    # right margin
                            t=60,    # top margin
                            b=40     # bottom margin
                        ),
                
                 yaxis=dict(
                    range=[0, y_max],
                    tickformat='€,.0f',
                    tickmode='linear',
                    dtick=50000, 
                    ticktext=[f'€{x/1000:.0f}K' if x < 1000000 else f'€{x/1000000:.1f}M' 
                    for x in range(0, int(y_max) + 50000, 50000)], 
                    tickvals=list(range(0, int(y_max) + 50000, 50000)),
                    
                ),
    
                plot_bgcolor='white',
                showlegend=False,
                height=500,
                width=800,
                font=dict(size=12),
                font_color = 'black',
                bargap=0.4
                )

                fig.update_layout(
                yaxis_gridcolor='lightgrey',
                yaxis_gridwidth=0.1,
                yaxis_zeroline=True,
                yaxis_zerolinecolor='black',
                yaxis_zerolinewidth=1
                )

                
                st.plotly_chart(fig, use_container_width=True)
                
                # st.bar_chart(grouped_data)
    else:
            st.error("Something went wrong!!!")






    




    





    



