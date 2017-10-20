# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 13:13:07 2017
@author: USITC Gravity Modeling Group / Serge Shikher
Estimate the gravity equation, solve for the baseline MRs, package the results
"""

from time import ctime as current_date_and_time, time as tictoc

import numpy as np
import pandas as pd  # import pandas
import statsmodels.api as sm  # import main statsmodels api
from numpy import multiply as mult
from scipy.optimize import root


class parameters(object):
    def __init__(self, z1, z2, number_of_countries):
        self.z1 = z1  # bilateral z1 parameters as a matrix
        self.z2 = z2  # bilateral z2 parameters as a matrix
        self.number_of_countries = number_of_countries


class model_state(object):
    def __init__(self, description, creation_date, country_variables, bilateral_variables,
                 number_of_countries, estimation_results, solver_results):
        self.description = description
        self.creation_date = creation_date
        self.country_variables = country_variables
        self.bilateral_variables = bilateral_variables
        self.number_of_countries = number_of_countries
        self.list_of_countries = list_of_countries
        self.estimation_results = estimation_results
        self.solver_results = solver_results


def func_base_mr(x, params):
    N = params.number_of_countries
    x1 = x[0:(0 + N - 1)]  # x1 is IMR, N-1 elements
    x2 = x[(N - 1):] * 1000  # x2 is OMR, N elements; multiplication by 1000 is done to correct the scaling problem
    z1 = params.z1
    z2 = params.z2

    out = [1 - mult(x1[j], sum(mult(z1[:, j], x2))) for j in range(0, (0 + N - 1))]  # match on exporter within the sum
    x1 = np.append(x1, 1)  # last IMR is normalized
    out.extend([1 - mult(x2[i], sum(mult(z2[i, :], x1))) for i in range(0, (0 + N))])  # match on importer within the sum

    return out


df = pd.read_stata('G:/data/Gravity Resources/Gravity modeling in Python/GE gravity 10.3.2017/ge_ppml_data.dta')  # read Yoto's dataset
df.sort_values(['exporter', 'importer'], inplace=True)
sigma = 7  # set elasticity equal to 7 following Yotov

### STEP 1 ###
# run glm poisson estimation with internally created fixed effects
# and using MacKinnon and White’s (1985) alternative heteroskedasticity robust standard errors
exp_fe = pd.get_dummies(df.exporter, prefix='exp_fe')
imp_fe = pd.get_dummies(df.importer, prefix='imp_fe')
rhs = pd.concat([df[['LN_DIST', 'CNTG', 'BRDR']], exp_fe, imp_fe.loc[:, 'imp_fe_ARG':'imp_fe_USA']], axis=1)
GLMres = sm.GLM(df.trade, rhs, family=sm.families.Poisson()).fit(cov_type='HC1')
print(GLMres.summary())

### STEP 2 ###
# calculate trade costs to the power of (1-sigma) using GLM estimates
tc_baseline = np.exp(GLMres.params['LN_DIST'] * rhs['LN_DIST'] + GLMres.params['CNTG'] * rhs['CNTG'] + GLMres.params['BRDR'] * rhs['BRDR'])
tc_baseline = pd.concat([df[['exporter', 'importer']], tc_baseline], axis=1)
tc_baseline.rename(columns={0: 'trade_cost_sigma'}, inplace=True)
tc_baseline.sort_values(['exporter', 'importer'], inplace=True)
# calculate trade costs
tc_baseline['trade_cost'] = tc_baseline['trade_cost_sigma'] ** (1 / (1 - sigma))
print('\nSummary of trade cost values:')
print(tc_baseline['trade_cost'].describe())

### STEP 3 ###
# solve for the baseline IMR and OMR
# (a) prepare y parameters (country-specific)
output = df[['exporter', 'output']].drop_duplicates().rename(columns={'exporter': 'country'})
expenditure = df[['importer', 'expndr']].drop_duplicates().rename(columns={'importer': 'country', 'expndr': 'expenditure'})
cdata = output.merge(expenditure, how='inner', on='country', sort=True)  # contains all country-specific data
cdata['phi'] = cdata['expenditure'] / cdata['output']
cdata['y1'] = cdata['output'] / sum(cdata['output'])
cdata['y2'] = cdata['expenditure'] / sum(cdata['expenditure'])
list_of_countries = cdata['country']

# (b) prepare z parameters (bilateral)
zparams = tc_baseline.merge(cdata[['country', 'y1']], how='left', left_on='exporter', right_on='country')
zparams = zparams.merge(cdata[['country', 'y2']], how='left', left_on='importer', right_on='country')
zparams['z1'] = mult(zparams['trade_cost_sigma'], zparams['y1'])
zparams['z2'] = mult(zparams['trade_cost_sigma'], zparams['y2'])
zparams.drop(['trade_cost_sigma', 'country_x', 'country_y', 'y1', 'y2'], axis=1, inplace=True)
zparams.sort_values(['exporter', 'importer'], inplace=True)
z1 = zparams.pivot(index='exporter', columns='importer', values='z1')  # create a matrix (exporter,importer)
z2 = zparams.pivot(index='exporter', columns='importer', values='z2')  # create a matrix (exporter,importer)
z1np = z1.as_matrix()  # transform the pandas dataframe to a numpy array for faster solver execution
z2np = z2.as_matrix()  # transform the pandas dataframe to a numpy array for faster solver execution

# (c) run the solver
N = 41  # number of countries
params = parameters(z1np, z2np, N)  # set parameter vales
x0 = [1] * (2 * N - 1)  # set starting values
# test=func_base_mr1(x0,params) # this is used to test the function if needed
tic = tictoc()  # get the initial clock value
solver_res = root(func_base_mr, x0, args=params, method='hybr', tol=1e-8, options={'xtol': 1e-8, 'maxfev': 1400})
# algorithms that can be used: hybr, lm, broyden2, krylov, and possibly others
toc = tictoc()  # get the final clock value
print('\nSolver run time:', toc - tic)  # print execution time

imr_baseline = solver_res.x[0:(0 + N - 1)]  # inverse of IMR
imr_baseline = np.append(imr_baseline, 1)  # last IMR is normalized
omr_baseline = solver_res.x[(N - 1):] * 1000  # inverse of OMR
beta_baseline = cdata['y1'].as_matrix() * omr_baseline  # preference parameters (baseline factory-gate prices are normalized)

### STEP 4 ###
# package the baseline model
country_variables = pd.concat([cdata[['country', 'output', 'expenditure']],
                               pd.DataFrame(data=imr_baseline, columns=['IMR']),
                               pd.DataFrame(data=omr_baseline, columns=['OMR'])], axis=1)
bilateral_variables = df[['exporter', 'importer', 'trade']].merge(tc_baseline, how='inner', on=['exporter', 'importer'])
baseline = model_state('Baseline AvW gravity model', current_date_and_time(), country_variables,
                       bilateral_variables, N, GLMres, solver_res)
