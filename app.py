import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(page_title="CO2 Emissions Dashboard", page_icon="🌍", layout="wide")

# Style
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    h1 { color: #2c3e50; text-align: center; }
    .stSlider, .stSelectbox { background-color: white; border-radius: 10px; padding: 10px; }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1>🌍 CO2 Emissions Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:gray;'>Visualisation des émissions de CO2 par habitant dans le monde</p>", unsafe_allow_html=True)
st.divider()

# Load data
co2_df = pd.read_csv('CO2_per_capita.csv', sep=';')
geo_df = pd.read_csv('geo_data.csv')
geo_df = geo_df[['Three_Letter_Country_Code', 'Continent_Name']]
merged_df = co2_df.merge(geo_df, left_on='Country Code', right_on='Three_Letter_Country_Code')

# Sidebar
st.sidebar.title("⚙️ Paramètres")
year = st.sidebar.slider('Sélectionne une année', min_value=1960, max_value=2020, value=2000)
nb_countries = st.sidebar.selectbox('Nombre de pays', [3, 5, 10, 20, 30], index=2)

# Functions
def top_n_emitters_v2(df, start_year, end_year, nb_displayed):
    df_filtered = df[(df['Year'] >= start_year) & (df['Year'] <= end_year)]
    df_avg = df_filtered.groupby(['Country Name', 'Country Code', 'Continent_Name'], as_index=False)['CO2 Per Capita (metric tons)'].mean()
    df_top = df_avg.sort_values('CO2 Per Capita (metric tons)', ascending=False).head(nb_displayed)
    fig = px.bar(df_top, x='Country Name', y='CO2 Per Capita (metric tons)', color='Continent_Name',
                 title=f'🏆 Top {nb_displayed} émetteurs ({start_year})',
                 color_discrete_sequence=px.colors.qualitative.Set2)
    fig.update_layout(plot_bgcolor='white', paper_bgcolor='white')
    return fig

def scatter_map(df, year):
    df_year = df[df['Year'] == year].dropna(subset=['CO2 Per Capita (metric tons)'])
    fig = px.scatter_geo(df_year, locations='Country Code', size='CO2 Per Capita (metric tons)',
                         hover_name='Country Name', color='Continent_Name',
                         projection='natural earth', title=f'🗺️ CO2 par habitant ({year})',
                         color_discrete_sequence=px.colors.qualitative.Set2)
    fig.update_layout(paper_bgcolor='white')
    return fig

def choropleth_map(df):
    fig = px.choropleth(df, locations='Country Code', color='CO2 Per Capita (metric tons)',
                        hover_name='Country Name', animation_frame='Year',
                        projection='natural earth', title='🌐 Evolution du CO2 par pays',
                        color_continuous_scale='Reds')
    fig.update_layout(paper_bgcolor='white')
    return fig

# Layout
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(top_n_emitters_v2(merged_df, year, year, nb_countries), use_container_width=True)
with col2:
    st.plotly_chart(scatter_map(merged_df, year), use_container_width=True)

st.plotly_chart(choropleth_map(merged_df), use_container_width=True)

# Data
with st.expander("📊 Voir les données brutes"):
    st.dataframe(merged_df[merged_df['Year'] == year].dropna())