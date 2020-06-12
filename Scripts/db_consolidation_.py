# -*- coding: utf-8 -*-
'''
  __________________________________________________________
 |                                                         |
 | CAPP 30235 - Homework3                                  |
 | Data consolidation                                      |
 | Authors:                                                |
 |    - Andrei bartra (andreibartra)                       |
 |    - Angelo Cozzubo (acozzubo)                          |
 | Date: May 2020                                          |
 |_________________________________________________________|

 =============================================================================
 Highlights:

 =============================================================================
'''


'''  ________________________________________
    |                                        |
    |              1: Libraries              |
    |________________________________________|'''

# System
import os
import sys

#Basic
import pandas as pd
import numpy as np

#Other
import string
from pyjarowinkler.distance import get_jaro_distance
import varlists as vl


OLD_PROJ = ['MEJORAMIENTO', 'REMODELACION', 'REHABILITACION', 'AMPLIACION', \
            'FORTALECIMIENTO', 'REPARACION', 'RECUPERACION', 'RENOVACION', \
            'AULAS', 'SUSTITUCION', 'MEJORA', 'OPTIMIZACION', \
            'REFORZAMIENTO', 'INCREMENT', 'REACONDICIONAMIENTO', \
            'CULMINACION', 'REEMPLAZO', 'REUBICACION', 'ADECUA', \
            'AFIANZAMIENTO', 'REVESTIMIENTO', 'INTEGRACION', 'ADAPTA']
NEW_PROJ = ['CONSTRUCCION', 'CREACION', 'ELECTRIFICACION', 'INSTALACION', \
            'PAVIMENTACION', 'AGUA', 'PUESTA', 'PUESTO', 'ENCAUZAMIENTO', \
            'HABILITACION', 'RIEGO', 'REPRESAMIENTO', 'CANAL', 'LINEA', \
            'GENERACION', 'SANEAMIENTO', 'SEMAFORIZACION', 'EDIFICIO', 'PUERTO']
INT_PROJ = ['ADQUISICION', 'APOYO', 'DESARROLLO', 'SISTEMA', \
            'IMPLEMENTACION', 'ASISTENCIA', 'PROTECCION', 'FOMENTO', \
            'REFORESTACION', 'CAPACITACION', 'PROYECTO', 'SENSIBILIZACION', \
            'PROMOCION', 'ADQUISICION', 'CONSERVACION', 'GESTION', 'PROGRAMA', \
            'INVESTIGACION', 'PILOTO', 'ERRADICACION', 'APROVECHAMIENTO', \
            'REDIMENSIONAMIENTO', 'TRANSFERENCIA', 'LIMPIEZA', 'CATASTRO', \
            'INTERVENCION']

JW_MIN = 0.75



'''  ________________________________________
    |                                        |
    |               2: Settings              |
    |________________________________________|'''

WD = r'D:\Google Drive\U Chicago\5. Q3\ML\5. Project'
os.chdir(WD)
sys.path.append(os.chdir(WD))
sys.path.insert(0, './code')

'''  ________________________________________
    |                                        |
    |          3: Helper Functions           |
    |________________________________________|'''

def categorize(df, codes, desc):
    '''
    Converts a numerical column to categorical, and creates a label dictionary
    assuming there is a variable with the labels.
    Inputs:
        - df: the dataframe with the data
        - codes: The numerical coolumns
        - desc: The column with the description

    Output: a dataframe with the label encoding.

    '''
    dic = df.groupby(desc)[codes].max().reset_index()
    dic = dic.rename(columns = {codes: 'codes', desc: 'labels'})
    dic['column']  = codes
    dic = dic.sort_values('codes')

    return dic


def year_cumul(df, idd, cond, var, new_var):
    df = df.sort_values([idd, 'ANO_EJE', 'mes'])
    temp = df.loc[df[cond] == 1] \
             .groupby([idd, 'ANO_EJE', 'mes'])[var] \
             .sum().reset_index()
    temp[new_var] = temp.groupby([idd, 'ANO_EJE'])[var] \
                               .cumsum()
    temp = temp.drop(columns=var)
    return  df.merge(temp, on = [idd, 'ANO_EJE', 'mes'])


def dummy_expand(df, var, suffix, iid):
    dummies = [dm for dm in df.columns if dm.startswith(suffix)]
    names = []
    temp = df.loc[:, iid + [var] + dummies]
    for dm in dummies:
        name = var + dm.replace(suffix, '')
        names += [name]
        temp[name] = temp[var]*temp[dm]
    return temp, names

def str_clean(x):
    x = x.replace('-', ' ')
    x = x.replace('/', ' ')
    x = x.translate(str.maketrans('', '', string.punctuation)).upper()
    x = x.replace('Á', 'A')
    x = x.replace('É', 'E')
    x = x.replace('Í', 'I')
    x = x.replace('Ó', 'O')
    x = x.replace('Ú', 'U')
    x = x.strip('1234567890¿')
    return x

def class_proj(x, terms):
    return max([get_jaro_distance(x, t) for t in terms])


'''  ________________________________________
    |                                        |
    |             4: Raw Datasets            |
    |________________________________________|'''


ex = pd.read_excel(r'data\raw\proj\exec.xlsx', sheet_name='data')
ex = ex.sort_values(['ACT_PROD_PROY', 'ANO_EJE', 'COD_NIVEL', 'COD_SECTOR', \
                     'COD_PLIEGO', 'FUENTE', 'CATEGORIA_GTO'])

pr = pd.read_excel(r'data\raw\proj\prog.xlsx', sheet_name='data')

ubi = pd.read_excel(r'data\raw\proj\ubigeo.xlsx', dtype={'UBIGEO': str})
ubi = ubi.loc[ubi['CODIGO_UNICO'].isnull() == False]

enaho = pd.read_excel(r'data\raw\ext\enaho.xlsx')
enaho['anio'] = enaho['anio'] + 1 ### IMPORTANTE shift de enaho un año
enaho = enaho.loc[enaho['anio'] >= 2011]


# ['anio', 'dpto', 'percepho', 'mieperho', 'totmieho', \
#                  'inghog1d', 'ingmo1hd', 'ipcr_0', 'gashog1d', \
#                  'gashog2d', 'gpgru0', 'gpgru1', 'gpgru2', 'gpgru3', \
#                  'gpgru4', 'gpgru5', 'gpgru6', 'gpgru7', 'gpgru8', \
#                  'gpgru9', 'gpgru10', 'pet', 'pea', 'ocupa', 'desocu', \
#                  'p_rama31', 'p_rama32', 'p_rama33', 'p_rama34', \
#                  'p_rama35', 'p_rama36', 'p_rama37', 'p_rama38', \
#                  'p_rama41', 'p_rama42', 'p_rama43', 'p_rama44', \
#                  'p_rama45', 'p_rama46', 'p_rama47', 'p_rama48', \
#                  'urbano', 'pisos_inadec', 'agua_inadec', 'sshh_inadec', \
#                  'p1121', 'nbi1', 'nbi2', 'nbi3', 'nbi4', 'nbi5', \
#                  'estratosocio_1', 'estratosocio_2', 'estratosocio_3', \
#                  'estratosocio_4', 'estratosocio_5', 'estratosocio_6', \
#                  'p303', 'anoeduc', 'lengua_nativa', 'p401', 'p401g1']

'''  ________________________________________
    |                                        |
    |         5: Panel Data Cleaning         |
    |________________________________________|'''


#4.A Filtering execution to only projects in the programming dataset
cols = ['CODIGO_UNICO', 'FECHA_REGISTRO', 'FECHA_VIABLE_APROBADO', 'SEC_EJEC']
ex = ex.merge(pr[cols], how='inner', left_on='ACT_PROD_PROY', right_on='CODIGO_UNICO')


#3.A.1 Dropping unnecesary variables
ex = ex.drop(columns=['RUBRO', 'DESCRIP_RUBRO', 'DES_ACT_PROD_PROY', ])

#3.A.2 Encoding
cols = ['table', 'column', 'codes', 'labels']
label_dic = pd.DataFrame(columns = cols)

code_desc = [('COD_NIVEL', 'NIVEL_GOBIERNO'), \
             ('COD_SECTOR', 'NOMBRE_SECTOR'), \
             ('COD_PLIEGO', 'NOMBRE_PLIEGO'), \
             ('FUENTE', 'DESCRIP_FUENTE')]

#Recoding Sectors
ex.loc[(ex['COD_NIVEL'] == 3) | (ex['COD_SECTOR'] == 98), \
       'NOMBRE_SECTOR'] = 'REGIONES'
ex.loc[(ex['COD_NIVEL'] == 3) | (ex['COD_SECTOR'] == 98), \
       'COD_SECTOR'] = 100 # All regions

low_inf = [40, 39, 38, 35, 33, 32, 31, 27, 24, 22, 21, 20, 19, 12, 9, 8, 4, 1]

ex.loc[ex['COD_SECTOR'].isin(low_inf), 'NOMBRE_SECTOR'] = 'BAJA INTENSIDAD'
ex.loc[ex['COD_SECTOR'].isin(low_inf), 'COD_SECTOR'] = 101


for codes, desc in code_desc:
    label_dic = label_dic.append(categorize(ex, codes, desc), \
                                 ignore_index=True, sort=True)
label_dic.loc[:, 'table'] = 'execution'
label_dic = label_dic[cols].sort_values(cols)

#3.A.3 Setting Filters
ex['ok_temp'] = 0
ex.loc[(ex['COD_NIVEL'] < 3) & \
       (ex['CATEGORIA_GTO'] == 6) & \
       (ex['SEC_EJEC'].isnull() == False)
       , 'ok_temp'] = 1


ex['ok'] = ex.groupby('ACT_PROD_PROY')['ok_temp'].transform('max')

#3.A.3.i  Eliminating PIM == 0
ex['ok_pim0'] = 1

ex.loc[ex['MONTO_PIM'] == 0, 'ok_pim0'] = 0
ex.loc[ex['MONTO_PIM'] == 0, 'ok'] = 0


#3.A.4 Converting to panel data
ex = ex.drop(columns = ['NIVEL_GOBIERNO', 'NOMBRE_SECTOR', \
                        'NOMBRE_PLIEGO', 'CATEGORIA_GTO',  \
                        'DESCRIP_FUENTE', 'DES_CATEGORIA_GTO', \
                        'ACT_PROD_PROY'])

id_vars = ['CODIGO_UNICO', 'ANO_EJE', 'COD_NIVEL', 'COD_SECTOR', \
           'COD_PLIEGO', 'FUENTE']

#Pre- Melting vars
ex['pim_proj'] = ex.groupby(['CODIGO_UNICO', 'ANO_EJE'])['MONTO_PIM']. \
                    transform('sum')
ex['pim_ue_year'] = ex.groupby(['SEC_EJEC', 'ANO_EJE'])['MONTO_PIM']. \
                       transform('sum')
ex['pim_st_year'] = ex.groupby(['COD_SECTOR', 'ANO_EJE'])['MONTO_PIM']. \
                       transform('sum')

ex['pim_st_proj'] = ex.groupby(['CODIGO_UNICO', 'COD_SECTOR', 'ANO_EJE']) \
                          ['MONTO_PIM'].transform('sum')
ex['pim_ft_proj'] = ex.groupby(['CODIGO_UNICO', 'FUENTE', 'ANO_EJE']) \
                         ['MONTO_PIM'].transform('sum')
ex['pim_nv_proj'] = ex.groupby(['CODIGO_UNICO', 'COD_NIVEL', 'ANO_EJE']) \
                          ['MONTO_PIM'].transform('sum')

ex['pim_st_proj_pr'] = ex['pim_st_proj']/ex['pim_proj']
ex['pim_ft_proj_pr'] = ex['pim_ft_proj']/ex['pim_proj']
ex['pim_nv_proj_pr'] = ex['pim_nv_proj']/ex['pim_proj']




#3.A.4.i Renaming
value_vars = [c  for c in ex.columns if 'DEV_' in c]
rename_dic = {col: 'DEV_' + str(ind + 1) for (ind, col) in enumerate(value_vars)}

ex = ex.rename(columns = rename_dic)
value_vars = [c  for c in ex.columns if 'DEV_' in c]

other_vars = [c for c in ex.columns if c not in id_vars + value_vars]


#3.A.4.ii Melting
ex = ex.melt(id_vars=id_vars + other_vars, value_vars=value_vars)
ex = ex.rename(columns = {'variable': 'mes', 'value': 'dev_delta'})
ex['mes'] = ex['mes'].str.slice(start=4).astype('int64')

ex = ex.sort_values(id_vars + ['mes'])

ex['new_id'] = ex.groupby(id_vars).ngroup()

ex['CODIGO_UNICO'] = ex['CODIGO_UNICO'].astype('int64')


'''  ________________________________________
    |                                        |
    |           6: Panel Variables           |
    |________________________________________|'''


#Cumulative execution
ex['dev_acc'] = ex.groupby('new_id')['dev_delta'].cumsum()

#  Ratio
ex['dev_acc_pr'] = ex['dev_acc']/ex['MONTO_PIM']



# Project Ratio
ex = year_cumul(ex, 'CODIGO_UNICO', 'ok_pim0', 'dev_delta', 'dev_acc_proj')
ex['exec'] = ex['dev_acc_proj']/ex['pim_proj']

# UE Ratio
ex = year_cumul(ex, 'SEC_EJEC', 'ok_pim0', 'dev_delta', 'dev_acc_ue')
ex['exec_ue']  =ex['dev_acc_ue']/ex['pim_ue_year']


# Sector Ratio
ex = year_cumul(ex, 'COD_SECTOR', 'ok_pim0', 'dev_delta', 'dev_acc_st')
ex['exec_st']  =ex['dev_acc_st']/ex['pim_st_year']

#Monthly Execution
ex['dev_proj'] = ex.groupby(['CODIGO_UNICO', 'mes', 'ok'])['dev_delta'] \
                   .transform('sum')

# Participacion fuente
ex['dev_ft_month_sh'] = ex.groupby(['CODIGO_UNICO', 'FUENTE', 'mes', 'ok']) \
                     ['dev_delta'].transform('sum')/ex['dev_proj']
ex.loc[ex.dev_proj == 0, 'dev_ft_month_sh'] = 0

# Participacion Sector
ex['dev_st_month_sh'] = ex.groupby(['CODIGO_UNICO', 'COD_SECTOR', 'mes', 'ok']) \
                     ['dev_delta'].transform('sum')/ex['dev_proj']
ex.loc[ex.dev_proj == 0, 'dev_st_month_sh'] = 0

# Participacion Nivel
ex['dev_nv_month_sh'] = ex.groupby(['CODIGO_UNICO', 'COD_NIVEL', 'mes', 'ok']) \
                     ['dev_delta'].transform('sum')/ex['dev_proj']
ex.loc[ex.dev_proj == 0, 'dev_nv_month_sh'] = 0

# Año electoral
ex['elect_year'] = ex['ANO_EJE'].apply(lambda x: 1 if x in [2018, 2014, 2012] else 0)

# Primer Año
ex['first_year'] = ex['ANO_EJE'].apply(lambda x: 1 if x in [2019, 2015, 2013] else 0)


# Año electoral
ex['elect_presi_year'] = ex['ANO_EJE'].apply(lambda x: 1 if x in [2016, 2011] else 0)

# Primer Año
ex['first_presi_year'] = ex['ANO_EJE'].apply(lambda x: 1 if x in [2017, 2012] else 0)


# Getting rid of the projects outside the scopre

ex = ex.loc[ex['ok'] == 1]

# Expand Dummies

nv_dm = pd.get_dummies(ex['COD_NIVEL'], prefix='nv')
st_dm = pd.get_dummies(ex['COD_SECTOR'], prefix='st')
ft_dm = pd.get_dummies(ex['FUENTE'], prefix='ft')
mes_dm = pd.get_dummies(ex['mes'], prefix='mes')
ex = pd.concat([ex, nv_dm], axis=1)
ex = pd.concat([ex, st_dm], axis=1)
ex = pd.concat([ex, ft_dm], axis=1)
ex = pd.concat([ex, mes_dm], axis=1)

del nv_dm, st_dm, ft_dm, mes_dm


# molde de la data

df = ex.groupby(['CODIGO_UNICO', 'ANO_EJE' ,'mes']). \
        agg({
            'FECHA_REGISTRO': 'first',
            'FECHA_VIABLE_APROBADO': 'first',
            'SEC_EJEC': 'first',
            'dev_acc_proj': 'first',
            'exec':  'first',
            'dev_acc_ue': 'first',
            'exec_ue': 'first',
            'pim_proj': 'first',
            'dev_proj': 'first',
            'elect_year': 'first',
            'first_year': 'first',
            'elect_presi_year': 'first',
            'first_presi_year': 'first',
            'nv_1': 'max',
            'nv_2': 'max',
            'nv_3': 'max',
            'st_3': 'max',
            'st_5': 'max',
            'st_6': 'max',
            'st_7': 'max',
            'st_10': 'max',
            'st_11': 'max',
            'st_13': 'max',
            'st_16': 'max',
            'st_26': 'max',
            'st_36': 'max',
            'st_37': 'max',
            'st_99': 'max',
            'st_100': 'max',
            'st_101': 'max',
            'ft_1': 'max',
            'ft_2': 'max',
            'ft_3': 'max',
            'ft_4': 'max',
            'ft_5': 'max'
            }).reset_index()

# Bucle para ir llenando las expansiones

idd = ['CODIGO_UNICO', 'ANO_EJE', 'mes']

exp_pairs = [('pim_st_year', 'st'),
             ('pim_st_proj', 'st'),
             ('pim_ft_proj', 'ft'),
             ('pim_nv_proj', 'nv'),
             ('pim_st_proj_pr', 'st'),
             ('pim_ft_proj_pr', 'ft'),
             ('pim_nv_proj_pr', 'nv'),
             ('dev_acc_st', 'st'),
             ('exec_st', 'st'),
             ('dev_ft_month_sh', 'ft'),
             ('dev_st_month_sh', 'st'),
             ('dev_nv_month_sh', 'nv')
             ('mes', 'mes')]

for pair in exp_pairs:
    var, pref = pair
    temp, dummies = dummy_expand(ex, var, pref, idd)
    temp = temp.groupby(idd)[dummies].max()
    df = df.merge(temp, on=idd, how = 'left')



df['target'] = (df['mes'] == 12)*df['exec']
df['target'] = df.groupby(['CODIGO_UNICO', 'ANO_EJE'])['target'].transform('max')

df['ok'] = (df['mes'] <= 10)*1

'''  ________________________________________
    |                                        |
    |        7: "Static" Data Cleaning       |
    |________________________________________|'''

#Filtering  Static dataset

uni_proy = ex.loc[ex.ok == 1, ['CODIGO_UNICO', 'ok']].groupby('CODIGO_UNICO') \
           ['ok'].first().reset_index()

pr = pr.merge(uni_proy, on='CODIGO_UNICO', how='inner')

# Clasificacion del nombre
pr['NOMBRE_PROYECTO'] = pr['NOMBRE_PROYECTO'].apply(lambda x: str_clean(x))
pr['key_word'] = pr['NOMBRE_PROYECTO'].str.split(n=1).str.get(0)
names = pr['key_word'].value_counts().reset_index().\
                       rename(columns={'key_word': 'count', 'index': 'key_word'})

names['jw_old'] = names['key_word'].apply(lambda x: class_proj(x, OLD_PROJ))

names['jw_new'] = names['key_word'].apply(lambda x: class_proj(x, NEW_PROJ))

names['jw_int'] = names['key_word'].apply(lambda x: class_proj(x, INT_PROJ))

names['max'] = names.loc[:, ['jw_old','jw_new', 'jw_int']].max(axis=1)

names['class'] = 'und'
names.loc[names['jw_new'] == names['max'], 'class'] = 'new'
names.loc[names['jw_old'] == names['max'], 'class'] = 'old'
names.loc[names['jw_int'] == names['max'], 'class'] = 'int'
names.loc[names['max'] < JW_MIN, 'class'] = 'und'

pr = pr.merge(names[['key_word', 'class']], on='key_word', how = 'left')


pr = pr.loc[:, ['CODIGO_UNICO', 'MONTO_VIABLE_APROBADO', 'reg_count', 'class']]


'''  ________________________________________
    |                                        |
    |         9: Time Series Operators       |
    |________________________________________|'''

def last_non_zero(vals):
    rv = [x for x  in vals if x != 0.0]
    if rv:
        return rv[-1]
    else:
        return 0.0

def time_to_last(vals):
    vals = vals.tolist()
    count = 0
    while len(vals) > 0 and vals[-1] == 0.0:
        _ = vals.pop(-1)
        count += 1
    return count



def win_lag(vals):
    if len(vals) > 0:
        return vals[0]
    return 0.0

def win_delta(vals):
    if len(vals) > 0:
        return vals[0] - vals[-1]
    return 0.0


# Create Dates
df['year'] = df['ANO_EJE']
df['month'] = df['mes'] + 1
df.loc[df.month == 13, 'year'] = df['year']  + 1
df.loc[df.month == 13, 'month'] = 1
df['day'] = 1

df['date'] = pd.to_datetime(df[['year', 'month', 'day']]) - \
             pd.to_timedelta(1, unit='d')

df = df.set_index('date')

# Windows

windows = [3, 6, 12]


df = df.sort_values(idd)

for var in vl.last_nz:
    df[var + '_12m_last'] = df.groupby('CODIGO_UNICO')['exec'] \
        .rolling(window=12, freq='M') \
        .apply(lambda x: last_non_zero(x)) \
        .reset_index(0, drop=True)

for var in vl.lag_vars:
    for w in windows:
        df[var + '_' + str(w) + 'm_lag'] = df.groupby('CODIGO_UNICO')[var] \
            .rolling(window=w, freq='M', min_periods=w) \
            .apply(lambda x: win_lag(x)) \
            .reset_index(0, drop=True)

for var in vl.mean_vars:
    for w in windows:
        df[var + '_' + str(w) + 'm_mean'] = df.groupby('CODIGO_UNICO')[var] \
            .rolling(window=w, freq='M', min_periods=w) \
            .mean() \
            .reset_index(0, drop=True)

for var in vl.time_to_vars:
    df[var + '_time_nz'] = df.groupby('CODIGO_UNICO')[var] \
        .rolling(window=w, freq='M', min_periods=w) \
        .apply(lambda x: time_to_last(x)) \
        .reset_index(0, drop=True)

for var in vl.year_lag:
    df[var + '_12m_lag'] = df.groupby('CODIGO_UNICO')[var] \
        .rolling(window=w, freq='M', min_periods=w) \
        .apply(lambda x: win_lag(x)) \
        .reset_index(0, drop=True)

for var in vl.year_delta:
    df[var + '_12m_delta'] = df.groupby('CODIGO_UNICO')[var] \
        .rolling(window=w, freq='M', min_periods=w) \
        .apply(lambda x: win_delta(x)) \
        .reset_index(0, drop=True)


enaho = enaho.sort_values(['dpto','anio'])

dmg_vars = [col for col in enaho.columns if col not in ['dpto','anio']]
for var in dmg_vars:
    enaho[var + '_12m_delta'] = enaho.groupby('dpto')[var] \
        .rolling(window=1, min_periods=1) \
        .apply(lambda x: win_delta(x)) \
        .reset_index(0, drop=True)


'''  ________________________________________
    |                                        |
    |             8: Regional Data           |
    |________________________________________|'''


ubi['CODIGO_UNICO'] = ubi['CODIGO_UNICO'].astype('int64')
ubi = ubi.merge(uni_proy, on = 'CODIGO_UNICO', how = 'right')


ubi['dpto'] = ubi['UBIGEO'].astype('str').str.slice(stop=2).astype('int64')
ubi = ubi.groupby(['CODIGO_UNICO', 'dpto'])['ok'].first().reset_index()

ubi['weight'] =1/ubi.groupby('CODIGO_UNICO')['ok'].transform('count')

ubi = ubi.merge(enaho, on='dpto', how = 'left')

ubi['uni_dpto'] = (ubi['weight'] == 1.0)*1
ubi = ubi.rename(columns={'anio': 'ANO_EJE'})

multi = ubi.loc[ubi.uni_dpto == 0]

w_ave = lambda x: np.average(x, weights=multi.loc[x.index, "weight"])

multi = multi.groupby(['CODIGO_UNICO', 'ANO_EJE']).agg(w_ave).reset_index()
multi['dpto'] = 0

dmg = ubi.loc[ubi.uni_dpto == 1].append(multi, ignore_index=True, sort=True)
dmg.loc[ubi.dpto > 25, 'dpto'] = 0
dmg = dmg.drop(columns='ok')


'''  ________________________________________
    |                                        |
    |        10: Data Consolidation          |
    |________________________________________|'''

df = df.merge(pr, on='CODIGO_UNICO', how='left')
df = df.merge(dmg, on=['CODIGO_UNICO', 'ANO_EJE'], how='left')
df = df.sort_values(['CODIGO_UNICO', 'ANO_EJE', 'mes'])

#Last variable
df['tag_proy'] = (df['mes'] == 12)*1
df['reg_count'] = df.groupby(['CODIGO_UNICO', 'ANO_EJE'])['tag_proy'].transform('sum')


anual_tg = df.groupby(['CODIGO_UNICO', 'ANO_EJE']).agg({'target': 'first',
                                                        'pim_proj': 'first',
                                                        'dev_acc_proj': 'last',
                                                        'reg_count': 'first'})
anual_tg = anual_tg.reset_index()
ubi = ubi.merge(anual_tg, on=['CODIGO_UNICO', 'ANO_EJE'], how='left')
ubi = ubi.loc[ubi.dpto <= 25]
ubi = ubi.loc[ubi.target.isnull() == False]

w_ave = lambda x: np.average(x, weights=ubi.loc[x.index, "weight"])
mapa_uni = ubi.loc[ubi.uni_dpto == 1].groupby(['dpto', 'ANO_EJE']) \
      ['target', 'pim_proj' ,'dev_acc_proj' ,'tag_proy'].agg(w_ave).reset_index()

mapa_multi = ubi.loc[ubi.uni_dpto == 0].groupby(['dpto', 'ANO_EJE']) \
      ['target', 'pim_proj' ,'dev_acc_proj' ,'tag_proy'].agg(w_ave).reset_index()

'''  ________________________________________
    |                                        |
    |                6: EXPORT               |
    |________________________________________|'''


df.to_csv(r'data/clean/df.csv', index=False)
mapa_uni.to_csv(r'data/clean/mapa_uni.csv', index=False)
mapa_multi.to_csv(r'data/clean/mapa_multi.csv', index=False)
label_dic.to_csv(r'data/clean/labels.csv', index=False)






