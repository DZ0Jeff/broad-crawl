import pandas as pd
from scrapper_boilerplate import dataToCSV
import urllib.parse


def base_url(url, with_path=False):
    parsed = urllib.parse.urlparse(url)
    path   = '/'.join(parsed.path.split('/')[:-1]) if with_path else ''
    parsed = parsed._replace(path=path)
    parsed = parsed._replace(params='')
    parsed = parsed._replace(query='')
    parsed = parsed._replace(fragment='')
    return parsed.geturl()


df = pd.read_csv('data.csv')        
    
for i in range(len(df)):
    print(f"{i}/{len(df)}")
    if i < 51772: continue
    data = dict()

    origin = df['origin'].iloc[i]
    link = df['link'].iloc[i]
    title = df['title'].iloc[i]
    content = df['content'].iloc[i]

    try:
        data['origin'] = base_url(link)
        data['link'] = link
        data['title'] = title
        data['content'] = content

        dataToCSV(data, 'filtered-origin.csv')

    except Exception:
        continue
