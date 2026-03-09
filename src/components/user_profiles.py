from src.exceptions.custom_exception import CustomException
from src.logging.logger import logger
import sys
import pickle
import os
import numpy as np


class UserProfile:
    """
    Creates user embeddings from rated movies
    """

    def build_movie_index(self,movie_ids):

        """
        Create mapping: movieId → embedding index
        """

        try:

            logger.info('Building movie index mapping')

            movie_index = {
                mvoie_id : idx
                for idx,movie_ids in enumerate(movie_ids)
            }

            return movie_index

        except Exception as e:

            logger.error('Error building movie index')

            raise CustomException(e,sys)


    def create_user_embeddings(self,user_id,rating_df,item_embedddings,movie_index):

        """
        Create embedding for a single user
        """

        try:

            user_ratings = rating_df[rating_df['userId']==user_id]

            if not user_ratings:
                return None
            
            vectors = []
            weights = []

            for _,row in user_ratings.iterrows():
                movie_id = row['movieId']
                rating = row['rating']

                if movie_id in movie_index:
                    idx = movie_index[movie_id]
                    vectors.append(item_embedddings[idx])
                    weights.append(rating)

            if not vectors:
                return None

            user_vector = np.average(vectors,axis=0,weights=weights)
            
            return user_vector

        except Exception as e:

            logger.error(f'Error creating embeddings for user {user_id}')

            raise CustomException(e,sys)


    def build_all_user_embeddings(self,rating_df,item_embedddings,movie_index):


        try:

            logger.info('Building user embeddings')

            user_embeddings = {}

            for user_id in rating_df['userId'].unique():

                vec = self.create_user_embeddings(
                    user_id,
                    rating_df,
                    item_embedddings,
                    movie_index
                    )

                if vec is not None:
                    user_embeddings[user_id] = vec

            logger.info('User embeddings created')

            return user_embeddings

        except Exception as e:
            logger.error('Error building user embeddings')
            raise CustomException(e,sys)


    def save_user_embeddings(self,user_embeddings,file_path):

        try:
            
            os.makedirs(os.path.dirname(file_path),exist_ok=True)

            with open(file_path,'wb') as file_obj:
                pickle.dump(user_embeddings,file_obj)

            logger.info(f'User embeddings saved at {file_path}')
            
        except Exception as e:

            logger.error('Error saving user embeddings')

            raise CustomException(e,sys)

