# 🛒 E-Commerce Hybrid Product Recommendation Engine

An end-to-end, production-ready recommendation system designed to boost customer conversion and average order value (AOV). This project combines **Content-Based Filtering** (TF-IDF & Cosine Similarity on product metadata) with **Collaborative Filtering** (Nearest Neighbors / Matrix Factorization on user interaction history) to deliver real-time personalized recommendations.

---

## 📌 Features & Highlights

- **Modular Architecture:** Structured standard Python package with robust logging, exception handling, and reusable utility scripts.
- **Hybrid Recommendation Logic:** Solves the cold-start problem by blending text metadata similarity with behavioral collaborative filtering.
- **REST API Integration:** High-performance, low-latency API built using **FastAPI** with Pydantic schema validation.
- **Interactive UI Dashboard:** User-friendly frontend built with **Streamlit** to showcase recommendations, confidence scores, and product metadata.

---

## 🏗️ System Architecture & Data Flow

```text
[ Raw Transaction & Product Data ]
                 │
                 ▼
     [ Data Ingestion Pipeline ]
                 │
                 ▼
  [ Data Transformation & Feature Eng. ]
   ├── TF-IDF Vectorization (Text)
   └── User-Item Matrix Creation (Behavioral)
                 │
                 ▼
      [ Hybrid Model Training ]
   ├── Cosine Similarity Matrix (Content-Based)
   └── K-Nearest Neighbors / SVD (Collaborative)
                 │
                 ▼
      [ Artifacts Serialization ]
   ├── preprocessor.pkl
   └── recommender_model.pkl
                 │
                 ▼
       [ FastAPI Serving Layer ]
                 │
                 ▼
     [ Streamlit UI Dashboard ]