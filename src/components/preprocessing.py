from src.logging.logger import logger
from src.exceptions.custom_exception import CustomException
import sys
import pandas as pd


class Preprocessing:

    """
    Handles data cleaning and feature engineering
    """

    def clean_movies(self,movies:pd.DataFrame) -> pd.DataFrame:

        try:
            """
        Clean movie titles and prepare combined text
        
        Args:
            movies (DataFrame): Raw movies dataframe
            
        Returns:
            DataFrame: Processed movies dataframe
        """

            logger.info("Movies preprocessing started")

            movies = movies.copy()

            # Remove year from title
            movies['clean_title'] = movies['title'].str.replace(r"\(\d{4}\)", "", regex=True).str.strip()

            # Replace pipe with space in genres
            movies['genres'] = movies['genres'].str.replace('|', ' ', regex=False)

            # Combine text for embeddings
            movies['combined_text'] = movies['clean_title'] + ' ' + movies['genres']

            logger.info("Movies preprocessing completed")

            return movies

        
        except Exception as e:

            logger.error('Error during preprocessing')

            raise CustomException(e,sys)

       
