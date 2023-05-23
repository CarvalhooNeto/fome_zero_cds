import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from folium.plugins   import MarkerCluster

st.set_page_config(
    page_title="Home"
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
#df = rename_columns(df)
df = df.drop_duplicates(keep='first')
df = df.reset_index()

df["Rating color"] = df["Rating color"].apply(color_name)

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

# ==============================
# LAYOUT
# ==============================

st.header("Fome zero!")
st.subheader("The Best Place to Find A Restaurant")
tab1, tab2, tab3 = st.tabs (['-', '-', '-'])

with tab1:
   
  
  with st.container():
    st.markdown('Overall Metrics:')
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
      number_restaurants=len(df['Restaurant Name'].unique())
      col1.metric('Number Of Restaurants: ',number_restaurants)

    with col2:
      number_country = len(df['Country Code'].unique())
      col2.metric('Number of Countries: ', number_country)

    with col3:
      number_cities = len(df['City'].unique())
      col3.metric('Number of Cities: ', number_cities)

    with col4:
      number_ratings = df.shape[0]
      col4.metric('Number of Ratings: ',number_ratings)

    with col5:
      number_cuisines = len(df['Cuisines'].unique())
      col5.metric('Number of Cuisines: ',number_cuisines)

    with st.container():  

        df_aux = df[['Restaurant Name','Longitude','Latitude', 'Average Cost for two',"Cuisines","Aggregate rating","Rating color"]].groupby(['Restaurant Name','Cuisines','Rating color']).median().reset_index()
        

    map = folium.Map(default_zoom_start = 15)
    marker_cluster = MarkerCluster().add_to(map)

    for index, info_location in df_aux.iterrows():
        folium.Marker([info_location['Latitude'], info_location['Longitude']],
                      popup = "<b>{0}</b> \n Cuisine:\n <b>{1}</b>\n \n  Price For Two:\n <b>{2}</b> \n Aggregate Rating:\n <b>{3}/5.0</b> ".format(info_location['Restaurant Name'],info_location['Cuisines'], info_location['Average Cost for two'], info_location["Aggregate rating"] ),
                      icon=folium.Icon(color= info_location["Rating color"], icon='info-sign')).add_to( marker_cluster )
    folium_static(map, width=1024, height=600)  
    
