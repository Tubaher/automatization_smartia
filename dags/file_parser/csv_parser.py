import logging
import pandas as pd

from file_parser.file_parser import FileParser

class CSVParser(FileParser):
    def __init__(self, metainfo):
        super().__init__(metainfo)

    
    def file_processing(self, path_file):
        #TODO: ver como cargar un csv en un data frame
        # considerar todos los casos

        return None
