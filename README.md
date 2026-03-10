# 🎬 Hybrid Recommender System  
### Production-Ready AI Recommendation Platform

An end-to-end hybrid recommendation system that combines **Collaborative Filtering** and **Transformer-based Content Embeddings** to deliver personalized movie recommendations with cold-start handling and a full-stack deployment.

---

## 🚀 Live Demo
- 🌐 Backend API: _Coming Soon (Render Deployment)_
- 🎨 Streamlit App: _Coming Soon_

---

## 🧠 Problem Statement

Modern streaming and e-commerce platforms must:

- Recommend items based on user behavior  
- Personalize suggestions over time  
- Handle **new users** (cold start)  
- Handle **new items**  
- Deliver results through scalable APIs  

This project solves all of the above using a hybrid ML architecture.

---

## 🏗️ System Architecture


User Activity → Feature Engineering →
├── Collaborative Filtering (Matrix Factorization)
├── Content-Based Filtering (Transformer Embeddings)
↓
Hybrid Scoring (Weighted Ranking)
↓
Top-N Recommendations
↓
FastAPI Backend
↓
Streamlit UI


---

## ✨ Key Features

### 🧠 Machine Learning
- Hybrid Recommender (CF + Embeddings)
- Transformer-based semantic embeddings
- User profile vectorization
- Matrix factorization (SVD)
- Precision@K evaluation
- Hyperparameter tuning (alpha optimization)

### ❄️ Cold Start Handling
- New users → Popularity-based recommendations  
- New items → Embedding similarity  

### ⚙️ Engineering
- Modular production architecture  
- End-to-end training pipeline  
- Config-driven design  
- Custom logging & exception handling  
- Serialized model artifacts  

### 🌐 Backend (FastAPI)
- `/recommend` → Personalized recommendations  
- `/similar/{movie_id}` → Similar movies  
- `/movies` → Movie metadata  
- Swagger documentation  
- JSON API responses  

### 🎨 Frontend (Streamlit)
- Netflix-style poster grid  
- Movie search bar  
- Hover animations  
- Personalized recommendations UI  
- Similar movie discovery  
- OMDb poster integration  

---

## 🛠️ Tech Stack

### Machine Learning
- Python  
- Pandas, NumPy  
- Scikit-learn  
- Surprise (Collaborative Filtering)  
- Sentence Transformers  
- Cosine Similarity  

### Backend
- FastAPI  
- Uvicorn  

### Frontend
- Streamlit  
- Custom CSS styling  

### Deployment
- Render (Backend)  
- Streamlit Cloud (Frontend)  
- GitHub  

---

## 📂 Project Structure


hybrid-product-recommender/
│
├── src/
│ ├── components/
│ │ ├── collaborative.py
│ │ ├── embeddings.py
│ │ ├── hybrid.py
│ │ ├── cold_start.py
│ │ └── ...
│ │
│ ├── pipeline/
│ │ └── training_pipeline.py
│ │
│ ├── api/
│ │ ├── main.py
│ │ └── schemas.py
│ │
│ └── ui/
│ └── streamlit_app.py
│
├── models/ # Trained artifacts
├── data/ # Raw datasets (gitignored)
├── logs/
├── requirements.txt
└── README.md


---

## ⚙️ Setup & Run Locally

### 1️⃣ Clone Repository
```bash
git clone https://github.com/YOUR_USERNAME/hybrid-recommender-system.git
cd hybrid-recommender-system
2️⃣ Create Virtual Environment
python -m venv myvenv
myvenv\Scripts\activate
3️⃣ Install Dependencies
pip install -r requirements.txt
🧪 Run Backend API
uvicorn src.api.main:app --reload

📘 API Docs:
http://127.0.0.1:8000/docs

🎨 Run Streamlit UI
streamlit run src/ui/streamlit_app.py
🧪 Example API Request
POST /recommend
{
  "user_id": 10,
  "top_n": 5
}
📊 Model Evaluation
Metric	Score
Precision@K	0.0705
Best Alpha	0.7

Optimized via grid-search hyperparameter tuning.

📦 Deployment Strategy
🧪 Training Environment

Uses full dataset

Generates model artifacts

🚀 Production Environment

Loads serialized models only

No raw dataset required

Lightweight & scalable

💼 Resume Highlights

Built hybrid recommender combining collaborative filtering and transformer embeddings

Implemented cold-start handling for users and items

Designed modular ML pipeline with evaluation and hyperparameter tuning

Deployed production-ready FastAPI backend and interactive Streamlit frontend

🔮 Future Improvements

User authentication

Watch history tracking

Real-time feedback loop

Vector database integration

Cloud-native scaling

👨‍💻 Author

Sarvesh Chhabra