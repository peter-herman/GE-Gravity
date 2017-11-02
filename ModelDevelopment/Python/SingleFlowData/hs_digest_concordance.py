
import numpy as np
import pandas as pd

trade_data = pd.read_csv("\\\\hq-fs-1.cloudnet.usitc.gov\\FS Econ only\\data\\Gravity Resources\\Data\\Africa Data\\africa_comtrade_data_single_flow_hs6agg.csv")
digest_data = pd.read_csv("\\\\hq-fs-1.cloudnet.usitc.gov\\FS Econ only\\data\\Gravity Resources\\Data\\Africa Data\\concordance_digest_hs6 (one to many).csv")
digest_data.drop(['ID'], axis = 1, inplace = True)

trade_data.columns
trade_data.shape
digest_data.columns
digest_data.shape[0]

num_years = len(trade_data['year'].unique())
num_importers = len(trade_data['importer'].unique())
num_exporters =  len(trade_data['exporter'].unique())
countries = np.concatenate((trade_data['importer'].unique(),trade_data['exporter'].unique()),axis=0)
countries = pd.DataFrame(pd.DataFrame(countries)[0].unique())
countries.columns = ['iso3']
countries.to_csv("\\\\hq-fs-1.cloudnet.usitc.gov\\FS Econ only\\data\\Gravity Resources\\Data\\Africa Data\\comtrade_country_list_2013-15.csv", index=False)
num_countries = len(countries)

merged_data = trade_data.merge(digest_data, how='left', left_on=('year', 'productcode'), right_on=('year', 'hs6'))
merged_data['weighted_flows'] = merged_data['single_flow']*merged_data['weight']
merged_data.drop(['trade_value_imports', 'trade_value_exports','single_flow', 'hs6', 'productcode', 'weight', 'year'], axis=1, inplace=True)
collapsed_data = merged_data.groupby(['importer','exporter','digest']).sum().reset_index()
collapsed_data['weighted_flows'] = collapsed_data['weighted_flows']/3


ind_report_count = collapsed_data.groupby(['digest']).count().reset_index()
ind_report_count = ind_report_count.drop(['importer', 'exporter'], axis = 1)
ind_report_count['number_zeros'] = (num_countries ** 2) - ind_report_count['weighted_flows']
ind_report_count['share_present'] = ind_report_count['weighted_flows'] / (num_countries ** 2)
ind_report_count['share_zero'] = 1 - ind_report_count['share_present']
#ind_report_count.to_csv("\\\\hq-fs-1.cloudnet.usitc.gov\\FS Econ only\\data\\Gravity Resources\\Data\\Africa Data\\trade_flows_by_digest.csv", index=False)

missing_threshold = 15

importer_exports_count = collapsed_data.groupby(['importer', 'digest']).count().reset_index()
importer_exports_count = importer_exports_count.pivot(index='importer', columns='digest', values='exporter').reset_index()
importer_exports_count = importer_exports_count.fillna(0)
importer_threshold_violations = pd.DataFrame(importer_exports_count[importer_exports_count < missing_threshold].count(axis=1))
importer_threshold_violations.columns = ['importer threshold violations']
importer_exports_count = importer_exports_count.merge(importer_threshold_violations, left_index = True, right_index = True)
importer_exports_count['threshold'] = missing_threshold

exporter_imports_count = collapsed_data.groupby(['exporter', 'digest']).count().reset_index()
exporter_imports_count = exporter_imports_count.pivot(index='exporter', columns='digest', values='importer').reset_index()
exporter_imports_count = exporter_imports_count.fillna(0)
exporter_threshold_violations = pd.DataFrame(exporter_imports_count[exporter_imports_count < missing_threshold].count(axis=1))
exporter_threshold_violations.columns = ['exporter threshold violations']
exporter_imports_count = exporter_imports_count.merge(exporter_threshold_violations, left_index = True, right_index = True)
exporter_imports_count['threshold'] = missing_threshold

merged_violations = importer_exports_count.merge(exporter_imports_count, left_on='importer', right_on='exporter')
merged_violations['ave_violations'] = (merged_violations['importer threshold violations']+merged_violations['exporter threshold violations'])/2

#merged_violations.to_csv("\\\\hq-fs-1.cloudnet.usitc.gov\\FS Econ only\\data\\Gravity Resources\\Data\\Africa Data\\importer_exporter_violations.csv", index=False)


trade_data.shape[0]
merged_data.shape[0]

digest_data.head(10)
