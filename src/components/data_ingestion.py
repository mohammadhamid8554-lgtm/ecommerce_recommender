import os
import sys
from dataclasses import dataclass
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sklearn.model_selection import train_test_split

from src.exception import CustomException
from src.logger import logging


load_dotenv()


@dataclass
class DataIngestionConfig:
    raw_data_path: str = os.path.join("artifacts", "raw.csv")
    train_data_path: str = os.path.join("artifacts", "train.csv")
    test_data_path: str = os.path.join("artifacts", "test.csv")

    # MySQL connection configuration
    db_user: str = os.getenv("DB_USER", "root")
    db_password: str | None = os.getenv("DB_PASSWORD")
    db_host: str = os.getenv("DB_HOST", "localhost")
    db_port: int = int(os.getenv("DB_PORT", "3306"))
    db_name: str = os.getenv("DB_NAME", "ecommerce_db")


class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Initiating MySQL Data Ingestion process...")
        try:
            db_password = self.ingestion_config.db_password
            if not db_password or db_password == "DB_PASSWORD":
                raise ValueError(
                    "Set DB_PASSWORD to your MySQL password in the environment "
                    "or in the project .env file."
                )

            connection_url = URL.create(
                drivername="mysql+pymysql",
                username=self.ingestion_config.db_user,
                password=db_password,
                host=self.ingestion_config.db_host,
                port=self.ingestion_config.db_port,
                database=self.ingestion_config.db_name,
            )

            logging.info("Connecting to MySQL database...")
            engine = create_engine(connection_url)

            # 2. Query transactional data from MySQL
            query = "SELECT * FROM churn_data"
            df = pd.read_sql(query, con=engine)
            logging.info(f"Query successful. Extracted dataframe with shape: {df.shape}")

            # 3. Create artifacts directory if it doesn't exist
            os.makedirs(
                os.path.dirname(self.ingestion_config.raw_data_path),
                exist_ok=True
            )

            # 4. Save raw dataset to artifacts
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)
            logging.info(f"Raw data saved to {self.ingestion_config.raw_data_path}")

            # 5. Perform Train-Test Split (80/20)
            logging.info("Initiating train-test split (80/20)...")
            train_set, test_set = train_test_split(
                df, test_size=0.2, random_state=42
            )

            # 6. Save train and test sets to artifacts
            train_set.to_csv(
                self.ingestion_config.train_data_path, index=False, header=True
            )
            test_set.to_csv(
                self.ingestion_config.test_data_path, index=False, header=True
            )
            logging.info("Train and test CSV files successfully written to artifacts.")

            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path,
            )

        except Exception as e:
            raise CustomException(e, sys)


if __name__ == "__main__":
    obj = DataIngestion()
    train_data, test_data = obj.initiate_data_ingestion()
    print(f"Data ingestion completed.\nTrain path: {train_data}\nTest path: {test_data}")