from src.exceptions.custom_exception import CustomException
from src.logging.logger import logger
from src.constants.config import ALPHA
from sklearn.metrics.pairwise import cosine_similarity
from src.components.collaborative import CollaborativeFiltering
import numpy as np
import sys


class HybridRecommender:
    """
    Combines collaborative filtering and embedding similarity
    """

    def minmax_normalize(self,scores):

        """
        Normalize scores to range [0,1]
        """

        try:

            scores = np.array(scores)

            return (scores - scores.min()) / (scores.max() - scores.min() + 1e-8)

        except Exception as e:
            logger.error('Error normalizing scores')
            raise CustomException(e,sys)


    def compute_embeddings_scores(self,user_vector,item_embedddings):
        """
        Cosine similarity between user and all items
        """

        try:

            sims = cosine_similarity([user_vector],item_embedddings)[0]
            return sims

        except Exception as e:
            logger.error('Error computing embeddings similarity')
            raise CustomException(e,sys)


    def combine_scores(self,cf_scores,emb_scores,alpha = ALPHA):
        """
        Hybrid weighted scoring
        """
        try:

            cf_scores = self.minmax_normalize(cf_scores)
            emb_scores = self.minmax_normalize(emb_scores)

            final_scores = alpha * cf_scores + (1 - alpha) * emb_scores

            return final_scores

        except Exception as e:
            logger.error('Error combining hybrid scores')
            raise CustomException(e,sys)

    def recommend(
        self,
        user_id,
        user_embeddings,
        item_embedddings,
        movie_meta,
        cf_model,
        cf_component:CollaborativeFiltering,
        top_n=10):
        """
        Generate hybrid recommendations
        """
        try:

            if user_id not in user_embeddings:
                logger.warning(f'Cold start user : {user_id}')
                return None
            
            user_vector = user_embeddings[user_id]

            #Embedding similarity
            emb_scores = self.compute_embeddings_scores(user_vector,item_embedddings)

            # Collabortive filtering scores
            cf_scores = cf_component.get_cf_scores(
                user_id,
                movie_meta['movieId'].values,
                cf_model
            )

            # Hybrid Score
            final_scores = self.combine_scores(cf_scores,emb_scores)

            # Rank movies
            top_indices = np.argsort(final_scores)[-top_n:][::-1]

            recs = movie_meta.iloc[top_indices].copy()

            recs['hybrid_scores'] = final_scores[top_indices]

            logger.info('Recommendations generated')

            return recs


        except Exception as e:
            logger.error('Error generating hybrid recommendations')
            raise CustomException(e,sys)