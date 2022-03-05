import ast
import json
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


ps = PorterStemmer()
cv = CountVectorizer(max_features=5000, stop_words='english')

def convert(movie):
    """return dynamic data of each movie """
    objects = []
    for obj in ast.literal_eval(movie):
        objects.append(obj['name'])
    return objects

def convert_cast(obj):
    """ return cast name != 3 """
    casts = []
    counter = 0
    for i in ast.literal_eval(obj):
        if counter != 3:
            casts.append(i['name'])
            counter += 1
        else:
            break
    return casts

def fetch_director(obj):
    """ return director of crew field """
    director = []
    for i in ast.literal_eval(obj):
        if i['job'] == 'Director':
            director.append(i['name'])
            break
    return director

def stem(text):
    """ return steam of words """
    stem_words = []
    for word in text.split():
        stem_words.append(ps.stem(word))
    return " ".join(stem_words)

def convert_tags(tag):
    """ return vectors of tags"""
    return cv.fit_transform(tag).toarray()

def get_similarity(vectors):
    """ return similarity of vectors"""
    return cosine_similarity(vectors)

def convert_movies(movies):
    """ convert title movies in json format"""
    movies = json.loads(movies.to_json(orient='records'))
    return movies


