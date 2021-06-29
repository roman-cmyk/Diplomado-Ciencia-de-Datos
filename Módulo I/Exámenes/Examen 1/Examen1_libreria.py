#!/usr/bin/env python
# coding: utf-8

# ## **Functions**

# In[2]:


# This function is used to correct invalid month' names => 'v_mes_hechos'
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


# In[4]:


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


# In[3]:


# This functions is used to validate 'lat' & 'lng' values
    ## Latitude must be a number between -90 and 90
    ## Longitude must a number between -180 and 180
def lng_val(value):
    try:
        if -180<=value<=+180:
            return value
        else:
            return 'Incorrect'
    except:
        value


# In[4]:


# This functions is used to validate 'lat' & 'lng' values
    ## Latitude must be a number between -90 and 90
    ## Longitude must a number between -180 and 180
def lat_val(value):
    try:
        if -90<=value<=+90:
            return value
        else:
            return 'Incorrect'
    except:
        value


# In[ ]:


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


# In[ ]:


# This function is used to replace invalid letters in text columns => 't_categoria_delito' column
def replace_words_catdelito(text):
    try:
        text = text.replace('VEHÃCULO','VEHICULO').replace('VÃA','VIA').replace('PÃBLICA','PUBLICA')
        text = text.replace('VIOLACIÃN','VIOLACION').replace('HABITACIÃN','HABITACION')
        return text
    except:
        return 'Check'


# In[5]:


# This function is used to correct invalid data entries in 't_colonia_hechos' => accented characters
# With the same purpose like functions described above (e.g. AMPLIACIÃN)

def accents_colonia_hechos(text):

    try:
        text = unicode(text, 'utf-8')
    except NameError:
        pass

    text = unicodedata.normalize('NFD', text)           .encode('ascii', 'ignore')           .decode("utf-8")

    return str(text)


# In[6]:


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


# In[7]:


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


# In[ ]:


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


# In[ ]:


# This function is used to know if weekend or not: 1 => YES and 0 => NO
def weekend(day):
    if day == 'Friday' or day == 'Saturday' or day == 'Sunday':
        return '1'
    else:
        return '0'


# In[ ]:


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


# In[ ]:


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


# In[ ]:


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


# In[ ]:


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

