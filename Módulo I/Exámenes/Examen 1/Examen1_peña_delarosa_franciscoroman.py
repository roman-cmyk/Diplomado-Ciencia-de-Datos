#!/usr/bin/env python
# coding: utf-8

# ## (a) **Import/Install Required Libraries**

# In[199]:


get_ipython().system('pip3 install fuzzywuzzy')
get_ipython().system('pip3 install pygal')
get_ipython().system('pip3 install keplergl')


# In[225]:


# Import required libraries
import pandas as pd
import numpy as np
import datetime
import unicodedata
import warnings
import os
from IPython.display import Image
pd.options.display.max_columns = None
pd.set_option('max_rows',50000)
warnings.filterwarnings('ignore')

# Useful libraries to check inconsistency data entries
import fuzzywuzzy
from fuzzywuzzy import process
import chardet


# In[226]:


import cufflinks as cf
from plotly.offline import plot,iplot
import plotly.graph_objects as go
pd.options.plotting.backend = "plotly"
import re
import plotly.express as px
cf.go_offline()


# In[227]:


import sys
sys.path.append('Examen1_libreria.py')
from Examen1_libreria import *


# In[228]:


# Read dataset => 'dataset_examen_1.csv'
path = '/home/roman/Documents/Diplomado en Ciencia de Datos - UNAM FES Acatlán/Módulo 1/Examen/Examen 1/dataset_examen_1.csv'
df = pd.read_csv(path)
print(df.shape)
df.head(5)


# # (b) **Part 1:**

# **PARTE I**
# * Etiquetado de variables
# 
# * Calidad de datos: Duplicados, Completitud, Consistencia
# 
# * Limpieza de Texto

# **PARTE I**
# * Variable Tagging
# 
# * Data Quality: Duplicate Records, Completeness, Consistency
# 
# * Text Cleaning

# ### **Variable Tagging**

# * id : Identificador
# * ao hechos : Año en el que se reporta el evento
# * mes hechos : Mes en el que sucedió el evento
# * fecha hechos : Momento en el que sucedió el evento
# * delito : Descripción del evento
# * categoria delito : Categorı́a del evento
# * fiscalı́a : Fiscalı́a en donde se denunció el delito
# * agencia : Agencia
# * unidad investigacion : Unidad encargada de la investigación del delito
# * colonia hechos : Colonia donde ocurrió el delito
# * alcaldia hechos : Alcaldı́a de la CDMX donde ocurrió el delito
# * fecha inicio : Momento en el que se reporta el evento
# * mes inicio : Mes en el que se reporta el evento
# * ao inicio : Año en el que se reporta el evento
# * calle hechos : Nombre de la calle donde sucedió el delito
# * calle hechos2 : Nombre de la calle donde sucedió el delito
# * longitud : Longitud donde sucedió el delito

# In[6]:


# Check columns names to identify them
df.columns


# In[7]:


# In the step above, 'Unnamed Columns' appeared => inspect and delete them
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
print(df.shape)
df.head(5)


# In[8]:


# Validate 'Unnamed' columns were deleted
df.columns


# In[9]:


# Prefixes for variable types
# 'c_' --> Numeric Variables: Discrete & Continous
# 'v_' --> Categorical Variables
# 'd_' --> Date Type Variables
# 't_' --> Text Type Variables

c_feats = ['longitud','latitud','geopoint']
v_feats = ['ao_hechos','','mes_hechos','agencia','unidad_investigacion','mes_inicio','ao_inicio','id']
t_feats = ['delito','categoria_delito','fiscalia','colonia_hechos','alcaldia_hechos','calle_hechos',
           'calle_hechos2']
d_feats = ['fecha_hechos','fecha_inicio']


# In[10]:


# Rename variables in each list according to their type
c_feats_new = ['c_' + x for x in c_feats]
v_feats_new = ['v_' + x for x in v_feats]
d_feats_new = ['d_' + x for x in d_feats]
t_feats_new = ['t_' + x for x in t_feats]


# In[11]:


# Verify new headers for variables were renammed
print(list(v_feats))
print(list(v_feats_new))


# In[12]:


# Rename columns according to their type of variable
df.rename(columns=dict(zip(d_feats,d_feats_new)),inplace=True)
df.rename(columns=dict(zip(v_feats,v_feats_new)),inplace=True)
df.rename(columns=dict(zip(t_feats,t_feats_new)),inplace=True)
df.rename(columns=dict(zip(c_feats,c_feats_new)),inplace=True)
print(df.shape)
df.head(3)


# ### **Check for Duplicate Records**

# In[13]:


df.duplicated()


# In[14]:


# Get a subset with all duplicate records using ".duplicated"
df[df.duplicated()]


# In[15]:


df.drop_duplicates(inplace = True)


# In[16]:


df.duplicated().sum()


# In[17]:


# Create a new index and delete the previous one
df.reset_index(drop = True, inplace = True)


# In[18]:


# Verify dataframe shape after remove duplicates
print(df.shape)
df.head(5)


# In[19]:


# Function used to get completeness values
# The input/argument is --> df
def completeness(dataframe):
    comp = pd.DataFrame(dataframe.isnull().sum())
    comp.reset_index(inplace = True)
    comp = comp.rename(columns = {'index':'column', 0:'total'})
    comp['completeness'] = (1 - comp['total']/dataframe.shape[0])*100
    comp = comp.sort_values(by = 'completeness', ascending = True)
    comp.reset_index(drop = True, inplace = True)
    return comp


# In[20]:


# Check for "completeness"
completeness(df)


# In[21]:


# **(d)** **Delete Variables With >= 20% of Missings Values**
df.drop(columns = ['t_calle_hechos2'], inplace = True)
df.reset_index(drop = True, inplace = True)
print(df.shape)
df.head(5)v


# In[21]:


# **(d)** **Delete Variables With >= 20% of Missings Values**
df.drop(columns = ['t_calle_hechos2'], inplace = True)
df.reset_index(drop = True, inplace = True)
print(df.shape)
df.head(5)


# In[21]:


# **(d)** **Delete Variables With >= 20% of Missings Values**
df.drop(columns = ['t_calle_hechos2'], inplace = True)
df.reset_index(drop = True, inplace = True)
print(df.shape)
df.head(5)


# In[21]:


# **(d)** **Delete Variables With >= 20% of Missings Values**
df.drop(columns = ['t_calle_hechos2'], inplace = True)
df.reset_index(drop = True, inplace = True)
print(df.shape)
df.head(5)


# In[21]:


# **(d)** **Delete Variables With >= 20% of Missings Values**
df.drop(columns = ['t_calle_hechos2'], inplace = True)
df.reset_index(drop = True, inplace = True)
print(df.shape)
df.head(5)


# In[21]:


# **(d)** **Delete Variables With >= 20% of Missings Values**
df.drop(columns = ['t_calle_hechos2'], inplace = True)
df.reset_index(drop = True, inplace = True)
print(df.shape)
df.head(5)


# In[21]:


# **(d)** **Delete Variables With >= 20% of Missings Values**
df.drop(columns = ['t_calle_hechos2'], inplace = True)
df.reset_index(drop = True, inplace = True)
print(df.shape)
df.head(5)


# In[21]:


# **(d)** **Delete Variables With >= 20% of Missings Values**
df.drop(columns = ['t_calle_hechos2'], inplace = True)
df.reset_index(drop = True, inplace = True)
print(df.shape)
df.head(5)


# ### **Check for Consistency**

# In[22]:


df.columns


# In[23]:


# Check for consistency => 'v_ao_hechos'
    ## "v_ao_hechos" cannot be: negatives, floats, month names
df['v_ao_hechos'].unique()


# In[24]:


df[df['v_ao_hechos'] == 'Junio']


# In[25]:


# Check for consistency => 'v_mes_hechos'
    ## "v_mes_hechos" must be categorical values belonging to 'calendar months'
df['v_mes_hechos'].unique()


# In[26]:


# Verify if incorrect 'v_mes_hechos' match exactly with month in 'd_fecha_hechos' => 2 cases are taken
df[df['v_mes_hechos'] == 'August']


# In[27]:


# Verify if incorrect 'v_mes_hechos' match exactly with month in 'd_fecha_hechos' => 2 cases are taken
df[df['v_mes_hechos'] == 'ENRO']


# 
# * **Month' names that must be adjusted:**
# 
#     * diciiembre | december => diciembre
#     * maro | march => marzo
#     * novembre | novimbre | november => noviembre
#     * septiemb | september => septiembre
#     * agossto | agosto-2017 | agosto3 | august => agosto
#     * abrill | april | aabril => abril
#     * mayo-2018 | may => mayo
#     * june => junio
#     * october => octubre
#     * february | febrero-2015 =>febrero
#     * july => julio
#     * january | enro => enero
# 

# In[28]:


# This function is used to invalid month' names
def correct_month(month):
    if month == 'Diciiembre' or month == 'December' or month == 'Diciembre':
        return 'Diciembre'
    elif month == 'Maro' or month == 'March' or month == 'Marzo':
        return 'Marzo'
    elif month == 'Novembre' or month == 'Novimbre' or month == 'November' or month == 'Noviembre':
        return 'Noviembre'
    elif month == 'Septiemb' or month == 'September' or month == 'Septiembre':
        return 'Septiembre'
    elif month == 'Agossto' or month == 'Agosto-2017' or month == 'agosto3' or month == 'August' or month == 'Agosto':
        return 'Agosto'
    elif month == 'abrill' or month == 'April' or month == 'Aabril' or month == 'Abril':
        return 'Abril'
    elif month == 'Mayo-2018' or month == 'May' or month == 'Mayo':
        return 'Mayo'
    elif month == 'June' or month == 'Junio':
        return 'Junio'
    elif month == 'October' or month == 'Octubre':
        return 'Octubre'
    elif month == 'February' or month == 'Febrero-2015' or month == 'Febrero':
        return 'Febrero'
    elif month == 'July' or month == 'Julio' or month == 'Julio .':
        return 'Julio'
    elif month == 'January' or month == 'ENRO' or month == 'Enero':
        return 'Enero'
    else:
        return 'Check'


# In[29]:


# Apply function 'correct_month' to adjust invalid month'names
df['v_mes_hechos'].astype(str)
df['v_mes_hechos'] = df['v_mes_hechos'].apply(lambda row: correct_month(row))
df.head(5)


# In[30]:


# Validate the results in 'v_mes_hechos' are correct
df['v_mes_hechos'].value_counts()


# In[31]:


# This function is used to correct invalid month' names => 'v_ao_hechos'
def correct_ao_hechos(year):
    if year == '-2017' or year == '-215' or year == '1800' or year == '321':
        return '2017'
    elif year == '-2016' or year == '1258' or year == '2058' or year == '235' or year == '19000' or year == 'Junio':
        return '2016'
    elif year == '2023':
        return '2015'
    elif year == 'Febrero':
        return '2018'
    else:
        return year


# In[32]:


# Check for consistency => 'v_mes_hechos'
    ## "v_mes_hechos" must be categorical values belonging to 'calendar months'
df['v_ao_hechos'].unique()


# In[33]:


# Apply function 'ao_hechos' to adjust invalid 'v_ao_hechos'
df['v_ao_hechos'] = df['v_ao_hechos'].astype(str)
df['v_ao_hechos'] = df['v_ao_hechos'].apply(lambda row: correct_ao_hechos(row))
df.head(5)


# In[34]:


# Validate the results in 'v_ao_hechos' are correct
df['v_ao_hechos'].value_counts()


# In[35]:


# Check for consistency => 'd_fecha_hechos'
    ## "d_fecha_hechos" must be date format, any other value is incorrect and must be adjusted
aux_fecha_hechos = df[df['d_fecha_hechos'].str.contains("[a-zA-Z]")]
print(aux_fecha_hechos.shape)
aux_fecha_hechos.head(5)


# In[36]:


# This function is used to clean invalid data entries in 'd_fecha_hechos' column
def clean_fecha_hechos(text):
    try:
        text = text.replace('lunes','').replace('martes','').replace('miércoles','').replace('jueves','').replace('viernes','')
        text = text.replace('sábado','').replace('sabado','').replace('domingo','').replace('|','').replace('()','').replace('de','')
        text = text.replace('enero','-1-').replace('febrero','-2-').replace('marzo','-3-').replace('abril','-4-')
        text = text.replace('mayo','-5-').replace('junio','-6-').replace('julio','-7-').replace('agosto','-8-')
        text = text.replace('septiembre','-9-').replace('octubre','-10-').replace('noviembre','-11-').replace('diciembre','-12-')
        return text
    except:
        return 'Check'


# In[37]:


aux_fecha_hechos['d_fecha_hechos'] = aux_fecha_hechos['d_fecha_hechos'].apply(lambda row: clean_fecha_hechos(row))
aux_fecha_hechos.head(5)


# In[38]:


aux_fecha_hechos['d_fecha_hechos'] = pd.to_datetime(aux_fecha_hechos['d_fecha_hechos']).dt.strftime('%Y-%m-%d %H:%M:%S')
aux_fecha_hechos.head(5)


# In[39]:


# Apply 'clean_fecha_hechos' to df
df['d_fecha_hechos'] = df['d_fecha_hechos'].apply(lambda row: clean_fecha_hechos(row))
df.head(5)


# In[40]:


# Convert to date format 'd_fecha_hechos' column
df['d_fecha_hechos'] = pd.to_datetime(df['d_fecha_hechos']).dt.strftime('%Y-%m-%d %H:%M:%S')
df.head(5)


# In[41]:


# Check for consistency => 'd_fecha_inicio'
    ## "d_fecha_hechos" must be date format, any other value is incorrect and must be adjusted
aux_fecha_inicio = df[df['d_fecha_inicio'].str.contains("[a-zA-Z]]")]
print(aux_fecha_inicio.shape)
aux_fecha_inicio.head(5)


# In[42]:


# Convert to date format 'd_fecha_inicio' column
df['d_fecha_inicio'] = pd.to_datetime(df['d_fecha_inicio'], errors = 'coerce').dt.strftime('%Y-%m-%d %H:%M:%S')
df.head(5)


# In[43]:


df.head(3)
# Pending features:
# 'v_mes_inicio' => DONE
# 'v_ao_inicio' => DONE
# 'c_longitud' => DONE
# 'c_latitud' => DONE


# In[44]:


# Verify 'v_mes_inicio' values are correct and consistent => OK
df['v_mes_inicio'].unique()


# In[45]:


# Verify 'v_ao_inicio' values are correct and consistent => OK
df['v_ao_inicio'].unique()


# In[46]:


# This functions is used to validate 'lat' & 'lng' values
    ## Latitude must be a number between -90 and 90
    ## Longitude must a number between -180 and 180
def lng_val(value):
    try:
        if -180<=value<=+180:
            return value
        else:
            return 'NaN'
    except:
        value    


# In[47]:


# Check for null values in 'c_longitud' variable
df['c_longitud'].isnull().sum()


# In[48]:


df['c_longitud'] = df['c_longitud'].fillna(0)
df.head(3)


# In[49]:


# Check for null values in 'c_longitud' variable
df['c_longitud'].isnull().sum()


# In[50]:


# Use '\D+' for replace non numeric values to '0':
df['c_longitud'].replace('\D+','0',regex=True,inplace=True)
df.head(3)


# In[51]:


# Verify 'c_longitud' values are correct and consistent
df['c_longitud'] = df['c_longitud'].astype(float)
df['c_longitud'] = df['c_longitud'].apply(lambda row: lng_val(row))
df.head(5)


# In[52]:


# This functions is used to validate 'lat' & 'lng' values
    ## Latitude must be a number between -90 and 90
    ## Longitude must a number between -180 and 180
def lat_val(value):
    try:
        if -90<=value<=+90:
            return value
        else:
            return 'NaN'
    except:
        value


# In[53]:


# Verify 'c_latitud' values are correct and consistent
df['c_latitud'] = df['c_latitud'].astype(float)
df['c_latitud'] = df['c_latitud'].apply(lambda row: lat_val(row))
df.head(5)


# In[54]:


# Check for consistency => 't_delito'
df['t_delito'].value_counts()


# In[55]:


# This function is used to replace invalid letters in text columns => 't_delito' column
def replace_words(text):
    try:
        text = text.replace('DAÃO','DAÑO').replace('TRÃNSITO','TRANSITO').replace('USURPACIÃN','USURPACION')
        text = text.replace('PÃBLICO','PUBLICO').replace('POSESIÃN','POSESION').replace('EXTORSIÃN','EXTORSION')
        text = text.replace('VEHÃCULO','VEHICULO').replace('COMUNICACIÃN','COMUNICACION').replace('AUTOBÃS','AUTOBUS')
        text = text.replace('FORÃNEO','FORANEO').replace('PÃBLICA','PUBLICA').replace('EXPLOTACIÃN','EXPLOTACION')
        text = text.replace('REGULACIÃN','REGULACION').replace('GESTIÃN','GESTION').replace('CONTAMINACIÃN','CONTAMINACION')
        text = text.replace('INFORMACIÃN','INFORMACION').replace('2015-09-15 00:00:00','NaN').replace('2017-10-09 08:00:00','NaN')
        text = text.replace('2016-02-27 22:30:00','NaN').replace('EXTORSIÃN','EXTORSION').replace('2016-06-14 16:30:00','NaN')
        return text
    except:
        return 'Check'


# In[56]:


# Apply 'replace_words' function to correct invalid data entries
df['t_delito'] = df['t_delito'].astype(str)
df['t_delito'] = df['t_delito'].apply(lambda row: replace_words(row))
df.head(5)


# In[57]:


# Check invalid data entries in 't_delito' were corrected
df['t_delito'].value_counts()


# In[58]:


# This function is used to replace invalid letters in text columns => 't_categoria_delito' column
def replace_words_catdelito(text):
    try:
        text = text.replace('VEHÃCULO','VEHICULO').replace('VÃA','VIA').replace('PÃBLICA','PUBLICA')
        text = text.replace('VIOLACIÃN','VIOLACION').replace('HABITACIÃN','HABITACION')
        return text
    except:
        return 'Check'


# In[59]:


# Apply 'replace_words_catdelito' to correct invalid data entries in 't_categoria_delito'
df['t_categoria_delito'] = df['t_categoria_delito'].astype(str)
df['t_categoria_delito'] = df['t_categoria_delito'].apply(lambda row: replace_words_catdelito(row))
df.head(5)


# In[60]:


# Check invalid data entries in 't_delito' were corrected => (text cleaning)
df['t_categoria_delito'].value_counts()


# In[61]:


# Check for consistency => 't_fiscalia'
df['t_fiscalia'].value_counts()


# In[62]:


# This function is used to replace invalid letters in text columns => 't_categoria_delito' column
def replace_words_fiscalia(text):
    try:
        text = text.replace('INVESTIGACIÃN','INVESTIGACION').replace('JUÃREZ','JUAREZ').replace('COYOACÃN','COYOACAN')
        text = text.replace('ÃLVARO','ALVARO').replace('OBREGÃN','OBREGON').replace('ATENCIÃN','ATENCION').replace('NIÃOS','NIÑOS')
        text = text.replace('NIÃAS','NIÑAS').replace('ATENCIÃN','ATENCION').replace('PROTECCIÃN','PROTECCION').replace('VÃCTIMAS','VICTIMAS')
        text = text.replace('BÃSQUEDA','BUSQUEDA').replace('LOCALIZACIÃN','LOCALIZACION').replace('DIRECCIÃN','DIRECCION')
        return text
    except:
        return 'Check'


# In[63]:


# Apply function 'replace_words_fiscalia' to correct invalid data entries in 't_fiscalia' column
df['t_fiscalia'] = df['t_fiscalia'].astype(str)
df['t_fiscalia'] = df['t_fiscalia'].apply(lambda row: replace_words_fiscalia(row))
df.head(5)


# In[64]:


# Check invalid data entries in 't_categoria_delito' were corrected => (text cleaning)
df['t_fiscalia'].value_counts()


# In[594]:


# Check for consistency => 't_colonia_hechos'
for c in df['t_colonia_hechos']:
    print(c)


# In[65]:


# This function is used to correct invalid data entries in 't_colonia_hechos' => accented characters
# With the same purpose like functions described above (e.g. AMPLIACIÃN)

def accents_colonia_hechos(text):

    try:
        text = unicode(text, 'utf-8')
    except NameError:
        pass

    text = unicodedata.normalize('NFD', text)           .encode('ascii', 'ignore')           .decode("utf-8")

    return str(text)


# In[66]:


# Apply function 'accents_colonia_hechos' to correct accented characters
df['t_colonia_hechos'] = df['t_colonia_hechos'].astype(str)
df['t_colonia_hechos'] = df['t_colonia_hechos'].apply(lambda row: accents_colonia_hechos(row))
df.head(5)


# In[597]:


# Check invalid data entries in 't_colonia_hechos' were corrected => (text cleaning)
for c in df['t_colonia_hechos'].unique():
    print(c)


# In[67]:


# This function is used to correct invalid data entries in 't_colonia_hechos' column
def replace_words_colonia_hechos(text):
    try:
        text = text.replace('SECCIAN','SECCION').replace('HIPADROMO','HIPODROMO').replace('ARSULA','URSULA')
        text = text.replace('AMPLIACIAN','AMPLIACION').replace('MAXICO','MEXICO').replace('CONSTITUCIAN','CONSTITUCION')
        text = text.replace('PEAON','PEÑON').replace('SIMAN','SIMON').replace('MARTAN','MARTIN').replace('ESCANDAN','ESCANDON')
        text = text.replace('HAROES','HEROES').replace('EDUCACIAN','EDUCACION').replace('ANDRAS','ANDRES').replace('PEAAS','PEÑA')
        text = text.replace('MARAA','MARIA').replace('RAO','RIO').replace('JERANIMO','JERONIMO').replace('GAMEZ','GOMEZ')
        text = text.replace('MARTAN','MARTIN').replace('AMPLIACIAN0','AMPLIACION').replace('HAROES','HEROES')
        text = text.replace('RENOVACIAN','RENOVACION').replace('DOMANGUEZ','DOMINGUEZ').replace('SIMAN','SIMON')
        text = text.replace('BOLAVAR','BOLIVAR').replace('IRRIGACIAN','IRRIGACION').replace('PARAASO','PARAISO')
        text = text.replace('LIBERACIAN','LIBERACION').replace('POLATICA','POLITICA').replace('CLAVERAA','CLAVERA')
        text = text.replace('BAAOS','BAÑOS').replace('PEAAN','PEÑA').replace('MARTANEZ','MARTINEZ').replace('JERANIMO','JERONIMO')
        text = text.replace('CONCEPCIAN','CONCEPCION').replace('BARTOLOMA','BARTOLOME').replace('NIAOS','NIÑOS').replace('GAMEZ','GOMEZ')
        text = text.replace('SIMAN','SIMON').replace('AMARICA','AMERICA').replace('AVIACIAN','AVIACION').replace('DOMANGUEZ','DOMINGUEZ')
        text = text.replace('JESAS','JESUS').replace('AAO','AÑO').replace('CONSTITUCIAN','CONSTITUCION').replace('SECCIAN','SECCION')
        text = text.replace('PEAA','PEÑA').replace('REFINERAA','REFINERIA').replace('AMPLIACIAN','AMPLIACION').replace('BOLAVAR','BOLIVAR')
        text = text.replace('MONTAAA','MONTAÑA').replace('LIBERACIAN','LIBERACION').replace('HAROES','HEROES').replace('MAXICO','MEXICO')
        text = text.replace('JESAS','JESUS').replace('SIMAN','SIMON').replace('ELAAS','ELIAS').replace('NIAO','NIÑO').replace('ARAAA','ARENA')
        text = text.replace('M?XICO','MEXICO').replace('RINCAN','RINCON').replace('ESCANDAN','ESCANDON').replace('TAXQUEAA','TAXQUEÑA')
        text = text.replace('MARAA','MARIA').replace('JOSA','JOSE').replace('PEAON','PEATON').replace('AGRACOLA','AGRICOLA').replace('HAROES','HEROES')
        text = text.replace('AMPLIACIAN','AMPLIACION').replace('ESCANDAN','ESCANDON').replace('JARDAN','JARDIN').replace('TAXQUEAA','TAXQUEÑA')
        text = text.replace('AGRACOLA','AGRICOLA').replace('COMPAAAA','CAÑADA').replace('LOTERAA','LOTERIA').replace('RINCAN','RINCON')
        text = text.replace('PEAA','PEÑA').replace('PERIFARICO','PERIFERICO').replace('PEQUE?A','PEQUEÑA').replace('ANDRAS','ANDRES')
        text = text.replace('FORTAN','FORTIN').replace('JAZMAN','JAZMIN').replace('ESPAAA','ESPAÑA').replace('CAAADA','CASADA')
        text = text.replace('MARAA','MARIA').replace('ECHEVERRAA','ECHEVERRIA').replace('ERMITAAO','ERMITAÑO').replace('REFINERAA','REFINERIA')
        return text
    except:
        return 'Check'


# In[68]:


# Convert to uppercase 't_colonia_hechos'
df['t_colonia_hechos'] = df['t_colonia_hechos'].str.upper()
df.head(5)


# In[69]:


# Apply 'replace_words_colonia_hechos' to correct invalid data entries in 't_colonia_hechos' and spelling errors
df['t_colonia_hechos'] = df['t_colonia_hechos'].apply(lambda row: replace_words_colonia_hechos(row))
df.head(5)


# In[70]:


# Check for errors in 't_alcaldia_hechos' =>(text cleaning)
    ## In this case data entries are correct: no invalid records and spelling error were identified
df['t_alcaldia_hechos'].value_counts()


# In[71]:


# Check for errors and apply correct format to 'd_fecha_inicio'
def check_fecha_inicio(texto):
    if texto == texto.str.contains("[a-zA-Z]"):
        return 'NaN'
    else:
        return texto.str()


# In[73]:


# Replace alphabet characters with '0'
df['d_fecha_inicio'] = df['d_fecha_inicio'].str.replace(r'[a-z A-Z]','NaT')
print(df.shape)
df.head(5)


# In[74]:


# Convert 'd_fecha_inicio' to date format => (consistency validation)
    ## After this operation: an error was identified and corrected in the next cell: there is no blank space between date and hour '2016-01-05018:35:37'
pd.to_datetime(df['d_fecha_inicio'], format='%Y-%m-%d %H:%M:%S',errors='coerce')
print(df.shape)
df.head(5)


# In[75]:


# Replace 'NaT' by 'empty space'
df['d_fecha_inicio'] = df['d_fecha_inicio'].str.replace('NaT',' ')
print(df.shape)
df.head(5)


# In[76]:


# Check for errors in 'v_mes_inicio'
    ## Data entries are correct => OK
df['v_mes_inicio'].unique()


# In[77]:


# Check for errors in 'v_ao_inicio'
    ## Data entries are correct => OK
df['v_ao_inicio'].unique()


# # (c) **Part 2:**

# # **Análisis Exploratorio de Datos** (Exploratory Data Analysis => EDA) 
# * En cada punto se debe contestar la siguiente pregunta: **¿Qué puede concluir de esto?**

# ## **Años y meses con más delitos**

# In[79]:


df.head(3)


# In[80]:


delitos = df.groupby(['v_ao_hechos','v_mes_hechos', 't_delito']).size().sort_values(ascending=False)
delitos.head(10)


# In[82]:


delitos = pd.DataFrame(delitos)
delitos = delitos.rename(columns={0:'Sum'})
delitos.head(15).style.background_gradient()


# * **¿Qué puede concluir de esto?**

# **Conclusiones:**
# 
# * 1.- Los delitos con mayor incidencia durante los años y meses con mayor cantidad de delitos fueron (Top 5):
#     
#    * **Violencia Familiar**
#        
#    * **Robo de Objetos**
#         
#    * **Denuncia de Hechos**
#         
#    * **Robo a Negocio sin Violencia**
#         
#    * **Robo a Transeunte en Vía Pública con Violencia**
# 
# * 2.- En el periodo 2016 - 2019 el delito con mayor frecuencia fue:
# 
#     * **Violencia Familiar**
#    
#  

# ## **Delegaciones con más actividad delictiva**

# In[83]:


delegacion_delito = df.groupby(['t_alcaldia_hechos','t_delito']).size().sort_values(ascending=False)
delegacion_delito.head(15)


# In[84]:


delegacion_delito = pd.DataFrame(delegacion_delito)
delegacion_delito = delegacion_delito.rename(columns={0:'Sum'})
delegacion_delito.head(20).style.background_gradient()


# In[85]:


delegacion = df.groupby(['t_alcaldia_hechos']).size().sort_values(ascending=False)
delegacion


# In[86]:


# Convert 'delegacion' to DataFrame (just for better visualization)
delegacion = pd.DataFrame(delegacion)
delegacion = delegacion.rename(columns={0:'Sum'})
delegacion.style.background_gradient()


# In[87]:


# Select Top 10 't_alcaldia_hechos' to highlight more criminal activity
delegacion.iloc[0:10]


# In[88]:


# Using pygal to plot 'Top 10 Delegaciones con Mayor Actividad Delictiva'
import pygal
from IPython.display import SVG, display
from pygal import Config

config = Config()
config.show_legend = True
config.human_readable = True


line_chart = pygal.HorizontalBar(print_labels=True, print_values=True)
line_chart.title = 'Top 10 Delegaciones con Mayor Actividad Delictiva'
line_chart.add('CUAUHTEMOC', 126168)
line_chart.add('IZTAPALAPA', 114682)
line_chart.add('GUSTAVO A. MADERO', 76935)
line_chart.add('BENITO JUAREZ', 69342)
line_chart.add('COYOACAN', 52767)
line_chart.add('MIGUEL HIDALGO', 52502)
line_chart.add('ALVARO OBREGON', 51135)
line_chart.add('TLALPAN', 44888)
line_chart.add('VENUSTIANO CARRANZA', 44474)
line_chart.add('AZCAPOTZALCO', 38876)
display(SVG(line_chart.render(disable_xml_declaration=True,show_legend=True, human_readable=True, fill=True
)))


# * **¿Qué puede concluir de esto?**

# * 1.- De acuerdo a fuentes externas (medios publicitarios y páginas oficiales del gobierno de la ciudad):
#     
#    * **Las delegaciones con mayor actividad delicitiva en 2020 fueron:**
#        * Álvaro Obregón, Cuauhtémoc, Coyoacán, Gustavo A. Madero, Iztapalapa, Miguel Hidalgo, Tlalpan, Venustiano Carranza y Xochimilco [**Infobae - Argentina**](https://www.infobae.com/america/mexico/2020/09/13/cuales-son-las-8-alcaldias-que-concentran-la-mayor-parte-de-los-delitos-en-cdmx/). De esta publicación podemos observar que de las 8 citadas, el 70% aparecen en el Top 10 de nuestro análisis.
#        
#     * **Iztapalapa ocupara el 1er lugar en actividad delictiva en la categoría de:** Violencia Familiar

# ## **¿Cuáles son los delitos más frecuentes?**

# In[89]:


df.head(3)


# In[90]:


delito_frq = df.groupby(['t_delito']).size().sort_values(ascending=False)
delito_frq.head(15)


# In[91]:


# Convert 'delito_frq' to DataFrame (just for better visualization)
delito_frq = pd.DataFrame(delito_frq)
delito_frq = delito_frq.rename(columns={0:'Sum'})
delito_frq.head(15).style.background_gradient()


# In[216]:


# Show Top 10 'delito_frq' to highlight 'most frequent crimes'
config = Config()
config.show_legend = True
config.human_readable = True


line_chart = pygal.HorizontalBar(print_labels=True, print_values=True)
line_chart.title = 'Delitos Más Frecuentes'
line_chart.add('VIOLENCIA FAMILIAR', 68004)
line_chart.add('ROBO DE OBJETOS', 51510)
line_chart.add('ROBO A NEGOCIO SIN VIOLENCIA', 51172)
line_chart.add('FRAUDE', 44198)
line_chart.add('DENUNCIA DE HECHOS', 40377)
line_chart.add('AMENAZAS', 36939)
line_chart.add('ROBO A TRANSEUNTE EN VIA PUBLICA CON VIOLENCIA', 28887)
line_chart.add('ROBO A TRANSEUNTE DE CELULAR CON VIOLENCIA', 25779)
line_chart.add('ROBO DE ACCESORIOS DE AUTO', 25332)
line_chart.add('ROBO DE OBJETOS DEL INTERIOR DE UN VEHICULO', 23652)
display(SVG(line_chart.render(disable_xml_declaration=True,show_legend=True, human_readable=True, fill=True
)))


# In[92]:


# Select Top 10 'delito_frq' to highlight 'most frequent crimes'
delito_frq.iloc[0:10]


# * **¿Qué puede concluir de esto?**

# * **Violencia Familiar** predomina como el crimen/delito con mayor incidencia y se replica en delegaciones como Iztapalapa en donde presenta un mayor foco de concentración, así como en Cuauhtémoc, con 68,004 y 5,554 respectivamente.

# ## **¿Qué tipo de delitos son los más frecuentes en la delegación con mayor incidencia delictiva?**

# In[95]:


# Filter DataFrame by 't_alcaldia_hechos' == 'CUAUHTEMOC' to identify most frequent crimes
delegacion_mayor = df[df['t_alcaldia_hechos'] == 'CUAUHTEMOC']
print(delegacion_mayor.shape)
delegacion_mayor.head(5)


# In[97]:


cua_frq = delegacion_mayor.groupby(['t_delito']).size().sort_values(ascending=False)
cua_frq.head(20)


# In[98]:


# Convert 'cua_frq' to DataFrame (just for better visualization)
cua_frq = pd.DataFrame(cua_frq)
cua_frq = cua_frq.rename(columns={0:'Sum'})
cua_frq.head(15).style.background_gradient()


# In[99]:


# Select Top 10 crimes in 'Cuauthemoc'
cua_frq.iloc[0:10]


# In[217]:


# Show Top 10 'delito_frq' to highlight 'most frequent crimes'
config = Config()
config.show_legend = True
config.human_readable = True


line_chart = pygal.HorizontalBar(print_labels=True, print_values=True)
line_chart.title = 'Delitos Más Frecuentes en la Delegación Cuauhtémoc'
line_chart.add('FRAUDE', 11610)
line_chart.add('ROBO DE OBJETOS', 10235)
line_chart.add('DENUNCIA DE HECHOS', 8207)
line_chart.add('ROBO A NEGOCIO SIN VIOLENCIA', 8074)
line_chart.add('ROBO A TRANSEUNTE DE CELULAR SIN VIOLENCIA', 5995)
line_chart.add('VIOLENCIA FAMILIAR', 5554)
line_chart.add('ROBO A TRANSEUNTE EN VIA PUBLICA CON VIOLENCIA', 5424)
line_chart.add('AMENAZAS', 5069)
line_chart.add('ROBO A TRANSEUNTE DE CELULAR CON VIOLENCIA', 4169)
line_chart.add('ROBO DE ACCESORIOS DE AUTO', 3975)
display(SVG(line_chart.render(disable_xml_declaration=True,show_legend=True, human_readable=True, fill=True
)))


# * **¿Qué puede concluir de esto?**

# * Esta delegación mantiene un comportamiento muy similar al volumen general de incidencia del Top 10 de los delitos/crímenes con mayor frecuencia, uno de sus principales diferenciadores es el número de casos.

# ## **¿En qué delegación suceden los delitos más graves (categoría_delito)?**

# In[100]:


df.head(3)


# In[101]:


cat_delito = df.groupby(['t_alcaldia_hechos','t_categoria_delito']).size().sort_values(ascending=False)
cat_delito.head(15)


# In[102]:


# Convert 'cat_delito' to DataFrame (just for better visualization)
cat_delito = pd.DataFrame(cat_delito)
cat_delito = cat_delito.rename(columns={0:'Sum'})
cat_delito.head(15).style.background_gradient()


# In[103]:


df['t_categoria_delito'].value_counts()


# ## **En la fiscalía de 'juzgados familiares, ¿Cuáles son los delitos más frecuentes?**

# In[104]:


df['t_fiscalia'].unique()


# In[105]:


# Filter 'juzgados civiles' in 't_fiscalia' column
juzgados = df[df['t_fiscalia'] == 'INVESTIGACION PARA LA ATENCION DE NIÑOS, NIÑAS Y ADOLESCENTES']
juzgados.reset_index(drop = True, inplace = True)
juzgados.head(15)


# In[106]:


juzgados_fam = juzgados.groupby(['t_delito']).size().sort_values(ascending=False)
juzgados_fam.head(15)


# In[107]:


# Convert 'juzgados_fam' to DataFrame (just for better visualization)
juzgados_fam = pd.DataFrame(juzgados_fam)
juzgados_fam = juzgados_fam.rename(columns={0:'Sum'})
juzgados_fam.head(15).style.background_gradient()


# In[108]:


juzgados_fam.columns


# In[111]:


# Select Top 15 crimes in fiscalía 'juzgados familiares'
juzgados_fam.iloc[0:15]


# In[112]:


# Using pygal to plot: 'Top 10 Delegaciones con Mayor Actividad Delictiva'
import pygal
from IPython.display import SVG, display
from pygal import Config

config = Config()
config.show_legend = True
config.human_readable = True


line_chart = pygal.HorizontalBar(print_labels=True, print_values=True)
line_chart.title = 'Top 10 Delitos más Frecuentes en Juzgados Familiares'
line_chart.add('VIOLENCIA FAMILIAR', 7427)
line_chart.add('SUSTRACCION DE MENORES', 2232)
line_chart.add('ROBO A NEGOCIO SIN VIOLENCIA', 2034)
line_chart.add('ABANDONO DE PERSONA', 1773)
line_chart.add('INSOLVENCIA ALIMENTARIA', 1531)
line_chart.add('AMENAZAS', 1243)
line_chart.add('NARCOMENUDEO POSESION SIMPLE', 994)
line_chart.add('DENUNCIA DE HECHOS', 887)
line_chart.add('ROBO A TRANSEUNTE EN VIA PUBLICA CON VIOLENCIA', 721)
line_chart.add('ABUSO SEXUAL', 502)
display(SVG(line_chart.render(disable_xml_declaration=True,show_legend=True, human_readable=True, fill=True
)))


# In[468]:


from IPython.display import HTML
import pygal
from pygal import Config

html_pygal = u"""
    <!DOCTYPE html>
    <html>
        <head>
            <script type="text/javascript" src="http://kozea.github.com/pygal.js/javascripts/svg.jquery.js"></script>
            <script type="text/javascript" src="http://kozea.github.com/pygal.js/javascripts/pygal-tooltips.js"></script>
        </head>
        <body><figure>{pygal_render}</figure></body>
    </html>
"""

line_chart = pygal.HorizontalBar()
line_chart.title = 'Top 10 Delitos más Frecuentes en Juzgados Familiares'
line_chart.add('VIOLENCIA FAMILIAR', 7427)
line_chart.add('SUSTRACCION DE MENORES', 2232)
line_chart.add('ROBO A NEGOCIO SIN VIOLENCIA', 2034)
line_chart.add('ABANDONO DE PERSONA', 1773)
line_chart.add('INSOLVENCIA ALIMENTARIA', 1531)
line_chart.add('AMENAZAS', 1243)
line_chart.add('NARCOMENUDEO POSESION SIMPLE', 994)
line_chart.add('DENUNCIA DE HECHOS', 887)
line_chart.add('ROBO A TRANSEUNTE EN VIA PUBLICA CON VIOLENCIA', 721)
line_chart.add('ABUSO SEXUAL', 502)
line_chart.render_in_browser()


# * **¿Qué puede concluir de esto?**

# * Violencia Familiar, al igual que en los casos de Iztapalapa y Cuauhtémoc se mantiene vigente y con un comportamiento a la alza en volumen de incidencia, seguida de Sustracción de Menores y Robo a Negocio Sin Violencia.

# ## **¿Cuál es el comportamiento del tiempo que pasa desde que el delito sucede hasta que se reporta?**

# In[113]:


df.head(3)


# In[114]:


df['d_fecha_hechos'] = pd.to_datetime(df['d_fecha_hechos']).dt.strftime('%d-%m-%Y')
df['d_fecha_inicio'] = pd.to_datetime(df['d_fecha_inicio']).dt.strftime('%d-%m-%Y')
df.head(5)


# In[115]:


df['d_fecha_hechos']= pd.to_datetime(df['d_fecha_hechos'])
df['d_fecha_inicio']= pd.to_datetime(df['d_fecha_inicio'])


# In[116]:


df.info()


# In[117]:


df['difference_in_datetime'] = abs(df['d_fecha_hechos'] - df['d_fecha_inicio'])
df.head(10)


# In[118]:


df['v_mes_hechos'].unique()


# In[119]:


df['v_mes_inicio'].unique()


# In[121]:


mes_hecho_inicio = df.groupby(['v_mes_hechos','v_mes_inicio','t_delito']).size().sort_values(ascending = False)
mes_hecho_inicio.head(15)


# In[122]:


# Convert 'mes_inicio' to DataFrame (just for better visualization)
mes_hecho_inicio = pd.DataFrame(mes_hecho_inicio)
mes_hecho_inicio = mes_hecho_inicio.rename(columns={0:'Sum'})
mes_hecho_inicio.head(20).style.background_gradient()


# In[123]:


fecha_hecho_inicio = df.groupby(['d_fecha_hechos','d_fecha_inicio','difference_in_datetime']).size().sort_values(ascending=False)
fecha_hecho_inicio.head(20)


# In[124]:


# Convert 'mes_inicio' to DataFrame (just for better visualization)
fecha_hecho_inicio = pd.DataFrame(fecha_hecho_inicio)
fecha_hecho_inicio = fecha_hecho_inicio.rename(columns={0:'Sum'})
fecha_hecho_inicio.head(20).style.background_gradient()


# * **¿Qué puede concluir de esto?**

# * 1.- Uno de los primeros puntos que podemos observar de este análisis es:
#    
#    * **Los meses en los que se suscita el delito/crimen y en el que es reportado a las autoridades es el mismo.**
#    
#    * **Lo anterior nos indica que no se presenta un desfase en 'meses' para realizar el reporte**
#    
#    * **Dentro de los principales delitos reportados, se encuentran:**
#    
#        * Violencia Familiar, Robo a Negocio Sin Violencia, Robo de Objetos, Amenazas y Robo a Transeunte en Vía Pública con Violencia.
#        
#     
#   * **Sin embargo para complementar nuestro análisis, necesitamos  conocer el rango de días en el cual el delito/crimen es reportado dentro del mismo mes como lo observamos antes**
#   
#        * **Se tienen 5 tipos de casos:**
#            * El delito/crimen es reportado en la misma fecha en la que ocurre. (Únicamente transcurren algunas horas)
#            * El delito/crimen es reportado 1 días después en el que ocurre.
#            * El delito/crimen es reportado 2 días después en el que ocurre.
#            * El delito/crimen es reportado 3 días después en el que ocurre.
#            
#   * **Un alto porcentaje de los delitos/crimenes son reportados dentro del mismo periodo en el que ocurren** 

# ## **Añada al menos tres análisis más que considere relevantes para mostrar**

# # (d) **Part 3:**

# # **Ingeniería de Variables/Normalización**

# In[125]:


df.head(2)


# ### **Reduzca la tabla de tal forma que solo se consideren los delitos que ocurrieron después de 2013.**

# In[126]:


# Filter 'v_ao_hechos' > 2013
df['v_ao_hechos'] = df['v_ao_hechos'].astype(int)
df_norm = df[df['v_ao_hechos'] > 2013]
print(df_norm.shape)
df.head(3)


# In[127]:


# Verify data entries in 'v_ao_hechos' are correct
df_norm['v_ao_hechos'].unique()


# ### **Normalice la variable categorı́a delito , disminuyendo el número de posibilidades, por ejemplo: secuestro,violacion, homicidio doloso podrı́a ser una categorı́a llamada ”delito de alto impacto”, la forma de normalización es abierta, solo se debe justificar en el PDF ¿por qué se hizo de esa forma?**

# In[128]:


# Using value_counts() to see total of records per category => 't_categoria_delito'
df_norm['t_categoria_delito'].value_counts()


# In[130]:


# "LabelEncoder" is used to encode categorical values, in this case 't_categoria_delito'
    ## and normalize it to: "Delito de Alto Impacto", "Delito de Medio Impacto", "Delito de Bajo Impacto"
    
df_norm_sklearn = df_norm.copy()

from sklearn.preprocessing import LabelEncoder

lb_make = LabelEncoder()
df_norm_sklearn['t_categoria_delito_label'] = lb_make.fit_transform(df_norm['t_categoria_delito'])

df_norm_sklearn.head()


# In[131]:


aux_norm = df_norm_sklearn[['t_delito','t_categoria_delito','t_categoria_delito_label']]
aux_norm.head(10)


# In[132]:


aux_norm['t_categoria_delito_label'].unique()


# In[133]:


catorce = aux_norm[aux_norm['t_categoria_delito_label'] == 14]
catorce.reset_index(drop=True, inplace=True)
print(catorce.shape)
catorce.head(5)


# In[134]:


trece = aux_norm[aux_norm['t_categoria_delito_label'] == 13]
trece.reset_index(drop=True, inplace=True)
print(trece.shape)
trece.head(5)


# In[135]:


quince = aux_norm[aux_norm['t_categoria_delito_label'] == 15]
quince.reset_index(drop=True, inplace=True)
print(quince.shape)
quince.head(5)


# In[136]:


cero = aux_norm[aux_norm['t_categoria_delito_label'] == 0]
cero.reset_index(drop=True, inplace=True)
print(cero.shape)
cero.head(5)


# ### **After normalization crime category is defined as follows:**
# * **15, 14, 13, 12 y 11 => "Delito de Alto Impacto"**
# 
# 
# * **10, 9, 8, 7 y 6 => "Delito de Medio Impacto"/"Delito de Impacto Medio"**
# 
# 
# * **5, 4, 3, 2, 1 y 0 => "Delito de Bajo Impacto"**

# In[137]:


df_norm = df_norm_sklearn
print(df_norm.shape)
df_norm.head(5)


# In[138]:


# This function is used to assign new colum: "categoria_delito_norm"
# whih belongs to 't_categoria_delito' but normalized
def cat_delito_norm(value):
    if 11<=value<=15:
        return 'Delito de Alto Impacto'
    elif 6<=value<=10:
        return 'Delito de Medio Impacto'
    elif 0<=value<=5:
        return 'Delito de Bajo Impacto'
    else:
        return 'Check'


# In[139]:


df_norm['t_categoria_delito_label'] = df_norm['t_categoria_delito_label'].astype(int)
df_norm['categoria_delito_norm'] = df_norm['t_categoria_delito_label'].apply(lambda row: cat_delito_norm(row))
print(df_norm.shape)
df_norm.head(5)


# In[140]:


# Validate operation and changes above were applied
test = df_norm[df_norm['t_categoria_delito_label'] == 14]
test.reset_index(drop = True, inplace = True)
print(test.shape)
test.head(5)


# In[141]:


df_norm['categoria_delito_norm'].value_counts()


# ### **Normalice la variable delegación de la siguiente forma:**

# #### **Zona Centro Poniente** ####
# 
# * **Cuauhtémoc**
# * **Miguel Hidalgo**
# * **Álvaro Obregón**
# * **Cuajimalpa**
# * **Azcapotzalco**
# 
# #### **Zona Sur** ####
# 
# * **Benito Juárez**
# * **Coyoacán**
# * **Tlalpan**
# * **Magdalena Contreras**
# 
# #### **Zona Norte** ####
# 
# * **Gustavo A. Madero**
# * **V. Carranza**
# * **Iztacalco**
# 
# #### **Zona Oriente** ####
# 
# * **Iztapalapa**
# * **Tláhuac**
# * **Xochimilco**
# * **Milpa Alta**

# In[142]:


df_norm.head(2)


# In[150]:


df_norm['t_alcaldia_hechos'].unique()


# In[151]:


# This function is used to normalice "t_alcaldia_hechos"
def norm_delegacion(delegacion):
    if delegacion == 'CUAUHTEMOC' or delegacion == 'MIGUEL HIDALGO' or delegacion == 'ALVARO OBREGON' or delegacion == 'CUAJIMALPA DE MORELOS' or delegacion == 'AZCAPOTZALCO':
        return 'Zona Centro Poniente'
    elif delegacion == 'BENITO JUAREZ' or delegacion == 'COYOACAN' or delegacion == 'TLALPAN' or delegacion == 'LA MAGDALENA CONTRERAS':
        return 'Zona Sur'
    elif delegacion == 'GUSTAVO A MADERO' or delegacion == 'VENUSTIANO CARRANZA' or delegacion == 'IZTACALCO':
        return 'Zona Norte'
    elif delegacion == 'IZTAPALAPA' or delegacion == 'TLAHUAC' or delegacion == 'XOCHIMILCO' or delegacion == 'MILPA ALTA':
        return 'Zona Oriente'
    else:
        return 'NaN'


# In[152]:


# Apply "norm_delegacion" function to normalize 'delegacion_hechos'
df_norm['t_alcaldia_hechos'] = df_norm['t_alcaldia_hechos'].astype(str)
df_norm['delegacion_norm'] = df_norm['t_alcaldia_hechos'].apply(lambda row: norm_delegacion(row))
print(df_norm.shape)
df_norm.head(5)


# In[153]:


# Validate results
df_norm['delegacion_norm'].value_counts()


# ### **Normalice la colonia de los hechos**

# In[155]:


df_norm['t_colonia_hechos'].value_counts()


# ### **Normalice la variable delito**

# In[156]:


df_norm['t_delito'].value_counts()


# In[157]:


# Normalize "t_delito" variable
df_norm_sklearn = df_norm.copy()

from sklearn.preprocessing import LabelEncoder

lb_make = LabelEncoder()
df_norm_sklearn['t_delito_label'] = lb_make.fit_transform(df_norm['t_delito'])

df_norm_sklearn.head(15)


# In[160]:


test1 = df_norm_sklearn[df_norm_sklearn['t_delito_label'] == 235]
test1.head(20)


# ### **Normalice la variable unidad de investigación**

# In[218]:


# Normalize "t_delito" variable
df_norm_sklearn = df_norm.copy()

from sklearn.preprocessing import LabelEncoder

lb_make = LabelEncoder()
df_norm_sklearn['v_unidad_investigacion_label'] = lb_make.fit_transform(df_norm['v_unidad_investigacion'])

df_norm_sklearn.head(15)


# In[221]:


df_norm = df_norm_sklearn
print(df_norm.shape)
df_norm.head(10)


# ### **Normalice la variable unidad de fiscalía**

# In[219]:


# Normalize "t_delito" variable
df_norm_sklearn = df_norm.copy()

from sklearn.preprocessing import LabelEncoder

lb_make = LabelEncoder()
df_norm_sklearn['t_fiscalia_label'] = lb_make.fit_transform(df_norm['t_fiscalia'])

df_norm_sklearn.head(15)


# In[222]:


df_norm = df_norm_sklearn
print(df_norm.shape)
df_norm.head(10)


# ### **Genere las siguientes variables para fecha_hechos: Cuatrimestre, día de la semana, si/no es fin de semana y día del evento**

# In[170]:


df_norm['d_fecha_hechos'] = pd.to_datetime(df_norm['d_fecha_hechos'])
print(df_norm.shape)
df_norm.head(5)


# In[172]:


# Get weekday from 'd_fecha_hechos'
df_norm['weekday'] = df_norm['d_fecha_hechos'].dt.day_name()
df_norm.head(5)


# In[173]:


# Get calendar month from 'd_fecha_hechos'
df_norm['Full_Month'] = df_norm['d_fecha_hechos'].dt.strftime('%B')
df_norm.head(5)


# In[174]:


def quarter(month):
    if month == 'Enero' or month == 'Febrero' or month == 'Marzo':
        return 'Q1'
    elif month == 'Abril' or month == 'Mayo' or month == 'Junio':
        return 'Q2'
    elif month == 'Julio' or month == 'Agosto' or month == 'Septiembre':
        return 'Q3'
    elif month == 'Octubre' or month == 'Noviembre' or month == 'Diciembre':
        return 'Q4'
    else:
        return 'Check'


# In[175]:


# Apply "quarter" function to 'v_mes_hechos' to get the correct Q.
df_norm['Quarter'] = df_norm['v_mes_hechos'].apply(lambda row: quarter(row))
print(df_norm.shape)
df_norm.head(5)


# In[177]:


# This function is used to know if weekend or not: 1 => YES and 0 => NO
def weekend(day):
    if day == 'Friday' or day == 'Saturday' or day == 'Sunday':
        return '1'
    else:
        return '0'


# In[178]:


df_norm['IsWeekend'] = df_norm['weekday'].apply(lambda row: weekend(row))
print(df_norm.shape)
df_norm.head(10)


# In[180]:


# Get month' day from 'd_fecha_hechos'
df_norm['MonthDay'] = df_norm['d_fecha_hechos'].dt.strftime('%d')
df_norm.head(10)


# ### **Results Validation**

# In[181]:


# Show results for: 'FIN DE SEMANA'
df_norm['IsWeekend'].value_counts()


# In[191]:


# Results for Weekends:
import plotly.graph_objects as go
days = ['Weekends']

fig = go.Figure(data=[
    go.Bar(name = '0', x = days, y = [453234]),
    go.Bar(name = '1', x = days, y = [315419])
])
# Change the bar mode
fig.update_layout(barmode='stack', title = 'Fecha Hechos Fin de Semana')
fig.show()


# In[185]:


# Show results for: 'DIA DE LA SEMANA'
df_norm['weekday'].value_counts()


# In[190]:


# Show results for: 'DIA DE LA SEMANA'
import plotly.graph_objects as go
days = ['Weekdays']

fig = go.Figure(data=[
    go.Bar(name = 'Lunes', x = days, y = [114093]),
    go.Bar(name = 'Martes', x = days, y = [112977]),
    go.Bar(name = 'Miércoles', x = days, y = [111799]),
    go.Bar(name = 'Jueves', x = days, y = [111799]),
    go.Bar(name = 'Viernes', x = days, y = [116068]),
    go.Bar(name = 'Sábado', x = days, y = [102994]),
    go.Bar(name = 'Domingo', x = days, y = [96357])
])
# Change the bar mode
fig.update_layout(barmode='stack', title = 'Fecha Hechos Día de la Semana')
fig.show()


# In[187]:


# Show results for: 'CUATRIMESTRE'
df_norm['Quarter'].value_counts()


# In[189]:


# Show results for: 'CUATRIMESTRE'
import plotly.graph_objects as go
days = ['Quarters']

fig = go.Figure(data=[
    go.Bar(name = 'Q4', x = days, y = [173401]),
    go.Bar(name = 'Q3', x = days, y = [167281]),
    go.Bar(name = 'Q2', x = days, y = [215870]),
    go.Bar(name = 'Q1', x = days, y = [212101])
])
# Change the bar mode
fig.update_layout(barmode='stack', title = 'Fecha Hechos Cuatrimestre')
fig.show()


# In[212]:


# Show results for: 'DIA DEL MES'
df_norm['MonthDay'].value_counts().sort_values(ascending = False)


# In[ ]:


# Show results for: 'DIA DEL MES'
import plotly.graph_objects as go
days = ['MonthDays']

fig = go.Figure(data=[
    go.Bar(name = '01', x = days, y = []),
    go.Bar(name = '02', x = days, y = []),
    go.Bar(name = '03', x = days, y = []),
    go.Bar(name = '04', x = days, y = []),
])
# Change the bar mode
fig.update_layout(barmode='stack', title = 'Fecha Hechos Día del Mes')
fig.show()


# # (e) **Part 4:**

# # **Adicional**

# ## **Genere mapa en Kepler u otra herramienta mostrando los delitos**

# In[192]:


df_norm.head(3)


# In[196]:


df_norm['c_longitud'] = df_norm['c_longitud'].astype(float)
df_norm['c_latitud'] = df_norm['c_latitud'].astype(float)

df_norm = df_norm.rename(columns = {'c_latitud':'Latitude','c_longitud':'Longitude'})
df_norm.dropna(inplace=True)

df_norm['Latitude'] = df_norm['Latitude'].map(lambda x:round(x,2))
df_norm['Longitude'] = df_norm['Longitude'].map(lambda x:round(x,2))


# In[197]:


df_norm.head(5)


# In[202]:


from keplergl import KeplerGl
map_1 = KeplerGl()


# In[205]:


df_norm_map = df_norm[['t_delito','Longitude','Latitude']]
print(df_norm_map.shape)
df_norm_map.head(5)


# In[206]:


map_1.add_data(data = df_norm_map, name='data_1')


# In[207]:


df_norm.shape


# In[208]:


map_1.save_to_html()


# # (f) **Part 5:**

# ## **Cuestionario**

# ### **¿Qué es la ciencia de datos?**

# * La ciencia de datos es una combinación multidisciplinaria de inferencia de datos, desarrollo de algoritmos y tecnología para resolver problemas analíticamente complejos con ayuda de herramientas estadísticas.
# 
# * Además, contribuye a revelar tendencias y genera información que las empresas pueden utilizar para tomar decisiones comerciales de manera inteligente, basada en datos y resultados.

# ### **¿Qué habilidades debe dominar un científico de datos?**

# * Un Científico de Datos debe dominar las siguientes habilidades:
# 
#     * Conocimientos en matemáticas y estadística.
#     
#     * Habilidades sólidas y robustas en programación y manejo de bases de datos.
#     
#     * Habilidades para comunicar de manera efectiva sus hallazgos de forma sencilla y en términos que sean fáciles de entender e interpretar por el negocio.
#     
#     * Establecer canales de comunicación efectivos con expertos en materia empresarial y liderazgo.
#     
#     * Conseguir elaborar gráficos atractivos, explicables y fáciles de interpretar por el negocio.
#     
#     * Del lado de Soft Skills, un Científico de Datos debe ser: estratégico, proactivo y cooperativo, además de innovador y apasionado por su trabajo en la manipulación/tratamiento de la información y su respectiva comunicación con stakeholders.

# ### **¿Qué es una tabla analítica?**

# * Una tabla analítica es el resultado de procesar los datos desde su estado en crudo, aplicando las herramientas estadísticas, matemáticas y de programación necesarias para que la  información sea utilizada para la toma de decisiones dentro de un ambiente empresarial, así como para servir de datos de entrada para modelos de machine learning.

# ### **¿Qué es la ingeniería de variables?**

# * Es el proceso de tranformar datos en características/features que permitan representar de mejor forma el problema, así como brindar un mejor entendimiento del mismo. A través de este proceso se manipulan los datos para corregir errores, ajustar variables y crear nuevas (si así se requiere) y  obtener como resultado un mejor rendimiento durante su uso en modelos de machine learning.

# ### **Describe la ingeniería de variables posible por cada tipo de variable**

# * **Codificación a Nivel Ordinal**
# 
# * **Codificación a Nivel Nominal** => Variables Categóricas
#     
#     * One-Hot Encoding
#     
#     * Count Encoding
#     
#     * Target Encoding
#     
# * **Variables Continuas**
# 
#     * Min-Max Standard Scaler
#     
#     * Standard Scaler
#     
# * **Texto**
# 
#     * Count Vectorizer
#     
#     * TF-IDF Vectorizer

# In[ ]:




