import zlib
import streamlit as st
import pandas as pd
import numpy as np
from itertools import cycle
from sqlalchemy import Table, MetaData, Select, create_engine

#function to get game_data with clusters
@st.cache_data(persist="disk")
def get_game_data():
    engine = create_engine('sqlite:///../Databases/streamlit_database.db')

    metadata_obj = MetaData()
    game_data_table = Table('game_data', metadata_obj, autoload_with=engine)

    query = game_data_table.select()

    game_data = pd.read_sql(sql=query, con=engine)

    engine.dispose()

    return game_data

#function to get distance data
def get_distance_data(id):
    engine = create_engine('sqlite:///../Databases/streamlit_database.db')
    conn = engine.connect()

    metadata_obj = MetaData()
    distances_table = Table('distances', metadata_obj, autoload_with=engine)

    query = Select(metadata_obj.tables['distances'].columns.id,
                   metadata_obj.tables['distances'].columns.distances).where(metadata_obj.tables['distances'].columns.id == id)
    result = conn.execute(query).fetchall()

    distances_str = zlib.decompress(result[0][1]).decode('utf-8')
    distances = np.fromstring(distances_str, dtype=np.float32, sep=',')

    engine.dispose()

    return distances

#getting game_data with clusters
cluster_data = get_game_data()

st.title('Gaming Recommendation')
st.write('Source: https://github.com/GabrielSaldanha/GamingRecommendation')

with st.container():
    #selection data for the checkbox where the user will choose the game to search for similar games
    game_select = cluster_data[['id','name','url']].sort_values(by='name', ascending=True)
    game_select_id = game_select['id'].tolist()
    game_select_name = game_select['name'].tolist()
    game_select_img = game_select['url'].tolist()

    #creating the checkbox
    game_option = st.selectbox(
                'Select the game:',
                range(len(game_select_name)),
                index=None,
                placeholder="Choose an option",
                format_func=lambda x: game_select_name[x]
                )
    
    #creating a button to choose the game
    col1_btn, col2_btn, col3_btn, col4_btn = st.columns(4)
    with col4_btn:
        confirm_button = st.button("Select", use_container_width=True)

    #creating an image of the selected game
    col1_game_selected, col2_game_selected, col3_game_selected = st.columns(3)
    with col2_game_selected:
        if(game_option is not None):
            if(not pd.isna(game_select_img[game_option])):
                st.image('https:'+game_select_img[game_option], width=150, caption=game_select_name[game_option])
            else:
                st.image('https://images.igdb.com/igdb/image/upload/t_cover_big/nocover.png', width=150, caption=game_select_name[game_option])

    #retrieval of games similar to the selected game
    if confirm_button and game_option is not None:
        st.dataframe(cluster_data[cluster_data['id']==game_select_id[game_option]])
        st.write('Games selected:')

        id_selected = game_select_id[game_option]

        #adding the distances of each row from the selected game
        distances = get_distance_data(id_selected)
        recomended_games = cluster_data.copy()
        recomended_games['distances'] = distances
        recomended_games = recomended_games.sort_values('distances')

        #filtering the games to those in the same cluster number as the selected game
        cluster = list(cluster_data[cluster_data['id']==id_selected]['clusters'])[0]
        recomended_games = recomended_games[recomended_games['clusters'] == cluster]

        #getting the top ten games similar to the selected game
        top_recommended_games = recomended_games.copy()
        top_recommended_games = top_recommended_games[top_recommended_games['id']!=id_selected]
        top_recommended_games = top_recommended_games.head(8)
        
        #variables to generate images of similar games
        list_names_recommended = top_recommended_games['name'].tolist()
        list_imgs = top_recommended_games['url'].tolist()

        #creating images of the similar games
        if(len(list_imgs) != 0):
            cols = cycle(st.columns(4))
            for idx,url in enumerate(list_imgs):
                if(not pd.isna(url)):
                    next(cols).image('https:'+url, width=150, caption=list_names_recommended[idx])
                else:
                    next(cols).image('https://images.igdb.com/igdb/image/upload/t_cover_big/nocover.png', width=150, caption=list_names_recommended[idx])
        
        else:
            st.write('No games found')

        st.dataframe(top_recommended_games)