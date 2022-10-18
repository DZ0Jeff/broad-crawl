import os
import re
import time
import multiprocessing

from functools import wraps, partial
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import pandas as pd
import sys
import warnings

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
    #     'pipelines.LazyInsertPipeline': 100,
    # },
    'COOKIES_ENABLED': False,
    'SCHEDULER_PRIORITY_QUEUE': 'scrapy.pqueues.DownloaderAwarePriorityQueue',
    'REACTOR_THREADPOOL_MAXSIZE': 20,
    'RETRY_ENABLED': False,
    'DOWNLOAD_TIMEOUT': 15,
    'REDIRECT_ENABLED': False,
    'AJAXCRAWL_ENABLED': True,
    'DEPTH_PRIORITY': 1,
    'SCHEDULER_DISK_QUEUE': 'scrapy.squeues.PickleFifoDiskQueue',
    'SCHEDULER_MEMORY_QUEUE': 'scrapy.squeues.FifoMemoryQueue',
    # 'LOG_FILE': 'crawler.log', # logging file
    # 'FEED_EXPORTERS': {
    #     'xlsx': 'scrapy_xlsx.XlsxItemExporter',toor

    # },
    'FEEDS': {
        f'{SAVE_DIRECTORY}/data.csv': {'format': 'csv'}
    }
}


def read_links():
    df = pd.read_excel('links.xlsx')
    return df['website'].tolist()


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


def get_base_domain(url:str):
    """
    return the base domain
    """
    # return [ url.split('/')[2] for url in urls if url]
    if url.startswith('http') or url.startswith('https'):
        return url.split('/')[2]
    
    return url


def save_to_folder(content, filename:str, parts_dir:str='site_body'):
    """
    save the html content inside of folder with site name
    """
    if not os.path.exists(f'{SAVE_DIRECTORY}/{parts_dir}'):
        os.makedirs(f'{SAVE_DIRECTORY}/{parts_dir}')

    with open(f"{SAVE_DIRECTORY}/{parts_dir}/{filename}.html", 'w') as html_file:
        try:
            html_file.write(content)

        except Exception:
            print('> Erro de inserção...')
            return


def spider_worker(spider, target_url:str):
    urls = [target_url]
    
    process = CrawlerProcess(settings)
    process.crawl(spider, start_urls=urls, allowed_domains = [get_base_domain(url) for url in urls])
    process.start()

    import sys
    del sys.modules['twisted.internet.reactor']
    from twisted.internet import reactor
    from twisted.internet import default
    default.install()


class BroadCrawler(CrawlSpider):
    name = 'broad_crawler'
    
    ignore=['#','/search/','/busca/','q=']
    rules = [ Rule (LinkExtractor(deny=(ignore)), callback="parse_link",  follow=True),]

    def parse_link(self, response):

        if response.status != 200 or response.body == "": return

        origin = get_base_domain(response.url)
        title = response.css('title::text').get()
        filename = f"{strip_ponctuation(origin)}_{strip_ponctuation(title)}"
        status = save_to_folder(response.text, filename)

        if not status: return

        yield {
            'origin': origin,
            'link': response.url, 
            'title': title,
            'content': f"site_body/{filename}"
        }


@execution_time
def main():
    # urls = ['https://www.morpheusmedspa.com', 'https://www.destinationaesthetics.com', 'https://www.dermacaresandiego.com', 'https://www.williamsfacialsurgery.com', 'https://www.williamsfacialsurgery.com/our-doctors/']

    website = read_links()
    urls = [ url for url in website if url != "Not Available" ]

    #urls = urls[:10]

    print(f"{len(urls)} found!")

    # if not os.path.exists(SAVE_DIRECTORY):
    #     os.mkdir(SAVE_DIRECTORY)

    # process = CrawlerProcess(settings)
    # process.crawl(BroadCrawler, start_urls=urls, allowed_domains = [get_base_domain(url) for url in urls])
    # process.start()

    with multiprocessing.Pool(5) as pool: #maxtasksperchild=1
        pool.map(partial(spider_worker, BroadCrawler), urls)



if __name__ == "__main__":
    main()
