
from bs4 import BeautifulSoup
import requests
import re
import csv 

def HTML_scores_parse (URL):

    response = requests.get(URL)
    page = BeautifulSoup(response.text, 'html.parser')

    mydivs = page.find_all("div", {"class": "post-body entry-content"})
    mydivs=str(mydivs)
    x = mydivs.find("1ra. Fecha")
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
                    ('</div>','')]

    for label in HTML_LABELS:
        mydivs=mydivs.replace(label[0], label[1])                

    with open('raw.txt', 'w') as file:
        file.write (mydivs)

    pattern = r'(\S*\/\S*\/\S*) en (.*): (\D*) (\d*)\s?(\((.*)\))?, (\D*) (\d*)\s?(\((.*)\))?\n?(Nota:\s?.*.)?'
    partidos = re.findall(pattern, mydivs)
    for partido in partidos:
        print (partido)

    with open('test.csv', 'w', encoding='utf-8') as file:
        file_writer = csv.writer(file)
        for row in partidos:
            file_writer.writerow(row)

if __name__ == "__main__":
    URL = 'http://josecarluccio.blogspot.com/2010/02/argentina-1ra-b-afa-1971.html'
    HTML_scores_parse(URL)

