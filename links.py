import requests


links = [
    {'name': 'vps1 (dinâmico parte 1)', 'link': 'http://191.101.71.155:5050'},
    {'name': 'vps1 (estático sem filtros)', 'link':'http://191.101.71.155:5051'},
    {'name': 'vps2 (estático c/filtros)', 'link': 'http://191.101.235.251:5051'},
    {'name': 'vps2 (dinâmico parte 2)', 'link': 'http://191.101.235.251:5050'},
    {'name': 'vps2 (estático s/ filtros parte II)', 'link': 'http://191.101.235.251:5052'},
    {'name': 'vps2 (dinámico s/ filtros parte II)', 'link': 'http://191.101.235.251:5053'},
    {'name': 'vps2 (nc adicionais, parte II, estático)', 'link': 'http://191.101.235.251:5054'},
    {'name': 'vps2 (nc adicionais, parte II, dinámico)', 'link': 'http://191.101.235.251:5055'},
    {'name': 'vps3 (batch maior I)', 'link': "http://181.215.134.20:5050"},
    {'name': 'vps4 (batch maior II)', 'link': "http://181.215.134.21:5050"},
    {'name': 'vps5 (batch maior III)', 'link': "http://181.215.134.23:5050"}
]

for link in links:
    try:
        response = requests.get(link['link'])
        if response.ok:
            print(f"{link} OK!")

        else:
            print(f"{link} code: {response.status_code}") 

    except Exception:
        print(f"{link} - ERRO!")