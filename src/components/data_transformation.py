import os
import sys
import pickle
from dataclasses import dataclass
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import csr_matrix

from src.exception import CustomException
from src.logger import logging


@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path: str = os.path.join("artifacts", "preprocessor.pkl")
    tfidf_matrix_path: str = os.path.join("artifacts", "tfidf_matrix.pkl")
    user_item_matrix_path: str = os.path.join("artifacts", "user_item_matrix.pkl")


class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Cleans raw transactional logs for recommendation modeling."""
        try:
            logging.info("Cleaning transaction dataset...")
            
            # 1. Drop rows missing Customer ID or Description
            df = df.dropna(subset=["Customer ID", "Description"])
            
            # 2. Remove cancellations (Invoices starting with 'C' or Quantity <= 0)
            df["Invoice"] = df["Invoice"].astype(str)
            df = df[~df["Invoice"].str.startswith("C")]
            df = df[df["Quantity"] > 0]
            
            # 3. Clean string values
            df["StockCode"] = df["StockCode"].astype(str).str.strip()
            df["Description"] = df["Description"].astype(str).str.lower().str.strip()
            df["Customer ID"] = df["Customer ID"].astype(int).astype(str)
            
            logging.info(f"Data cleaning complete. Active records: {len(df)}")
            return df

        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_transformation(self, train_path: str, test_path: str):
        try:
            logging.info("Initiating Data Transformation component...")
            
            # Read train and test files
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            # Clean datasets
            train_df = self.clean_data(train_df)
            test_df = self.clean_data(test_df)

            # --- 1. Content-Based Preprocessing (TF-IDF on Description) ---
            logging.info("Building Content-Based TF-IDF matrix...")
            unique_items = train_df[["StockCode", "Description"]].drop_duplicates("StockCode")
            
            tfidf = TfidfVectorizer(max_features=5000, stop_words="english")
            tfidf_matrix = tfidf.fit_transform(unique_items["Description"])

            # --- 2. Collaborative Filtering Preprocessing (User-Item Matrix) ---
            logging.info("Building Collaborative User-Item interaction matrix...")
            user_item_df = train_df.pivot_table(
                index="Customer ID",
                columns="StockCode",
                values="Quantity",
                aggfunc="sum",
                fill_value=0
            )
            
            user_item_matrix = csr_matrix(user_item_df.values)

            # --- 3. Save Pickled Artifacts ---
            os.makedirs(
                os.path.dirname(self.data_transformation_config.preprocessor_obj_file_path),
                exist_ok=True
            )

            # Save TF-IDF Vectorizer
            with open(self.data_transformation_config.preprocessor_obj_file_path, "wb") as f:
                pickle.dump(tfidf, f)

            # Save TF-IDF Matrix & Item Index Map
            with open(self.data_transformation_config.tfidf_matrix_path, "wb") as f:
                pickle.dump(
                    {"matrix": tfidf_matrix, "item_ids": unique_items["StockCode"].values},
                    f
                )

            # Save User-Item Matrix & Index Maps
            with open(self.data_transformation_config.user_item_matrix_path, "wb") as f:
                pickle.dump(
                    {
                        "matrix": user_item_matrix,
                        "users": user_item_df.index.values,
                        "items": user_item_df.columns.values,
                    },
                    f
                )

            logging.info("All Data Transformation artifacts successfully generated and saved.")
            return self.data_transformation_config.preprocessor_obj_file_path

        except Exception as e:
            raise CustomException(e, sys)


if __name__ == "__main__":
    from src.components.data_ingestion import DataIngestion
    
    ingestion = DataIngestion()
    train_path, test_path = ingestion.initiate_data_ingestion()
    
    transformer = DataTransformation()
    transformer.initiate_data_transformation(train_path, test_path)
    print("Data Transformation executed successfully!")