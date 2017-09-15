___author___ = Peter Herman
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
grav_data = pd.get_dummies(grav_data, "imp", columns = ["importer"]) #Create fixed effects
grav_data = pd.get_dummies(grav_data, "exp", columns = ["exporter"]) #Create fixed effects

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
FormulaFE = 'trade ~ LN_DIST + CNTG + BRDR + C(importer) + C(exporter) + C(year)' #define a regression formula with fixed effects; C() creates a categorical variable
ppml_output = smf.GLM(endog_var, exog_var, family = sm.families.Poisson()).fit(cov_type='HC1')
ppml_output.summary() #print output



###############
# Trade Costs #
###############
#gen t_ij_bsln=exp(_b[LN_DIST]*LN_DIST+_b[CNTG]*CNTG+_b[BRDR]*BRDR)
cost = 'LN_DIST'
grav_data['t_ij_bsln'] = 0
for cost in select_vars:
    grav_data['t_ij_bsln'] += ppml_output.params[cost]*grav_data[cost]

