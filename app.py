import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from streamlit_option_menu import option_menu
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
import matplotlib.pyplot as plt

st.set_page_config(
    layout="wide",
    page_title = "Taylor Swift's Emotional Impact on Success")

# Implementar el cache en el sitio web para evitar el reload
@st.cache_data   #Quitar el reload
def load_data_df(file):
    df = pd.read_csv(file)
    return df

@st.cache_data
def load_data_dfTour(file):
    df_tour = pd.read_csv(file)
    return df_tour

# Cargar los datos
df = load_data_df("df_taylor.csv")
df_tour = load_data_dfTour('df_tour.csv')

st.markdown(
    """
    <style>
        footer {display: none}
        [data-testid="stHeader"] {display: none}
    </style>
    """, unsafe_allow_html = True
)
# ------------------------------------------------
# INICIO DE DISEÑO DE PAGINA DE KPIS PARTE SUPERIOR
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html = True)

title_col, emp_col, pop_col, ear_col, dur_col, trev_col, xrp_col = st.columns([1,0.2,1,1,1,1,1])


# TITULO DEL PROYECTO
with title_col:
    st.markdown("<p class='dashboard_title'>Taylor Swift's<br>Emotional Impact<br>on her Success</p>", unsafe_allow_html = True)

# POPULARIDAD
with pop_col:
    with st.container():
        kpi1 = round(df['popularity'].mean(),2)
        st.markdown(f'<p class="kpi1_text">SPOTIFY RATING AVG<br></p><p class="price_details">{kpi1}</p>', unsafe_allow_html = True)

# EMOTIONS AND RYTHM
with ear_col:
    with st.container():
        kpi2 = round(df['valence'].mean(),2)

        # Determinar la categoría
        if 0.33 <= kpi2 < 0.66:
            category = '<span style="font-size: 80%; color: #555;">Neutral</span>'
        else:
            category = ""  # Otra categoría si es necesario

        # Mostrar el KPI2 y la categoría
        st.markdown(f'<p class="kpi2_text">VALENCE AVG<br></p><p class="price_details">{kpi2}<br>{category}</p>', unsafe_allow_html=True)

# DURATION
with dur_col:
    with st.container():
        kpi3 = round(df['min_duration'].mean(), 2)

        # Mostrar el KPI3 y la unidad 'Minutes'
        st.markdown(f'<p class="kpi3_text">DURATION AVG<br></p><p class="price_details">{kpi3}<br>Minutes</p>', unsafe_allow_html=True)

# TOUR REVENUES
with trev_col:
    with st.container():
        kpi4 = df_tour['Revenue'].mean()

        # Formatear el resultado como dinero en dólares
        formatted_kpi4 = "${:,.2f}".format(kpi4)

        # Mostrar el KPI4 y la unidad 'USD'
        st.markdown(f'<p class="kpi4_text" style="font-size: 90%;">REVENUE AVG PER CONCERT<br></p><p class="price_details" style="font-size: 150%;">{formatted_kpi4}<br>USD</p>', unsafe_allow_html=True)# SE TERMINA DISEÑO FRONTAL DE KPIS 

# FIN DE DISEÑO DE PAGINA DE KPIS PARTE SUPERIOR
# ------------------------------------------------

# Horizontal menu
selected_menu = option_menu(None,
                            ["Overview", "Popularity", "Emotions and Rythm", "Tour Revenues"],
                            icons=['eye', 'star', 'emoji-smile', 'cash'],
                            menu_icon="cast", default_index=0, orientation="horizontal")

# --------------------------------------------------------------------
if selected_menu == "Overview":
    st.write("Let's take a look of the databases we will use in this project. ")
    df = df
    with st.expander("Spotify API"):
      st.write(df.head())

    df_tour = df_tour
    with st.expander('Tours:'):
        st.write(df_tour.head())

    st.write('Inside this section we will introduce the description that includes each song to discover more about.')

     # Text input for song selection
    user_input = st.text_input("Write a song name:")

    # Filter songs based on user input
    matching_songs = df[df['name'].str.contains(user_input, case=False)]['name'].tolist()
    
    # Remove duplicates using a set
    matching_songs = list(set(matching_songs))

    # Multiselect for song selection
    selected_songs = st.multiselect("Select songs:", matching_songs)

    # Display information for the selected songs
    for selected_song in selected_songs:
        selected_song_data = df[df['name'] == selected_song].iloc[0]
        st.write('----------------------------------------')
        st.write(f"**Song:** {selected_song}")
        st.write(f"**Popularity:** {selected_song_data['popularity']}")
        st.write(f"**Dance Category:** {selected_song_data['dance_category']}")
        st.write(f"**Duration:** {round(selected_song_data['min_duration'], 2)} minutes")
        st.write(f"**Valence Category:** {selected_song_data['valence_category']}")


# --------------------------------------------------------------------
if selected_menu == "Popularity":
    # Seccion 2.1
    st.subheader('Top 10 songs')
    st.write('''Result of an exploratory analysis of the most popular songs by the singer Taylor Swift.''')
    top_10_popular = df.nlargest(10, 'popularity')

    bar_top10_canc = px.bar(
        top_10_popular,
        x='name',
        y='popularity',
        color = 'popularity',
        title='Top 10 Popular Songs',
        color_continuous_scale='Plasma_r'
    )
    st.plotly_chart(bar_top10_canc)

    # Seccion 2.2
    st.subheader('Top 5 albums')
    st.write('''Result of an exploratory analysis that displays the 5 most popular albums''')

    # Agrupar por álbum y el promedio la popularidad de las canciones en cada álbum
    album_popularity = df.groupby('album')['popularity'].mean().reset_index()
    # 5 álbumes más populares
    top_5_popular_albums = album_popularity.nlargest(5, 'popularity')

    bar_top5_album = px.bar(
        top_5_popular_albums,
        x='album',
        y='popularity',
        color = 'popularity',
        title='Top 5 Albums',
        color_continuous_scale='Plasma_r'

    )
    st.plotly_chart(bar_top5_album)
    st.write("""
In this chart of the Top 5 most popular albums, we observe coherence with current events.
**1989 (Taylor's Version)** is a recent album released by the singer, and there's a theory circulating on social media that suggests the next album to be released after this recent one will be **Reputation (Taylor's Version)**.
However, it's worth noting that the latest concert of the current tour, **The Eras Tour**, has already taken place, and there hasn't been an announcement regarding such an album.
**Midnights** is another recent album that came out in 2022.
As for **Lover**, it's notably famous for **Cruel Summer**.
The mention of the deluxe version of **1989** is because it is an identical version with the ownership label called **Taylor's Version**.
""")

    # Sección 2.3
    st.subheader('Top 5 songs per top 5 álbum')

    # Crear un selectbox con la lista de álbumes en top_5_popular_albums
    selected_album = st.selectbox('Select an album', top_5_popular_albums['album'])

    # Mapear las paletas de colores para cada álbum
    paleta_colores = {
        "1989 (Taylor's Version)": 'blues',
        "reputation": 'gray_r',
        "Midnights": 'purples',
        "Lover": 'pinkyl',
        "1989 (Taylor's Version) [Deluxe]": 'blues'
    }

    # Obtener la paleta de colores para el álbum seleccionado
    paleta_color_seleccionado = paleta_colores.get(selected_album, 'Plasma_r')

    # Filtrar el DataFrame df para obtener las top 5 canciones del álbum seleccionado
    top_songs_per_selected_album = df[df['album'] == selected_album].nlargest(5, 'popularity')

    # Crear el gráfico de barras para las top 5 canciones del álbum seleccionado
    bar_top5_songs_album = px.bar(
        top_songs_per_selected_album,
        x='name',
        y='popularity',
        color='popularity',
        title=f'Top 5 Canciones from album {selected_album}',
        color_continuous_scale=paleta_color_seleccionado
    )

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(bar_top5_songs_album)


# --------------------------------------------------------------------
elif selected_menu == "Emotions and Rythm":
    # Sección para emociones basadas en la categoría de valencia
    st.subheader('Emotions based on Valence Category')
    st.write('''Exploratory analysis of emotions based on the valence category (Negative, Neutral, Positive).''')
    # Explanation of valence categories
    st.write('''* **Positive** - Happy, euphoric, upbeat songs.
* **Neutral** - Emotional neutrality, not conveying a specific feeling.
* **Negative** - Sad, angry, or depressive songs.''')

    # Conteo de canciones en cada categoría de valencia
    valence_counts = df['valence_category'].value_counts()

    # Gráfico de barras
    bar_valence_emotions = px.bar(
        valence_counts,
        x=valence_counts.index,
        y=valence_counts.values,
        title='Distribution of Songs Based on Valence Category',
        labels={'x': 'Valence Category', 'y': 'Number of Songs'},
        color=valence_counts.index,
        color_discrete_map={'Negative': 'red', 'Neutral': 'gray', 'Positive': 'green'}
    )
    st.plotly_chart(bar_valence_emotions)
    st.write("""
Based on this recent chart, we can visualize that almost 50% of the total songs, which is 530, fall into the category labeled as Negative.
These songs are characterized as Sad, Angry, or Depressive. Additionally, a significant portion of the songs is neutral, neither explicitly happy nor sad.
""")

    top5_songs_by_category_valence = pd.concat(
    [df[df['valence_category'] == category].nlargest(5, 'valence') for category in df['valence_category'].unique()],
    ignore_index=True
    )

    # top 5 de canciones por categoría de Valence
    sunburst_top5_songs_valence = px.sunburst(
        top5_songs_by_category_valence,
        path=['valence_category', 'name'],
        color = 'valence',
        color_continuous_scale= ['red', 'gray', 'green'],
        title='Top 5 Songs per Valence Category'
    )

    st.plotly_chart(sunburst_top5_songs_valence)
    st.write("""
Equally, we are emphasizing that out of the total 530 songs, special attention will be given for a more in-depth analysis to the top 5 songs in terms of their corresponding Valence category, representing the most prevalent emotions in these songs.
""")

  # Sección para emociones basadas en la categoría de valencia
    st.subheader('Albums Majority Valence Category Distribution')
    st.write('''Exploratory analysis of majority valence category distribution for each album.''')

    # Group by album and calculate the majority valence category for each album
    majority_valence_by_album = df.groupby('album')['valence_category'].agg(lambda x: x.mode().iloc[0]).reset_index(name='majority_valence_category')

    # Sunburst chart for majority valence category distribution per album
    sunburst_majority_valence_albums = px.sunburst(
        majority_valence_by_album,
        path=['majority_valence_category', 'album'],
        title='Majority Valence Category Distribution per Album',
        color='majority_valence_category',
        color_discrete_map={'Negative': 'red', 'Neutral': 'gray', 'Positive': 'green'}
    )

    st.plotly_chart(sunburst_majority_valence_albums)
    st.write("""
Although there are songs that represent a positive value, on average, each album only contains two categories: Neutral and Negative.
""")
    import hashlib

    # Function to get a hash of the selected songs
    def get_selected_songs_hash(selected_songs):
        return hashlib.md5(str(selected_songs).encode()).hexdigest()

    # Initialize session state
    if 'selected_songs_hash' not in st.session_state:
        st.session_state.selected_songs_hash = None

    # Multiselect for song selection
    all_songs = df['name'].unique()  # Get unique songs from the DataFrame
    selected_songs_parallel = st.multiselect("Select songs for Parallel Coordinates:", all_songs)

    # Get the hash of the selected songs
    selected_songs_hash = get_selected_songs_hash(selected_songs_parallel)

    # Check if the hash has changed, indicating a change in selected songs
    if st.session_state.selected_songs_hash != selected_songs_hash:
        st.session_state.selected_songs_hash = selected_songs_hash

        # Filter the DataFrame based on the selected songs
        filtered_df_parallel = df[df['name'].isin(selected_songs_parallel)]

        # Check if any songs are selected
        if not filtered_df_parallel.empty:
            # Remove duplicates from the filtered DataFrame
            filtered_df_parallel = filtered_df_parallel.drop_duplicates(subset='name')

            # Parallel Coordinates diagram
            parallel_fig = px.parallel_coordinates(
                filtered_df_parallel,
                dimensions=['popularity', 'min_duration', 'valence'],
                color='popularity',
                labels={'popularity': 'Popularity', 'min_duration': 'Duration (minutes)', 'valence': 'Valence'},
                title='Parallel Coordinates for Selected Songs',
                color_continuous_scale='Plasma_r'
            )

            st.plotly_chart(parallel_fig)
        else:
            st.warning("Please select at least one song to display in the Parallel Coordinates diagram.")


# --------------------------------------------------------------------
elif selected_menu == "Tour Revenues":

    st.header('Revenue average per Tour')
        # Definir el diccionario de colores para cada tour
    color_discrete_map = {
        'Fearless Tour': 'yellow',
        'Speak Now World Tour': 'purple',
        'The Red Tour': 'red',
        'The 1989 World Tour': 'blue',
        'Reputation Stadium Tour': 'black'
    }

    # Agrupar por el nombre del tour y calcular el promedio de ganancias
    avg_revenue_by_tour = df_tour.groupby('Tour')['Revenue'].mean().reset_index()

    # Crear el gráfico de barras con colores personalizados
    fig_avg_revenue_by_tour = px.bar(
        avg_revenue_by_tour,
        x='Tour',
        y='Revenue',
        title='Average Revenue per Tour',
        labels={'Revenue': 'Average Revenue', 'Tour': 'Tour Name'},
        color='Tour',
        color_discrete_map=color_discrete_map
    )

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig_avg_revenue_by_tour)
    st.write("""
The earnings from the Reputation Stadium Tour are coherent considering the circumstances leading up to it. Before this tour and album, Taylor Swift intentionally took a hiatus from social media and public attention for several months. This retreat was prompted by various personal missteps that were magnified and used against her, primarily in the form of rumors. These speculations revolved around her heartbreak and the humiliation she experienced at the hands of Kanye West during the 2009 MTV Video Music Awards. In response to these challenges, Taylor Swift decided, "*There will be no further explanation. There will just be Reputation.*"
""")

    # Sección 6.1
    st.subheader('''Revenue Map by Country per Tour''')
    st.write('''In this map, you can visualize the earnings generated by each tour for the artist, from a global perspective.''')

    # Obtener los top 5 países con mayores ganancias de todos los tours
    top5_paises_ganancias = df_tour.groupby('Country')['Revenue'].sum().nlargest(5).index.tolist()

    # Seleccionar Tour específico
    selected_tour = st.selectbox("Select your album", ["All Albums", "Fearless Tour", "The Red Tour", "The 1989 World Tour", "Reputation Stadium Tour"])

    # Filtrar el DataFrame según las selecciones
    filtered_df = df_tour.copy()
    if selected_tour != "All Albums":
        filtered_df = filtered_df[filtered_df["Tour"] == selected_tour]

    # Obtener la lista de países para el menú desplegable
    paises_disponibles = ["All"] + top5_paises_ganancias

    # Seleccionar País
    selected_country = st.selectbox("Seleccionar a country", paises_disponibles)

    # Filtrar el DataFrame según las selecciones
    if selected_country != "All":
        filtered_df = filtered_df[filtered_df["Country"] == selected_country]

    # Definir la escala de colores según el tour seleccionado
    if selected_tour == "Fearless Tour":
        color_scale = 'YlOrBr'
    elif selected_tour == "The Red Tour":
        color_scale = 'Reds'
    elif selected_tour == "The 1989 World Tour":
        color_scale = 'Blues'
    elif selected_tour == "Reputation Stadium Tour":
        color_scale = 'Greys'
    else:
        color_scale = 'Viridis_r'

    # Crear el mapa de burbujas
    fig = px.scatter_geo(
        filtered_df,
        lat="Latitude",
        lon="Longitude",
        size="Revenue",
        color="Revenue",
        hover_name="City",
        size_max=30,
        title=f"Revenues per city on ({selected_tour} Tour - {selected_country})",
        color_continuous_scale=color_scale
    )

    # Configurar el diseño del mapa
    fig.update_geos(
        projection_type="natural earth",
        center=dict(lon=filtered_df["Longitude"].mean(), lat=filtered_df["Latitude"].mean()),
        scope='world',
    )

    # Configurar la información al pasar el ratón (hover)
    fig.update_traces(
        hovertemplate="<b>%{hovertext}</b><br>Revenue: $%{marker.size:,.2f}",
    )

    # Configurar la leyenda
    fig.update_layout(
        coloraxis_colorbar=dict(title="Revenue", tickformat="$,.2f"),
    )

    # Mostrar el mapa
    st.plotly_chart(fig)

    # Seccion 6.2
    # Seleccionar el formato de moneda
    
    # Seccion 6.2
    st.subheader('''Revenues in USA''')
    st.write('''In this map, you can visualize the earnings generated in the United States, either for all tours or for a specific tour.''')

    # Seleccionar Opción (Todos los tours o por Tour)
    opcion_seleccionada = st.radio("Select an option", ["All Tours", "Per Tour"])

    # Obtener la lista de tours
    tours_disponibles = df_tour["Tour"].unique().tolist()

    # Seleccionar tour según la opción
    if opcion_seleccionada == "Per Tour":
        selected_tour = st.selectbox("Seleccionar Tour", ["All Tours"] + tours_disponibles)
    else:
        selected_tour = "All Tours"

    # Filtrar el DataFrame según las selecciones
    filtered_df = df_tour.copy()

    if selected_tour != "All Tours":
        filtered_df = filtered_df[filtered_df["Tour"] == selected_tour]

    # Filtrar por United States
    filtered_df_us = filtered_df[filtered_df["Country"] == "United States"]

    # Modificar el DataFrame para consolidar ganancias
    if selected_tour == "All Tours":
        # Agrupar por Tour, Venue y calcular la suma de las ganancias
        grouped_df = filtered_df_us.groupby(["Tour", "Venue"]).agg({
            "Revenue": "sum",
            "Latitude": "mean",
            "Longitude": "mean",
            "City": "first"  # Tomar la primera ciudad en caso de múltiples
        }).reset_index()
        # Actualizar filtered_df_us con las sumas calculadas
        filtered_df_us = grouped_df.copy()

    # Crear un mapa con Folium
    if not filtered_df_us.empty and 'Latitude' in filtered_df_us.columns and 'Longitude' in filtered_df_us.columns:
        m = folium.Map(location=[filtered_df_us["Latitude"].mean(), filtered_df_us["Longitude"].mean()], zoom_start=4)

        # Agregar los marcadores al mapa
        marker_cluster = MarkerCluster().add_to(m)
        for index, row in filtered_df_us.iterrows():
            # Formatear la ganancia en formato de dinero
            formatted_revenue = "${:,.2f}".format(row['Revenue'])
            # Construir el contenido del popup con información adicional
            popup_content = f"Tour: {row['Tour']}<br>City: {row['City']}<br>Revenue: {formatted_revenue}<br>Venue: {row['Venue']}"

            # Agregar el marcador al mapa con el contenido del popup
            folium.Marker([row["Latitude"], row["Longitude"]],
                        popup=popup_content,
                        icon=None).add_to(marker_cluster)

        # Mostrar el mapa de Folium en Streamlit
        st.markdown(f'<h3>Revenue Map by Tour in the United States ({selected_tour})</h3>', unsafe_allow_html=True)
        folium_static(m)
        

    

    st.write("""
It can be concluded that, at least for Taylor Swift's fans, the most captivating experiences seem to be reflected in songs that are neutral and/or negative. This preference contributes to the success and exponential growth of the artist.
""")
