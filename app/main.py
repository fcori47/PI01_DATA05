from fastapi import FastAPI
from starlette.responses import RedirectResponse
import pandas as pd
import numpy as np
from collections import Counter

app = FastAPI()

@app.get('/')
def raiz():
    return RedirectResponse(url="/docs/")

@app.get('/')
def separation (column):
    test = []
    for item in column:
        splited_item = item.split(' ')
        test.append(int(splited_item[0]))
        
    return test


@app.get("/get_max_duration/")
async def get_max_duration(year:int, platform:str, min_or_season:str):
    df = pd.read_csv('Datasets/all_frames.csv')
    df.drop(columns='Unnamed: 0', inplace=True)
    df.duration = pd.Series(separation(df.duration))
    df = df.loc[(df.release_year == year) & (df.platform == platform)]
    
    if min_or_season == 'min':
        df = df.loc[df.type == 'Movie']
    elif min_or_season == 'season':
        df = df.loc[df.type == 'TV Show']
    
    result = df.sort_values(by='duration', ascending=False).head(1)
    
    for resultado in result.title: 
        return {'titulo': resultado}
    
@app.get("/get_listedin/")    
async def get_listedin(genero:str):
    df = pd.read_csv('Datasets/all_frames.csv')
    df.drop(columns='Unnamed: 0', inplace=True)
    df_amazon = df.loc[df.platform == 'Amazon Prime']
    df_disney = df.loc[df.platform == 'Disney+']
    df_hulu = df.loc[df.platform == 'Hulu']
    df_netflix = df.loc[df.platform == 'Netflix']
    
    listed_in_by_platform = []
    amazon_genre = []
    netflix_genre = []
    hulu_genre = []
    disney_genre = []
    
    for genres in df_amazon['listed_in']:
        genre = genres.split(',')
        for splited_genre in genre:
            amazon_genre.append(splited_genre.strip())
        
    listed_in_by_platform.append(('Amazon',amazon_genre.count(genero)))
    
    for genres in df_hulu['listed_in']:
        genre = genres.split(',')
        for splited_genre in genre:
            hulu_genre.append(splited_genre.strip())
        
    listed_in_by_platform.append(('Hulu',hulu_genre.count(genero)))
    
    for genres in df_disney['listed_in']:
        genre = genres.split(',')
        for splited_genre in genre:
            disney_genre.append(splited_genre.strip())
        
    listed_in_by_platform.append(('Disney',disney_genre.count(genero)))
    
    
    for genres in df_netflix['listed_in']:
        genre = genres.split(',')
        for splited_genre in genre:
            netflix_genre.append(splited_genre.strip())
        
    listed_in_by_platform.append(('Netflix',netflix_genre.count(genero)))
    
    result = max(listed_in_by_platform, key=lambda tup: tup[1])
    
    return {'platforma': result[0], 'cantidad': result[1]}


@app.get("/get_count_platform/")
async def get_count_plataform(platform:str):
    df = pd.read_csv('Datasets/all_frames.csv')
    df.drop(columns='Unnamed: 0', inplace=True)
    df = df.loc[df.platform == platform]
    df_movies = df.loc[df.type == 'Movie'] 
    df_series= df.loc[df.type == 'TV Show'] 
    
    return {'platforma': platform, 'movie': len(df_movies), 'tvshow': len(df_series)}


@app.get("/get_actor/")
async def get_actor(platform:str,year:int):
    df = pd.read_csv('Datasets/all_frames.csv')
    df.drop(columns='Unnamed: 0', inplace=True)
    df = df.loc[(df.release_year == year) & (df.platform == platform)]
    
    all_actors_list = []
    
    for actors in df.cast:
        if type(actors) == float:
            continue
        else:
            splited_actors = actors.split(',')
            for striped_actor in splited_actors:
                all_actors_list.append(striped_actor.strip())
            
    all_actors_list = Counter(all_actors_list)
    result = all_actors_list.most_common()[0]
    
    return {'platform': platform, 'cantidad': result[1], 'actores':result[0]}