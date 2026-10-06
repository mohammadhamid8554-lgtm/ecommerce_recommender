import os
import sys
import pickle
from src.exception import CustomException

def save_object(file_path: str, obj: object) -> None:
    """
    Saves any Python object (e.g., TF-IDF model, Scaler, Classifier) as a .pkl file.
    """
    try:
        # Extract folder directory from path (e.g., "artifacts/model.pkl" -> "artifacts")
        dir_path = os.path.dirname(file_path)

        # Ensure directory exists on disk
        os.makedirs(dir_path, exist_ok=True)

        # Open file in Write-Binary mode ("wb") and dump the object
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)

    except Exception as e:
        raise CustomException(e, sys)

def load_object(file_path: str) -> object:
    """
    Loads a serialized .pkl object from disk back into RAM.
    """
    try:
        # Open file in Read-Binary mode ("rb") and load the object
        with open(file_path, "rb") as file_obj:
            return pickle.load(file_obj)

    except Exception as e:
        raise CustomException(e, sys)