import os
import pandas as pd


class Status_job:

    def __init__(self) -> None:
        self.status_file = 'status.txt'

    def _create_status(self):
        try:
            with open(self.status_file, 'r') as file:
                file.read()

        except FileNotFoundError:
            with open(self.status_file, 'w') as file:
                file.write(str('0'))

    def _set_status(self, status: str):
        self._create_status()

        with open(self.status_file, 'w') as file:
            file.write(str(status))

    def set_true(self):
        self._set_status('1')
    
    def set_false(self):
        self._set_status('0')

    def check_status(self):
        self._create_status()
        
        with open(self.status_file, 'r') as file:
            is_true = file.read()
            
            if is_true == "1":
                return True
            
            else:
                return False


def read_links(filename, column, excel=False):
    if excel:
        df = pd.read_excel(filename)

    else:
        df = pd.read_csv(filename)

    return df[column].tolist()

