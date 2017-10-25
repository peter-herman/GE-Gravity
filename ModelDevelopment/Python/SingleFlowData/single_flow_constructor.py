__all__ = ['single_flow_constructor']
__author__ = "Peter Herman"
__project__ = "GE-Gravity.ModelDevelopment.Python.SingleFlowData"
__created__ = "10-23-2017"
__altered__ = "10-23-2017"
__version__ = "1.0.0"

import pandas as pd

from ModelDevelopment.Python.SingleFlowData.get_data_query_constructor import get_data_query_constructor


def single_flow_constructor(data_request: object):
    """
    A function that accepts a request for data and returns a pandas data fram given the parameters of the request.  The
    returned data provides reported imports, exports, and a single flow measure equal to the average of reported imports and exports.
    In the case of missing imports or exports, the single flow value equal to whichever flow is not missing.
    :param data_request: A ''single_flow_data_request'' object that specifies the parameters of the data to pull.
    :return: a pandas data frame
    """

    imports_request_url = get_data_query_constructor(years=data_request.years,
                                                     reporters=data_request.importers,
                                                     partners=data_request.exporters,
                                                     source=data_request.source,
                                                     aggregation=data_request.aggregation,
                                                     file_format=data_request.file_format,
                                                     flow_type='imports')
    print(imports_request_url)
    exports_request_url = get_data_query_constructor(years=data_request.years,
                                                     reporters=data_request.exporters,
                                                     partners=data_request.importers,
                                                     source=data_request.source,
                                                     aggregation=data_request.aggregation,
                                                     file_format=data_request.file_format,
                                                     flow_type='exports')
    print(exports_request_url)
    imports_data = pd.read_json(imports_request_url)
    exports_data = pd.read_json(exports_request_url)

    imports_data.rename(columns={'reporterIso3': 'importer', 'partnerIso3': 'exporter',
                                 'costBasis': 'costBasis_imports', 'tradeFlow': 'trade_flow_imports',
                                 'tradeValue': 'trade_value_imports'}, inplace=True)
    exports_data.rename(columns={'reporterIso3': 'exporter', 'partnerIso3': 'importer',
                                 'costBasis': 'costBasis_exports',
                                 'tradeFlow': 'trade_flow_exports',
                                 'tradeValue': 'trade_value_exports'}, inplace=True)

    merged_data = imports_data.merge(exports_data, how='outer', on=('importer', 'exporter', 'year', 'productCode'))
    merged_data['trade_value_exports_temp'] = merged_data['trade_value_exports']
    merged_data['trade_value_imports_temp'] = merged_data['trade_value_imports']
    merged_data['trade_value_exports_temp'].fillna(merged_data['trade_value_imports'], inplace=True)
    merged_data['trade_value_imports_temp'].fillna(merged_data['trade_value_exports'], inplace=True)
    merged_data['single_flow'] = (merged_data['trade_value_exports_temp'] + merged_data['trade_value_imports_temp']) / 2
    del merged_data['trade_value_exports_temp']
    del merged_data['trade_value_imports_temp']

    return merged_data
