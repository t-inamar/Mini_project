import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
import json
from copy import deepcopy
import pandas as pd
import plotly.io as pio


df_raw = pd.read_csv("./data/renewable_power_plants_CH.csv")
df = deepcopy(df_raw)

geojson_file = "./data/georef-switzerland-kanton.geojson"

with open(geojson_file) as f:
    geojson_data = json.load(f)
    print(geojson_data.keys())  
print(geojson_data['features'][0])


st.title('Clean Energy Sources in Switzerland')
#st.header('Data Exploration')

if st.checkbox("Show Dataframe"):
    st.dataframe(df)


nuts3_regions_codes = {
    "CH011": "22",
    "CH012": "23",
    "CH013": "25",
    "CH021": "02",
    "CH022": "10",
    "CH023": "11",
    "CH024": "24",
    "CH025": "26",
    "CH031": "12",
    "CH032": "13",
    "CH033": "19",
    "CH040": "01",
    "CH051": "08",
    "CH052": "14",
    "CH053": "15",
    "CH054": "16",
    "CH055": "17",
    "CH056": "18",
    "CH057": "20",
    "CH061": "03",
    "CH062": "04",
    "CH063": "05",
    "CH064": "06",
    "CH065": "07",
    "CH066": "09",
    "CH070": "21"}


df["kan_code"] = df["nuts_3_region"].map(nuts3_regions_codes)
df.loc[(df["nuts_3_region"].isna()) & (df["canton"] == "ZH"), "kan_code"] = "01"
df.loc[(df["nuts_3_region"].isna()) & (df["canton"] == "AR"), "kan_code"] = "15"
df.loc[(df["nuts_3_region"].isna()) & (df["canton"] == "GR"), "kan_code"] = "18"
df.loc[(df["nuts_3_region"].isna()) & (df["canton"] == "AG"), "kan_code"] = "19"
df.loc[(df["nuts_3_region"].isna()) & (df["canton"] == "VD"), "kan_code"] = "22"
df["production_per_canton"] = df["kan_code"].map(df.groupby("kan_code")["production"].sum())
df["kan_code"].map(df.groupby("kan_code")["production"].sum()).round().astype(int)


canton_name_list = []
for feature in geojson_data['features']:
    canton_name_list.append({feature["properties"]["kan_code"]: feature["properties"]["kan_name"]})

canton_name_dict = {}
for element in canton_name_list:
    canton_name_dict.update(element)

df["kan_name"] = df["kan_code"].map(canton_name_dict)


######## Total production per canton graph


st.subheader("Total production per canton")
fig = px.choropleth_mapbox(
    df,
    geojson=geojson_data,
    featureidkey="properties.kan_code",
    locations="kan_code",
    color="production_per_canton",
    mapbox_style="carto-positron",
    zoom=6,
    center={"lat": 47, "lon": 8},
    hover_name = "kan_name",
    color_continuous_scale = [
        (0, "white"),  
        (0.5, "lightgreen"), 
        (1, "green") 
    ] 
)
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
fig.update_traces(hovertemplate="<b>%{hovertext}</b><br>Production: %{z}<extra></extra>")

st.plotly_chart(fig)


######## Renewable energy production sites graph
st.subheader("Renewable energy production sites")


df.loc[df["production"] <= 0, "production"] = 0

left_column, middle_column, right_column = st.columns([3, 1, 1])
with left_column:
    selected_energy_source = st.selectbox(
        "Select an Energy Source:",
        options=["All"] + list(df["energy_source_level_2"].unique()),
)

if selected_energy_source == "All":
    filtered_df = df
else:
    filtered_df = df[df["energy_source_level_2"] == selected_energy_source]

filtered_df['Energy source'] = filtered_df['energy_source_level_2']

fig2 = px.scatter_mapbox(filtered_df, lat = "lat", lon = "lon",
    hover_name="project_name",  
    color="energy_source_level_2",
    size = "production",
    size_max=15,
    zoom=7,
    mapbox_style="carto-positron", 
    hover_data={"lat": False, "lon": False, "energy_source_level_2": False, "Energy source": True }, 
    center={"lat": 47, "lon": 8}, ) 
filtered_df.drop(columns=["Energy source"], inplace=True)
st.plotly_chart(fig2)




url = "https://open-power-system-data.org/"
st.write("Data Source:", url)
 

