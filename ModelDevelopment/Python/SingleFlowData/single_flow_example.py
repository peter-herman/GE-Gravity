



from ModelDevelopment.Python.SingleFlowData.data_request_class import single_flow_data_request
from ModelDevelopment.Python.SingleFlowData.single_flow_constructor import single_flow_constructor

request_test = single_flow_data_request(years = (2013,2014,2015),
                                            importers = ("USA","CAN","MEX"),
                                            exporters = ("USA", "CAN", "MEX"),
                                            source = 'comtrade',
                                            aggregation = 'hs2',
                                            file_format = 'json')

single_flow_test = single_flow_constructor(request_test)