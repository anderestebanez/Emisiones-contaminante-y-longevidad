
########################################################################
##########################  PRUEBAS DE FUNCIONES WAD #######################
########################################################################
import pandas as pd
from scr.wad_utils import *


df = pd.read_csv('resultados/emisiones_x_municipio.csv', decimal=".")

target = 'qx_tot_tot'
feature = 'COT_sum_b10'
by = 'age_num'

features = [c for c in df.columns if ('qx' not in c) and ('edv65' not in c) and (c[-2:].isnumeric())]  + [c for c in df.columns if (len(c)==7) and (c[2:6].isnumeric())]

feature_byAge = [c for c in df.columns if (target in c) and c.split("_")[-1].isnumeric()]

df_2 = df[['NAMEUNIT']+features+feature_byAge]
df_2.columns = [i if i in [features, 'NAMEUNIT'] else '_'.join(i.split("_")[-3:]) for i in df_2.columns]
df2 = df_2.melt(id_vars=features + ['NAMEUNIT'],var_name='age', value_name=target)
df2['age_num'] = df2['age'].str.split('_').str[-3].astype(int)
df2.head()
len(df2.columns)

features_cont = [c for c in features if c[-2:].isnumeric()]
#get_best_wad_q(df2, target, feature, by)
metrica = 'life_squared_error'
result = []
feature_error = []
for feature in features:
    #dt = get_best_wad_q(df2, target, feature, by, corrector=1)
    #dt = get_best_wad_q(df2, target, feature, by, corrector=10)
    #dt = get_best_wad_q(df2, target, feature, by, relacion=1, relative=True, metric='life_squared_error',corrector=1.5)
    #dt = get_best_wad_q(df2, target, feature, by, metric='life_squared_error', corrector=1)
    try:
        #dt = get_best_wad_q(df2[df2[feature].isnull()==False], target, feature, by, relacion=1, relative=True, metric=metrica,corrector=1.5)
        dt = get_best_wad_q(df2[df2[feature].isnull()==False], target, feature, by, relative=True, metric=metrica)
        result.append(dt)
    except:
        feature_error.append(feature)
        print(f'Error en {feature}')
        pass


result
features
[i["feature"] for i in result]
df2['CR1010V']
df2[df2['CR1010V'].isnull()==False]

ax = plt.axes()
plot_wad(sort_result[0], ax=ax)
sort_result[0]['higher_avg']
sort_result[0]['lower_avg']

higher_lower_values = []

sort_result = sorted(result, key=lambda x: x['higher_wad'], reverse=True)
pd.DataFrame([{'features':r['feature'],'higher_wad':r['higher_wad'],'higher_q':r['higher_q']} 
              for r in sort_result]
              ).head(10)
higher_lower_values += sort_result[:3]
#plot_multiple_wad(sort_result[:3], 'imagenes/plot_higher.png')

sort_result = sorted(result, key=lambda x: x['lower_wad'], reverse=False)
pd.DataFrame([{'features':r['feature'],'lower_wad':r['lower_wad'],'lower_q':r['lower_q']} 
              for r in sort_result]
              ).head(10)
higher_lower_values += sort_result[:3]
#plot_multiple_wad(sort_result[:3], 'imagenes/plot_lower.png')
#plot_multiple_wad(sort_result[:3], 'imagenes/plot_lower.png',type='life_squared_error')

plot_multiple_wad(higher_lower_values, f'imagenes/higher_lower_values_{metrica}.png',type=metrica)
len(higher_lower_values)

a = [1,2,3]
b = [5,6]
a.append(4)
a += b
a

sort_result[0]["higher_q"]
filter = df2[sort_result[0]["feature"]]>df2[sort_result[0]["feature"]].quantile(q=0.9)
df2[filter]["NAMEUNIT"].unique()

avg = df2.groupby("age_num")['qx_tot_tot'].mean().sort_index()
var = df2.groupby("age_num")['qx_tot_tot'].var().sort_index()
lim = df2['COT_max_b30'].quantile(q=0.8)

df2.columns

avg1 = df2[df2['COT_max_b30']>lim].groupby("age_num")['qx_tot_tot'].mean().sort_index()
var1 = df2[df2['COT_max_b30']>lim].groupby("age_num")['qx_tot_tot'].var().sort_index()
n1 = df2[df2['COT_max_b30']>lim].groupby("age_num")['qx_tot_tot'].count().sort_index()
avg2 = df2[df2['COT_max_b30']<=lim].groupby("age_num")['qx_tot_tot'].mean().sort_index()
var2 = df2[df2['COT_max_b30']<=lim].groupby("age_num")['qx_tot_tot'].var().sort_index()
n2=df2[df2['COT_max_b30']<=lim].groupby("age_num")['qx_tot_tot'].count().sort_index()

sum((var1*n1+var2*n2)/(var*(n1+n2)))

pd.concat([avg,avg1,avg2], axis=1)

z = get_best_wad_q(df2, target, 'SO2_sum_b30', by,metric='life_squared_error')
z = get_best_wad_q(df2, target, 'SO2_sum_b30', by, relacion=1, relative=True, metric='life_squared_error', corrector=1)
z2 = get_best_wad_q(df2, target, 'NO2_sum_b30', by, relacion=1, relative=True, metric='life_squared_error', corrector=1)

z.keys()
avg=z['total_avg']
avg_q=z['lower_avg']
z['lower_wad']
z2['lower_wad']

z['lower_q']
filtro=(avg_q - avg)>0

avg_2 = avg.copy() 
avg_2[filtro==False] = avg_2[filtro==False]*2

avg
avg_2

pd.concat([avg, avg_q,z2['lower_avg']],axis=1)
