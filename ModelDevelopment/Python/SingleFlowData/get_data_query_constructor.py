__all__ = ['get_data_query_constructor']
from typing import List


def get_data_query_constructor(years: List,
                               reporters: List = [""],
                               partners: List = [""],
                               source: str = 'comtrade',
                               flow_type: str = "imports",
                               frequency: str = "annual",
                               nomenclature: str = "HS6",
                               file_format: str = 'csv',
                               iso3: str = 'True',
                               aggregation: str = ""):
    """
    Function that constructs a request url for the USITC data API from inputted specifications.
    :param years: A list of years. e.g. [2013, 2014, 2015]
    :param reporters: A list of reporter iso3's or "all" for all available countries. (e.g. reporters=["CAN", "MEX", "USA"])
    :param partners: A list of partner iso3's or "all" for all available countries. (e.g. partners=["CAN", "MEX", "USA"])
    :param source: database to draw from. i.e. 'comtrade' or 'dataweb'
    :param flow_type: 'imports' or 'exports'
    :param frequency: 'annual', *fill in other options*
    :param nomenclature: 'hs6' *fill in other options*
    :param file_format: 'csv', 'json', etc
    :param iso3: 'True' to return iso3s with results, 'False' otherwise.
    :param aggregation: desired level of aggregation. e.g. 'hs2', 'hs6'
    :return: a URL to submit to the USITC data API
    """
    if not isinstance(years, List):
        raise TypeError("years is not a list")
    if not isinstance(reporters, List):
        raise TypeError("reporters is not a list")
    if not isinstance(partners, List):
        raise TypeError("partners is not a list")
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

    server_address = 'http://itcmmodel:8085/api/'

    nomenclature_str = 'country?nomenclature=' + nomenclature
    year_str = '&years=' + ",".join(map(str, years))
    if (reporters == "all") or (reporters == "ALL") or (reporters == "All") or (reporters == ""):
        reporters_str = ""
    else:
        reporters_str = '&reporters=' + ",".join(reporters)
    if (partners == "all") or (partners == "ALL") or (partners == "All") or (partners == ""):
        partners_str=""
    else:
        partners_str = '&partners=' + ",".join(partners)

    url_out = server_address + \
              source + '/' + \
              flow_type + '/' + \
              frequency + '/' + \
              nomenclature_str + \
              '&format=' + file_format + \
              '&iso3=' + iso3 + \
              year_str + \
              reporters_str + \
              partners_str + \
              '&aggregation=' + aggregation

    return url_out

