from pydantic import BaseModel
from typing import List


class RecommendationRequest(BaseModel):
    user_id : int
    top_n : int = 10


class MovieRecommendation(BaseModel):
    movieId : int
    title : str
    genres : str
    score : float


class RecommendationResponse(BaseModel):
    user_id : int
    recommendations : List[MovieRecommendation]