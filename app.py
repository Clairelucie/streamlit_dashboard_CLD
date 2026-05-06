import streamlit as st
import pandas as pd
import plotly.express as px

st.title('CO2 Emissions Dashboard 🌍')

co2_df = pd.read_csv('CO2_per_capita.csv', sep=';')
geo_df = pd.read_csv('geo_data.csv')

geo_df = geo_df[['Three_Letter_Country_Code', 'Continent_Name']]
merged_df = co2_df.merge(geo_df, left_on='Country Code', right_on='Three_Letter_Country_Code')

st.dataframe(merged_df.head())

def top_n_emitters_v2(df, start_year, end_year, nb_displayed):
    df_filtered = df[(df['Year'] >= start_year) & (df['Year'] <= end_year)]
    df_avg = df_filtered.groupby(['Country Name', 'Country Code', 'Continent_Name'], as_index=False)['CO2 Per Capita (metric tons)'].mean()
    df_top = df_avg.sort_values('CO2 Per Capita (metric tons)', ascending=False).head(nb_displayed)
    fig = px.bar(df_top, x='Country Name', y='CO2 Per Capita (metric tons)', color='Continent_Name', title=f'Top {nb_displayed} emetteurs ({start_year}-{end_year})')
    return fig

def scatter_map(df, year):
    df_year = df[df['Year'] == year].dropna(subset=['CO2 Per Capita (metric tons)'])
    fig = px.scatter_geo(df_year, locations='Country Code', size='CO2 Per Capita (metric tons)', hover_name='Country Name', color='Continent_Name', projection='natural earth', title=f'CO2 par habitant ({year})')
    return fig

def choropleth_map(df):
    fig = px.choropleth(df, locations='Country Code', color='CO2 Per Capita (metric tons)', hover_name='Country Name', animation_frame='Year', projection='natural earth', title='CO2 Per Capita par pays')
    return fig

year = st.slider('Selectionne une annee', min_value=1960, max_value=2020, value=2000)
nb_countries = st.selectbox('Nombre de pays', [3, 5, 10, 20, 30])

st.plotly_chart(top_n_emitters_v2(merged_df, year, year, nb_countries))
st.plotly_chart(scatter_map(merged_df, year))
st.plotly_chart(choropleth_map(merged_df))