from src.exceptions.custom_exception import CustomException
from src.logging.logger import logger
from src.components.data_loader import DataLoader
from src.components.preprocessing import Preprocessing
from src.components.embeddings import EmbeddingGenerator
from src.components.user_profiles import UserProfile
from src.components.collaborative import CollaborativeFiltering
from src.components.hybrid import HybridRecommender
from src.components.evaluation import Evaluator
from src.components.cold_start import ColdStartHandler
import numpy as np

from src.constants.config import (EMBEDDING_MODEL,
                                    MODEL_PATH,
                                    Ratings_Path,
                                    Movies_Path,
                                    Item_Embeddings_File_Path,
                                    User_Embeddings_File_Path,
                                    Movie_Meta_File_Path,
                                    CF_Model_File_Path,
                                    Popular_Movies_File)

from sklearn.model_selection import train_test_split
import pickle
import os
import sys

print("TRAINING PIPELINE ENTRY FILE RUNNING")

class TrainingPipeline:
    """
    End-to-end training pipeline for hybrid recommender
    """
    def __init__(self):
        self.ratings_path = Ratings_Path
        self.movies_path = Movies_Path
        self.model_dir = MODEL_PATH
        self.item_embeddings_path = Item_Embeddings_File_Path
        self.user_embeddings_path = User_Embeddings_File_Path
        self.movie_meta_path = Movie_Meta_File_Path
        self.cf_model_path = CF_Model_File_Path
        self.popular_movies_file = Popular_Movies_File

    def run(self):

        try:

            logger.info('Training Pipeline Started')

            #Load Data
            loader = DataLoader(self.ratings_path,self.movies_path)
            ratings,movies = loader.load_data()

            #Preprocessing
            pre = Preprocessing()
            movies = pre.clean_movies(movies)
            
            # Train/Test Split
            train_ratings,test_ratings = train_test_split(
                ratings,
                test_size=0.2,
                random_state=42
            )

            #Embeddings
            embedder = EmbeddingGenerator()
            item_embeddings = embedder.create_item_embedding(movies)
            embedder.save_embeddings(item_embeddings,os.path.join(self.model_dir,self.item_embeddings_path))

            #Save movies metadata
            movie_meta = movies[['movieId','clean_title','genres']]
            with open(os.path.join(self.model_dir,self.movie_meta_path),'wb') as f:
                pickle.dump(movie_meta,f)

            #User Embeddings
            profiler = UserProfile()
            movie_index = profiler.build_movie_index(movie_meta['movieId'])
            user_embeddings = profiler.build_all_user_embeddings(
                train_ratings,
                item_embeddings,
                movie_index
            )
            profiler.save_user_embeddings(user_embeddings,os.path.join(self.model_dir,self.user_embeddings_path))

            #Collaborative Filtering
            cf = CollaborativeFiltering()
            cf_model = cf.train_model(train_ratings)
            cf.save_model(cf_model,os.path.join(self.model_dir,self.cf_model_path))

            #Hybrid Recommender
            evaluator = Evaluator()

            alpha_values = [0.5,0.6,0.7,0.8,0.9]
            best_score = 0
            best_alpha = None

            for alpha in alpha_values:
                logger.info(f'Evaluating for alpha = {alpha}')

                hybrid = HybridRecommender(alpha=alpha)

                score = evaluator.evaluate_model(
                recommender=hybrid,
                train_ratings=train_ratings,
                test_ratings=test_ratings,
                movie_meta=movie_meta,
                user_embeddings=user_embeddings,
                item_embeddings=item_embeddings,
                cf_model=cf_model,
                cf_component=cf
                )
                print(f"Alpha={alpha} → Precision@K={score:.4f}")

                if score > best_score:
                    best_score = score
                    best_alpha = alpha

            logger.info(f"Best Alpha: {best_alpha} | Best Precision@K: {best_score:.4f}")
            print(f"\n🏆 Best Alpha={best_alpha} | Precision@K={best_score:.4f}")


            popular = (
                ratings.groupby('movieId')
                .agg(
                    avg_rating=('rating','mean'),
                    rating_count=('rating','count')
                )
                .reset_index()
            )

            popular['score'] = popular['avg_rating'] * np.log1p(popular['rating_count'])
            popular = popular.sort_values(by='score', ascending=False)

            with open(os.path.join(self.model_dir, self.popular_movies_file), "wb") as f:
                pickle.dump(popular, f)


        except Exception as e:
            logger.error('Training pipeline failed')
            raise CustomException(e,sys)



if __name__ == '__main__':
    pipeline = TrainingPipeline()
    pipeline.run()
