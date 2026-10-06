import logging
import os
from datetime import datetime

# 1. Generate a timestamped filename so every run creates its own unique log file
# Example output: "10_06_2026_13_05_30.log"
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# 2. Build absolute path to a 'logs' folder inside your project directory
logs_path = os.path.join(os.getcwd(), "logs")

# 3. Create the 'logs/' folder if it does not already exist
os.makedirs(logs_path, exist_ok=True)

# 4. Join folder path and filename -> "logs/10_06_2026_13_05_30.log"
LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)

# 5. Configure Python's built-in logging system
logging.basicConfig(
    filename=LOG_FILE_PATH,
    # Format pattern: [Timestamp] LineNum Module - Level - Message
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO, # Capture INFO, WARNING, ERROR, and CRITICAL logs
)