from src.logging.logger import logger
from src.exceptions.custom_exception import CustomException
from surprise import Dataset,SVD,Reader
import numpy as np
import sys
import pickle
import os


class CollaborativeFiltering:
    """
    Handles collaborative filtering using SVD
    """
    def train_model(self,rating_df):
        """
        Train SVD collaborative filtering model
        """
        try:

            logger.info('Training collaborative filtering model')

            reader = Reader(rating_scale=(1,5))
            data = Dataset.load_from_df(
                rating_df[['userId', 'movieId', 'rating']],
                reader
            )

            trainset = data.build_full_trainset()

            model = SVD()
            model.fit(trainset)

            logger.info('Collaborative filtering model trained')

            return model

        except Exception as e:
            logger.error('Error training collaborative filtering')
            raise CustomException(e,sys)

    def predict_rating(self,user_id,movie_id,model):
        """
        Predict rating for a single user-movie pair
        """

        try:

            prediction = model.predict(user_id,movie_id)
            return prediction.est

        except Exception as e:
            logger.error(f'Error predicting rating for user {user_id}, movie {movie_id}')
            raise CustomException(e,sys)
   
    def get_cf_scores(self,user_id,movie_ids,model):
        """
        Get predicted ratings for all movies for a user
        """

        try:

            scores = []

            for movie_id in movie_ids:
                pred = model.predict(user_id,movie_id)
                scores.append(pred.est)

            return np.array(scores)

        except Exception as e:
            logger.error('Error generating cf score')
            raise CustomException(e,sys)


    def save_model(self,model,file_path):
        """
        Save trained CF model
        """

        try:

            os.makedirs(os.path.dirname(file_path),exist_ok=True)

            with open(file_path,'wb') as file_obj:
                pickle.dump(model,file_obj)

            logger.info(f'Cf model saved at {file_path}')

            

        except Exception as e:
            logger.error(f'Error saving Cf model')
            raise CustomException(e,sys)
    


