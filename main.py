import os
import re
import time
import multiprocessing
import pandas as pd
import logging
import urllib.parse
import argparse
import sys
import warnings
import uuid

from functools import wraps, partial
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapper_boilerplate import TelegramBot, remove_duplicates_on_list, load_dynamic_page
from config import PROCESS


if not sys.warnoptions:
    warnings.simplefilter("ignore")

# Programa rodou em 64 seconds
SAVE_DIRECTORY = 'data'
settings = {
    'LOG_LEVEL': 'INFO',
    'DEPTH_LIMIT': 2,
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)', 
    # descomentar aqui se usar o recurso de insert a cada x dados
    'CONCURRENT_REQUESTS': 100, # default to 16
    # 'CONCURRENT_REQUESTS_PER_DOMAIN': 16, # default to 8
    # 'CONCURRENT_REQUESTS_PER_IP': 0, # default to 0

    # 'ITEM_PIPELINES': {
    #     'pipelines.CSVCustomPipeline': 100,
    # },
    'DOWNLOADER_MIDDLEWARES': {
        'middlewares.SeleniumMiddleware': 543,
    },
    'COOKIES_ENABLED': False,
    # 'SCHEDULER_PRIORITY_QUEUE': 'scrapy.pqueues.DownloaderAwarePriorityQueue',
    # 'REACTOR_THREADPOOL_MAXSIZE': 20,
    'RETRY_ENABLED': True,
    'DOWNLOAD_TIMEOUT': 15,
    'REDIRECT_ENABLED': True,
    'AJAXCRAWL_ENABLED': True,
    'DEPTH_PRIORITY': 1,
    'TELNETCONSOLE_PORT': None,
    # 'SCHEDULER_DISK_QUEUE': 'scrapy.squeues.PickleFifoDiskQueue',
    # 'SCHEDULER_MEMORY_QUEUE': 'scrapy.squeues.FifoMemoryQueue',
    # 'LOG_FILE': 'crawler.log', # logging file
    'FEEDS': {
        f'{SAVE_DIRECTORY}/data.csv': {'format': 'csv'}
    }
}

def save_error(link):
    with open('error.txt', 'a') as file_error:
        file_error.write(f"{link}\n")


def base_url(url, with_path=False):
    parsed = urllib.parse.urlparse(url)
    path   = '/'.join(parsed.path.split('/')[:-1]) if with_path else ''
    parsed = parsed._replace(path=path)
    parsed = parsed._replace(params='')
    parsed = parsed._replace(query='')
    parsed = parsed._replace(fragment='')
    return parsed.geturl()


def read_links(filename:str):
    df = pd.read_excel(filename)
    return df["website_corrigido"].tolist()


def execution_time(func):
    """
    monite the function execution time
    """
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'Programa rodou em {total_time:.0f} seconds')
        return result
    return timeit_wrapper


def strip_ponctuation(text):
    """
    removes the ponctiation of text and special caracters
    """
    return re.sub(u'[^a-zA-Z0-9áéíóúÁÉÍÓÚâêîôÂÊÎÔãõÃÕçÇ: ]', '_', text)


def get_base_domain(url:str, partial=False):
    """
    return the base domain
    """

    if partial:
        if url.startswith('http') or url.startswith('https') :
            bases = url.split('//')[1].split('.')
            
            if "www" in url:
                del bases[0]

            joined =  ".".join(bases)
            return joined.replace('/', '')

    else:       
        if url.startswith('http') or url.startswith('https'):
            return url.split('/')[2]
        
        return url


def save_to_folder(content, filename:str, parts_dir:str='site_body'):
    """
    save the html content inside of folder with site name
    """
    if not os.path.exists(f'{SAVE_DIRECTORY}/{parts_dir}'):
        os.makedirs(f'{SAVE_DIRECTORY}/{parts_dir}')

    filename = f"{SAVE_DIRECTORY}/{parts_dir}/{filename}.html"
    with open(filename, 'w', encoding='utf8') as html_file:
        try:
            html_file.write(content)
            return True

        except Exception as error:
            print(error)
            os.remove(filename)
            return


def spider_worker(spider, url:str):
     
    process = CrawlerProcess(settings)
    process.crawl(spider, start_urls=[url]) # allowed_domains=[get_base_domain(url, partial=True)] 
    process.start()

    import sys
    del sys.modules['twisted.internet.reactor']
    from twisted.internet import reactor
    from twisted.internet import default
    default.install()


class BroadCrawler(CrawlSpider):
    name = 'broad_crawler'
    
    # ignore=['#','/search/','/busca/','q=']
    rules = [ Rule (LinkExtractor(), callback="parse_link",  follow=True),]

    def parse_link(self, response):

        if response.status != 200 or response.body == "": return

        origin = base_url(response.url)
        title = response.css('title::text').get()
        filename = f"{get_base_domain(response.url)}_{str(uuid.uuid4())}"
        
        status = save_to_folder(response.text, filename)
 
        if not status: 
            save_error(response.url)
            return

        yield {
            'origin': origin,
            'link': response.url, 
            'title': title,
            'content': f"site_body/{filename}"
        }


@execution_time
def main_handler():

    website = read_links('assets/sites_faltantes_2.xlsx')

    urls = [base_url(url) for url in website ]

    # urls = remove_duplicates_on_list(urls)
    print(f"{len(urls)} found!")

    if not os.path.exists(SAVE_DIRECTORY):
        os.mkdir(SAVE_DIRECTORY)

    # with multiprocessing.Pool(PROCESS) as pool: #maxtasksperchild=1
    #     results = pool.map_async(partial(spider_worker, BroadCrawler), urls)
    #     results.get()

    # print(urls)
    process = CrawlerProcess(settings)
    process.crawl(BroadCrawler, start_urls=urls) # allowed_domains=[get_base_domain(url) for url in urls]
    process.start()


if __name__ == "__main__":
    try:
        main_handler()

    except Exception as error:
        from dotenv import load_dotenv
        import os

        load_dotenv()

        chat_id = os.getenv('CHAT_ID')
        token = os.getenv('TELEGRAM_TOKEN')

        telegram = TelegramBot(token, [chat_id])
        telegram.send_message(str(error))
        raise
