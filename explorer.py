import streamlit as st
import os
import sys
import pandas as pd
import numpy as np
import mysql.connector
import datetime
from pathlib import Path
import seaborn as sns
import plotly_express as px
import SessionState
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# """
# SessionState file should be in the same 
# folder the Python code is located.
# Run it once before using the Streamlit.

# """
session_state = SessionState.get(
        tel_path=0,url=0,selected_filename=0,upload=0,columns=0  ,
        show_dataframe=0 , show_summary=0 , write_equation=0     ,
        enter_equation_1=0,enter_equation_2=0,enter_equation_3=0 ,
        calculate_columns=0 , write_filter=0 , enter_filter_1=0  ,
        apply_filter=0,seaborn=0 ,scatter_plot=0,generate_plot=0 ,
        line_plot=0 , add_range=0 ,write_range=0 , apply_range=0 ,
        generate_lineplot=0
        )

# Data loader function
@st.cache(allow_output_mutation=True)
def load_data(path):
    data = pd.read_hdf(path)
    return data

html_temp = """
<div style="background-color:yellow;"><p style="color:Black;
font-size:25px;padding:8px">ML Dataset Explorer/Sherry Vedadi</p></div>
"""
st.markdown(html_temp,unsafe_allow_html=True)

st.header("DataFrame")
choose = ['','Server', 'Computer', 'CSV File Picker']

session_state.choose_method = st.sidebar.selectbox('Choose How to Upload Data' , choose)
        #  SERVER
if session_state.choose_method == 'Server':
    lst = ["x1","x2","x3","x4"]
    list_list = st.selectbox("Select:" , lst)
    list_list = f"{list_list}"
    st.info("You Selected {}".format(list_list))
    # insert the path
    if list_list:
        session_state.tel_path = st.text_input('Enter your Path:', value=session_state.tel_path)
        tel_path = session_state.tel_path
        if tel_path:
            tel_path = f"{tel_path}"
            sys.path.insert(1, tel_path)
            st.info("You Selected {}".format(tel_path))
            import tel.table
            sd = tel.table.ServerDB()
        
        # Upload from SQL Database

        mydb = mysql.connector.connect(host=r'development-app.AAASHERRY.com',
        user="sherry",password="sherry",database="sherry_data")
        mycursor = mydb.cursor()
        sdate = mycursor.execute("SELECT * FROM table.data where lst = 'x1'")
        sdate = mycursor.execute("SELECT * FROM table.data where lst = 'x1'" = \''.$ list_list")
        start_date = mycursor.fetchall()
        end_date = pd.read_sql_query("SELECT * FROM table.data where lst = list_list")
        
    start_date = st.sidebar.date_input('Start Date', datetime.date(sdate))
    end_date = st.sidebar.date_input('End Date', datetime.date(date.today()))
    period = [start_date , end_date]
         
        # Upload from COMPUTER 
if session_state.choose_method == 'Computer':
    session_state.url = st.text_input('Enter the Path', value=session_state.url)
    url = session_state.url
    st.info("You Entered {}".format(url))
    if url != '0':
        filename = os.listdir(url)
        session_state.selected_filename = st.selectbox('Select a File', filename)
        selected_filename = session_state.selected_filename
        if selected_filename:
            selected_filename = f"{selected_filename}"
            st.info("You Selected {}".format(selected_filename))
            full_path = Path(url) / selected_filename
            st.info(f"You Selected {full_path}")

        # Data Picker 
if session_state.choose_method == 'CSV File Picker':
    input_buffer = st.file_uploader("Pick the File")
# Upload data
session_state.upload = st.sidebar.checkbox('Upload', value=session_state.upload)
if session_state.upload:
    if session_state.choose_method == 'Server':
        data = tel.table.get_data_db(list_list, (period[0],period[1]), 
        ['Date','Column1', 'Column2', 'Column3'], sd, multiprocess=False)
    
    if session_state.choose_method == 'Computer':
        data = load_data(full_path)
    
    if session_state.choose_method == 'CSV File Picker':
        data = pd.read_csv(input_buffer)

# Select columns
session_state.columns = st.checkbox('Select Columns', value=session_state.columns)
if session_state.columns:
    select_col = st.multiselect('Select Column' , data.columns)

    session_state.show_dataframe = st.sidebar.checkbox('Create Dataframe', value=session_state.show_dataframe)
    if session_state.show_dataframe:
        df = data[select_col]
        st.write(df.head())

# Summary of Data
session_state.show_summary = st.checkbox('Summary of Data', value=session_state.show_summary)
if session_state.show_summary:
    st.subheader("Shape of Dataset")
    st.write(df.shape)
    st.subheader("Data Types")
    st.write(df.dtypes)
    st.subheader("Statistics Summary")
    st.write(df.describe().T)

# Equations and Filter Selection
st.header("Equation & Filter")
session_state.write_equation = st.checkbox('Equations', value=session_state.write_equation)
if session_state.write_equation:
    session_state.enter_equation_1 = st.sidebar.text_input('Enter Equation 1', value=session_state.enter_equation_1)
    equ1 = session_state.enter_equation_1
    if equ1:
        equ1 = f"NewColumn1 = {equ1}" 
    session_state.enter_equation_2 = st.sidebar.text_input('Enter Equation 2', value=session_state.enter_equation_2)
    equ2 = session_state.enter_equation_2
    if equ2:
        equ2 = f"NewColumn2 = {equ2}"
    session_state.enter_equation_3 = st.sidebar.text_input('Enter Equation 3', value=session_state.enter_equation_3)
    equ3 = session_state.enter_equation_3
    if equ3:
        equ3 = f"NewColumn3 = {equ3}"
    # Calculation
    session_state.calculate_columns = st.sidebar.checkbox('Apply Equations', value=session_state.calculate_columns)
    if session_state.calculate_columns:
        if equ1:
            df.eval(equ1,inplace=True)
        if equ2:
            df.eval(equ2, inplace=True)
        if equ3:
            df.eval(equ3, inplace=True)
        st.write(df.head())

# Filter Selection
session_state.write_filter = st.checkbox('Filter Selection', value=session_state.write_filter)
if session_state.write_filter:
    session_state.enter_filter_1 = st.sidebar.text_input('Enter Filter', value=session_state.enter_filter_1)
    filter_selection1 = session_state.enter_filter_1
    if filter_selection1:
        filter_selection1 = f"{filter_selection1}"
    session_state.apply_filter = st.sidebar.checkbox('Apply Filter', value=session_state.apply_filter)
    if session_state.apply_filter:
        if filter_selection1:
            df = df[df.eval(filter_selection1)]
            st.write(df.head())
            st.subheader("Summary")
            st.write(df.describe().T)

# Data Visualization
st.header("Visualization")

session_state.seaborn = st.checkbox('Correlation Plot [Seaborn]', value=session_state.seaborn)
if session_state.seaborn:
    st.write(sns.heatmap(df.corr(),annot=True))
    st.pyplot()

session_state.scatter_plot = st.checkbox('Scatter Plot', value=session_state.scatter_plot)
if session_state.scatter_plot:
    col_x = st.selectbox('Which Feature on X axis?', df.columns[0:])
    col_y = st.selectbox('Which Feature on Y axis?', df.columns[0:])
    session_state.generate_plot = st.sidebar.checkbox('Generate Scatter Plot', value=session_state.generate_plot)
    if session_state.generate_plot:
        st.success("Generating Scatter Plot")
        figs = px.scatter(df, x =col_x,y=col_y)
        st.plotly_chart(figs)

# Multi Line chart
session_state.line_plot = st.checkbox('Line Plot', value=session_state.line_plot)
if session_state.line_plot:
    axis_x = st.selectbox('Select X axis:', df.columns[0:])
    axis_y = st.multiselect('Select Y axis:', df.columns[0:])

    # Add range/filter
    session_state.add_range = st.checkbox('Add Range', value=session_state.add_range)
    if session_state.add_range:
        session_state.write_range = st.sidebar.text_input('Type the Range...', value = session_state.write_range)
        rangee = session_state.write_range
        if rangee:
            rangee = f"{rangee}"
        session_state.apply_range = st.sidebar.checkbox('Apply Range', value=session_state.apply_range)
        if session_state.apply_range:
            if rangee:
                df = df[df.eval(rangee)]

    session_state.generate_lineplot = st.sidebar.checkbox('Generate Line Plot', value=session_state.generate_lineplot)
    if session_state.generate_lineplot:
        st.success("Generating Line Plot")
        figl = make_subplots(rows=len(axis_y), cols=1, shared_xaxes=True, vertical_spacing=0.03)
        
        for i in range(len(axis_y)):
            figl.add_trace(go.Line(x = df[axis_x], y = df[axis_y[i]],name=axis_y[i]),row=len(axis_y)-i, col=1)
        st.plotly_chart(figl)



