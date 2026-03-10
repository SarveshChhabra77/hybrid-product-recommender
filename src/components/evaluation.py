from src.exceptions.custom_exception import CustomException
from src.logging.logger import logger
from src.constants.config import TOP_K,RATING_THRESHOLD
from src.components.hybrid import HybridRecommender
import numpy as np
import sys


class Evaluator:

    """
    Evaluate recommender performance
    """

    def precision_at_k(self,recommended_ids,relevant_ids,k=TOP_K):
        """
        Compute Precision@K
        
        Args:
            recommended_ids: list of recommended movie IDs
            relevant_ids: list of relevant movie IDs
            k: number of recommendations
            
        Returns:
            precision score
        """
        try:

            if len(relevant_ids) == 0:
                return None

            recommended_ids = recommended_ids[:k]
            hits = len(set(recommended_ids) & set(relevant_ids))

            return hits / k

        except Exception as e:
            logger.error('Error computing Precision@K')


    def evaluate_user(
        self,
        user_id,
        recommender:HybridRecommender,
        train_ratings,
        test_ratings,
        movie_meta,
        user_embeddings,
        item_embeddings,
        cf_model,
        cf_component
    ):
        """
            Evaluate a single user
            """

        try:

            recs = recommender.recommend(
                user_id=user_id,
                user_embeddings=user_embeddings,
                item_embeddings=item_embeddings,
                movie_meta=movie_meta,
                cf_model=cf_model,
                cf_component=cf_component,
                top_n=50
            )

            if recs is None:
                return None

            # Remove seen movies
            seen = train_ratings[train_ratings['userId']==user_id]['movieId'].values
            recs = recs[~recs['movieId'].isin(seen)]

            recommended_ids = recs['movieId'].values

            # Revelant movies
            user_test = test_ratings[test_ratings['userId']==user_id]
            relevant_ids = user_test[
                user_test['rating'] >= RATING_THRESHOLD
            ]['movieId'].values

            return self.precision_at_k(recommended_ids,relevant_ids)

        except Exception as e:
            logger.error(f'Error evaluating user : {user_id}')
            raise CustomException(e,sys)


    def evaluate_model(
        self,
        recommender:HybridRecommender,
        train_ratings,
        test_ratings,
        movie_meta,
        user_embeddings,
        item_embeddings,
        cf_model,
        cf_component
        ):
        """
        Evaluate model across all users
        """
        try:

            logger.info('Starting model evaluation')

            scores = []

            for user_id in user_embeddings.keys():
                score = self.evaluate_user(
                    user_id,
                    recommender,
                    train_ratings,
                    test_ratings,
                    movie_meta,
                    user_embeddings,
                    item_embeddings,
                    cf_model,
                    cf_component
                )
                if score is not None:
                    scores.append(score)

            mean_score = np.mean(scores) if scores else 0.0

            logger.info(f'Evaluation complete. Precision@K: {mean_score:.4f}')

            return mean_score

        except Exception as e:
            logger.error(f'Error during model evaluation')
            raise CustomException(e,sys)