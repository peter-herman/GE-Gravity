__author__ = "Peter Herman"
__project__ = "GE-Gravity.ModelDevelopment.Python.SingleFlowData"
__created__ = "10-24-2017"
__altered__ = "10-24-2017"
__version__ = "1.0.0"

"""
Example for how to request data and construct a single flow column
"""
from ModelDevelopment.Python.SingleFlowData.data_request_class import single_flow_data_request
from ModelDevelopment.Python.SingleFlowData.single_flow_constructor import single_flow_constructor



request_africa = single_flow_data_request(years=[2013, 2014, 2015],
                                        importers=["all"],
                                        exporters=["all"],
                                        source='comtrade',
                                        aggregation='hs2',
                                        file_format='json')

africa_data = single_flow_constructor(request_africa)

africa_data.to_csv("\\\\hq-fs-1.cloudnet.usitc.gov\\FS Econ only\\data\\Gravity Resources\\Data\\Africa Data\\africa_comtrade_data_single_flow.csv", index = False)