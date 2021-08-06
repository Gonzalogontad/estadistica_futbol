from bs4 import BeautifulSoup
import requests
import re
import csv 
import pathlib
from pathlib import Path
import numpy as np
import math
from difflib import SequenceMatcher
from Estadios import get_stadium, get_stadiums_list

def unique_similars (rep_elements):
    uni_elements=[]
    uni_elements.append (rep_elements[0])
    
    for rep_element in rep_elements:
        match= False
        for uni_element in uni_elements:
            if SequenceMatcher(None, rep_element, uni_element).ratio()>0.8:
                match = True
        if match == False:
            uni_elements.append(rep_element)
    return uni_elements

def calcular_fechas(partidos):
    nfant=0 #Numero de fecha anterior
    equipos1 = [partido [2] for partido in partidos if len(partido)>2]
    #equipos = list(set(equipos1))
    equipos = unique_similars(equipos1)
    #print (equipos)
    for npartido in range(len(partidos)):
        partidos[npartido]=list (partidos[npartido])
        cant=len(equipos)
        cpf=math.floor(cant/2)
        nf=(npartido+1)/cpf
        nf=math.ceil(nf)
        nf=int(nf)
        partidos[npartido].append (str(nf))


        

        
def HTML_scores_parse (URL):

    response = requests.get(URL)
    page = BeautifulSoup(response.text, 'html.parser')
    #Reemplazo los tags <br> por \n para poder hacer split de lineas
    for br in page.find_all("br"):
        br.replace_with("\n")
    
    mydivs = page.getText()#Elimino todos los tags HTML

    '''
    #Busco el contenido de la pagina
    mydivs = page.find_all("div", {"class": "post-body entry-content"})
    mydivs=str(mydivs)
    '''
    #x = mydivs.find("1ra. Fecha")
    x = mydivs.find("El Torneo")
    if x < len(mydivs):
        mydivs=mydivs[x:]
    '''
    HTML_LABELS=   [('<br/>','\n'),
                    ('<em>',''),
                    ('<span style="color:#33cc00;">',''),
                    ('<span style="color:#cc66cc;">',''),
                    ('<span style="color:#009900;">',''),
                    ('<strong>',''),
                    ('</strong>',''),
                    ('</em>',''),
                    ('</span>',''),
                    ('<div style="clear: both;">',''),
                    ('<div>',''),
                    ('</div>',''),
                    ('<title>',''),
                    ('</title>','')]
    elimino etiquetas HTML para obtener texto plano
    for label in HTML_LABELS:
        mydivs=mydivs.replace(label[0], label[1])  
    '''              
    
    pattern = r'(\S*\/\S*\/\S*):? en (.*): (\D*) (\d*)\s?(?:\((.*)\))?, (\D*) (\d*)\s?(?:\((.*)\))?-?(Nota:\s?.*.)?'
    pattern_date = r'(\d\d\/\d\d\/\d*)'
    mydivs=mydivs.replace('\nNota:','-Nota:') #si se encuantra una nota, se quita \n para que se anexe al partido
    lines = mydivs.splitlines()
    
    partidos=[]
    error_lines=[]
    errors=[]
    #Parseo los resultados de los partidos
    for line in lines:
        partido = re.findall(pattern, line)
        if partido:
            partidos.append(partido[0])
        #Si hay error al parsear guardo la linea para correccion manual    
        else:   
            partido=re.findall(pattern_date, line)
            if partido:
                partidos.append(partido)
                error_line = len (partidos)+1
                error_lines.append(error_line)
                errors.append(f'Error en linea {error_line}: {line}\n')
    
    calcular_fechas(partidos)

    #Obtener nombre del torneo
    page_title=page.find('title') #uso el nombre de la pagina web como nombre del torneo
    page_title=page_title.getText()
    page_title=page_title.replace('historiayfutbol: Argentina: ','')
    page_title=page_title.replace('"','')
    page_title=page_title.replace('/','-')

    stadiums_list = get_stadiums_list('Stadiums.csv')
    if (not stadiums_list):
        raise Exception('Error al leer el archivo de Estadios')
    for index, partido in enumerate(partidos):
        if len(partido) == 10:
            stadium_name,stadium_wikiname = get_stadium (partido [1], partido [2], partido [5],partido [0],partido [8],stadiums_list)
            partidos[index].append(stadium_name)
            partidos[index].append(stadium_wikiname)
            partidos[index].append(page_title)


    #Output files path
    current_dir = ''#str(pathlib.Path(__file__).parent) #Path actual

    #raw_data_path =Path(current_dir+'/output/'+page_title+'_raw.txt')
    #csv_path = Path(current_dir+'/output/'+page_title+'.csv')
    #csv_error_path = Path(current_dir+'/output/'+page_title+'_errors.txt')
    raw_data_path ='output/'+page_title+'_raw.txt'
    csv_path = 'output/'+page_title+'.csv'
    csv_error_path = 'output/'+page_title+'_errors.txt'
    print (page_title)
    
    #Creo archivo de datos en bruto
    with open(raw_data_path, 'w', encoding='utf-8') as file:
        file.write (mydivs)

    #Encabezado del archivo CSV
    header=('Fecha','Lugar','Equipo1','Goles1','Goleadores1','Equipo2','Goles2','Goleadores2','Notas', 'N_Fecha','Estadio','Estadio_wikiname','Torneo')

    #Creo archivo de datos CSV
    with open(csv_path, 'w', encoding='utf-8') as file:
        file_writer = csv.writer(file)
        file_writer.writerow(header)
        for row in partidos:
            file_writer.writerow(row)

    #Creo archivo de errores a corregir manualmente
    with open(csv_error_path,'w',encoding= 'utf-8') as file:
        file.writelines(errors)

if __name__ == "__main__":
    URLs = [ 'http://josecarluccio.blogspot.com/2010/02/argentina-1ra-b-afa-1971.html',
            'http://josecarluccio.blogspot.com/2010/02/argentina-1ra-division-afa-1972_24.html',
            'http://josecarluccio.blogspot.com/2010/02/argentina-1ra-division-afa-1972.html',
            'http://josecarluccio.blogspot.com/2010/02/argentina-1ra-aficionados-afa-1971.html',
            'http://josecarluccio.blogspot.com/2010/02/argentina-1ra-aficionados-afa-1971-zona_21.html',
            'http://josecarluccio.blogspot.com/2010/02/argentina-1ra-aficionados-afa-1971-zona.html'
    ]
    #URLs = [ 'http://josecarluccio.blogspot.com/2009/06/argentina-1ra-b-afa-1953.html']
    for url in URLs:
        HTML_scores_parse(url)

