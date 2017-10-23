import requests
from get_data_query_builder import *

imports_request_url = get_data_query_builder(years = (2013,2014,2015),
                                            reporters = ("USA","CAN","MEX"),
                                            partners = ("USA", "CAN", "MEX"),
                                            source = 'comtrade',
                                            aggregation = 'hs2',
                                            file_format = 'json',
                                            flow_type = 'imports')

exports_request_url = get_data_query_builder(years = (2013,2014,2015),
                                            reporters = ("USA","CAN","MEX"),
                                            partners = ("USA", "CAN", "MEX"),
                                            source = 'comtrade',
                                            aggregation = 'hs2',
                                            file_format = 'json',
                                             flow_type = 'exports')



response_imports = requests.get(imports_request_url)
response_exports = requests.get(exports_request_url)

imports_data = response_imports.json()
type(imports_data[1])
imports_data[1]



def rekey_comtrade(dict_list, old_key, new_key):
    for key in range(len(dict_list)):
        dict_list[key][new_key] = dict_list.pop[key](old_key)


temp = rekey_comtrade(imports_data, 'reporter', 'importer')

imports_data[1]['reporterIso3']