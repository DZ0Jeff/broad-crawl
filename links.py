import requests


links = [
    {'name':'vps1-dinamic-I', 'link': 'http://191.101.71.155:5050'},
    {'name': 'vps1-static-new', 'link':'http://191.101.71.155:5051'},
    {'name': 'vps2-static-old', 'link': 'http://191.101.235.251:5051'},
    {'name': 'vps2-dinamico-part-I', 'link': 'http://191.101.235.251:5050'},
    {'name': 'vps3', 'link': "http://181.215.134.20:5050"},
    {'name': 'vps4', 'link': "http://181.215.134.21:5050"},
    {'name': 'vps5', 'link': "http://181.215.134.23:5050"}
]

for link in links:
    response = requests.get(link['link'])
    if response.ok:
        print(f"{link} OK!")

    else:
        print(f"{link} code: {response.status_code}") 
