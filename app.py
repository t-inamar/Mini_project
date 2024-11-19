import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
import json
from copy import deepcopy
import pandas as pd


mpg_df = pd.read_csv("./data/mpg.csv")


st.title('Introduction to Streamlit')
st.header('MPG Data Exploration')

st.subheader("This is my dataset:")
if st.checkbox("Show Dataframe"):
    st.dataframe(mpg_df)
#st.table(mpg_df)


url = "https://cheat-sheet.streamlit.app/"
st.write("Data Source:", url)
 
