from scipy.stats import shapiro, kstest
import pandas as pd

def check_normality(df:pd.DataFrame, columns:list[str]):
    shapiro_p_value = [shapiro(df[col].values).pvalue for col in columns]
    kstest_p_value = [kstest(df[col].values, 'norm').pvalue for col in columns]

    normality_tests = pd.DataFrame(
        {'columns': columns, 'shapiro_p_value': shapiro_p_value, 'kstest_p_value': kstest_p_value})

    normality_tests['failed'] = normality_tests.apply(lambda row: 'yes' if row['shapiro_p_value'] > 0.05 or row['kstest_p_value'] > 0.05 else 'no', axis=1)
    return normality_tests
