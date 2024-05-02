import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings

def wad(avg_tot, avg_q, relative=True):
    """
    Calculates the Weighted Average Difference (WAD) between two series.

    Parameters:
    - avg (serie): The total average values by a factor, in life insurance the age.
    - avg_q (serie): The average values of a subset of data by a factor, in life insurance the age.
    - relative (bool, optional): If True, returns the relative WAD. If False, returns the absolute WAD. Default is True.

    Returns:
    - float: The WAD value.

    """
    v = avg_q - avg_tot

    if relative:
        return sum(v / avg_tot) / len(v)
    else:
        return sum(v) / len(v)

def wad_estable(avg_tot, avg_q, corrector=1, relative=True):
    """
    Calculates the weighted average difference (WAD) harming the WAD when the difference between total average 
    and subset averange is not estable over or below.

    Parameters:
    - avg_tot (serie): The total average values by a factor, in life insurance the age.
    - avg_q (serie): The average values of a subset of data by a factor, in life insurance the age.
    - corrector (float, optional): Corrector to harm the WAD when all the avg_q are not estable over/below the total avg. Defaults to 1, no corrector.
    - relative (bool, optional): If True, returns the relative WAD. If False, returns the absolute WAD. Default is True.
    
    Returns:
    float: The calculated WAD value.

    """
    if relative:
        trend = np.average((avg_q-avg_tot)/avg_tot)
    else:
        trend = np.average(avg_q-avg_tot)
        
    if trend>0:
        if relative:
            return max(0, sum([(i[0]-i[1])/i[1] if i[0]>i[1] else (i[0]-i[1])*corrector/i[1] for i in zip(avg_q, avg_tot)])/len(avg_tot))
        else:
            return max(0, sum([i[0]-i[1] if i[0]>i[1] else (i[0]-i[1])*corrector for i in zip(avg_q, avg_tot)])/len(avg_tot))
    else:
        if relative:
            return min(0, sum([(i[0]-i[1])/i[1] if i[0]<i[1] else (i[0]-i[1])*corrector/i[1] for i in zip(avg_q, avg_tot)])/len(avg_tot))
        else:
            return min(0, sum([i[0]-i[1] if i[0]<i[1] else (i[0]-i[1])*corrector for i in zip(avg_q, avg_tot)])/len(avg_tot))

def wad_relacion(avg_tot, avg_q, relacion, q_pos, relative=True):
    """
    Calculate the weighted average difference (WAD) defining the expected relation between th target and the factor. 
    If the observed relation is not the expected it does not increase the WAD.

    Parameters:
    - avg_tot (serie): The total average values by a factor, in life insurance the age.
    - avg_q (serie): The average values of a subset of data by a factor, in life insurance the age.
    - relacion (int): Theexpected relation between the target and the factor. 1 for positive relation, -1 for negative relation.
    - q_pos (str): The position of the quantile. 'Top' for the top quantile, 'Bot' for the bottom quantile.
    - relative (bool, optional): If True, returns the relative WAD. If False, returns the absolute WAD. Default is True.
    
    Returns:
        float: The calculated WAD.

    """
    if q_pos=='Top':
        if relacion==1:
            v = [i[0]-i[1] if i[0]>i[1] else 0 for i in zip(avg_q, avg_tot)]
        else:
            v = [i[0]-i[1] if i[0]<i[1] else 0 for i in zip(avg_q, avg_tot)]
    else:        
        if relacion==1:
            v= [i[0]-i[1] if i[0]<i[1] else 0 for i in zip(avg_q, avg_tot)]
        else:
            v = [i[0]-i[1] if i[0]>i[1] else 0 for i in zip(avg_q, avg_tot)]
    
    if relative:
        return sum(v/avg_tot)/len(v)
    else:
        return sum(v)/len(v)

def life_squared_error(avg, avg_q, var, var_q, N_q, var_q_inv, N_q_inv, relacion=None, q_pos=None, corrector=2):
    """
    Calculate the square error reduction by age, and sum.
    """ 
    if relacion:
        if q_pos=='Top':
            if relacion==1:
                filtro = (avg_q - avg)>0
            else:
                filtro = (avg_q - avg)<0
        else:
            if relacion==1:
                filtro = (avg_q - avg)<0
            else:
                filtro = (avg_q - avg)>0
    else:
        filtro = avg>0

    kpi_by = ((N_q*var_q)+(var_q_inv*N_q_inv))/(var*(N_q+N_q_inv))
    kpi_prev = sum(kpi_by)
    kpi = sum(kpi_by[filtro==False]*corrector) + sum(kpi_by[filtro])
    return kpi

# get_best_wad_q(df2, target, 'SO2_sum_b30', by,metric='life_squared_error')
# wad(result[0]['total_avg'], result[0]['total_avg']-1)
# wad_estable(result[0]['total_avg'], result[0]['total_avg']-1, corrector=10)

# a = result[0]['total_avg']-1
# a[1] = a[1]+3
# wad(result[0]['total_avg'], a)
# wad_estable(result[0]['total_avg'], a, corrector=2)
# wad(result[0]['total_avg'], a, relative=False)
# wad_estable(result[0]['total_avg'], a, corrector=2, relative=False)

def get_best_wad_q(df, target, feature, by, metric='WAD', corrector=1, relacion=None, relative=True):
    """
    Calculate the best weighted average difference (WAD) for different quantiles of a feature in a DataFrame. 
    And select the quantiles that gives the highest and lowest WAD.

    Args:
        df (pandas.DataFrame): The DataFrame containing the data.
        target (str): The name of the target variable column.
        feature (str): The name of the feature column.
        by (str): The column(s) to group the data by. In life insurance Age 
        corrector (float, optional): A correction factor to apply to the WAD_estable metric. Defaults to 1.
        relacion (int, optional): The expected relationship between the feature and the target variable. 
            Must be 1 or -1. Defaults to None.
        relative (bool, optional): Whether to calculate the WAD relative or absolute. Defaults to True.

    Returns:
        dict: A dictionary containing the following information:
            - 'feature': The name of the feature.
            - 'total_avg': The serie of target average group by define factor.
            - 'higher_q': The quantile label for the higher WAD.
            - 'higher_wad': The higher WAD value.
            - 'higher_avg': The serie of target average of the subset highest_q group by define factor.
            - 'lower_q': The quantile label for the lower WAD.
            - 'lower_wad': The lower WAD value.
            - 'lower_avg': The serie of target average of the subset lower_q group by define factor.
    """
    q_v = df[feature].quantile(q=np.arange(0.1,1,0.1)).reset_index().rename(columns={'index':'quantile'})

    avg = df.groupby(by)[target].mean().sort_index()
    var = df.groupby(by)[target].var().sort_index()

    higher_q = 0
    higher_wad = None
    higher_avg = None
    lower_q = 0
    lower_wad = None
    lower_avg = None

    #Raise error if selected metric has not enough parameters
    if (metric=='wad_relacion') and (relacion is None):
        raise ValueError('ERROR wad_relacion neer relacion parameter')
    elif (metric=='wad_estable') and (corrector==1):
        warnings.warn('WARNING wad_estable parameters: corrector=1, no correction will be applied') 
    elif relacion:
        if relacion not in [1,-1]:
            raise ValueError('ERROR wad_relacion parameters: relacion debe ser 1 o -1')


    for i, qv in q_v.iterrows():
        if qv["quantile"]>0.5:
            avg_q = df.loc[df[feature] > qv[feature]].groupby(by)[target].mean().sort_index()

            var_q = df.loc[df[feature] > qv[feature]].groupby(by)[target].var().sort_index()
            N_q = df.loc[df[feature] > qv[feature]].groupby(by)[target].count().sort_index()

            var_q_inv = df.loc[df[feature] <= qv[feature]].groupby(by)[target].var().sort_index()
            N_q_inv = df.loc[df[feature] <= qv[feature]].groupby(by)[target].count().sort_index()

            str_q = f'Top {round((1-qv["quantile"])*100)}%'
        else:
            avg_q = df.loc[df[feature] <= qv[feature]].groupby(by)[target].mean().sort_index()

            var_q = df.loc[df[feature] <= qv[feature]].groupby(by)[target].var().sort_index()
            N_q = df.loc[df[feature] <= qv[feature]].groupby(by)[target].count().sort_index()

            var_q_inv = df.loc[df[feature] > qv[feature]].groupby(by)[target].var().sort_index()
            N_q_inv = df.loc[df[feature] > qv[feature]].groupby(by)[target].count().sort_index()

            str_q = f'Bottom {round(qv["quantile"]*100)}%'
        

        if metric=='wad_relacion':
            wad_v = wad_relacion(avg, avg_q, relacion, str_q[:3])
        elif metric=='wad_estable':
            wad_v = wad_estable(avg, avg_q, corrector)
        elif metric=='wad':
            wad_v = wad(avg, avg_q)
        elif metric=='life_squared_error':
            wad_v = life_squared_error(avg, avg_q, var, var_q, N_q, var_q_inv, N_q_inv,relacion=relacion, q_pos=str_q[:3], corrector=corrector)
        else:
            raise ValueError('ERROR metric parameter: metric must be wad, wad_estable or wad_relacion')

        if (higher_wad is None) or (wad_v>=higher_wad):
            higher_wad = wad_v
            higher_q = str_q
            higher_avg = avg_q
        
        if (lower_wad is None) or (wad_v<=lower_wad):
            lower_wad = wad_v
            lower_q = str_q
            lower_avg = avg_q
    
    return {'feature': feature,
            'total_avg': avg,
            'higher_q': higher_q,   
            'higher_wad': higher_wad,
            'higher_avg': higher_avg,
            'lower_q': lower_q,
            'lower_wad': lower_wad,
            'lower_avg': lower_avg}

def plot_wad(obj_wad, ax=None, log_y=True, text_box=True, type='WAD'): #, output_path='plot.png'
    """
    Plots the weighted average difference (WAD) for a given object.

    Parameters:
    - obj_wad (dict): The object containing the WAD data.
    - ax (matplotlib.axes.Axes, optional): The axes on which to plot. If not provided, the current axes will be used.
    - log_y (bool, optional): Whether to use a logarithmic scale for the y-axis. Default is True.
    - text_box (bool, optional): Whether to add a text box with additional information. Default is True.

    Returns:
    - bool: True if the plot was successfully created.

    """
    if ax is None:
        ax = plt.gca()

    i = obj_wad['total_avg'].index

    if type=='life_squared_error':    
        q = int(obj_wad['lower_q'].split(" ")[1][:-1])/100
        lado = 'Bottom' if obj_wad['lower_q'].split(" ")[0]=='Top' else 'Top'

        ax.plot(i, (obj_wad['total_avg']-obj_wad['lower_avg']*q)/(1-q), '-r', label=f'{lado} {(1-q)*100}%')
        ax.plot(i, obj_wad['lower_avg'], '-g', label=obj_wad['lower_q'])
    else:
        ax.plot(i, obj_wad['higher_avg'], '-r', label=f'Higher WAD: {obj_wad["higher_q"]}')
        ax.plot(i, obj_wad['lower_avg'], '-g', label=f'Lower Wad: {obj_wad["lower_q"]}')
    
    if log_y:
        ax.semilogy(i, obj_wad['total_avg'], '-b', label='avg')
    else:
        ax.plot(i, obj_wad['total_avg'], '-b', label=f'Avg')

    if type!='life_squared_error':
        ax.fill_between(i, obj_wad['total_avg'], obj_wad['higher_avg'], interpolate=True, color='red', alpha=0.2)
        ax.fill_between(i, obj_wad['total_avg'], obj_wad['lower_avg'], interpolate=True, color='green', alpha=0.2)
    
    #ax.xlim([i.min(), i.max()])
    
    labels = ax.get_xticklabels()
    newlabel = [l.get_text().split("_")[-1] for l in labels]
    ax.set_xticklabels(newlabel)

    ax.set_title(obj_wad['feature'])
    ax.legend()


    # Add text box
    if text_box:
        if type=='life_squared_error': 
            textstr = f"Lower SUM of SquareErrors by age: {round(obj_wad['lower_wad'],3)}"
            props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
            ax.text(0.35, 0.7, textstr, transform=ax.transAxes, fontsize=14,verticalalignment='top', bbox=props)
        else:
            textstr = f"Higher WAD: {round(obj_wad['higher_wad'],3)}\nLower WAD: {round(obj_wad['lower_wad'],3)}"
            props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
            ax.text(0.35, 0.7, textstr, transform=ax.transAxes, fontsize=14,verticalalignment='top', bbox=props)

    return True

def plot_multiple_wad(obj_wad_list, output_path='imagenes/plot.png', show=False, type='WAD'):
    """
    Plots multiple waveforms using the `plot_wad` function and saves the plot to a file.

    Parameters:
    - obj_wad_list (list): A list of WAD data to be plotted.
    - output_path (str): The path where the plot will be saved. Default is 'plot.png'.

    Returns:
    - bool: True if the plot is successfully saved, False otherwise.
    """
    fig, axs = plt.subplots(len(obj_wad_list), 2, figsize=(20,4*len(obj_wad_list)))
    for i, obj_wad in enumerate(obj_wad_list):
        plot_wad(obj_wad, ax=axs[i,0], log_y=False, type=type)
        plot_wad(obj_wad, ax=axs[i,1], log_y=True, text_box=False, type=type)
    plt.savefig(output_path)

    if show:
        plt.show()
    return True


#get_best_wad_q(df2, target, feature, by)
#result = []
#for feature in features:
    #dt = get_best_wad_q(df2, target, feature, by, corrector=1)
    #dt = get_best_wad_q(df2, target, feature, by, corrector=10)
#    dt = get_best_wad_q(df2, target, feature, by, relacion=1, relative=True, metric='life_squared_error')
#    result.append(dt)
#sort_result[0]

#a = get_best_wad_q(df2, target, feature, by, relacion=1, relative=True, metric='life_squared_error')
#a

#plot_multiple_wad(sort_result[:3], 'imagenes/plot_lower.png', type='life_squared_error')
#obj_wad = sort_result[0]


#(obj_wad['total_avg']-obj_wad['lower_avg']*obj_wad['lower_q'])/(1-obj_wad['lower_q'])
#obj_wad['total_avg'].shape