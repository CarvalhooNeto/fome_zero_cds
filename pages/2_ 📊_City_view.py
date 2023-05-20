import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from PIL import Image
from streamlit_folium import folium_static
import inflection

st.set_page_config(
    page_title="City"
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

selected_rows = df.loc[:, "Cuisines"] != 'nan'
df = df.loc[selected_rows,:]

df["Country Code"] = df["Country Code"].apply(country_name)
df["Country Code"] = df["Country Code"].astype(str)

df["Rating color"] = df["Rating color"].apply(color_name)

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


linhas_selecionadas = df["Country Code"].isin(country_options)
df = df.loc[linhas_selecionadas, :]

# ==============================
# LAYOUT
# ==============================

st.header("Marketplace - City View")

tab1, tab2, tab3 = st.tabs (['General View', '-', '-'])
with tab1:


    with st.container():

        st.subheader('Top 10 Cities With Most Variety Of Cuisisnes')
        df_aux = df.groupby("City")['Cuisines'].unique()
        df_aux = df_aux.apply(lambda x: len(x))
        df_aux = df_aux.sort_values(ascending=False)
        df_aux = df_aux.head(10)
        
        st.dataframe(df_aux)
      
    with st.container():
        st.markdown("""---""")
        st.subheader('Top 10 Cities With Lowest Average Price For Two By City')
        df_aux = df.loc[:, ["Average Cost for two","City","Country Code"]].groupby(["City","Country Code"]).mean().reset_index().sort_values("Average Cost for two", ascending = True)
        df_aux = round(df_aux.head(10),2)

        #st.dataframe(df_aux)
        
        fig = px.bar(df_aux, x="City", y = "Average Cost for two", color = df_aux["Country Code"], labels={'City':'Cities'}) 
        st.plotly_chart(fig, use_container_width= True)

    with st.container():    
        st.markdown("""---""")
        st.subheader('Top 7 Cities')

        col1, col2 = st.columns(2)
        with col1:
        
          st.subheader('Above 4 Star')
          selected_rows = df.loc[:,'Aggregate rating'] >= 4
          df_aux = df.loc[selected_rows , ["Aggregate rating","City","Country Code"]].groupby(["City","Country Code"]).count().reset_index().sort_values("Aggregate rating", ascending = False)
          df_aux = df_aux.head(7)

          fig = px.bar(df_aux, x="City", y = "Aggregate rating", color = df_aux["Country Code"], labels={'City':'Cities'}) 
          st.plotly_chart(fig, use_container_width= True)

        with col2:  
          
          st.subheader('Below 3 Star')
          selected_rows = df.loc[:,'Aggregate rating'] <= 3
          df_aux = df.loc[selected_rows , ["Aggregate rating","City","Country Code"]].groupby(["City","Country Code"]).count().reset_index().sort_values("Aggregate rating", ascending = False)
          df_aux = df_aux.head(7)

          fig = px.bar(df_aux, x="City", y = "Aggregate rating", color = df_aux["Country Code"], labels={'City':'Cities'} ) 
          st.plotly_chart(fig, use_container_width= True)
            
    with st.container():    
        st.markdown("""---""")
        st.subheader('Deliverys And Table Booking')

        col1, col2 = st.columns(2) 

        with col1:
            st.markdown('##### Cities With Deliverys')
            selected_rows = df.loc[:,"Is delivering now"] == 1
            df_aux = (df.loc[:, ["Is delivering now","City"]].groupby("City")
                            .count()
                            .reset_index()
                            .sort_values("Is delivering now", ascending = False) )
            df_aux.rename(columns={'Is delivering now': 'Number Of Restaurants'}, inplace=True)
            st.dataframe(df_aux)  

        with col2:

            st.markdown('##### Cities With Table Booking')
            selected_rows = df.loc[:,"Has Table booking"] == 1
            df_aux = (df.loc[:, ["Has Table booking","City"]].groupby("City")
                            .count()
                            .reset_index()
                            .sort_values("Has Table booking", ascending = False) )
            df_aux.rename(columns={'Has Table booking': 'Number Of Restaurants'}, inplace=True)
            st.dataframe(df_aux)