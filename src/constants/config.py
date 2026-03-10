import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

DATA_DIR = os.path.join(BASE_DIR, "data")


EMBEDDING_MODEL = "all-MiniLM-L6-v2"

ALPHA = 0.7
TOP_K = 10
RATING_THRESHOLD = 3.5

DATA_PATH = "data/"
MODEL_PATH = "models/"

Ratings_Path = os.path.join(DATA_DIR, "ratings.csv")
Movies_Path =  os.path.join(DATA_DIR, "movies.csv")

Item_Embeddings_File_Path = 'item_embeddings.pkl'
User_Embeddings_File_Path = 'user_embeddings.pkl'
Movie_Meta_File_Path = 'movie_meta.pkl'
CF_Model_File_Path = 'cf_model.pkl'



Item_Embeddings_Path = os.path.join(MODEL_PATH,Item_Embeddings_File_Path)
User_Embeddings_Path = os.path.join(MODEL_PATH,User_Embeddings_File_Path)
Movie_Meta_Path = os.path.join(MODEL_PATH,Movie_Meta_File_Path)
CF_Model_Path = os.path.join(MODEL_PATH,CF_Model_File_Path)
Popular_Movies_File = 'popular_movies.pkl'
Popular_Movies_File_Path = os.path.join(MODEL_PATH,Popular_Movies_File)