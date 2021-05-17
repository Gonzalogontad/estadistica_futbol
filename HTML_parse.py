
from bs4 import BeautifulSoup
import requests
import re
import csv 
import pathlib
from pathlib import Path

def HTML_scores_parse (URL):

    response = requests.get(URL)
    page = BeautifulSoup(response.text, 'html.parser')
    
    #Busco el contenido de la pagina
    mydivs = page.find_all("div", {"class": "post-body entry-content"})
    mydivs=str(mydivs)
    #x = mydivs.find("1ra. Fecha")
    x = mydivs.find("El Torneo")
    if x < len(mydivs):
        mydivs=mydivs[x:]
    HTML_LABELS=   [('<br/>','\n'),
                    ('<em>',''),
                    ('<span style="color:#33cc00;">',''),
                    ('<span style="color:#cc66cc;">',''),
                    ('<strong>',''),
                    ('</strong>',''),
                    ('</em>',''),
                    ('</span>',''),
                    ('<div style="clear: both;">',''),
                    ('<div>',''),
                    ('</div>',''),
                    ('<title>',''),
                    ('</title>','')]
    #elimino etiquetas HTML para obtener texto plano
    for label in HTML_LABELS:
        mydivs=mydivs.replace(label[0], label[1])                
    
    pattern = r'(\S*\/\S*\/\S*):? en (.*): (\D*) (\d*)\s?(?:\((.*)\))?, (\D*) (\d*)\s?(?:\((.*)\))?-?(Nota:\s?.*.)?'
    pattern_date = r'(\S*\/\S*\/\S*)'
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



    #Output files path
    current_dir = ''#str(pathlib.Path(__file__).parent) #Path actual
    page_title=page.find('title') #uso el nombre de la pagina web como nombre de los archivos
    for label in HTML_LABELS:
        page_title=str(page_title).replace(label[0], label[1])
    page_title=page_title.replace('historiayfutbol: Argentina: ','')
    #raw_data_path =Path(current_dir+'/output/'+page_title+'_raw.txt')
    #csv_path = Path(current_dir+'/output/'+page_title+'.csv')
    #csv_error_path = Path(current_dir+'/output/'+page_title+'_errors.txt')
    raw_data_path ='output/'+page_title+'_raw.txt'
    csv_path = 'output/'+page_title+'.csv'
    csv_error_path = 'output/'+page_title+'_errors.txt'
    print (page_title)
    
    #Creo archivo de datos en bruto
    with open(raw_data_path, 'w') as file:
        file.write (mydivs)

    #Encabezado del archivo CSV
    header=('Fecha','Lugar','Equipo 1','Goles 1','Goleadores 1','Equipo 2','Goles 2','Goleadores 2','Notas')

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

    for url in URLs:
        HTML_scores_parse(url)

