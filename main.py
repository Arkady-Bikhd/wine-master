from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas as pd
from collections import defaultdict
from pprint import pprint


def get_wine_description():
   
    wine_description = pd.read_excel('wine3.xlsx', engine='openpyxl', keep_default_na=False)
    wine_description = wine_description.to_dict(orient='records')    
    commodity_group = defaultdict(list)     
    for commodity in wine_description:       
        commodity_group[commodity['Категория']].append(commodity)  
            
    return commodity_group


def get_declension(year): 

    remainder = year % 100
    suffix = ["лет", "год", "года"] 
    if remainder % 10 == 1 and remainder != 11: 
        return suffix[1] 
    if remainder % 10 in {2, 3, 4} and not (remainder in {12, 13, 14}): 
        return suffix[2]
    return suffix[0]

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')
time_duration = datetime.date.today().year - 1920
w = get_wine_description()
for ww, www in sorted(w.items()):
    print(www)


rendered_page = template.render(
    checked_time = time_duration,
    years_stamp = get_declension(time_duration),
    wine_description = get_wine_description()
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)



server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
