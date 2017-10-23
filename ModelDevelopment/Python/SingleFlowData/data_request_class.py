__all__ = ['single_flow_data_request']
__author__ = "Peter Herman"
__project__ = "GE-Gravity.ModelDevelopment.Python.SingleFlowData"
__created__ = "10-23-2017"
__altered__ = "10-23-2017"
__version__ = "1.0.0"

from typing import List


class single_flow_data_request(object):
    """
    Object for storing the specifications for a USITC data api request
    """

    def __init__(self,
                 importers: List,
                 exporters: List,
                 years: List,
                 source: str = 'comtrade',
                 frequency: str = 'annual',
                 nomenclature: str = "HS6",
                 file_format: str = 'json',
                 iso3: str = 'True',
                 aggregation: str = ""
                 ):
        """

        :param importers: a list of importer Iso3s
        :param exporters: a list of exporter Iso3s
        :param years: a list of years
        :param source: a string specifying data source ('comtrade', 'dataweb')
        :param frequency: frequency of observation ('annual')
        :param nomenclature: product nomenclature ('hs6')
        :param file_format: file format to return ('csv', 'json')
        :param iso3: boolean for inclusion of ISO3 codes
        :param aggregation: level of aggregation ('hs2', 'hs4', 'hs6')
        """
        self.importers = importers
        self.exporters = exporters
        self.years = years
        self.source = source
        self.frequency = frequency
        self.nomenclature = nomenclature
        self.file_format = file_format
        self.iso3 = iso3
        self.aggregation = aggregation
