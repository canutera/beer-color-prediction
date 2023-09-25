from typing import Literal
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
def correlation_level(x): 
    corr = abs(x)
    if corr < 0.1: return 'None'
    if corr >= 0.1 and corr < 0.3: return 'Weak'
    if corr >= 0.3 and corr < 0.6: return 'Moderate'
    if corr >= 0.6 and corr < 0.95: return 'Strong'
    if x >= 0.95: return 'Perfect'
    return 'None'

def map_correlation_levels(x, cmap='Dark2'):
    levels = ['None', 'Weak', 'Moderate', 'Strong', 'Perfect']
    colors = [getattr(plt.cm, cmap)(i) for i in range(len(levels)-1)]
    map = dict(zip(levels, colors))
    return map.get(x, colors[0])

def plot_correlation_heatmap(df:pd.DataFrame, corr_method:Literal['pearson', 'spearman', 'kendall']):
    plt.rcParams["figure.figsize"] = (10,10)
    
    corr_df = df.dropna().corr(corr_method)
    ax = sns.heatmap(corr_df, 
                    vmin=-1, vmax=1, center=0, 
                    cmap='bwr', annot=corr_df.values,annot_kws={'fontsize':8})
    ax.set(title=f'{corr_method.title()} Correlation plot')
    return ax

def plot_correlation_bars(df:pd.DataFrame, column:str,  corr_method:Literal['pearson', 'spearman', 'kendall']):
    # absolute correlation 
    corr_df = df.dropna().corr(corr_method)
    plt.rcParams["figure.figsize"] = (20,5)
    corr_abs = (corr_df[[column]].assign(abs=corr_df[column].abs())
                                 .assign(category=corr_df[column].apply(lambda x: correlation_level(x)))
                                 .sort_values('abs', ascending=False)
                                 .reset_index(names=['columns'])
                                 .query(f'columns != "{column}"'))
    fig, ax = plt.subplots()
    from matplotlib.patches import Patch
    color = dict(zip(corr_abs.category.unique(), [map_correlation_levels(x) for x in corr_abs.category.unique()]))
    (corr_abs.plot.bar(x='columns', y=column, color=[map_correlation_levels(x) for x in corr_abs.category.values], ax=ax)
                  .legend([Patch(facecolor=color[i])for i in color], color))
    
    ax.set(title=f'{corr_method.title()} Correlation with {column} by column')
    def addlabels(x,y):
        for i in range(len(x)):
            plt.text(i-0.2,y[i]+0.005 if y[i] > 0 else 0.005,y[i])
    addlabels(corr_abs.index, [float('%.3f'%x) for x in corr_abs[column].values])

    return ax