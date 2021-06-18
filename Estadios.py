import csv 
from difflib import SequenceMatcher
import time
import re
def get_stadium(place, team1, team2, date, notes, stadiums):
    pattern=r'Nota: ?Se ?jug[oó] ?en ?cancha ?de ?(.*).?'
    notes_team_stadium=re.findall(pattern, notes)
    if notes_team_stadium:#parsear nota
        team1=notes_team_stadium[0]
    

    #Busco los estadios en el mismo lugar(ciudad)
    same_place=[]
    name = '***'+team1
    for stadium in stadiums:
        if SequenceMatcher(None, stadium['Place'], place).ratio()>0.6:
            if SequenceMatcher(None, stadium['Team'], team1).ratio()>0.6 or SequenceMatcher(None, stadium['Team'], team2).ratio()>0.6:
                match_date = time.strptime(date, "%d/%m/%Y")
                start_date = time.strptime(stadium['Start'], "%d/%m/%Y")
                end_date = time.strptime(stadium['End'], "%d/%m/%Y")
                if match_date>= start_date and match_date < end_date:
                    name=stadium['Name']
    return name

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