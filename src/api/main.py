from fastapi import FastAPI
import pickle

from src.components.hybrid import HybridRecommender
from src.components.collaborative import CollaborativeFiltering
from src.components.cold_start import ColdStartHandler
from src.api.schemas import RecommendationRequest,RecommendationResponse,MovieRecommendation
from src.constants.config import (
     Item_Embeddings_Path,User_Embeddings_Path,Movie_Meta_Path,CF_Model_Path,Popular_Movies_File_Path
)


app = FastAPI(title='Hybrid Recommender API')


with open(Item_Embeddings_Path, "rb") as f:
    item_embeddings = pickle.load(f)

with open(User_Embeddings_Path, "rb") as f:
    user_embeddings = pickle.load(f)

with open(Movie_Meta_Path, "rb") as f:
    movie_meta = pickle.load(f)

with open(CF_Model_Path, "rb") as f:
    cf_model = pickle.load(f)

with open(Popular_Movies_File_Path, "rb") as f:
    popular_movies = pickle.load(f)


cf_component = CollaborativeFiltering()
cold_start = ColdStartHandler()
hybrid = HybridRecommender(alpha=0.7)

movie_index={m:i for i,m in enumerate(movie_meta['movieId'])}

@app.get('/')
def home():
    return {'status' : 'API Running'}



@app.post('/recommend',response_model=RecommendationResponse)
def recommend(req:RecommendationRequest):

    recs = hybrid.recommend(
        user_id=req.user_id,
        user_embeddings=user_embeddings,
        item_embeddings=item_embeddings,
        movie_meta=movie_meta,
        cf_model=cf_model,
        cf_component=cf_component,
        top_n=req.top_n
    )

    if recs is None:
        top_ids = popular_movies['movieId'].values[:req.top_n]
        recs = movie_meta[movie_meta['movieId'].isin(top_ids)]
        print("Cold start recs:", type(recs))
    
    if recs is None or len(recs) == 0:
        return RecommendationResponse(
            user_id=req.user_id,
            recommendations=[]
        )

    movies = []

    for _,row in recs.iterrows():
        score = float(row['hybrid_score']) if 'hybrid_score' in row else 0.0
        movies.append(
            MovieRecommendation(
                movieId=int(row['movieId']),
                title = row['clean_title'],
                genres = row['genres'],
                score = score
            )
        )

    return RecommendationResponse(
        user_id = req.user_id,
        recommendations=movies
    )


@app.get('/similar/{movie_id}')
def similar(movie_id:int,top_n:int = 10):

    recs = cold_start.similar_movies(
        movie_id=movie_id,
        movie_index=movie_index,
        item_embeddings=item_embeddings,
        movie_meta=movie_meta,
        top_n=top_n
    )

    if recs is None:
        return {'error' : 'Movie not found'}
    
    result = []

    for _,row in recs.iterrows():
        result.append(
            {
            "movieId": int(row["movieId"]),
            "title": row["clean_title"],
            "genres": row["genres"]
            }
        )

    return {'similar_movies':result}



@app.get('/movies')
def get_movies():
    movies = movie_meta[['movieId', 'clean_title']].to_dict(orient='records')
    return {'movies' : movies}