
import numpy as np
import pandas as pd

trade_data = pd.read_csv("G:\\data\\Gravity Resources\\Data\\Africa Data\\africa_comtrade_data_single_flow_hs6agg.csv")
digest_data = pd.read_csv("G:\\data\\Gravity Resources\\Data\\Africa Data\\concordance_digest_hs6 (one to many).csv")
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
# countries_to_drop =
# collapsed_data[collapsed_data['exporter'].isin(countries_to_drop)].index, inplace = True

collapsed_data.to_csv("\\\\hq-fs-1.cloudnet.usitc.gov\\FS Econ only\\data\\Gravity Resources\\Data\\Africa Data\\COMTRADE_digest_aggregation_singleflow_2013to2015average.csv", index=False)

ind_report_count = collapsed_data.groupby(['digest']).count().reset_index()
ind_report_count = ind_report_count.drop(['importer', 'exporter'], axis = 1)
ind_report_count['number_zeros'] = (num_countries ** 2) - ind_report_count['weighted_flows']
ind_report_count['share_present'] = ind_report_count['weighted_flows'] / (num_countries*(num_countries-1))
ind_report_count['share_zero'] = 1 - ind_report_count['share_present']
#ind_report_count.to_csv("\\\\hq-fs-1.cloudnet.usitc.gov\\FS Econ only\\data\\Gravity Resources\\Data\\Africa Data\\trade_flows_by_digest.csv", index=False)

missing_threshold = 15 # Minimum number of required positive trade flows to be considered not in violation

country_drop_list_history = list()
country_violation_threshold = 200 # Number of sectors a country is permited to exhibit violations in (averaged between importer/exporter)
sector_violation_threshold = 200 # Number of countries a sector is permitted to exhibit violations in (averaged across importer/exporter)
iteration_stop_condition = False
iteration_stop_condition_country = False
iteration_stop_condition_sector = False
i=0
while iteration_stop_condition == False:
#while i == 0:

    importer_exports_count = collapsed_data.groupby(['importer', 'digest']).count().reset_index()
    importer_exports_count = importer_exports_count.pivot(index='importer', columns='digest', values='exporter').reset_index()
    importer_exports_count = importer_exports_count.fillna(0)
    importer_threshold_violations = pd.DataFrame(importer_exports_count[importer_exports_count < missing_threshold].count(axis=1)-1)
    importer_threshold_violations.columns = ['importer threshold violations']
    importer_exports_count = importer_exports_count.merge(importer_threshold_violations, left_index = True, right_index = True)
    importer_exports_count['threshold'] = missing_threshold

    exporter_imports_count = collapsed_data.groupby(['exporter', 'digest']).count().reset_index()
    exporter_imports_count = exporter_imports_count.pivot(index='exporter', columns='digest', values='importer').reset_index()
    exporter_imports_count = exporter_imports_count.fillna(0)
    exporter_threshold_violations = pd.DataFrame(exporter_imports_count[exporter_imports_count < missing_threshold].count(axis=1)-1)
    exporter_threshold_violations.columns = ['exporter threshold violations']
    exporter_imports_count = exporter_imports_count.merge(exporter_threshold_violations, left_index = True, right_index = True)
    exporter_imports_count['threshold'] = missing_threshold

    merged_violations = importer_exports_count.merge(exporter_imports_count, left_on='importer', right_on='exporter')
    merged_violations['ave_violations'] = (merged_violations['importer threshold violations']+merged_violations['exporter threshold violations'])/2

    if max(merged_violations['ave_violations']) < country_violation_threshold:
        iteration_stop_condition_country = True
    else:
        country_drop_list = list(merged_violations['exporter'][merged_violations['ave_violations'] ==max(merged_violations['ave_violations'])])
        print('Current max average violations: ' + str(max(merged_violations['ave_violations'])) )
        print('dropping: '+ ",".join(country_drop_list))
        collapsed_data.drop(collapsed_data[collapsed_data['exporter'].isin(country_drop_list)].index, inplace=True)
        collapsed_data.drop(collapsed_data[collapsed_data['importer'].isin(country_drop_list)].index, inplace=True)
        country_drop_list_history.append(country_drop_list)



    import_sector_count = collapsed_data.groupby(['importer', 'digest']).count().reset_index()
    import_sector_count = import_sector_count.pivot(index='digest', columns='importer', values='exporter').reset_index()
    import_sector_count = import_sector_count.fillna(0)
    importer_sector_threshold_violations = pd.DataFrame(import_sector_count[import_sector_count < missing_threshold].count(axis=1)-1)
    importer_sector_threshold_violations.columns = ['importer sector threshold violations']
    import_sector_count = import_sector_count.merge(importer_sector_threshold_violations, left_index = True, right_index = True)
    import_sector_count['threshold'] = missing_threshold

    export_sector_count = collapsed_data.groupby(['exporter', 'digest']).count().reset_index()
    export_sector_count = export_sector_count.pivot(index='digest', columns='exporter', values='importer').reset_index()
    export_sector_count = export_sector_count.fillna(0)
    exporter_sector_threshold_violations = pd.DataFrame(export_sector_count[export_sector_count < missing_threshold].count(axis=1)-1)
    exporter_sector_threshold_violations.columns = ['exporter sector threshold violations']
    export_sector_count = export_sector_count.merge(exporter_sector_threshold_violations, left_index = True, right_index = True)
    export_sector_count['threshold'] = missing_threshold

    merged_sector_violations = import_sector_count.merge(export_sector_count, left_on='digest', right_on='digest')
    merged_sector_violations['ave_sector_violations'] = (merged_sector_violations['importer sector threshold violations']+merged_sector_violations['exporter sector threshold violations'])/2

    if max(merged_sector_violations['ave_sector_violations']) < sector_violation_threshold:
        iteration_stop_condition_sector = True
    else:
        sector_drop_list = list(merged_sector_violations['digest'][merged_sector_violations['ave_sector_violations'] ==max(merged_sector_violations['ave_sector_violations'])])
        print('Current max average sector violations: ' + str(max(merged_sector_violations['ave_sector_violations'])) )
        print('dropping: '+ ",".join(sector_drop_list))
        collapsed_data.drop(collapsed_data[collapsed_data['digest'].isin(sector_drop_list)].index, inplace=True)
        country_drop_list_history.append(sector_drop_list)

    if (iteration_stop_condition_sector) & (iteration_stop_condition_country):
        iteration_stop_condition = True

print(country_drop_list_history)
## TO DO: repeat for dropping industries.  Put second condition in while loop and put an if statement around each so that if countries become acceptable, you can stop dropping countries.










#merged_violations.to_csv("\\\\hq-fs-1.cloudnet.usitc.gov\\FS Econ only\\data\\Gravity Resources\\Data\\Africa Data\\importer_exporter_violations.csv", index=False)


trade_data.shape[0]
merged_data.shape[0]

digest_data.head(10)
