__all__ = ['single_flow_constructor']
__author__ = "Peter Herman"
__project__ = "GE-Gravity.ModelDevelopment.Python.SingleFlowData"
__created__ = "10-23-2017"
__altered__ = "10-23-2017"
__version__ = "1.0.0"


import pandas as pd

from ModelDevelopment.Python.SingleFlowData.get_data_query_builder import *


def single_flow_constructor(data_request: object):

    imports_request_url = get_data_query_builder(years = data_request.years,
                                            reporters = data_request.importers,
                                            partners = data_request.exporters,
                                            source = data_request.source,
                                            aggregation = data_request.aggregation,
                                            file_format = data_request.file_format,
                                            flow_type = 'imports')

    exports_request_url = get_data_query_builder(years = data_request.years,
                                            reporters = data_request.exporters,
                                            partners = data_request.importers,
                                            source = data_request.source,
                                            aggregation = data_request.aggregation,
                                            file_format = data_request.file_format,
                                             flow_type = 'exports')







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

    return merged_data

