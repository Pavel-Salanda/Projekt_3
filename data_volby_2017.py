"""
data_volby_2017.py: the third project to the Engeto Online Python Academy

author: Pavel Šalanda
email: pavel.salanda@gmail.com
discord: pavelsalanda
"""

import sys
import requests
from bs4 import BeautifulSoup
import csv


'''checking the correctness of the arguments'''
if len(sys.argv) != 3:
    print('You entered an invalid number of arguments')
    exit()
elif 'https:' not in sys.argv[1]:
    print('You entered the first argument wrong, the first argument must be a link')
    exit()
elif 'https:' in sys.argv[2]:
    print('The second argument must be the name of the output file, not a link')
    exit()
else:
    print('Argument checking is OK')
def server_response_processing (url):
    '''Checking the response and loading the page conten'''
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
    else:
        print('The request failed with code:', response.status_code)
        exit()
    return (html)

def create_soup_object (html):
    '''Creates a BeautifulSoup object'''
    soup = BeautifulSoup(html, 'html.parser')
    return (soup)

def find_table (soup):
    '''Finds all tables on the page'''
    tables = soup.find_all('table')
    return (tables)

def data_from_tables (tables):
    '''Creates an empty list for output.
    It goes through all the tables and produces a concatenated output without headers and columns with "X"'''
    data = []
    for table in tables:
        lines = table.find_all('tr')
        for line in lines:
            if line.find('th') is None:
                columns = line.find_all(['td'])
                text_line = [column.get_text() for column in columns]
                text_line.pop()
                if '-' not in text_line:
                    data.append(text_line)
    return(data)

def find_links (tables):
    '''Creates an empty list for links.
    It goes through all the tables, looks for links and village number, filters out the wrong ones, saves the right ones'''
    links_to_data = []
    for table in tables:
        links = table.find_all('a')
        for link in links:
            link_and_number = link.get('href'),link.get_text('hrev')
            if 'X' != link.get_text('hrev'):
                links_to_data.append(link_and_number)
    return (links_to_data)

def link_verification (url):
    '''It will verify the links to individual village results'''
    complete_link = []
    for i in url:
        complete_link.append(i[1])
        complete_link.append(f'https://volby.cz/pls/ps2017nss/{i[0]}')
    html = []
    for a in complete_link:
        data = []
        if 'https' in a:
            verification = server_response_processing(a)
            data.append(verification)
        else:
           data.append(a)
        html.append(data)
    new_html = [html[i:i + 2] for i in range(0, len(html), 2)]
    return (new_html)

def create_soup (html):
    '''Creates a soup object for individual village links'''
    soup_links = []
    for i in html:
        data = []
        data.append(i[0])
        string = ', '.join(map(str, i[1]))
        soup = create_soup_object(string)
        data.append(soup)
        soup_links.append(data)
    return (soup_links)

def summary_data_village (links):
    '''Gets summary data for a village'''
    data = []
    for i in links:
        data_village = []
        for a in i:
            if isinstance(a,list):
                data_village.append(a)
            elif isinstance(a, BeautifulSoup):
                voter_table = a.find('table', {'class': 'table'})
                data_village.append(voter_table.find_all('td')[3].get_text().replace('\xa0', '')) #voters in the list
                data_village.append(voter_table.find_all('td')[4].get_text().replace('\xa0', '')) #issued envelopes
                data_village.append(voter_table.find_all('td')[7].get_text().replace('\xa0', '')) #valid votes
        data.append(data_village)
    return (data)

def party_results (links):
    '''Find the table with the number of votes for the candidate parties'''
    data_party = []
    for i in links:
        data = []
        for a in i:
            if isinstance(a,list):
                data.append(a)
            elif isinstance(a, BeautifulSoup):
                table_party = a.find_all('table')[1:]
                for table in table_party:
                    lines = table.find_all('tr')[2:]
                for line in lines:
                    columns = line.find_all('td')[1:3]
                    text_line = [column.get_text() for column in columns]
                    data.append(text_line)
        data_party.append(data)
    return (data_party)

def create_dictionary (village,data,party):
    '''Creates a dictionary where all data is combined'''
    dictionary_data = []
    for i in village:
        dictionary_village = {}
        dictionary_village['code'] = i[0]
        dictionary_village['location'] = i[1]
        for a in data:
            b = ', '.join(map(str, a[0]))
            if b == dictionary_village['code']:
                dictionary_village['registered'] = a[1]
                dictionary_village['envelopes'] = a[2]
                dictionary_village['valid'] = a[3]
        for c in party:
            d = ', '.join(map(str, c[0]))
            if d == dictionary_village['code']:
                for e in c[1:]:
                    if '-' not in e:
                        dictionary_village[e[0]] = e[1]
        dictionary_data.append(dictionary_village)
    dictionary_data.append(dictionary_village)
    return (dictionary_data)

def create_csv (dictionary, name):
    '''Creates a csv file'''
    csv_file = (f'{name}.csv')
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=dictionary[0].keys(), delimiter=';')
        writer.writeheader()
        writer.writerows(dictionary)
    return (print(f'CSV file "{csv_file}" has been created.'))


def main(url):
    soup = create_soup_object(server_response_processing(url))
    table = find_table(soup)
    data = data_from_tables(table)
    links_to_data = find_links(table)
    link_checking = link_verification(links_to_data)
    link_soup = create_soup(link_checking)
    table_of_voters = summary_data_village(link_soup)
    party = party_results(link_soup)
    final_data = create_dictionary(data,table_of_voters,party)
    creation_of_csv = create_csv(final_data, file_name)

if __name__ == '__main__':
    url = sys.argv[1]
    file_name = sys.argv[2]
    main(url)









