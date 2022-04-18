import pandas as pd
from util import all_variable_names_in_df
from scipy.stats import ttest_1samp, ttest_ind, ttest_rel, chi2_contingency

def one_sample_ttest(values, population_mean):
    '''
    Description: runs a one-sample t-test on the given values
    Inputs: a Dataframe of values in the sample, an Integer representing the population mean
    Returns: the t-stat and p-values
    '''
    tstats, pvalue = ttest_1samp(values, population_mean)
    print("One Sample t-Test: t-stat = " + str(tstats) + " and p-value = " + str(pvalue))
    return tstats, pvalue

def two_sample_ttest(values_a, values_b):
    '''
    Description: runs a two-sample t-test between the two populations samples
    Inputs: a Dataframe of samples from one population, a Dataframe of samples from another population
    Returns: the t-stat and p-values
    '''
    tstats, pvalue = ttest_ind(values_a, values_b)
    print("Two Sample t-Test: t-stat = " + str(tstats) + " and p-value = " + str(pvalue))
    return tstats, pvalue

def paired_ttest(values_a, values_b):
    '''
    Description: runs a paired t-test on the given population sample
    Inputs: a Dataframe of some values from the sample, a Dataframe of different values from the sample
    Returns: the t-stat and p-values
    '''
    tstats, pvalue = ttest_rel(values_a, values_b)
    print("Paired t-Test: t-stat = " + str(tstats) + " and p-value = " + str(pvalue))
    return tstats, pvalue

def chisquared_independence_test(df, column_a_name, column_b_name):
    '''
    Description: runs a chi squared independence test on the two values for the given population sample
    Inputs: a Dataframe, the String name of the column for one set values,
        the String name of the column for the other set of values
    Returns: the t-stat and p-values
    '''
    assert all_variable_names_in_df([column_a_name, column_b_name], df)
    cross_table = pd.crosstab(df[column_a_name], df[column_b_name])
    obs = cross_table.iloc[0:, 0:]
    tstats, pvalue, _, _ = chi2_contingency(cross_table)
    print("Chi-squared test: t-stat = " + str(tstats) + " and p-value = " + str(pvalue))
    return tstats, pvalue