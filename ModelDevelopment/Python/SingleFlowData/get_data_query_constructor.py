__all__ = ['get_data_query_constructor']
__author__ = "Peter Herman"
__project__ = "GE-Gravity.ModelDevelopment.Python.SingleFlowData"
__created__ = "10-23-2017"
__altered__ = "10-26-2017"
__version__ = "1.0.0"

from typing import List


def get_data_query_constructor(years: List,
                               reporters: List = ["all"],
                               partners: List = ["all"],
                               data_source: str = 'comtrade',
                               flow_type: str = "imports",
                               frequency: str = "annual",
                               nomenclature: str = "HS6",
                               file_format: str = 'csv',
                               aggregation: str = "",
                               iso3: str = 'True',
                               reporter_iso3: str = 'True',
                               partner_iso3: str = 'True',
                               names: str = 'False',
                               reporter_names: str = 'False',
                               partner_names: str = 'False',
                               gtap_regions: str = 'False',
                               quantity: str = 'False',
                               descriptions: str = 'False',
                               cost_basis: str = 'False',
                               trade_flow: str = 'False',
                               source: str = 'False',
                               ):
    """
    Function that constructs a request url for the USITC data API from inputted specifications.
    :param years: A list of years. e.g. [2013, 2014, 2015]
    :param reporters: A list of reporter iso3's or "all" for all available countries. (e.g. reporters=["CAN", "MEX", "USA"])
    :param partners: A list of partner iso3's or "all" for all available countries. (e.g. partners=["CAN", "MEX", "USA"])
    :param data_source: database to draw from. i.e. 'comtrade' or 'dataweb'
    :param flow_type: 'imports' or 'exports'
    :param frequency: 'annual', *fill in other options*
    :param nomenclature: 'hs6' *fill in other options*
    :param file_format: 'csv', 'json', etc
    :param aggregation: desired level of aggregation. e.g. 'hs2', 'hs6'
    :param iso3: 'True' to return iso3s with results, 'False' otherwise.
    :param reporter_iso3: 'True' to return reporter iso3 codes.
    :param partner_iso3: 'True' to return partner iso3 codes.
    :param names: 'True' to return both reporter and partner country names.
    :param reporter_names: 'True' to return reporter country names.
    :param partner_names: 'True' to return partner country names.
    :param gtap_regions: 'True' to return gtap-region codes.
    :param quantity: 'True' to return quantities and first quantity units.
    :param descriptions: 'True' to return product descriptions.
    :param cost_basis: 'True' to return cost basis (e.g. CIF, FOB).
    :param trade_flow: 'True' to return type of flow indicator.
    :param source: 'True' to return indicator for source database.
    :return: a URL to submit to the USITC data API
    """
    if not isinstance(years, List):
        raise TypeError("years is not a list")
    if not isinstance(reporters, List):
        raise TypeError("reporters is not a list")
    if not isinstance(partners, List):
        raise TypeError("partners is not a list")
    if not isinstance(data_source, str):
        raise TypeError("source is not a string")
    if not isinstance(frequency, str):
        raise TypeError("frequency is not a string")
    if not isinstance(nomenclature, str):
        raise TypeError("nomenclature is not a string")
    if not isinstance(file_format, str):
        raise TypeError("file_format is not a string")
    if not isinstance(aggregation, str):
        raise TypeError("aggregation is not a string")

    if not (iso3 == "True" or iso3 == "False"):
        raise TypeError("iso3 must take the string value 'True' or 'False'")
    if not (reporter_iso3 == "True" or reporter_iso3 == "False"):
        raise TypeError("reporter_iso3 must take the string value 'True' or 'False'")
    if not (partner_iso3 == "True" or partner_iso3 == "False"):
        raise TypeError("partner_iso3 must take the string value 'True' or 'False'")
    if not (names == "True" or names == "False"):
        raise TypeError("names must take the string value 'True' or 'False'")
    if not (reporter_names == 'True' or reporter_names == 'False'):
        raise TypeError("reporter_names must take the string value 'True' or 'False'")
    if not (partner_names == "True" or partner_names == "False"):
        raise TypeError("partner_names must take the string value 'True' or 'False'")
    if not (gtap_regions == "True" or gtap_regions == "False"):
        raise TypeError("gtap_regions must take the string value 'True' or 'False'")
    if not (quantity == "True" or quantity == "False"):
        raise TypeError("quantity must take the string value 'True' or 'False'")
    if not (descriptions == "True" or descriptions == "False"):
        raise TypeError("descriptions must take the string value 'True' or 'False'")
    if not (cost_basis == "True" or cost_basis == "False"):
        raise TypeError("cost_basis must take the string value 'True' or 'False'")
    if not (trade_flow == "True" or trade_flow == "False"):
        raise TypeError("trade_flow must take the string value 'True' or 'False'")
    if not (source == "True" or source == "False"):
        raise TypeError("source must take the string value 'True' or 'False'")


    server_address = 'http://itcmmodel:8085/api/'

    nomenclature_str = 'country?nomenclature=' + nomenclature
    year_str = '&years=' + ",".join(map(str, years))
    if (reporters[0] == "all") or (reporters[0] == "ALL") or (reporters[0] == "All") or (reporters[0] == ""):
        reporters_str = ""
    else:
        reporters_str = '&reporters=' + ",".join(reporters)
    if (partners[0] == "all") or (partners[0] == "ALL") or (partners[0] == "All") or (partners[0] == ""):
        partners_str = ""
    else:
        partners_str = '&partners=' + ",".join(partners)

    url_out = server_address + \
              data_source + '/' + \
              flow_type + '/' + \
              frequency + '/' + \
              nomenclature_str + \
              '&format=' + file_format + \
              '&iso3=' + iso3 + \
              year_str + \
              reporters_str + \
              partners_str + \
              '&aggregation=' + aggregation + \
              '&reporter-iso3=' + reporter_iso3 + \
              '&partner-iso3=' + partner_iso3 + \
              '&names=' + names + \
              '&reporter-names=' + reporter_names + \
              '&partner-names=' + partner_names + \
              '&gtap-regions=' + gtap_regions + \
              '&quantity=' + quantity + \
              '&descriptions=' + descriptions + \
              '&cost-basis=' + cost_basis + \
              '&trade-flow=' + trade_flow + \
              '&source=' + source

    return url_out
