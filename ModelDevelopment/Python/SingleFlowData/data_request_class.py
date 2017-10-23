__author__ = "Peter Herman"
__project__ = "GE-Gravity.ModelDevelopment.Python.SingleFlowData"
__created__ = "10-23-2017"
__altered__ = "10-23-2017"
__version__ = "1.0.0"

from typing import List

class single_flow_data_request(object):
    def __init__(self,
                 importers: List,
                 exporters: List,
                 source: str = 'comtrade',
                 frequency: str = 'annual',
                 nomenclature: str = "HS6",
                 file_format: str = 'json',
                 iso3: str = 'True',
                 aggregation: str = ""
                 ):
        self.importers = importers
        self.exporters = exporters
        self.source = source
        self.frequency = frequency
        self.nomenclature = nomenclature
        self.file_format = file_format
        self.iso3 = iso3
        self.aggregation = aggregation

