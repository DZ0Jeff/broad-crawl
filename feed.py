# from infolink.utils import read_links
import requests
import numpy as np
from config import HOSTS
from utils import read_links
from scrapper_boilerplate import remove_duplicates_on_list


def feed(host:str, datalink:list):
    try:
        res = requests.post(f"{host}/send", json=list(datalink))
        return {"host": host, "code": res.status_code, "status": res.text}

    except Exception as error:
        return str(error)


def main():
    links = read_links('assets/sites_faltantes.xlsx', 'website', excel=True) #read_links(limit=LINK_LIMIT) # numbers of links

    # print(links)
    links = remove_duplicates_on_list(links)
    print(f'{len(links)} links found!')

    # split the origin links to send across the vps
    parts_to_send_across_vps = np.array_split(links, len(HOSTS))

    # distribute the links across the numbers of vps selected
    for host, links in zip(HOSTS, parts_to_send_across_vps):
        print(feed(host, links))


if __name__ == "__main__":
    main()
