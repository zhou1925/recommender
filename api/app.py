from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from api.recommenderv2 import recommend_me, all_movies

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/movies/')
async def getMovielist():
    """ return movies list """
    movies = all_movies()
    return {'movies': movies}

@app.get('/recommender/{movie}/')
async def recommender(movie: str):
    """ recommender system """
    movies = recommend_me(movie)
    return {'movies': movies}
