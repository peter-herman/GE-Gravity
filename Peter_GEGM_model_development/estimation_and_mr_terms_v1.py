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


# Reformat Wide
trade_costs = grav_data[['importer','exporter','t_ij_bsln']]
trade_costs['t_exp_'] = trade_costs.groupby('exporter').cumcount()
trade_costs_wide = trade_costs.pivot('importer', 'exporter', 't_ij_bsln')
