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
```

## Database Setup

Data ingestion reads MySQL settings from environment variables or a `.env` file
in the project root. Set the following values, replacing the password with the
password for your MySQL account:

```dotenv
DB_USER=root
DB_PASSWORD=your_actual_mysql_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=ecommerce_db
```

The configured MySQL account must be allowed to connect from `localhost`, and
the database must contain the `online_retail_ii` table. Do not commit `.env`;
it is ignored by Git.