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
    page_title="Cuisines"
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

st.header("Marketplace - Cuisines View")

tab1, tab2, tab3 = st.tabs (['General View', '-', '-'])

with tab1:
   
  
  with st.container():
    st.subheader('Bests Restaurante By Cuisines')
    col1, col2, col3, col4, col5 = st.columns(5, gap="small")

    with col1:
      selected_rows1 = df.loc[:,"Cuisines"] == "Italian"
      df_aux=df.loc[selected_rows1, ["Restaurant Name","Aggregate rating"]].sort_values("Aggregate rating", ascending = False)
      empty = 0
      if not df_aux.empty:
        italian_food = df_aux.iloc[0,0]
        italian_note = df_aux.iloc[0,1]
      
        col1.metric(label='Italian: {0}'.format(italian_food), value = '{0}/5.0'.format(italian_note) )
      else:
        col1.metric('Italian: ',  empty)
    with col2:
      selected_rows1 = df.loc[:,"Cuisines"] == "American"
      df_aux=df.loc[selected_rows1, ["Restaurant Name","Aggregate rating"]].sort_values("Aggregate rating", ascending = False)
      empty = 0
      if not df_aux.empty:
        american_food = df_aux.iloc[0,0]
        american_note = df_aux.iloc[0,1]
      
        col2.metric(label='American: {0}'.format(american_food), value = '{0}/5.0'.format(american_note) )
      else:
        col2.metric('American:', empty)

    with col3:
      selected_rows1 = df.loc[:,"Cuisines"] == "Arabian"
      df_aux=df.loc[selected_rows1, ["Restaurant Name","Aggregate rating"]].sort_values("Aggregate rating", ascending = False)
      empty = 0
      if not df_aux.empty:
        
        arabian_food = df_aux.iloc[0,0]
        arabian_note = df_aux.iloc[0,1]
      
        col3.metric(label='Arabain: {0}'.format(arabian_food), value = '{0}/5.0'.format(arabian_note) )
      else:
        col3.metric('Arabian: ' , empty)

    with col4:
      selected_rows1 = df.loc[:,"Cuisines"] == "Japanese"
      df_aux=df.loc[selected_rows1, ["Restaurant Name","Aggregate rating"]].sort_values("Aggregate rating", ascending = False)
      empty = 0
      if not df_aux.empty:
        japanese_food = df_aux.iloc[0,0]
        japanese_note = df_aux.iloc[0,1]
      
        col4.metric(label='Japanese: {0}'.format(japanese_food), value = '{0}/5.0'.format(japanese_note) )
      else:
        col4.metric('Japanese:', empty)

    with col5:
      selected_rows1 = df.loc[:,"Cuisines"] == "Home-made"
      df_aux=df.loc[selected_rows1, ["Restaurant Name","Aggregate rating"]].sort_values("Aggregate rating", ascending = False)
      empty = 0
      if not df_aux.empty:
        home_made_food = df_aux.iloc[0,0]
        home_made_note = df_aux.iloc[0,1]
      
        col5.metric(label='Home-made: {0}'.format(home_made_food), value = '{0}/5.0'.format(home_made_note) )
      else:
        col5.metric('Home-made:', empty)

  with st.container():    
        st.markdown("""---""")
        st.subheader('Top 10 Restaurants')
        df_aux = (df.loc[:, ["Restaurant Name","Country Code","City", "Cuisines", "Average Cost for two","Aggregate rating", "Votes"]]
                        .sort_values("Aggregate rating", ascending = False))
                       
        df_aux = round(df_aux.head(10), 2)

        st.dataframe(df_aux)  
  with st.container():    
        st.markdown("""---""")
        st.subheader('Top 10 Cuisines:')

        col1, col2 = st.columns(2)
        with col1:
        
          st.subheader('Bests Cuisines')
          df_aux = df.loc[: , ["Votes","Cuisines"]].groupby("Cuisines").mean().reset_index().sort_values("Votes", ascending = False)
          df_aux = round(df_aux.head(7), 2)

          fig = px.bar(df_aux, x="Cuisines", y = "Votes" ) 
          st.plotly_chart(fig, use_container_width= True)

        with col2:  
          
          st.subheader('Worst Cuisines')
          df_aux = df.loc[: , ["Votes","Cuisines"]].groupby("Cuisines").mean().reset_index().sort_values("Votes", ascending = True)
          df_aux = df_aux.head(7)

          fig = px.bar(df_aux, x="Cuisines", y = "Votes" ) 
          st.plotly_chart(fig, use_container_width= True)
