from bs4 import BeautifulSoup
import requests
import re
import csv 

URL = 'http://josecarluccio.blogspot.com/2010/02/argentina-1ra-b-afa-1971.html'
response = requests.get(URL)
#print (response.text)
pattern = r'(\S*\/\S*\/\S*) en (\S*): (\D*) (\d*)\s?(\((.*)\))?, (\D*) (\d*)\s?(\((.*)\))?\n?(Nota:\s?.*.)?'
page = BeautifulSoup(response.text, 'html.parser')



mydivs = page.find_all("div", {"class": "post-body entry-content"})
#print (type(mydivs))
mydivs=str(mydivs)
x = mydivs.find("1ra. Fecha")
mydivs=mydivs[x:]

mydivs=mydivs.replace('<br/>','\n')
mydivs=mydivs.replace('<em>','')
mydivs=mydivs.replace('<span style="color:#33cc00;">','')
mydivs=mydivs.replace('<span style="color:#cc66cc;">','')
mydivs=mydivs.replace('<strong>','')
mydivs=mydivs.replace('</strong>','')
mydivs=mydivs.replace('</em>','')
mydivs=mydivs.replace('</span>','')
mydivs=mydivs.replace('<div style="clear: both;">','')
mydivs=mydivs.replace('<div>','')
mydivs=mydivs.replace('</div>','')
#print (mydivs)
partidos = re.findall(pattern, mydivs)
for partido in partidos:
    print (partido)

  
lol = [(1,2,3),(4,5,6),(7,8,9)]
item_length = len(lol[0])

with open('test.csv', 'w') as file:
    file_writer = csv.writer(file)
    for row in partidos:
        file_writer.writerow(row)


'''
20/03/1971 en Mataderos: Nueva Chicago 10 (Jorge Jhones y Jorge Pietrone), All Boys 2 (Luis Medina (p) y Antonio Borruto)
Nota: Se jugó en cancha de Argentinos Juniors.
20/03/1971 en Caseros: Estudiantes 0, Dep. Morón 1 (Daniel Bilbao)
20/03/1971 en Paternal: Comunicaciones 3 (Eduardo Ricagni (hijo) 2 y Juan A. Dedovich), Temperley 1 (Maurilio Alves de Souza)
Nota: Se jugó en cancha de Argentinos Juniors.
20/03/1971 en Sarandí: Arsenal FC. 3 (José Martino, Eduardo Janín y Juan C. Santiago), Almirante Brown 0
20/03/1971 en Quilmes: Quilmes 0, Excursionistas 1 (Albino Valentini)'''