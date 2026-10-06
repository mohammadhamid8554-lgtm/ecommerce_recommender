import sys
from src.logger import logging

def error_message_detail(error, error_detail: sys):
    """
    Extracts the script name, line number, and error message from Python execution details.
    """
    # sys.exc_info() returns (Type, Value, Traceback)
    # We only care about the 3rd item: traceback (exc_tb)
    _, _, exc_tb = error_detail.exc_info()

    # Get filename where error occurred from the traceback frame
    file_name = exc_tb.tb_frame.f_code.co_filename

    # Format a custom detailed string
    error_message = (
        f"Error occurred in script [{file_name}] "
        f"at line number [{exc_tb.tb_lineno}] "
        f"with error message [{str(error)}]"
    )
    return error_message

class CustomException(Exception):
    def __init__(self, error_message, error_detail: sys):
        # 1. Pass raw message to parent Exception class
        super().__init__(error_message)

        # 2. Extract detailed custom error message
        self.error_message = error_message_detail(
            error_message, error_detail=error_detail
        )

    def __str__(self):
        # When print(e) or raise CustomException is called, display our custom string
        return self.error_message