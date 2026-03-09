from src.exceptions.custom_exception import CustomException
from src.logging.logger import logger
from sklearn.metrics.pairwise import cosine_similarity
from constants.config import TOP_K
import numpy as np 
import sys


class ColdStartHandler:
    """
    Handles cold-start scenarios
    """

    def recommend_new_user(self,rating_df,movie_meta,top_n=TOP_K):
        """
        Recommend popular movies for new users
        """

        try:

            logger.info('Generating popularity-based recommendations')

            popular = (
                rating_df.groupby('movieId').agg(avg_rating=('rating','mean'),
                rating_count = ('rating','count').reset_index())
                
            )
            popular = popular[popular['rating_count']>50]

            popular['score'] = (
                popular['avg_rating'] * np.log1p(popular['rating_count'])
            )

            popular = popular.sort_values(by='score',ascending=False)

            top_ids = popular['movieId'].values[:top_n]
            recs = movie_meta[movie_meta['movieId'].isin(top_ids)]

            return recs


        except Exception as e:
            logger.error('Error generating new user recommendations')

    def similar_movies(self,movie_id,movie_index,item_embedddings,movie_meta,top_n=TOP_K):
        """
        Recommend similar movies for new items
        """
        try:
            if movie_id not in movie_index:
                logger.warning('Movie ID not found')
                return None
            
            idx = movie_index[movie_id]

            sims = cosine_similarity(
                [item_embedddings[idx]],
                item_embedddings
            )[0]

            top_indices = np.argsort(sims)[-top_n-1:][::-1]

            recs = movie_meta.iloc[top_indices]
            recs = recs[recs['movieId']!=movie_id]

            return recs.head(top_n)


        except Exception as e:
            logger.error('Error finding similar movies')
            raise CustomException(e,sys)

  