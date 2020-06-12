import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib as mpl
import matplotlib.pyplot as plt 
import seaborn as sns
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
import matplotlib.font_manager as fm
pd.options.display.max_columns = None
pd.options.display.max_rows = None

def low_corr_vars(X, y, threshold):
    '''
    Obtain set of var not correlated with each other
    to use in ML model. 
    Inputs: features df, target df, threshold value
    Output: Set of names of variables
    '''
    candidates = set(X.columns.values.tolist())
    for var in X.columns.values.tolist():
        for var2 in X.columns.values.tolist():
            if var != var2 and var in candidates and var2 in candidates:
                if abs(X[var].corr(X[var2])) >= threshold:
                    if abs(X[var].corr(y.iloc[:,0])) <= abs(X[var2].corr(y.iloc[:,0])):
                        candidates.remove(var)
                    else: candidates.remove(var2)                   

    return candidates

def share_maps(df, year, variable, color, k, title, source, leg):
    '''
    Create a map for Peru with regional yearly data and proportion 
    variable in format [0-1]. Does Natural Breaks Clustering.
    '''
    #create maps
    df = df.to_crs({'init': 'epsg:3857'})
    fig_, ax = plt.subplots(1, figsize=(15, 8))
    df[variable] = df[variable]*100
    fig = df[df['anio'].astype(int)==year].plot(column=variable, cmap=color, 
                                                  linewidth=0.5, ax=ax, edgecolor='0.2', 
                                                  scheme='naturalbreaks', k=k, legend = True)
    #title and source
    ax.set_title(title, fontdict={'fontsize': '15', 'fontweight':'3'})
    plt.figtext(0.38, 0.13, source)

    #legend 
    ax.axis('off')
    ax.get_legend().set_bbox_to_anchor((0.40, 0.26))
    ax.get_legend().set_title(leg)
    leg = fig.get_legend()
    for lbl in leg.get_texts():
        label_text = lbl.get_text()
        lower = label_text.split()[0]
        upper = label_text.split()[2]
        new_text = f'{float(lower):,.1f} - {float(upper):,.1f}'
        lbl.set_text(new_text)

    #arrow
    x_arr, y_arr, arrow_length = 0.90, 0.99, 0.065
    ax.annotate('N', xy=(x_arr, y_arr), xytext=(x_arr, y_arr-arrow_length),
                arrowprops=dict(facecolor='black', width=2, headwidth=9),
                ha='center', va='center', fontsize=20,
                xycoords=ax.transAxes)

    #scale bar
    scalebar = AnchoredSizeBar(ax.transData,
                               500000, '500 km', 'lower right', 
                               pad=0.1,
                               color='black',
                               frameon=False,
                               size_vertical=1,
                               fontproperties=fm.FontProperties(size=10))
    ax.add_artist(scalebar)
    return fig_

def share_maps_cb(df, year_var, year, variable, color, title, source, vmin, vmax, share=True):
    '''
    Create a map for Peru with regional yearly data. Must give min max for
    scale bar, year, variable, color, title and source 
    df must be geodataframe merged with the regional shape
    '''
    df = df.to_crs({'init': 'epsg:3857'})
    fig_, ax = plt.subplots(1, figsize=(10, 10))
    if share: df[variable] = df[variable]*100
    fig = df[df[year_var].astype(int)==year].plot(column=variable, cmap=color, ax=ax,  
                                                        figsize=(10,10), linewidth=0.8, 
                                                        edgecolor='0.8', vmin=vmin, vmax=vmax,
                                                        legend=True, 
                                                        norm=plt.Normalize(vmin=vmin, vmax=vmax))
    ax.axis('off')

    #title and source
    ax.set_title(title, fontdict={'fontsize': '15', 'fontweight':'3'})
    plt.figtext(0.28, 0.13, source)

    #arrow
    x_arr, y_arr, arrow_length = 0.90, 0.99, 0.065
    fig.annotate('N', xy=(x_arr, y_arr), xytext=(x_arr, y_arr-arrow_length),
                arrowprops=dict(facecolor='black', width=2, headwidth=9),
                ha='center', va='center', fontsize=20,
                xycoords=fig.transAxes)

    #scale bar
    scalebar = AnchoredSizeBar(fig.transData,
                               500000, '500 km', 'lower right', 
                               pad=0.1,
                               color='black',
                               frameon=False,
                               size_vertical=1,
                               fontproperties=fm.FontProperties(size=10))
    ax.add_artist(scalebar)
    
    return fig_

def fix_hist_step_vertical_line_at_end(ax):
    axpolygons = [poly for poly in ax.get_children() if isinstance(poly, mpl.patches.Polygon)]
    for poly in axpolygons:
        poly.set_xy(poly.get_xy()[:-1])

def cdf_elec_years(df, year_var, all_years, variable, election_y, title, xlab, ylab, source):
    '''
    CDF plot for variable in election and non election years.
    df dataframe, variable string name of col, 
    all_years and election_y is year list,
    title, xlab, ylab, source all strings
    '''
    fig, ax = plt.subplots(figsize=(12, 6))
    elections_df = df[df[year_var].astype(int).isin(election_y)]
    non_elections_df = df[~df[year_var].astype(int).isin(election_y)]

    n, bins, patches = ax.hist(elections_df[variable], 5000, density=1, 
                               histtype='step', alpha=0.8, color='r',
                               cumulative=True, label='Election & pre-elec. years {}'.format(election_y))

    # Overlay non eleciton years .
    ax.hist(non_elections_df[variable], 5000, density=1, 
            histtype='step', cumulative=1, alpha=0.8, color='k', 
            label='Non-election years between {}-{}'.format(all_years[0], all_years[-1]))

    fix_hist_step_vertical_line_at_end(ax)
    # tidy up the figure
    ax.grid(True)
    ax.legend(loc='right')
    ax.set_title(title, fontdict={'fontsize': '15', 'fontweight':'3'})
    ax.set_xlabel(xlab)
    ax.set_ylabel(ylab)
    plt.figtext(0.1, 0.01, source)
    plt.show()


def mv_treat(df, vars, val, dummy=True):
    '''
    Sets a fixed value to the missing values (i.e. zero)
    and creates a control dummy if needed.
    It registers the new dummy in the variable dictionary.
    '''
    #dic = {}
    for var in vars:
        if df[var].isnull().sum() > 0:
            if dummy:
                df['mv_' + var] = 0
                df.loc[df[var].isnull(), 'mv_' + var] = 1

                # dic['mv_' + var] = {'types': 'binary', 'role': 'MV control',
                #                     'desc': 'MV control for ' + var,
                #                     'MV': val}
            df.loc[df[var].isnull(), var] = val
    return df 


def outliers_imputation(df, percentile, varlist, nuniq=100):
    '''
    Obtains list of likely continous vars (more than nuniq unique values)
    For those vars, imputes the p95 of each var to values above it. 
    '''
    for var in varlist:
        if df[var].nunique() > nuniq:
            perc = df[var].quantile(1-percentile)
            df.loc[df[var] > perc, var] = perc

    return df 
    
