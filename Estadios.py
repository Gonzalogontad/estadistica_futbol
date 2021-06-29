import csv 
from difflib import SequenceMatcher
import time
import re
import requests
from bs4 import BeautifulSoup

def scrap_stadiums(URL,csv_file):
    response = requests.get(URL)
    page = BeautifulSoup(response.text, 'html.parser')
    menu = page.find(id= 'taxonomy_dropdown_widget_dropdown_3')
    menu=str(menu)
    pattern = r'<option value="(http\S*)">'
    stadiums_URLS=re.findall(pattern, menu)
    data=[]
    #print (stadiums_URLS)
    header = ['Propietario del estadio', 'Fecha de fundación del club', 'Deporte', 'Nombre oficial','Nombre oficial del estadio', 'Fecha de inauguración', 'Dirección', 'Capacidad','Afiliación / Liga de origen']
    default_dict= {}
    for key in header:
        default_dict[key]='None'

    for index,stadium_URL in enumerate(stadiums_URLS[0:]):
        try:
            response = requests.get(stadium_URL)
        except:
            data.append (default_dict)
            continue
        page = BeautifulSoup(response.text, 'html.parser')
        #mydivs = page.find_all("div", {"class": "inside-article"})
        mydivs = page.find_all("h2", {"class": "entry-title"})
        print (f'{index+1}/{len(stadiums_URLS)}')
        for div in mydivs:
            div=div.find ('a')
            link=div.get('href')
            try:
                response = requests.get(link)
            except:
                data.append (default_dict)
                continue
            page = BeautifulSoup(response.text, 'html.parser')
            table = page.find_all("table", {"class": "width200"})
            data.append(HTML_table2dict (str(table)))
        #Creo archivo de datos CSV
    with open('raw_stadiums.txt', 'a') as file:
        for row in data:
            file.write (str(row)+'\n')

    with open(csv_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writeheader()
        for row in data:
            writer.writerow(row)
    print (data)

def HTML_table2dict(HTML_table):
    table = BeautifulSoup(HTML_table,'html.parser')
    results = {}
    for row in table.findAll('tr'):
        aux = row.findAll('td')
        results[aux[0].string] = aux[1].string

    return results

def get_stadium(place, team1, team2, date, notes, stadiums):
    pattern=r'Nota: ?Se ?jug[oó] ?en ?cancha ?de ?(.*).?'
    notes_team_stadium=re.findall(pattern, notes)
    if notes_team_stadium:#parsear nota
        team1=notes_team_stadium[0]
    

    #Busco los estadios en el mismo lugar(ciudad)
    same_place=[]
    name = '***'+team1
    wikiname= '***'+team1
    for stadium in stadiums:
        if SequenceMatcher(None, stadium['Place'], place).ratio()>0.6:
            if SequenceMatcher(None, stadium['Team'], team1).ratio()>0.6 or SequenceMatcher(None, stadium['Team'], team2).ratio()>0.6:
                match_date = time.strptime(date, "%d/%m/%Y")
                start_date = time.strptime(stadium['Start'], "%d/%m/%Y")
                end_date = time.strptime(stadium['End'], "%d/%m/%Y")
                if match_date>= start_date and match_date < end_date:
                    name=stadium['Name']
                    wikiname=stadium['WikiName']
    return name, wikiname

def get_stadiums_list (CSV_path):
    stadiums_list=[]
    with open(CSV_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            stadiums_list.append(row)
    return stadiums_list


if __name__ == "__main__":
    stadiums_list = get_stadiums_list('Stadiums.csv')
    stadium_name=get_stadium ('Nuñez', 'huracan', 'boca','25/11/1990','Nota: Se jugo en cancha de river.',stadiums_list)
    print (stadium_name)

    #scrap_stadiums('https://www.estadiosdeargentina.com.ar/','Stadiums2.csv')