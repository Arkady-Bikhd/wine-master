from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas as pd
from collections import defaultdict
from pprint import pprint
import argparse


def get_wine_description(wine_filename):
   
    wine_description = pd.read_excel(wine_filename, keep_default_na=False)
    wine_description = wine_description.to_dict(orient='records')    
    commodity_group = defaultdict(list)     
    for commodity in wine_description:       
        commodity_group[commodity['Категория']].append(commodity)  
            
    return commodity_group


def get_declension(year): 

    remainder = year % 100    
    if remainder % 10 == 1 and remainder != 11: 
        return "год" 
    if remainder % 10 in {2, 3, 4} and not (remainder in {12, 13, 14}): 
        return "года"
    return "лет"

def main():
    
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    wine_file = get_initial_args()

    template = env.get_template('template.html')
    foundation_year = 1920
    time_duration = datetime.date.today().year - foundation_year

    rendered_page = template.render(
        checked_time = time_duration,
        years_stamp = get_declension(time_duration),
        wine_description = get_wine_description(wine_file)   
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)



    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


def get_initial_args():
     
    parser = argparse.ArgumentParser(
        description='Новое русское вино',               
    )
    parser.add_argument('-wf','--wfile', default='wine.xlsx', help='Введите название файла')
    args = parser.parse_args()
    return args.wfile
    

if __name__ == '__main__':

    main()