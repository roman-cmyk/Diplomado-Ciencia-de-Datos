#!/usr/bin/env python
# coding: utf-8

# <h1 style="color:blue"> LIBRERIAS </h1>

# In[5]:


import pandas as pd
import numpy as np
import datetime
import re
import os
import unicodedata
import warnings
from nltk.corpus import stopwords
import nltk
from IPython.display import Image 
pd.options.display.max_columns = None
pd.set_option('max_rows',500)
warnings.filterwarnings('ignore')
nltk.download('stopwords')
from decimal import Decimal


# ## Read dataset

# In[6]:


# Importamos dataset y lo asignamos a la variable df
df = pd.read_csv('data_examen_2_.csv')

# Convertimos todo a minúsculas
df.columns = df.columns.map(str.lower)

# Mostramos la dimensión del dataset
print(df.shape)

# Imprimimos primeros 5 registros
df.head(5)


# In[7]:


# Importamos dataset y lo asignamos a la variable ocupaciones
ocupaciones = pd.read_csv('ocupaciones_examen2.csv')

# Convertimos todo a minúsculas
ocupaciones.columns = ocupaciones.columns.map(str.lower)

# Mostramos la dimensión del dataset
print(ocupaciones.shape)

# Mostramos los primeros 5 registros
ocupaciones.head(5)


# <h1 style="color:blue"> IMPORTAMOS LIBRERÍA PERSONALIZADA </h1>

# In[8]:


get_ipython().run_line_magic('run', "'/home/roman/Documents/Diplomado en Ciencia de Datos - UNAM FES Acatlán/Módulo 1/Examen/Examen 2/Classroom/examen_2_francisco_roman_peña_dela_rosa_libreria.ipynb'")


# <h1 style="color:blue"> CALIDAD DE DATOS </h1>

# ## ETIQUETADO DE VARIABLES

# In[9]:


df.head(5)


# In[10]:


df.columns


# In[11]:


# Definimos generador para tener mejor acceso al nombre de las columnas
gen_columns = (col for col in df.columns)


# In[12]:


# Prefixes for variable types
# 'c_' --> Numeric Variables: Discrete & Continous
# 'v_' --> Categorical Variables
# 'd_' --> Date Type Variables
# 't_' --> Text Type Variables

# Numeric Variables: Discrete & Continous
c_feats = ['age','quant_dependants','months_in_residence','months_in_the_job','mate_income','quant_banking_accounts',
          'personal_net_income','quant_additional_cards_in_the_application','shop_rank','payment_day']

#Categorical Variables
v_feats = ['id_client','id_shop','sex','marital_status','education','flag_residencial_phone','area_code_residencial_phone',
          'residence_type','flag_mothers_name','flag_fathers_name','flag_residence_town=working_town',
          'flag_residence_state=working_state','profession_code','flag_residencial_address=postal_address','flag_other_card',
          'flag_mobile_phone','flag_contact_phone','cod_application_booth','flag_card_insurance_option','tgt']
# Date Type Variables
d_feats = []

#Text Type Variables
t_feats = ['personal_reference_#1','personal_reference_#2']


# In[13]:


# Etiquetamos columnas
df = label_columns(df,c_feats,"c_")
df = label_columns(df,v_feats,"v_")
df = label_columns(df,t_feats,"t_")
df = label_columns(df,d_feats,"d_")


# In[14]:


# Visualizamos cinco primeros registros para validar etiquetado de variables
print(df.shape)
df.head(5)


# In[15]:


df.columns


# ## DUPLICIDAD

# ### Identificamos duplicados y los eliminamos a través del método 'df.drop_duplicates'

# In[16]:


# Asignamos una copia del dataframe (df) original a "df1" para aplicar el método 'df.drop_duplicates'
df1 = df.copy(deep = True)
print(df1.shape)
df1.head(5)


# In[17]:


# Obtenemos el total de registros duplicados en el dataset
df1.duplicated().sum()


# In[18]:


# Identificamos los 5 registros dupicados
df1[df1.duplicated()]


# In[19]:


# Una vez cuantificados e identificados, procedemos a eliminar duplicados
df1.drop_duplicates(inplace = True)
print(df1.shape)
df1.head(5)


# ### Identificamos duplicados y los eliminamos a través del método de llave 'v_id_client'

# In[20]:


# Asignamos una copia del dataframe (df) original a "df2" para aplicar el método de llave 'v_id_client'
df2 = df.copy(deep = True)
print(df2.shape)
df2.head(5)


# In[21]:


# Eliminamos los registros duplicados por medio a través de la llave 'v_id_client'
df2 = df2.drop_duplicates(subset=['v_id_client','v_id_shop'],keep="first")
print(df2.shape)
df2.head(5)


# ### Comparamos los resultados de la identificación de duplicados por ambos métodos

# In[22]:


# Mostramos la dimensión del DataFrame 'df1' y los primeros 5 registros
print(df1.shape)
df1.head(5)


# In[23]:


# Mostramos la dimensión del DataFrame 'df2' y los primeros 5 registros
print(df2.shape)
df2.head(5)


# ## COMPLETITUD

# ### Analizamos completitud del DataFrame 'df1'

# In[24]:


# Analizamos completitud de 'df1'
completitud(df1).style.background_gradient()


# ### Analizamos completitud del DataFrame 'df2'

# In[25]:


# Analizamos completitud de 'df2'
completitud(df2).style.background_gradient()


# ## CONSISTENCIA Y CONFORMIDAD

# In[26]:


df1.info()


# In[27]:


df2.info()


# ## NORMALIZACIÓN

# ### CONSISTENCIA

# * Después de analizar el comportamiento de los "**Duplicados**" y la "**Completitud**", procedemos a trabajar con el DataFrame "**df2**"

# In[28]:


df2.head(5)


# #### Revisamos consistencia de **"v_id_shop"**

# In[29]:


# Convertimos la variable 'v_id_shop' a "integer"
df2['v_id_shop'] = df2['v_id_shop'].astype(int)


# #### Revisamos consistencia de **"v_sex"**

# In[30]:


# Normalizamos los valor a M y F, y los valores identificados como n.a. son reemplazados como 'NaN'
df2['v_sex'] = df2['v_sex'].apply(lambda row: sex(row))
df2.head(5)


# #### Revisamos consistencia de **"v_marital_status"**

# In[31]:


df2['v_marital_status'].unique()


# In[32]:


# Cambiamos a formato "string" la variable 'v_marital_status'
df2['v_marital_status'] = df2['v_marital_status'].astype(str)


# In[33]:


df2['v_marital_status'] = df2['v_marital_status'].apply(lambda row: marital(row))


# In[34]:


df2['v_marital_status'].unique()


# #### Revisamos consistencia de **"v_age"**

# In[35]:


for i in df2['c_age'].unique():
    print(i)


# In[36]:


# Convertimos el formato de object to string
df2['c_age'] = df2['c_age'].astype(str)


# In[37]:


df2['c_age'] = df2['c_age'].replace('nan','0')


# In[38]:


df2['c_age'] = df2['c_age'].astype(float).astype(int)


# #### Revisamos consistencia de **"c_quant_dependants"**

# In[39]:


# Revisamos la variable "c_quant_dependants"
df2['c_quant_dependants'].unique() # Toda la variable contiene ceros en los diferentes registros, no se considera
                                         # necesario normalizarla


# #### Revisamos consistencia de **"v_education"**

# In[40]:


# Revisamos la variable "v_education"
df2['v_education'].unique() # Todos los registros de la variable se encuentran como 'NaN', no consideramos
                                # necerario normalizarla


# #### Revisamos consistencia de **"v_flag_residencial_phone'"**

# In[41]:


# Convertimos el formato de object a string
df2['v_flag_residencial_phone'] = df2['v_flag_residencial_phone'].astype(str) 


# In[42]:


df2.columns


# #### Revisamos consistencia de **"v_area_code_residencial_phone'"**

# In[43]:


# Convertimos el formato de object a integer
df2['v_area_code_residencial_phone'] = df2['v_area_code_residencial_phone'].astype(int) 


# #### Revisamos consistencia de **"c_payment_day'"**

# In[44]:


# Convertimos el formato de object a integer
df2['c_payment_day'] = df2['c_payment_day'].astype(int) 


# #### Revisamos consistencia de **"c_shop_rank'"**

# In[45]:


# Convertimos el formato de object a integer
df2['c_shop_rank'] = df2['c_shop_rank'].astype(int) 


# #### Revisamos consistencia de **"v_residence_type'"**

# In[46]:


df2['v_residence_type'].unique()


# In[47]:


# Convertimos el formato de object a string
df2['v_residence_type'] = df2['v_residence_type'].astype(str) 


# In[48]:


df2['v_residence_type'] = df2['v_residence_type'].apply(lambda row: residence(row))


# In[49]:


df2['v_residence_type'].unique()


# #### Revisamos consistencia de **"c_months_in_residence'"**

# In[50]:


# Convertimos el formato de object a string
df2['c_months_in_residence'] = df2['c_months_in_residence'].astype(str) 


# #### Revisamos consistencia de **"v_flag_mothers_name'"**

# In[51]:


# Convertimos el formato de object a string
df2['v_flag_mothers_name'] = df2['v_flag_mothers_name'].astype(str) 


# #### Revisamos consistencia de **"v_flag_fathers_name'"**

# In[52]:


# Convertimos el formato de object a string
df2['v_flag_fathers_name'] = df2['v_flag_fathers_name'].astype(str) 


# #### Revisamos consistencia de **"v_flag_residence_town=working_town'"**

# In[53]:


# Convertimos el formato de object a string
df2['v_flag_residence_town=working_town'] = df2['v_flag_residence_town=working_town'].astype(str) 


# #### Revisamos consistencia de **"v_flag_residence_state=working_state'"**

# In[54]:


# Convertimos el formato de object a string
df2['v_flag_residence_state=working_state'] = df2['v_flag_residence_state=working_state'].astype(str) 


# #### Revisamos consistencia de **"c_months_in_the_job'"**

# In[55]:


# Convertimos el formato de object a integer
df2['c_months_in_the_job'] = df2['c_months_in_the_job'].astype(int) 


# #### Revisamos consistencia de **"v_profession_code"**

# In[56]:


# Convertimos el formato de object a integer
df2['v_profession_code'] = df2['v_profession_code'].astype(int) 


# #### Revisamos consistencia de **"c_mate_income"**

# In[57]:


for i in df2['c_mate_income'].unique():
    print(i)


# In[58]:


# Convertimos el formato de object a integer
df2['c_mate_income'] = df2['c_mate_income'].astype(str)


# In[59]:


df2['c_mate_income'] = df2['c_mate_income'].str.replace('nan','0')


# In[60]:


for i in df2['c_mate_income'].unique():
    print(i)


# In[61]:


df2['c_mate_income'] = df2['c_mate_income'].astype(float).astype(int)


# In[62]:


for i in df2['c_mate_income'].unique():
    print(i)


# #### Revisamos consistencia de **"v_flag_residencial_address=postal_address"**

# In[63]:


# Convertimos el formato de object a string
df2['v_flag_residencial_address=postal_address'] = df2['v_flag_residencial_address=postal_address'].astype(str) 


# #### Revisamos consistencia de **"v_flag_other_card"**

# In[64]:


# Convertimos el formato de object a string
df2['v_flag_other_card'] = df2['v_flag_other_card'].astype(str) 


# #### Revisamos consistencia de **"c_quant_banking_accounts"**

# In[65]:


# Convertimos el formato de object a integer
df2['c_quant_banking_accounts'] = df2['c_quant_banking_accounts'].astype(int) 


# #### Revisamos consistencia de **"t_personal_reference_#1"**

# In[66]:


# Convertimos el formato de object a string
df2['t_personal_reference_#1'] = df2['t_personal_reference_#1'].replace('nan',np.nan)
df2['t_personal_reference_#1'] = df2['t_personal_reference_#1'].astype(str) 


# #### Revisamos consistencia de **"t_personal_reference_#2"**

# In[67]:


# Convertimos el formato de object a string
df2['t_personal_reference_#2'] = df2['t_personal_reference_#2'].replace('nan',np.nan)
df2['t_personal_reference_#2'] = df2['t_personal_reference_#2'].astype(str)


# #### Revisamos consistencia de **"v_flag_mobile_phone"**

# In[68]:


# Convertimos el formato de object a string
df2['v_flag_mobile_phone'] = df2['v_flag_mobile_phone'].astype(str) 


# #### Revisamos consistencia de **"v_flag_contact_phone"**

# In[69]:


# Convertimos el formato de object a string
df2['v_flag_contact_phone'] = df2['v_flag_contact_phone'].astype(str) 


# #### Revisamos consistencia de **"c_personal_net_income"**

# In[70]:


for i in df2['c_personal_net_income'].unique():
    print(i)


# In[71]:


df2['c_personal_net_income'] = df2['c_personal_net_income'].str.replace('n.a.','0')


# In[72]:


df2['c_personal_net_income'] = df2['c_personal_net_income'].astype(int)


# #### Revisamos consistencia de **"v_cod_application_booth"**

# In[73]:


# Convertimos el formato de object a integer
df2['v_cod_application_booth'] = df2['v_cod_application_booth'].astype(int)


# #### Revisamos consistencia de **"c_quant_additional_cards_in_the_application"**

# In[74]:


# Convertimos el formato de object a integer
df2['c_quant_additional_cards_in_the_application'] = df2['c_quant_additional_cards_in_the_application'].astype(int)


# #### Revisamos consistencia de **"v_flag_card_insurance_option"**

# In[75]:


# Convertimos el formato de object a string
df2['v_flag_card_insurance_option'] = df2['v_flag_card_insurance_option'].astype(str)


# #### Revisamos consistencia de **"v_tgt"**

# In[76]:


# Convertimos el formato de object a integer
df2['v_tgt'] = df2['v_tgt'].astype(int)


# In[77]:


df2.dtypes


# ## ELIMINAR VARIABLES CON COMPLETITUD MENOR AL 80%

# In[78]:


completitud(df2).style.background_gradient()


# In[79]:


# Eliminamos variables con valor de completitud menor al 80%
df2 = df2.drop(columns = ['v_education'])


# In[80]:


# Mostramos nueva dimensión de df2 y primeros 5 registros
print(df2.shape)
df2.head(5)


# ## CRUCE CON TABLA DE OCUPACIONES

# * Cruce con la tabla de ocupaciones

# In[81]:


# Mostramos los primeros 5 registros de la tabla 'ocupaciones'
ocupaciones.head(5)


# In[82]:


# Realizamos cruce con la tabla de 'ocupaciones'
df2 = df2.merge(ocupaciones, right_on = 'profession_code', left_on = 'v_profession_code', how = 'left')
df2.drop(columns = 'profession_code', inplace = True)
df2.head(5)


# In[83]:


# Mostramos la nueva dimensión de df2, después de haber hecho el cruce
df2.shape


# <h1 style="color:blue"> ANÁLISIS EXPLORATORIO DE DATOS (EDA) </h1>

# * Realice análisis interesantes sobre los datos proporcionados , generé gráficas representativas.
# 
# 
# * Se deben realizar al menos el análisis de 4 variables , los análisis deben estar acompañados de una gráfica por variables analizada y en el PDF de entrega deben estar las gráficas acompañadas con la descripción de qué representa ese análisis.
# 

# ### Variable analizada: **c_age**

# In[84]:


# Distribución de la variable c_age
my_histogram(df2,'c_age',bins = 85,title = 'Distribución de la Edad',x_title = '',y_title = 'Conteo')


# In[85]:


# Mostramos el comportamiento de la "**Edad**" de las personas que solicitan un crédito VS el "**Sexo**"
my_box(df2,'v_sex','c_age',title = 'Distribución de la Edad', x_title = 'Sexo',y_title = 'Edad')


# In[86]:


fig = px.histogram(df2[['c_age','v_sex']], x='c_age', color='v_sex', marginal="box")
fig.show()


# ### Variable analizada: **c_mate_income**

# In[87]:


# Mostramos la distribución del "**Ingreso Mate"
my_histogram(df2,'c_mate_income',bins = 50,title = 'Distribución del Mate Income',x_title = '',y_title = 'Conteo')


# In[88]:


# Mostramos el comportamiento del "**c_mate_income**" VS "**v_sex**"
fig = px.bar(df2, x = 'v_sex', y = 'c_mate_income', color = 'v_sex', barmode="group")
fig.show()


# ### Variable analizada: **c_personal_net_income**

# In[89]:


# Mostramos la distribución del "**c_personal_net_income**"
my_histogram(df2,'c_personal_net_income',bins = 50,title = 'Distribución del Ingreso Neto',x_title = '',y_title = 'Conteo')


# In[90]:


# Mostramos el comportamiento del "**c_personal_net_income**" VS "**v_sex**"
fig = px.bar(df2, x = 'v_sex', y = 'c_personal_net_income', color = 'v_sex', barmode="group")
fig.show()


# ### Variable analizada: **v_sex**

# In[91]:


# Mostramos la proporción de los datos para "**v_sex**"
my_pie_count(df2,'v_sex',title = 'Porcentaje de Hombres y Mujeres que Solicitan Crédito')


# ### Variable analizada: **v_marital_status**

# In[92]:


# Mostramos la proporción de los datos para "**v_marital_status**"
my_pie_count(df2,'v_marital_status',title = 'Porcentaje de Personas por Estado Civil')


# ### Variable analizada: **c_months_in_the_job**

# In[93]:


# Mostramos la distribución de los datos para "**c_months_in_the_job**"
my_histogram(df2,'c_months_in_the_job',bins = 30,title = 'Distribución del Número de Meses en el Trabajo',x_title='Meses',y_title='Conteo')


# ### Variable analizada: **v_residence_type**

# In[94]:


# Mostramos la proporción de los datos para "**v_residence_type**"
my_pie_count(df2,'v_residence_type',title = 'Porcentaje de Personas por Tipo de Vivienda')


# In[95]:


# Mostramos el comportamiento del "**c_mate_income**" VS "**v**"
vivienda = px.histogram(df2[['v_residence_type','v_sex']], x='v_residence_type', color='v_sex', marginal="box")
vivienda.show()


# ### Variable analizada: **c_payment_day**

# In[96]:


# Análisis de la distribución de la variable c_age
my_bar_count(df2,'c_payment_day',title = 'Distribución del Día de Pago',x_title = 'Dia', y_title = 'Conteo')


# <h1 style="color:blue"> TRATAMIENTO I </h1>

# * Realice dos copias de la tabla limpia y haga lo siguiente con una de las tablas que debe llevar por nombre **tratamiento 1**:

# In[97]:


tratamiento_1 = df2.copy(deep = True)
print(tratamiento_1.shape)
tratamiento_1.head(5)


# In[98]:


display(tratamiento_1.dtypes)


# ## DATOS ANÓMALOS

# In[99]:


# Búsqueda de datos anómalos
feats = list(tratamiento_1.filter(like = 'c_').columns)
feats


# ### GRÁFICOS DE DATOS ANÓMALOS - **CON OUTLIERS**

# #### **c_age**

# In[100]:


# Comparando - 'c_quant_dependants'
# Distribución con Outliers
# Revisamos la variable "c_quant_dependants"
tratamiento_1['c_age'].iplot(kind='box', color = 'blue')


# In[101]:


# Aplicamos el método de "IQR" para identificar datos anómalos en la variable "c_age"
results = pd.DataFrame()
total = []
indices_=[]
Q1 = tratamiento_1['c_age'].quantile(0.25)
Q3 = tratamiento_1['c_age'].quantile(0.75)
IQR = Q3-Q1
INF = Q1-1.5*(IQR)
SUP = Q3+1.5*(IQR)
    
        
n_outliers = tratamiento_1[(tratamiento_1['c_age'] < INF) | (tratamiento_1['c_age'] > SUP)].shape[0]
total.append(n_outliers)
indices_iqr = list(tratamiento_1[(tratamiento_1['c_age'] < INF) | (tratamiento_1['c_age'] > SUP)].index)
results['n_outliers_IQR'] = total
results['n_outliers_IQR_%'] = round((results['n_outliers_IQR']/tratamiento_1.shape[0])*100,2)
#results['indices'] = indices_iqr
results


# In[102]:


indices_iqr


# In[103]:


# Aplicamos el método de "Percentiles" para identificar datos anómalos en la variable "c_age"
results = pd.DataFrame()
total = []
total_per = []
INF_pe = np.percentile(tratamiento_1['c_age'].dropna(),5)
    
SUP_pe = np.percentile(tratamiento_1['c_age'].dropna(),95)
n_outliers_per = tratamiento_1[(tratamiento_1['c_age'] < INF_pe) | (tratamiento_1['c_age'] > SUP_pe)].shape[0]
total_per.append(n_outliers_per)
indices_per = list(tratamiento_1[(tratamiento_1['c_age'] < INF_pe) | (tratamiento_1['c_age'] > SUP_pe)].index)
results['n_outliers_Percentil'] = total_per
results['n_outliers_Percentil_%']=round((results['n_outliers_Percentil']/tratamiento_1.shape[0])*100,2)
results


# In[104]:


# Aplicamos el método de "Z-Score" para identificar datos anómalos en la variable "c_mate_income"    
total_z = []
z = np.abs(stats.zscore(tratamiento_1['c_age'],nan_policy = 'omit'))
total_z.append(tratamiento_1[['c_age']][(z >= 3)].shape[0])
indices_z=list(tratamiento_1[['c_age']][(z >= 3)].index)
results["n_outliers_Z_Score"] = total_z
results["n_outliers_Z_Score_%"]=round((results["n_outliers_Z_Score"]/tratamiento_1.shape[0])*100,2)
results


# * **No** utilizamos el método de Z-Score porque la distribución de nuestra variable "c_net_personal_net_income" no tiene el comportamiento de una distribución Normal.

# #### **c_quant_dependants**

# In[105]:


# Comparando - 'c_quant_dependants'
# Distribución con Outliers
# Revisamos la variable "c_quant_dependants"
tratamiento_1['c_quant_dependants'].iplot(kind='box', color = 'blue')


# * Toda la variable contiene ceros en los registros.
# 

# #### **c_months_in_residence**

# In[106]:


# Comparando - 'c_months_in_residence'
# Distribución con Outliers
# Toda la variable contiene ceros en los diferentes registros, no se consideró necesario homologarla
tratamiento_1['c_months_in_residence'].iplot(kind='box', color = 'blue')


# #### **c_months_in_the_job**

# In[107]:


# Comparando - 'c_months_in_residence'
# Distribución con Outliers
# Toda la variable contiene ceros en los diferentes registros, no se consideró necesario homologarla
tratamiento_1['c_months_in_the_job'].iplot(kind='box', color = 'blue')


# #### **c_mate_income**

# In[108]:


# Comparando - 'c_mate_income'
# Distribución con Outliers
tratamiento_1['c_mate_income'].iplot(kind='box', color = 'blue')


# In[109]:


# Aplicamos el método de "IQR" para identificar datos anómalos en la variable "c_mate_income"
results = pd.DataFrame()
total = []
indices_=[]
Q1 = tratamiento_1['c_mate_income'].quantile(0.25)
Q3 = tratamiento_1['c_mate_income'].quantile(0.75)
IQR = Q3-Q1
INF = Q1-1.5*(IQR)
SUP = Q3+1.5*(IQR)
    
        
n_outliers = tratamiento_1[(tratamiento_1['c_mate_income'] < INF) | (tratamiento_1['c_mate_income'] > SUP)].shape[0]
total.append(n_outliers)
indices_iqr = list(tratamiento_1[(tratamiento_1['c_mate_income'] < INF) | (tratamiento_1['c_mate_income'] > SUP)].index)
results['n_outliers_IQR'] = total
results['n_outliers_IQR_%'] = round((results['n_outliers_IQR']/df.shape[0])*100,2)
#results['indices'] = indices_iqr
results


# In[110]:


indices_iqr


# In[111]:


# Aplicamos el método de "Percentiles" para identificar datos anómalos en la variable "c_mate_income"
results = pd.DataFrame()
total = []
total_per = []
INF_pe = np.percentile(tratamiento_1['c_mate_income'].dropna(),5)
SUP_pe = np.percentile(tratamiento_1['c_mate_income'].dropna(),95)
n_outliers_per = tratamiento_1[(tratamiento_1['c_mate_income'] < INF_pe) | (tratamiento_1['c_mate_income'] > SUP_pe)].shape[0]
total_per.append(n_outliers_per)
indices_per = list(tratamiento_1[(tratamiento_1['c_mate_income'] < INF_pe) | (tratamiento_1['c_mate_income'] > SUP_pe)].index)
results['n_outliers_Percentil'] = total_per
results['n_outliers_Percentil_%']=round((results['n_outliers_Percentil']/tratamiento_1.shape[0])*100,2)
results


# In[112]:


indices_per


# In[113]:


# Aplicamos el método de "Z-Score" para identificar datos anómalos en la variable "c_mate_income"    
total_z = []
z = np.abs(stats.zscore(tratamiento_1['c_mate_income'],nan_policy = 'omit'))
total_z.append(tratamiento_1[['c_mate_income']][(z >= 3)].shape[0])
indices_z=list(tratamiento_1[['c_mate_income']][(z >= 3)].index)
results["n_outliers_Z_Score"] = total_z
results["n_outliers_Z_Score_%"]=round((results["n_outliers_Z_Score"]/tratamiento_1.shape[0])*100,2)
results


# In[114]:


indices_z


# * **No** utilizamos el método de Z-Score porque la distribución de nuestra variable "c_net_personal_net_income" no tiene el comportamiento de una distribución Normal.

# #### **c_quant_banking_accounts**

# In[115]:


# Comparando - 'c_quant_banking_accounts'
# Distribución con Outliers
# Toda la variable contiene ceros en los diferentes registros, no se consideró necesario homologarla
tratamiento_1['c_quant_banking_accounts'].iplot(kind='box', color = 'blue')


# #### **c_personal_net_income**

# In[116]:


# Comparando - 'c_personal_net_income'
# Distribución con Outliers
tratamiento_1['c_personal_net_income'].iplot(kind='box', color = 'blue')


# In[117]:


# Aplicamos el método de "IQR" para identificar datos anómalos en la variable "c_personal_net_income"
results = pd.DataFrame()
total = []
Q1 = tratamiento_1['c_personal_net_income'].quantile(0.25)
Q3 = tratamiento_1['c_personal_net_income'].quantile(0.75)
IQR = Q3 - Q1
INF = Q1 - 1.5*(IQR)
SUP = Q3 + 1.5*(IQR)
    
        
n_outliers = tratamiento_1[(tratamiento_1['c_personal_net_income'] < INF) | (tratamiento_1['c_personal_net_income'] > SUP)].shape[0]
total.append(n_outliers)
indices_iqr = list(tratamiento_1[(tratamiento_1['c_personal_net_income'] < INF) | (tratamiento_1['c_personal_net_income'] > SUP)].index)
results['n_outliers_IQR'] = total
results['n_outliers_IQR_%'] = round((results['n_outliers_IQR']/tratamiento_1.shape[0])*100,2)
results


# In[118]:


# Aplicamos el método de "Percentiles" para identificar datos anómalos en la variable "c_personal_net_income"
results = pd.DataFrame()
total = []
total_per = []
INF_pe = np.percentile(tratamiento_1['c_personal_net_income'].dropna(),5)
    
SUP_pe = np.percentile(tratamiento_1['c_personal_net_income'].dropna(),95)
n_outliers_per = tratamiento_1[(tratamiento_1['c_personal_net_income'] < INF_pe) | (tratamiento_1['c_personal_net_income'] > SUP_pe)].shape[0]
total_per.append(n_outliers_per)
indices_per = list(tratamiento_1[(tratamiento_1['c_personal_net_income'] < INF_pe) | (tratamiento_1['c_personal_net_income'] > SUP_pe)].index)
results['n_outliers_Percentil'] = total_per
results['n_outliers_Percentil_%'] = round((results['n_outliers_Percentil']/tratamiento_1.shape[0])*100,2)
results


# In[119]:


# Aplicamos el método de "Z-Score" para identificar datos anómalos en la variable "c_mate_income"    
total_z = []
z = np.abs(stats.zscore(tratamiento_1['c_personal_net_income'],nan_policy = 'omit'))
total_z.append(tratamiento_1[['c_personal_net_income']][(z >= 3)].shape[0])
indices_z=list(tratamiento_1[['c_personal_net_income']][(z >= 3)].index)
results["n_outliers_Z_Score"] = total_z
results["n_outliers_Z_Score_%"]=round((results["n_outliers_Z_Score"]/tratamiento_1.shape[0])*100,2)
results


# * **No** utilizamos el método de Z-Score porque la distribución de nuestra variable "c_net_personal_net_income" no tiene el comportamiento de una distribución Normal.

# #### **c_quant_additional_cards_in_the_application**

# In[120]:


# Comparando - 'c_quant_additional_cards_in_the_application'
# Distribución con Outliers
tratamiento_1['c_quant_additional_cards_in_the_application'].iplot(kind='box', color = 'blue')


# ### GRÁFICOS DE DATOS ANÓMALOS - **SIN OUTLIERS**

# #### **c_age**

# In[121]:


tratamiento_1['c_age'].iplot(kind='box', color = 'orange')


# #### **c_quant_dependants**

# In[122]:


tratamiento_1['c_quant_dependants'].iplot(kind='box', color = 'orange')


# #### **c_months_in_residence**

# In[123]:


tratamiento_1['c_months_in_residence'].iplot(kind='box', color = 'orange')


# #### **c_months_in_the_job**

# In[124]:


tratamiento_1['c_months_in_the_job'].iplot(kind='box', color = 'orange')


# #### **c_mate_income**

# In[125]:


tratamiento_1['c_mate_income'].iplot(kind='box', color = 'orange')


# #### **c_quant_banking_accounts**

# In[126]:


tratamiento_1['c_quant_banking_accounts'].iplot(kind='box', color = 'orange')


# #### **c_personal_net_income**

# In[127]:


tratamiento_1['c_personal_net_income'].iplot(kind='box', color = 'orange')


# #### **c_quant_additional_cards_in_the_application**

# In[128]:


tratamiento_1['c_quant_additional_cards_in_the_application'].iplot(kind='box', color = 'orange')


# <h1 style="color:blue"> DATOS FALTANTES </h1>

# In[129]:


completitud(tratamiento_1).style.background_gradient()


# * En la segunda prueba de completitud vemos que todas las columnas presentan 100% y 0 valores de datos faltantes. Por esta razón no se trabaja en la imputación de missings.

# <h1 style="color:blue"> INGENIERÍA DE DATOS I </h1>

# In[130]:


from sklearn.model_selection import train_test_split
X_train,X_test=train_test_split(tratamiento_1,test_size=.3,random_state=0)


# ## Categóricas

# ### One Hot Encoding / Dummies

# In[131]:


cate = list(tratamiento_1.filter(like = 'v_').columns)
cate


# In[132]:


feats = [
 'v_sex',
 'v_marital_status',
 'v_flag_residencial_phone',
 'v_area_code_residencial_phone',
 'v_residence_type',
 'v_flag_mothers_name',
 'v_flag_fathers_name',
 'v_flag_residence_town=working_town',
 'v_flag_residence_state=working_state',
 'v_profession_code',
 'v_flag_residencial_address=postal_address',
 'v_flag_other_card',
 'v_flag_mobile_phone',
 'v_flag_contact_phone',
 'v_cod_application_booth',
 'v_flag_card_insurance_option']

for col in feats:
    X_train = pd.get_dummies(X_train, columns = [col], prefix = col)
    X_test = pd.get_dummies(X_test, columns = [col], prefix = col)
X_train.head(5)


# In[133]:


# Añadimos columnas que no estan presentes entre los sets.
miss_cols_test = set(X_train.columns)-set(X_test.columns)
for col in miss_cols_test:
    X_test[col]=0
    
# Asegurando mismo orden de columnas
X_test =X_test[X_train.columns]


# In[134]:


miss_cols_test


# In[135]:


X_test


# In[136]:


print(X_train.shape)
X_test.shape


# <h1 style="color:blue"> REDUCCIÓN DE DIMENSIONES </h1>

# ### Filtro de Baja Varianza

# In[137]:


X_train.columns


# In[138]:


X_train.filter(like="c_").describe(percentiles=np.arange(0.1,1.1,.1))


# In[139]:


X_train.drop(columns=['c_quant_dependants','c_shop_rank','c_quant_banking_accounts','c_quant_additional_cards_in_the_application','c_mate_income'],inplace=True)
X_test.drop(columns=['c_quant_dependants','c_shop_rank','c_quant_banking_accounts','c_quant_additional_cards_in_the_application','c_mate_income'],inplace=True)


# In[140]:


X_train


# In[141]:


X_test


# ### PCA

# In[142]:


from sklearn.decomposition import PCA
pca_= PCA(n_components=3)


# In[143]:


con = list(X_train.filter(like = 'c_').columns)
con


# In[144]:


x = X_train[['c_age',
 'c_payment_day',
 'c_months_in_residence',
 'c_months_in_the_job',
 'c_personal_net_income']]
print(x.shape)
x


# In[145]:


tgt = X_train[['v_tgt']]
tgt


# In[146]:


pca_.fit(x)


# In[147]:


pca_data = pd.DataFrame(pca_.transform(x),columns=['PC1','PC2','PC3'])
pca_data['v_tgt'] = tgt


# In[148]:


pca_data


# In[149]:


# Porcentaje de varianza explicada por cada uno de los componentes seleccionados.
pca_.explained_variance_ratio_


# In[150]:


sum(pca_.explained_variance_ratio_[:-1])


# In[151]:


# Gráfico 3D del PCA
pca = PCA(n_components=3)
dimention_3 = pca.fit_transform(x)
total_var = pca.explained_variance_ratio_.sum() * 100
fig = px.scatter_3d(dimention_3, x = 0, y = 1, z = 2,title = f'Total de Varianza Explicada: {total_var:.10f}%',
                 labels={'0': 'Componente Principal 1', '1': 'Componente Principal 2', '2': 'Componente Principal 3'})
fig.show()


# # TABLAS FINALES - TRATAMIENTO I

# In[152]:


X_train


# In[153]:


X_test


# In[ ]:




