import os
import json
import time
from requests import post
import concurrent.futures

def modify_string_for_file(data, first_file=False):
    #removing empty data
    if(data == '[]'):
        data = ''
    else:
        #removing brackets
        data = data[1:-1]
        #continuing the data
        if(first_file == False):
            data = ',' + data

    return data

def extract_data_offset(link, client_id, token, exclude=None, filter=None, offset=None):
    #creating requisition query to get data
    response = post(link, **
    {
        'headers':
            {
            'Client-ID': client_id,
            'Authorization': 'Bearer '+ token
            },
        'data':
            f'''
                fields *;
                {'exclude '+exclude+'; ' if exclude!=None else ''}
                {'where '+filter+'; ' if filter!=None else ''}
                sort id asc;
                limit 500;
                offset {str(offset)};
            '''
    })

    return response

def extract_data_igdb(file_name, link, client_id, token, exclude=None, filter=None):   
    print('Creating ' + file_name)

    #setting up variables and file to start extraction
    offset = 0
    data_1_text,data_2_text,data_3_text,data_4_text = '','','',''
    
    open(file_name, 'w').close()
    f = open(file_name, "a", encoding='utf-8')
    f.write('[')
    
    while (data_1_text!='[]') or (data_2_text!='[]') or (data_3_text!='[]') or (data_4_text!='[]'):
        if(offset%5000 == 0):
            print('Offset ' + str(offset))

        #creating threads to get more data from requisitions
        executor = concurrent.futures.ThreadPoolExecutor()
        
        #IGDB's rate limit is 4 concurrent requests at once
        future_data_1 = executor.submit(extract_data_offset, link, client_id, token, exclude, filter, offset)
        future_data_2 = executor.submit(extract_data_offset, link, client_id, token, exclude, filter, offset+500)
        future_data_3 = executor.submit(extract_data_offset, link, client_id, token, exclude, filter, offset+1000)
        future_data_4 = executor.submit(extract_data_offset, link, client_id, token, exclude, filter, offset+1500)

        data_1 = future_data_1.result()
        data_2 = future_data_2.result()
        data_3 = future_data_3.result()
        data_4 = future_data_4.result()

        #waiting all threads to finish
        executor.shutdown(wait=True)

        data_1_text = data_1.text
        data_2_text = data_2.text
        data_3_text = data_3.text
        data_4_text = data_4.text

        #setting up to write data to files
        if(offset == 0):
            f.write(modify_string_for_file(data_1_text, True))
        else:
            f.write(modify_string_for_file(data_1_text))

        f.write(modify_string_for_file(data_2_text))
        f.write(modify_string_for_file(data_3_text))
        f.write(modify_string_for_file(data_4_text))

        time.sleep(1)
        offset += 2000
    
    f.write(']')
    f.close()

#extract credentials for API access
keys_dir = os.path.join(os.path.dirname(__file__),'cred','keys.json')
file = open(keys_dir)
keys = json.load(file)
file.close()

client_id_json = keys['client_id']
token_json = keys['token']

#defining database directory
parent_dir = os.path.dirname(os.path.dirname(__file__))
database_dir = os.path.join(parent_dir, 'Databases')

#extracting data from IGDB Database API
extract_data_igdb(
                os.path.join(database_dir, 'games.json'),
                'https://api.igdb.com/v4/games',
                client_id_json,
                token_json,
                'age_ratings, aggregated_rating, aggregated_rating_count, alternative_names, artworks, bundles, category, checksum, collection, collections, created_at, dlcs, expanded_games, expansions, external_games, follows, forks, franchise, franchises, game_engines, game_localizations, hypes, involved_companies, keywords, language_supports, multiplayer_modes, parent_game, player_perspectives, ports, rating, rating_count, release_dates, remakes, remasters, screenshots, similar_games, slug, standalone_expansions, status, storyline, summary, tags, total_rating_count, updated_at, url, version_parent, version_parent, version_title, videos, websites',
                'category=(0,8)'
                )

extract_data_igdb(
                os.path.join(database_dir, 'covers.json'),
                'https://api.igdb.com/v4/covers',
                client_id_json,
                token_json,
                'checksum, image_id',
                )

extract_data_igdb(
                os.path.join(database_dir, 'game_modes.json'),
                'https://api.igdb.com/v4/game_modes',
                client_id_json,
                token_json,
                'created_at, updated_at, url, checksum',
                )

extract_data_igdb(
                os.path.join(database_dir, 'genres.json'),
                'https://api.igdb.com/v4/genres',
                client_id_json,
                token_json,
                'created_at, updated_at, url, checksum',
                )

extract_data_igdb(
                os.path.join(database_dir, 'platforms.json'),
                'https://api.igdb.com/v4/platforms',
                client_id_json,
                token_json,
                'abbreviation, alternative_name, category, created_at, platform_logo, platform_family, summary, updated_at, url, versions, websites, checksum',
                )

extract_data_igdb(
                os.path.join(database_dir, 'themes.json'),
                'https://api.igdb.com/v4/themes',
                client_id_json,
                token_json,
                'created_at, updated_at, url, checksum',
                )