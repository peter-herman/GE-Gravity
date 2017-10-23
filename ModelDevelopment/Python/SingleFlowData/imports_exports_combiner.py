import pandas as pd
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





type(response_imports.text)

imports_data = pd.read_json(imports_request_url)
exports_data = pd.read_json(exports_request_url)

imports_data.rename(columns = {'reporterIso3':'importer', 'partnerIso3':'exporter',
                               'costBasis': 'costBasis_imports', 'tradeFlow':'trade_flow_imports',
                               'tradeValue':'trade_value_imports'}, inplace = True)
exports_data.rename(columns = {'reporterIso3':'exporter', 'partnerIso3':'importer',
                               'costBasis': 'costBasis_exports',
                               'tradeFlow':'trade_flow_exports',
                               'tradeValue': 'trade_value_exports'}, inplace = True)

merged_data = imports_data.merge(exports_data, how = 'outer', on = ('importer', 'exporter', 'year', 'productCode'))
merged_data['trade_value_exports'].fillna(merged_data['trade_value_imports'], inplace = True)
merged_data['trade_value_imports'].fillna(merged_data['trade_value_exports'], inplace = True)
merged_data['single_flow'] = (merged_data['trade_value_exports'] + merged_data['trade_value_imports'])/2


