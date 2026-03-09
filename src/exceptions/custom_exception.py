import sys


class CustomException(Exception):
    def __init__(self, error_message: str, error_detail: sys):
        super().__init__(error_message)
        self.error_message = error_message
        _,_,exc_db = error_detail.exc_info()
        self.file_name = exc_db.tb_frame.f_code.co_filename
        self.line_no = exc_db.tb_lineno
        
    def __str__(self):
        return "An error occurred on line {0} of '{1}': {2}".format(self.line_no, self.file_name, self.error_message)

