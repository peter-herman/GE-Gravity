__author__ = "Peter Herman"
__project__ = "GE-Gravity.ModelDevelopment.Python.SingleFlowData"
__created__ = "10-24-2017"
__altered__ = "10-26-2017"
__version__ = "1.0.0"

"""
Example for how to request data and construct a single flow column
"""
from ModelDevelopment.Python.SingleFlowData.data_request_class import single_flow_data_request
from ModelDevelopment.Python.SingleFlowData.single_flow_constructor import single_flow_constructor

output_csv_file_name = "africa_comtrade_data_single_flow_hs6agg_fewer_columns.csv"
save_location = "\\\\hq-fs-1.cloudnet.usitc.gov\\FS Econ only\\data\\Gravity Resources\\Data\\Africa Data\\"

request_africa = single_flow_data_request(years=[2013, 2014, 2015],
                                        importers=["all"],
                                        exporters=["all"],
                                        source='comtrade',
                                        aggregation='hs6',
                                        file_format='json')

africa_data = single_flow_constructor(request_africa)

africa_data.to_csv((save_location+ output_csv_file_name), index = False)