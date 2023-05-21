import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import folium
from PIL import Image
from streamlit_folium import folium_static
import inflection

st.set_page_config(
    page_title="Country"
)

# ==============================
# Funções
# ==============================

COUNTRIES = {
1: "India",
14: "Australia",
30: "Brazil",
37: "Canada",
94: "Indonesia",
148: "New Zeland",
162: "Philippines",
166: "Qatar",
184: "Singapure",
189: "South Africa",
191: "Sri Lanka",
208: "Turkey",
214: "United Arab Emirates",
215: "England",
216: "United States of America",
}
def country_name(country_id):
  return COUNTRIES.get(country_id)

def create_price_tye(price_range):
  if price_range == 1:
    return "cheap"
  elif price_range == 2:
    return "normal"
  elif price_range == 3:
    return "expensive"
  else:
    return "gourmet"

COLORS = {
"3F7E00": "darkgreen",
"5BA829": "green",
"9ACD32": "lightgreen",
"CDD614": "orange",
"FFBA00": "red",
"CBCBC8": "darkred",
"FF7800": "darkred",
}
def color_name(color_code):
  return COLORS.get(color_code)

def rename_columns(dataframe):
    df = dataframe.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new
    return df


# Read csv file
data = pd.read_csv('./dataset/zomato.csv')

# Copy of main file
df = data.copy()

# Cleaning Dataset

df["Cuisines"] = df["Cuisines"].astype(str)
df["Cuisines"] = df.loc[:, "Cuisines"].apply(lambda x: x.split(",")[0])
rename_columns(df)
df = df.drop_duplicates(keep='first')
df = df.reset_index()



# Layout in Streamlit

# ==============================
# SIDEBAR
# ==============================


st.sidebar.header(' Fome zero')
st.sidebar.subheader(' Chose your country, city and restaurant ;-)')
st.sidebar.markdown('''---''')

st.sidebar.subheader(' Select a Country')

country_options = st.sidebar.multiselect(
    'Wich Country Do You Like?',
    ['Australia','Brazil','Canada','England','India','Indonesia','New Zeland','Philippines','Qatar',
    'Singapure','South Africa','Sri Lanka','Turkey','United Arab Emirates','United States of America'],

    default = ['England', 'India', 'South Africa', 'Brazil', 'New Zeland']
)
st.sidebar.markdown('''---''')
st.sidebar.markdown('Powered by Aderaldo Neto - Comunidade DS')
# Filter

df["Country Code"] = df["Country Code"].apply(country_name)
linhas_selecionadas = df["Country Code"].isin(country_options)
df = df.loc[linhas_selecionadas, :]

# ==============================
# LAYOUT
# ==============================

st.header("Marketplace - Country View")

tab1, tab2, tab3 = st.tabs (['General View', '-', '-'])
with tab1:

    with st.container():
        st.subheader('Number Of Restaurants Registered By Country')
        df_aux = df.loc[:, ["Restaurant ID","Country Code"]].groupby("Country Code").count().reset_index()
      

        fig = px.bar(df_aux, x="Country Code", y = "Restaurant ID", labels={'Country Code':'Countries', 'Restaurant ID': 'Number of Restaurants'}, color = df_aux["Country Code"] )
        st.plotly_chart(fig, use_container_width= True)
        
    with st.container():
        st.subheader('Average Of Votes By Country')
        df_aux = round(df.loc[:, ["Votes","Country Code"]].groupby("Country Code").mean().reset_index(), 2)
        

        fig = px.bar(df_aux, x="Country Code", y = "Votes", labels={'Country Code':'Countries', 'Votes': 'Votes'}, color = df_aux["Country Code"] )
        st.plotly_chart(fig, use_container_width= True)
    
    with st.container():
        st.subheader('Average Cost for two By Country')
        df_aux = round(df.loc[:, ["Average Cost for two","Country Code"]].groupby("Country Code").mean().reset_index(),2)
        

        fig = px.bar(df_aux, x="Country Code", y = "Average Cost for two", labels={'Country Code':'Countries'}, color = df_aux["Country Code"] ) 
        st.plotly_chart(fig, use_container_width= True)
