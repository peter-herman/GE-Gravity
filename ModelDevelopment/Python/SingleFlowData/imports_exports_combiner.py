import json

import requests
from get_data_query_builder import get_data_query_builder

imports_request_url = get_data_query_builder(years = (2013,2014,2015),
                                            reporters = ("USA","CAN","MEX"),
                                            partners = ("USA", "CAN", "MEX"),
                                            source = 'comtrade',
                                            aggregation = 'hs4')


response = requests.get('http://itcmmodel:8085/api/dataweb/imports/annual/country?nomenclature=hs6&format=csv&iso3=true&years=2012,2014,2015&reporters=USA&partners=CAN,MEX,JPN,CHN&aggregation=hs2')