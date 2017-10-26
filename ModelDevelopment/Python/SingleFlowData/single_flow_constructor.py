__all__ = ['single_flow_constructor']
__author__ = "Peter Herman"
__project__ = "GE-Gravity.ModelDevelopment.Python.SingleFlowData"
__created__ = "10-23-2017"
__altered__ = "10-26-2017"
__version__ = "1.0.0"

import time

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
    proc_time = time.time()
    imports_request_url = get_data_query_constructor(years=data_request.years,
                                                     reporters=data_request.importers,
                                                     partners=data_request.exporters,
                                                     data_source=data_request.source,
                                                     aggregation=data_request.aggregation,
                                                     file_format=data_request.file_format,
                                                     flow_type='imports',
                                                     iso3='True',
                                                     reporter_iso3='True',
                                                     partner_iso3='True',
                                                     names='False',
                                                     reporter_names='False',
                                                     partner_names='False',
                                                     gtap_regions='False',
                                                     quantity='False',
                                                     descriptions='False',
                                                     cost_basis='True',
                                                     trade_flow='False',
                                                     source='False'
                                                     )
    print(imports_request_url)
    exports_request_url = get_data_query_constructor(years=data_request.years,
                                                     reporters=data_request.exporters,
                                                     partners=data_request.importers,
                                                     data_source=data_request.source,
                                                     aggregation=data_request.aggregation,
                                                     file_format=data_request.file_format,
                                                     flow_type='exports',
                                                     iso3='True',
                                                     reporter_iso3='True',
                                                     partner_iso3='True',
                                                     names='False',
                                                     reporter_names='False',
                                                     partner_names='False',
                                                     gtap_regions='False',
                                                     quantity='False',
                                                     descriptions='False',
                                                     cost_basis='True',
                                                     trade_flow='False',
                                                     source='False'
                                                     )
    print(exports_request_url)
    proc_time = time.time()
    print("Imports request sent to API:  " + time.strftime('%I:%M:%p %Z on %b %d, %Y'))
    imports_data = pd.read_json(imports_request_url)
    print("Imports request returned:  " + time.strftime('%I:%M:%p  on %b %d, %Y') + ".   Total time elapsed: " + str(
        (time.time() - proc_time) / 60) + " minutes")
    print("Exports request sent to API:  " + time.strftime('%I:%M:%p %Z on %b %d, %Y'))
    exports_data = pd.read_json(exports_request_url)
    print("Exports request returned:  " + time.strftime('%I:%M:%p  on %b %d, %Y') + ".   Total time elapsed: " + str(
        (time.time() - proc_time) / 60) + " minutes")
    print("Merging data....")

    unneeded_columns = ['aggregation']
    imports_data.drop(unneeded_columns, inplace=True, axis=1)
    exports_data.drop(unneeded_columns, inplace=True, axis=1)

    imports_data.rename(columns={'reporterIso3': 'importer', 'partnerIso3': 'exporter',
                                 'costBasis': 'costBasis_imports',
                                 'tradeValue': 'trade_value_imports'}, inplace=True)
    exports_data.rename(columns={'reporterIso3': 'exporter', 'partnerIso3': 'importer',
                                 'costBasis': 'costBasis_exports',
                                 'tradeValue': 'trade_value_exports'}, inplace=True)

    merged_data = imports_data.merge(exports_data, how='outer', on=('importer', 'exporter', 'year', 'productCode'))
    merged_data['trade_value_exports_temp'] = merged_data['trade_value_exports']
    merged_data['trade_value_imports_temp'] = merged_data['trade_value_imports']
    merged_data['trade_value_exports_temp'].fillna(merged_data['trade_value_imports'], inplace=True)
    merged_data['trade_value_imports_temp'].fillna(merged_data['trade_value_exports'], inplace=True)
    merged_data['single_flow'] = (merged_data['trade_value_exports_temp'] + merged_data['trade_value_imports_temp']) / 2
    del merged_data['trade_value_exports_temp']
    del merged_data['trade_value_imports_temp']
    print("Data merged:  " + time.strftime('%I:%M:%p  on %b %d, %Y') + ".   Total time elapsed: " + str(
        (time.time() - proc_time) / 60) + " minutes")

    return merged_data
