___author___ = "Peter Herman"
___created___ = "09/15/2017"
___altered___ = "09/15/2017"


# Ongoing work to replicate the Yotov Matlab code in Python


###################
# PPML Estimation #
###################

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
import scipy.optimize as spo

# read in data
grav_data = pd.read_csv("\\\\hq-fs-1.cloudnet.usitc.gov\\FS Econ only\\data\\Gravity Resources\\GEPPMLwithMatlab\\working\\Peter\\ge_ppml_data.csv") #read in csv as DataFrame


# get rid of the predefined dummies
delete_columns = [col for col in grav_data if col.startswith('imp_fe') | col.startswith('exp_fe')]
for col in delete_columns:
    del grav_data[col]

# Create a new set of dummies
#df = pd.concat([df, pd.get_dummies(df['YEAR'])], axis=1); df
grav_data['importer_fe'] = grav_data['importer'] #create a second variable of country identifiers because get_dummies canibalizes one
grav_data['exporter_fe'] = grav_data['exporter']
grav_data = pd.get_dummies(grav_data, "imp", columns = ["importer_fe"]) #Create fixed effects
grav_data = pd.get_dummies(grav_data, "exp", columns = ["exporter_fe"]) #Create fixed effects

reg_data = grav_data #create a temporary dataset from which to delete the German importer fixed effect
del reg_data['imp_ZZZ'] #delete variable 'imp_ZZZ'


# Create model specification
select_vars = ['LN_DIST', 'CNTG', 'BRDR'] #specify desired gravity variables
select_fe = [col for col in reg_data if col.startswith('imp_') | col.startswith('exp_')] # create a list of the fixed effects
select_full = select_vars + select_fe #combine gravity variable list with the fixed effects list

#create exog and endog datasets
endog_var = reg_data['trade']
exog_var = reg_data[select_full]

### Poisson Model
ppml_output = smf.GLM(endog_var, exog_var, family = sm.families.Poisson()).fit(cov_type='HC1')
ppml_output.summary() #print output



###############
# Trade Costs #
###############

# Baseline
grav_data['t_ij_bsln'] = 0 # initialize variable
for cost in select_vars: # for each of the included costs from before
    grav_data['t_ij_bsln'] += ppml_output.params[cost]*grav_data[cost] # add beta_cost * cost_ij
grav_data['t_ij_bsln'] = np.exp(grav_data['t_ij_bsln']) # t_ij = exp(costs)

# Counterfactual
grav_data['t_ij_cfl'] = 0 # initialize variable
cfl_vars = ['LN_DIST', 'CNTG'] # define the costs to be included in the counterfactual
for cost in cfl_vars: # for each of the included costs from before
    grav_data['t_ij_cfl'] += ppml_output.params[cost] * grav_data[cost] # add beta_cost * cost_ij
grav_data['t_ij_cfl'] = np.exp(grav_data['t_ij_cfl']) # t_ij = exp(costs)


##########################
## Prep Data For Solver ##
##########################

## Trade Costs
# Reformat Wide
trade_costs = grav_data[['importer','exporter','t_ij_bsln']]
#trade_costs['t_exp_'] = trade_costs.groupby('exporter').cumcount()
trade_costs_imp = trade_costs.pivot('importer', 'exporter', 't_ij_bsln')


## Country stats (output, expenditure, phi)



country_stats = grav_data[['importer', 'exporter','output','expndr']].sort_values(by = 'importer')
country_stats = country_stats[(country_stats.importer == country_stats.exporter)]
country_stats['phi'] = country_stats.expndr/country_stats.output

#set index as country names so that df.loc[] can be used to call specific entries
country_stats.set_index('importer', inplace = True, drop = False)
country_list = country_stats['importer']

#calculate output shares
total_output = sum(country_stats['output'])
country_stats['output_share'] = country_stats['output']/total_output

#calculate expenditure shares
total_expenditure = sum(country_stats['expndr'])
country_stats['expend_share'] = country_stats['expndr']/total_expenditure



###
#Set up MRS solver
####
mrs = pd.DataFrame(country_stats.importer)
mrs['mrs_inward'] = 1
mrs['mrs_outward'] = 1
mrs.set_index('importer', drop = True, inplace = True)
country_info = country_stats

def mrs_functions(mrs, trade_costs, country_info,country_list):
    mrs_slack = np.zeros(2*len(country_info.importer))  # create list of zeros
    for i in range(len(country_info.importer)-1):
        imp_index = country_list.iloc[i] #select a country for the current iteration for an index location
        cost_calculation = 0
        for k in range(len(country_info.importer)):
            exp_index = country_list.iloc[k]
            cost_calculation += trade_costs_imp.loc[imp_index, exp_index] * \
                    country_info.output_share.loc[exp_index] * \
                    mrs.mrs_outward.loc[exp_index]
        mrs_slack[i] = 1 - mrs.mrs_inward.loc[imp_index] * cost_calculation

    for j in range(len(country_info.importer)):
        exp_index = country_list.iloc[j]
        cost_calculation = 0
        for k in range(len(country_info.importer)):
            imp_index = country_list.iloc[k]
            cost_calculation += trade_costs_imp.loc[imp_index,exp_index] *\
                    country_info.expend_share.loc[imp_index] * \
                    mrs.mrs_inward.loc[imp_index]
        mrs_slack[j + len(country_info.importer)] = 1 - mrs.mrs_outward.loc[exp_index] * cost_calculation
    return mrs_slack


mrs_functions(mrs,trade_costs_imp,country_stats, country_list)

feeder = lambda mrs_0: mrs_functions(mrs_0, trade_costs_imp,country_stats, country_list)

solution_1 = spo.root(feeder, mrs)
#It does not seem to like having a dataframe fed in as an optimization arguement. Try convertin mrs to a simple vector.