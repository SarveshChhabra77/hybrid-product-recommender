from src.logging.logger import logger
from src.exceptions.custom_exception import CustomException
import pandas as pd
import os
import sys 


class DataLoader:

    """
    Class to load ratings and movies datasets
    """

    def __init__(self,ratings_path,movies_path):
        
        self.ratings_path = ratings_path
        self.movies_path = movies_path

    def load_data(self):

        """
        Load ratings and movies CSV files
        
        Returns:
            ratings (DataFrame), movies (DataFrame)
        """

        try:
            logger.info("Loading data started")

            if not os.path.exists(self.ratings_path):
                raise FileNotFoundError(f"Ratings file not found at {self.ratings_path}")
            if not os.path.exists(self.movies_path):
                raise FileNotFoundError(f"Movies file not found at {self.movies_path}")

            ratings = pd.read_csv(self.ratings_path)
            movies = pd.read_csv(self.movies_path)

            logger.info("Data loaded successfully")

            return ratings, movies

        except Exception as e:

            raise CustomException(e,sys)



        