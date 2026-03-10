from src.exceptions.custom_exception import CustomException
from src.logging.logger import logger
from src.constants.config import EMBEDDING_MODEL
from sentence_transformers import SentenceTransformer
import pickle
import os
import sys


class EmbeddingGenerator:
    """
    Generates and saves item embeddings using transformer models
    """

    def __init__(self):

        self.model_name = EMBEDDING_MODEL
    
    def load_model(self):

        try:

            """
            Load sentence transformer model
            """
            logger.info('Loading embedding model')

            model = SentenceTransformer(self.model_name)

            logger.info('Embedding model loaded')

            return model

        except Exception as e:

            logger.error('Error loading embedding model')

            raise CustomException(e,sys)


    def create_item_embedding(self,movies):
        
        """
        Generate embeddings for movies
        
        Args:
            movies (DataFrame): Movies dataframe with combined_text
            
        Returns:
            numpy array: Item embeddings
        """

        try:

            logger.info('Generating item embeddings')

            model = self.load_model()

            texts = movies['combined_text'].tolist()

            embeddings = model.encode(
                texts,
                show_progress_bar = True,
                normalize_embeddings = True
            )

            logger.info('Item embeddings generated')

            return embeddings

        except Exception as e:

            logger.error('Error occur during generating embeddings')

            raise CustomException(e,sys)


    def save_embeddings(self,embeddings,file_path):
        """
        Save embeddings to disk
        """

        try:

            os.makedirs(os.path.dirname(file_path),exist_ok=True)

            with open(file_path,'wb') as file_obj:
                pickle.dump(embeddings,file_obj)

            logger.error(f'Embeddings saved at {file_path}')

        except Exception as e:

            raise CustomException(e,sys)

    
    
    


    