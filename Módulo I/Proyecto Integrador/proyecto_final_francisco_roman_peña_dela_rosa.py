#!/usr/bin/env python
# coding: utf-8

# <h1 style="color:blue"> LIBRERIAS </h1>

# In[1]:


get_ipython().system('pip3 install --upgrade category_encoders')


# In[2]:


# *****Bibliotecas*****
import sys
import os
import warnings
import pathlib
from termcolor import colored

# *****Librerías para Manipulación de Datos*****
import pandas as pd
import numpy as np
from scipy import stats
import re
import unicodedata
import nltk
import unicodedata
from random import sample
from textblob import TextBlob
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.impute import SimpleImputer
from category_encoders import TargetEncoder
from unidecode import unidecode
from nltk.corpus import stopwords
from nltk import FreqDist
from statsmodels.stats.outliers_influence import variance_inflation_factor

# *****Librerías para Visualización de Datos*****
import plotly
import plotly.graph_objects as go
import plotly.express as px
import cufflinks as cf
import stylecloud
from PIL import Image
from plotly.offline import plot,iplot
pd.options.plotting.backend = "plotly"
cf.go_offline()
pd.set_option("display.max_columns",20000)
warnings.filterwarnings('ignore')
pd.options.display.max_columns = None
#pd.set_option('max_rows',500000)


# <h1 style="color:blue"> IMPORTAMOS LIBRERÍA </h1>

# ## IMPORTAMOS ARCHIVO .IPYNB DE FUNCIONES

# In[3]:


get_ipython().run_line_magic('run', "'/home/roman/Documents/Diplomado en Ciencia de Datos - UNAM FES Acatlán/Módulo 1/Proyecto Final/Version Final/proyecto_final_francisco_roman_peña_dela_rosa_libreria.ipynb'")


# ### VARIABLES DEL DATASET

# * **Row ID:**
# * **Order ID:** ID de la orden de compra.
# * **Order Date:** Fecha en la que fue ordenado el artículo.
# * **Ship Date:** Fecha en la que se envia el artículo.
# * **Ship Mode:** Medio o tipo de envío.
# * **Customer ID:** ID del cliente.
# * **Segment:** Segmento o categoría a la que pertenece el producto.
# * **City:** Ciudad.
# * **State:** Estado.
# * **Country:** País.
# * **Postal Code:** Código postal.
# * **Market:** Mercado de acuerdp a la región, en el cual se distribuye el artículo.
# * **Region:** Región en donde es distribuiodo el producto.
# * **Product ID:** ID del producto.
# * **Category:** Categoría a la que pertenece el producto vendido.
# * **Sub-Category:** Sub-categoría a la que pertenece el atículo vendido.
# * **Product Name:** Nombre del producto comercializado.
# * **Sales:** Total de ventas. *** => **TARGET**
# * **Quantity:** Cantidad de artículos vendidos.
# * **Discount:** Descuento aplicado.
# * **Profit:** Utilidad/Ganancia derivada de la venta.
# * **Shipping Cost:** Costo de envío.
# * **Order Priority:** Prioridad de la orden de comprar.

# ### IMPORTAMOS DATASET

# In[4]:


# Importamos dataset y le asignamos el nombre de "gs" => 'Global Superstore 2016'
gs = pd.read_excel('Global_Superstore.xlsx')

#Eliminamos la columna de índice: Row ID
gs = gs.drop(gs.columns[:1], axis=1)

# Cambiamos espacios en nombre de variables por '_' y convertimos todo a minúsculas
gs.columns = gs.columns.str.replace(' ','_').map(str.lower)

# Mostramos el tamaño del dataset
print(gs.shape)

# Mostramos los primeros 5 registros
gs.head(5)


# <h1 style="color:blue"> ETIQUETADO DE VARIABLES </h1>

# In[5]:


# Definimos generador para tener mejor acceso al nombre de las columnas
gen_columns = (col for col in gs.columns)


# In[6]:


# Prefixes for variable types
# 'c_' --> Numeric Variables: Discrete & Continous
# 'v_' --> Categorical Variables
# 'd_' --> Date Type Variables
# 't_' --> Text Type Variables

# Numeric Variables: Discrete & Continous
c_feats = ['sales','quantity','discount','profit','shipping_cost']

#Categorical Variables
v_feats = ['order_id','ship_mode','segment','city','state','country','postal_code',
          'market','region','product_id','category','sub-category','order_priority']

# Date Type Variables
d_feats = ['order_date','ship_date']

#Text Type Variables
t_feats = ['customer_name','product_name']


# In[7]:


# Etiquetamos columnas
gs = label_columns(gs,c_feats,"c_")
gs = label_columns(gs,v_feats,"v_")
gs = label_columns(gs,t_feats,"t_")
gs = label_columns(gs,d_feats,"d_")


# In[8]:


# Visualizamos cinco primeros registros para validar etiquetado de variables
print(gs.shape)
gs.head(5)


# <h1 style="color:blue"> DUPLICADOS </h1>

# In[9]:


gs.head(10)


# In[10]:


# Obtenemos el total de registros duplicados en el dataset
gs.duplicated().sum()


# In[11]:


# Identificamos los 59 registros dupicados
gs[gs.duplicated()]


# In[12]:


# Una vez cuantificados e identificados, procedemos a eliminar duplicados
gs.drop_duplicates(inplace = True)


# In[13]:


# Obtenemos shape y primeros registros del DataFrame actualizado
print(gs.shape)
gs.head(5)


# <h1 style="color:blue"> COMPLETITUD </h1>

# In[14]:


# Aplicamos la función de completitud al DataFrame "gs"
completitud(gs).style.background_gradient()


# In[15]:


# Eliminamos columnas con menos del 80% de completitud
gs = gs.drop(columns = ['v_postal_code'])

# Verificamos shape y aplicación de cambios en DataFrame
print(gs.shape)
gs.head(5)


# * Después de eliminar la(s) variable(s) < 80% de completitud, identificamos que tenemos 7 valores ausentes distribuidos de la siguiente forma:
# 
#     * **2 en v_market**
#     * **2 en t_customer_name**
#     * **1 en v_category**
#     * **1 en v_order_priority**

# In[16]:


completitud(gs).style.background_gradient()


# <h1 style="color:blue"> LIMPIEZA DE TEXTO </h1>

# ## Limpieza de la columna 'v_ship_mode'

# In[17]:


# Revisión preliminar de las variables de texto para identificar: caracteres especiales, errores ortográficos, etc.
gs['v_ship_mode'].value_counts()


# In[18]:


# Eliminamos caracteres que se encuentre fuera del patrón establecido ([^a-zA-Z ]) para la columna => v_ship_mode
gs['v_ship_mode'] = gs['v_ship_mode'].astype(str)
gs['v_ship_mode'] = gs['v_ship_mode'].map(lambda x: clean_text(x.lower(), pattern = '[^a-zA-Z ]', replace = ''))


# ## Limpieza de la columna 't_customer_name'

# In[19]:


gs['t_customer_name'].value_counts()


# In[20]:


# Eliminamos caracteres que se encuentre fuera del patrón establecido ([^a-zA-Z ]) para la columna => t_customer_name
gs['t_customer_name'] = gs['t_customer_name'].astype(str)
gs['t_customer_name'] = gs['t_customer_name'].map(lambda x: clean_text(x.lower(), pattern = '[^a-zA-Z ]', replace = ' '))


# ## Limpieza de la columna 'v_segment'

# In[21]:


gs['v_segment'].value_counts()


# In[22]:


# Eliminamos caracteres que se encuentre fuera del patrón establecido ([^a-zA-Z ]) para la columna => v_segment
gs['v_segment'] = gs['v_segment'].astype(str)
gs['v_segment'] = gs['v_segment'].map(lambda x: clean_text(x.lower(), pattern = '[^a-zA-Z]', replace = ' '))


# ## Limpieza de la columna 'v_city'

# In[23]:


gs['v_city'].value_counts()


# In[24]:


# Eliminamos caracteres que se encuentre fuera del patrón establecido ([^a-zA-Z ]) para la columna => v_city
gs['v_city'] = gs['v_city'].astype(str)
gs['v_city'] = gs['v_city'].map(lambda x: clean_text(x.lower(), pattern = '[^a-zA-Z]', replace = ' '))


# In[25]:


gs.head(3)


# ## Limpieza de la columna 'v_state'

# In[26]:


gs['v_state'].value_counts()


# In[27]:


# Eliminamos caracteres que se encuentre fuera del patrón establecido ([^a-zA-Z ]) para la columna => v_state
gs['v_state'] = gs['v_state'].astype(str)
gs['v_state'] = gs['v_state'].map(lambda x: clean_text(x.lower(), pattern = '[^a-zA-Z]', replace = ' '))


# In[28]:


gs.head(3)


# ## Limpieza de la columna 'v_country'

# In[29]:


gs['v_country'].value_counts()


# In[30]:


# Eliminamos caracteres que se encuentre fuera del patrón establecido ([^a-zA-Z ]) para la columna => v_country
gs['v_country'] = gs['v_country'].astype(str)
gs['v_country'] = gs['v_country'].map(lambda x: clean_text(x.lower(), pattern = '[^a-zA-Z]', replace = ' '))


# In[31]:


gs.head(3)


# ## Limpieza de la columna 'v_market'

# In[32]:


gs['v_market'].value_counts()


# ## Limpieza de la columna 'v_region'

# In[33]:


gs['v_region'].value_counts()


# In[34]:


# Eliminamos caracteres que se encuentre fuera del patrón establecido ([^a-zA-Z ]) para la columna => v_region
gs['v_region'] = gs['v_region'].astype(str)
gs['v_region'] = gs['v_region'].map(lambda x: clean_text(x.lower(), pattern = '[^a-zA-Z]', replace = ''))


# In[35]:


gs.head(3)


# ## Limpieza de la columna 'v_category'

# In[36]:


gs['v_category'].value_counts()


# In[37]:


# Eliminamos caracteres que se encuentre fuera del patrón establecido ([^a-zA-Z ]) para la columna => v_category
gs['v_category'] = gs['v_category'].astype(str)
gs['v_category'] = gs['v_category'].map(lambda x: clean_text(x.lower(), pattern = '[^a-zA-Z]', replace = ''))


# In[38]:


gs.head(3)


# ## Limpieza de la columna 'v_sub-category'

# In[39]:


gs['v_sub-category'].value_counts()


# In[40]:


# Eliminamos caracteres que se encuentre fuera del patrón establecido ([^a-zA-Z ]) para la columna => v_sub-category
gs['v_sub-category'] = gs['v_sub-category'].astype(str)
gs['v_sub-category'] = gs['v_sub-category'].map(lambda x: clean_text(x.lower(), pattern = '[^a-zA-Z]', replace = ''))


# In[41]:


gs.head(3)


# ## Limpieza de la columna 'v_order_priority'

# In[42]:


gs['v_order_priority'].value_counts()


# In[43]:


# Eliminamos caracteres que se encuentre fuera del patrón establecido ([^a-zA-Z ]) para la columna => t_customer_name
gs['v_order_priority'] = gs['v_order_priority'].astype(str)
gs['v_order_priority'] = gs['v_order_priority'].map(lambda x: clean_text(x.lower(), pattern = '[^a-zA-z]', replace = ''))


# In[44]:


print(gs.shape)
gs.head(3)


# <h1 style="color:blue"> CONSISTENCIA </h1>

# In[45]:


# Verificamos que los registros en la columna 'd_order_date' sean válidos: no contengas letras o caracteres especiales
gs['d_order_date'] = gs['d_order_date'].astype(str)
gs['d_order_date'] = gs['d_order_date'].str.replace(r'[a-zA-Z]','')
gs['d_order_date'] = pd.to_datetime(gs['d_order_date'])
gs['d_order_date'] = gs['d_order_date'].dt.strftime('%Y-%m-%d %H:%M:%S')


print(gs.shape)
gs.head(50)


# <h1 style="color:blue"> NORMALIZACIÓN </h1>

# ## Normalización de 'v_ship_mode'

# In[46]:


# Revisar la variable 'v_ship_mode' y verificar si es necesario normalizarla
gs['v_ship_mode'].value_counts()


# ## Normalización de 't_customer_name'

# In[47]:


# Revisar la variable 't_customer_name' y verificar si es necesario normalizarla
gs['t_customer_name'].value_counts()


# ## Normalización de 'v_segment'

# In[48]:


# Revisar la variable 'v_segment' y verificar si es necesario normalizarla
gs['v_segment'].value_counts()


# ## Normalización de 'v_category'

# In[49]:


# Revisar la variable 'v_category' y verificar si es necesario normalizarla
gs['v_category'].value_counts()


# ## Normalización de 'v_sub-category'

# In[50]:


# Revisar la variable 'v_sub-category' y verificar si es necesario normalizarla
gs['v_sub-category'].value_counts()


# ## Normalización de 't_product_name'

# In[51]:


# Revisar la variable 't_product_name' y verificar si es necesario normalizarla
gs['t_product_name'].value_counts()


# In[52]:


gs.dtypes


# In[53]:


gs.describe()


# In[54]:


gs.info()


# <h1 style="color:blue"> ANÁLISIS EXPLORATORIO DE DATOS </h1>

# In[55]:


gs.describe()


# ## Distribución de la variable (v_ship_mode) - Forma de Envío

# In[56]:


my_bar_count(gs,'v_ship_mode','Formas de Envío','','Cantidad')


# In[57]:


my_pie_count(gs,'v_ship_mode','Formas de Envío')


# In[58]:


# groupby v_ship_mode
ship = gs.groupby('v_ship_mode').sum()
ship.style.background_gradient()


# ## Distribución de la variable (v_segment) - Segmento

# In[59]:


my_bar_count(gs,'v_segment','Segmento','','Cantidad')


# In[60]:


my_pie_count(gs,'v_segment','Segmento')


# In[61]:


# groupby v_segment
segment = gs.groupby('v_segment').sum()
segment.style.background_gradient()


# ## Distribución de la variable (v_market) - Mercado

# In[62]:


my_bar_count(gs,'v_market','Mercado','','Cantidad')


# In[63]:


my_pie_count(gs,'v_market','Mercado')


# In[64]:


# groupby v_market
mercado = gs.groupby('v_market').sum()
mercado.style.background_gradient()


# ## Distribución de la variable (v_region) - Región

# In[65]:


my_bar_count(gs,'v_region','Region','','Cantidad')


# In[66]:


my_pie_count(gs,'v_region','Region')


# ## Distribución de la variable (v_category) - Category

# In[67]:


my_bar_count(gs,'v_category','Categoría','','Cantidad')


# In[68]:


my_pie_count(gs,'v_category','Categoría')


# In[69]:


# groupby v_category
category = gs.groupby('v_category').sum()
category.style.background_gradient()


# ## Distribución de la variable (v_sub-category) - Sub-Categoría

# In[70]:


my_bar_count(gs,'v_sub-category','Sub-Categoría','','Cantidad')


# In[71]:


my_pie_count(gs,'v_sub-category','Sub-Categoría')


# ## Distribución de la variable (v_order_priority) - Prioridad de la Orden

# In[72]:


my_bar_count(gs,'v_order_priority','Prioridad de la Orden','','Cantidad')


# In[73]:


my_pie_count(gs,'v_order_priority','Prioridad de la Orden')


# In[74]:


# groupby v_order_priority
order = gs.groupby('v_order_priority').sum()
order.style.background_gradient()


# ## Distribución de la media para la variable (c_sales) - Ventas

# In[75]:


my_histogram(gs,'c_sales',bins = 18,title='',x_title='Ventas',y_title='Conteo')


# ## Distribución de la media para la variable (c_profit) - Utilidad

# In[76]:


my_histogram(gs,'c_profit',bins = 20,title='',x_title='Utilidad',y_title='Conteo')


# ## Distribución de la media para la variable (c_shipping_cost) - Costo de Envío

# In[77]:


my_histogram(gs,'c_shipping_cost',bins = 20,title='',x_title='Costo de Envío',y_title='Conteo')


# ## Distribución de la media para la variable (c_discount) - Descuento

# In[78]:


my_histogram(gs,'c_discount',bins = 20,title='',x_title='Decuento',y_title='Conteo')


# In[79]:


my_box(gs,'v_order_priority','c_discount','Distribucion del Descuento Aplicado',x_title='Prioridad',y_title='Descuento')


# In[80]:


correlacion = abs(gs[['c_profit', 'c_discount', 'c_quantity', 'c_shipping_cost']].corr(method="spearman"))


# In[81]:


correlacion.iplot(kind="heatmap",colorscale="orrd",title="Matriz de Correlación")


# <h1 style="color:blue"> OUTLIERS </h1>

# In[82]:


# Buscar Outliers
feats = list(gs.filter(like="c_").columns)
outliers = OUTLIERS(gs,feats)
outliers


# In[83]:


# Separandolos
indices = list(outliers[outliers['features'] == 'c_sales']['indices'].values)[0]
aux = gs[~gs.index.isin(indices)]


# ## Comparación de Distribución 'c_sales': Con y Sin Outliers

# In[84]:


# Comparando - 'c_sales'
# Distribución con Outliers
gs['c_sales'].iplot(kind='box', color = 'blue')


# In[85]:


# Distribución sin Outliers
aux['c_sales'].iplot(kind='box', color = 'green')


# ## Comparación de Distribución 'c_discount': Con y Sin Outliers

# In[86]:


# Comparando - 'c_discount'
# Distribución con Outliers
gs['c_discount'].iplot(kind='box', color = 'blue')


# In[87]:


# Distribución sin Outliers
aux['c_discount'].iplot(kind='box', color = 'green')


# ## Comparación de Distribución 'c_profit': Con y Sin Outliers

# In[88]:


# Comparando - 'c_profit'
# Distribución con Outliers
gs['c_profit'].iplot(kind='box', color = 'blue')


# In[89]:


# Distribución sin Outliers
aux['c_profit'].iplot(kind='box', color = 'green')


# ## Comparación de Distribución 'c_shipping_cost': Con y Sin Outliers

# In[90]:


# Comparando - 'c_shipping_cost'
# Distribución con Outliers
gs['c_shipping_cost'].iplot(kind='box', color = 'blue')


# In[91]:


# Distribución sin Outliers
aux['c_shipping_cost'].iplot(kind='box', color = 'green')


# ## Comparación de Distribución 'c_quantity': Con y Sin Outliers

# In[92]:


# Comparando - 'c_quantity'
# Distribución con Outliers
gs['c_quantity'].iplot(kind='box', color = 'blue')


# In[93]:


# Distribución sin Outliers
aux['c_quantity'].iplot(kind='box', color = 'green')


# In[94]:


gs.isnull().sum()


# <h1 style="color:blue"> VALORES AUSENTES </h1>

# In[95]:


completitud(gs).style.background_gradient()


# In[96]:


gs['v_market'].value_counts()


# In[97]:


from sklearn.model_selection import train_test_split
X_train,X_test=train_test_split(gs,test_size=.2,random_state=0)


# In[98]:


missings = completitud(X_train)
missings.style.background_gradient()


# ### v_market

# In[99]:


X_train['v_market'],X_test['v_market'] = imputar_moda(gs,'v_market',X_train,X_test)


# In[100]:


X_train['v_market'].value_counts()


# In[101]:


completitud(X_train).style.background_gradient()


# In[102]:


# Revisamos el shape del dataframe antes de la ingeniería de variables
print(X_train.shape)
X_test.shape


# <h1 style="color:blue"> INGENIERÍA DE VARIABLES </h1>

# ## CATEGÓRICAS

# ### One-Hot Encoding / Dummies

# In[103]:


cate = list(gs.filter(like = 'v_').columns)
cate


# In[104]:


feats = ['v_ship_mode','v_segment','v_city','v_state','v_country','v_market','v_region','v_category','v_sub-category',
        'v_order_priority']

for col in feats:
    X_train = pd.get_dummies(X_train, columns = [col], prefix = col)
    X_test = pd.get_dummies(X_test, columns = [col], prefix = col)
X_train.head(5)


# In[105]:


# Añadimos columnas que no estan presentes entre los sets.
miss_cols_test = set(X_train.columns)-set(X_test.columns)
for col in miss_cols_test:
    X_test[col]=0
    
# Asegurando mismo orden de columnas
X_test =X_test[X_train.columns]


# In[106]:


miss_cols_test


# In[107]:


X_test


# In[108]:


print(X_train.shape)
X_test.shape


# ## TEXTO - Count Vectorizer

# In[109]:


text = list(gs.filter(like = 't_').columns)
text


# **t_product_name**

# In[110]:


# Eliminamos stopwords
sw = stopwords.words('english')
X_train['t_product_name'] = X_train['t_product_name'].map(lambda text:' '.join([x for x in text.split(' ') if x not in sw]))
X_test['t_product_name'] = X_test['t_product_name'].map(lambda text:' '.join([x for x in text.split(' ') if x not in sw]))


# In[111]:


X_train.head(5)


# In[112]:


X_test.head(5)


# In[113]:


corpus_jd = " ".join(gs['t_product_name'].values)
corpus_jd


# In[114]:


len(corpus_jd)


# In[115]:


fdist = FreqDist(corpus_jd.split())
hapaxes = fdist.hapaxes()
len(hapaxes)


# In[116]:


hapaxes_ratio = len(hapaxes)/len(corpus_jd)
hapaxes_ratio


# * Nos damos cuenta que tenemos 105 hapaxes, y procedemos a eliminarlos dado que es una cantidad pequeña y el tiempo de cómputo no sería demasiado extenso.

# In[117]:


# Eliminamos hapaxes
X_train['t_product_name'] = X_train['t_product_name'].map(lambda texto:' '.join([word for word in texto.split(' ') if word not in hapaxes]))
X_train['t_product_name'] = X_train['t_product_name'].map(lambda texto:' '.join([word for word in texto.split(' ') if word not in hapaxes]))


# In[118]:


# Tokenizando
X_train['t_product_name'] = X_train['t_product_name'].map(lambda x:x.split())
X_test['t_product_name'] = X_test['t_product_name'].map(lambda x:x.split())


# In[119]:


X_train.head(5)


# In[120]:


X_test.head(5)


# In[121]:


# Lematizando
nltk.download('wordnet')
lem = nltk.stem.wordnet.WordNetLemmatizer()
X_train['t_product_name'] = X_train['t_product_name'].map(lambda text:[lem.lemmatize(word) for word in text])
X_test['t_product_name'] = X_test['t_product_name'].map(lambda text:[lem.lemmatize(word) for word in text])


# In[122]:


X_train.head(5)


# In[123]:


X_test.head(5)


# * El modelo para vectorizar visto en clase sólo usa palabras con 15% o más de frecuencia, y como parte del análisis se observó que más del 80% de los productos que son adquiridos por los diferentes clientes tienen un mínimo de 1 y máximo de 2, además de la diferente ubicación geográfica de cada cliente y el segmento de mercado al que pertenece.
# 
# * **Por esta razón no se aplica el modelo de vectorización de palabras**
# 

# In[124]:


# Se revisan dimensiones del df
print(X_train.shape)
X_test.shape


# <h1 style="color:blue"> REDUCCIÓN DE VARIABLES </h1>

# ### Filtro de alta correlación

# In[125]:


X_train.columns


# In[126]:


X_train.describe()


# In[127]:


list(X_train.columns)


# In[128]:


correlacion = abs(X_train[['v_ship_mode_first class', 'v_ship_mode_same day', 'c_sales', 'v_ship_mode_second class',
       'v_ship_mode_standard class', 'v_segment_consumer','v_segment_corporate','v_segment_home office',
                          'v_market_APAC','v_market_Africa','v_market_Canada','v_market_EMEA','v_market_EU','v_market_LATAM','v_market_US']].corr(method="spearman"))


# In[129]:


correlacion.iplot(kind="heatmap",colorscale="orrd",title="Matriz de Correlación")


# In[130]:


for col in correlacion.columns:
    aux = correlacion[[col]][correlacion[[col]]>0.7].dropna()
    if len(aux)>1:
        display(aux)


# ### Correlación con Objetivo

# In[131]:


correlacion = abs(X_train[['v_ship_mode_first class', 'v_ship_mode_same day', 'c_sales', 'v_ship_mode_second class',
       'v_ship_mode_standard class', 'v_segment_consumer','v_segment_corporate','v_segment_home office',
                          'v_market_APAC','v_market_Africa','v_market_Canada','v_market_EMEA','v_market_EU','v_market_LATAM','v_market_US']].corr(method='spearman'))

low_corr = correlacion[correlacion['c_sales'] < 0.1][['c_sales']].sort_values(by = 'c_sales')
low_corr.style.background_gradient()


# In[132]:


# Eliminamos las columnas con correlacion menor a 0.1 con el objetivo
X_train = X_train.drop(columns = low_corr.index)
X_test = X_test.drop(columns = low_corr.index)


# In[133]:


X_train.head(3)


# <h1 style="color:blue"> TABLA FINAL </h1>

# In[135]:


# Renombramos variable objetivo
X_train = X_train.rename(columns = {'c_sales':'tgt_sales'})
X_test = X_test.rename(columns = {'c_sales':'tgt_sales'})


# In[136]:


print(X_train.shape)
X_train.head(5)


# In[137]:


print(X_test.shape)
X_test.head(5)


# In[138]:


X_train.describe()

