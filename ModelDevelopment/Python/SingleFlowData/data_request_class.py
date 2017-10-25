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

        :param importers: A list of importer iso3's or "all" for all available countries. (e.g. importers=["CAN", "MEX", "USA"])
        :param exporters: A list of exporter iso3's or "all" for all available countries. (e.g. exporters=["CAN", "MEX", "USA"])
        :param years: a list of years e.g. [2013, 2014, 2015]
        :param source: a string specifying data source ('comtrade', 'dataweb')
        :param frequency: frequency of observation ('annual')
        :param nomenclature: product nomenclature ('hs6')
        :param file_format: file format to return ('csv', 'json')
        :param iso3: boolean for inclusion of ISO3 codes
        :param aggregation: level of aggregation ('hs2', 'hs4', 'hs6')
        """
        if not isinstance(years, List):
            raise TypeError("years is not a list")
        if not isinstance(importers, List):
            raise TypeError("importers is not a list")
        if not isinstance(exporters, List):
            raise TypeError("exporters is not a list")
        if not isinstance(source, str):
            raise TypeError("source is not a string")
        if not isinstance(frequency, str):
            raise TypeError("frequency is not a string")
        if not isinstance(nomenclature, str):
            raise TypeError("nomenclature is not a string")
        if not isinstance(file_format, str):
            raise TypeError("file_format is not a string")
        if not isinstance(iso3, str):
            raise TypeError("iso3 is not a string")
        if not isinstance(aggregation, str):
            raise TypeError("aggregation is not a string")


        self.importers = importers
        self.exporters = exporters
        self.years = years
        self.source = source
        self.frequency = frequency
        self.nomenclature = nomenclature
        self.file_format = file_format
        self.iso3 = iso3
        self.aggregation = aggregation
