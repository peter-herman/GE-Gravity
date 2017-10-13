from typing import Sequence

import numpy as np
import pandas as pd
import statsmodels.api as sm

from ModelDevelopment.Python.Classes.Country import Country


def Construct(stata_data_path: str) -> Sequence[Country]:
    """
    This function exists to encapsulate ugly data manipulations until it can be refactored into a formal object factory.
    :param stata_data_path: The path to the Stata data file against which we are prototyping.
    :return: A collection of country data objects.
    """

    df = pd.read_stata(stata_data_path)

    # run glm poisson estimation with internally created fixed effects
    # and using MacKinnon and White’s (1985) alternative heteroskedasticity robust standard errors
    exp_fe = pd.get_dummies(df.exporter, prefix="exp_fe")
    imp_fe = pd.get_dummies(df.importer, prefix="imp_fe")
    rhs = pd.concat([df[["LN_DIST", "CNTG", "BRDR"]], exp_fe, imp_fe.loc[:, "imp_fe_ARG":"imp_fe_USA"]], axis=1)
    GLMres = sm.GLM(df.trade, rhs, family=sm.families.Poisson()).fit(cov_type="HC1")
    print(GLMres.summary())

    # calculate trade costs using GLM estimates
    t_ij_bsln = np.exp(
        GLMres.params["LN_DIST"] * rhs["LN_DIST"] + GLMres.params["CNTG"] * rhs["CNTG"] + GLMres.params["BRDR"] * rhs[
            "BRDR"])
    t_costs_bsln = pd.concat([df[["exporter", "importer"]], t_ij_bsln], axis=1)
    t_costs_bsln.rename(columns={0: "trade_costs"}, inplace=True)

    output = df[["exporter", "output"]].drop_duplicates().rename(columns={"exporter": "country"})
    expenditure = df[["importer", "expndr"]].drop_duplicates().rename(columns={"importer": "country", "expndr": "expenditure"})
    cdata = output.merge(expenditure, how="inner", on="country", sort=True)

    countries = list(cdata["country"])

    output_sum = sum(cdata["output"])
    output_shares = [x / output_sum for x in cdata["output"]]

    expenditure_sum = sum(cdata["expenditure"])
    expenditure_shares = [x / expenditure_sum for x in cdata["expenditure"]]

    import_trade_costs = [dict([(x[2], x[3]) for x in t_costs_bsln.itertuples() if x[1] == country]) for country in countries]
    export_trade_costs = [dict([(x[1], x[3]) for x in t_costs_bsln.itertuples() if x[2] == country]) for country in countries]

    country_records = [
        Country(
            countries[i],
            expenditure_shares[i],
            output_shares[i],
            import_trade_costs[i],
            export_trade_costs[i])
        for i in range(len(countries))]

    return country_records
