import numpy as np
import pandas as pd
from api.utils import (convert, convert_cast, convert_movies,
                    stem, fetch_director,
                    convert_tags, get_similarity)

movies = pd.read_csv('tmdb_5000_movies.csv')
credits = pd.read_csv('tmdb_5000_credits.csv')

# merge credits to movies
movies = movies.merge(credits, on='title')

#EDA
movies = movies[['movie_id', 'title', 'overview', 'genres', 'keywords','cast','crew']]
movies.dropna(inplace=True)
movies.duplicated().sum()

# 
movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)
movies['cast'] = movies['cast'].apply(convert_cast)
movies['overview'] = movies['overview'].apply(lambda x:x.split())
movies['crew'] = movies['crew'].apply(fetch_director)

# concadenate strings
movies['keywords'] = movies['keywords'].apply(lambda x:[i.replace(" ", "") for i in x])
movies['genres'] = movies['genres'].apply(lambda x:[i.replace(" ", "") for i in x])
movies['cast'] = movies['cast'].apply(lambda x:[i.replace(" ", "") for i in x])
movies['crew'] = movies['crew'].apply(lambda x:[i.replace(" ", "") for i in x])

# create a tags field
movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

# new dateframe to train model
new_df = movies[['movie_id', 'title', 'tags']]
new_df['tags'] = new_df['tags'].apply(lambda x:" ".join(x))
new_df['tags'] = new_df['tags'].apply(lambda x:x.lower())

# vectorization
vectors = convert_tags(new_df['tags'])

# get similarity by cosin
similarity = get_similarity(vectors)

# stem tags
new_df['tags'] = new_df['tags'].apply(stem)


def recommend_me(movie):
    """ return similar movies """
    movie_index = new_df[new_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]
    similar_movies = []
    for movie in movies_list:
        movie_title = new_df.iloc[movie[0]].title
        similar_movies.append(movie_title)
    return similar_movies

def all_movies():
    """return just 15 movies in json format"""
    return convert_movies(new_df['title'][:15])

