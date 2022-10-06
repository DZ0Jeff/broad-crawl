import os
from scrapy.crawler import CrawlerProcess

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


def get_base_domain(url:str):
    """
    return the base domain
    """
    # return [ url.split('/')[2] for url in urls if url]
    if url.startswith('http') or url.startswith('https'):
        return url.split('/')[2]
    
    return url


def save_to_folder(content, filename:str):
    """
    save the html content inside of folder with site name
    """
    if not os.path.exists('site_body'):
        os.makedirs('site_body')

    with open(f"site_body/{filename}.html", 'wb') as html_file:
        html_file.write(content)
    


class Infolink(CrawlSpider):
    name = 'infolink'
    
    ignore=['#','/search/','/busca/','q=']
    start_urls = ['https://www.morpheusmedspa.com' ,'https://www.destinationaesthetics.com', 'https://www.dermacaresandiego.com', 'https://www.williamsfacialsurgery.com', 'https://www.williamsfacialsurgery.com/our-doctors/']
    allowed_domains = [get_base_domain(url) for url in start_urls]
    rules = [ Rule (LinkExtractor(deny=(ignore)), callback="parse_link",  follow=True),]

    def parse_link(self, response):

        origin = get_base_domain(response.url)
        title = response.css('title::text').get()
        filename = f"{origin.replace('.','_')}_{title.replace(' ','_').replace('.', '_').replace('|','_').replace('/','_').replace('?', '_')}"
        save_to_folder(response.body, filename)

        yield {
            'origin': origin,
            'link': response.url, 
            'title': title,
            'content': f"site_body/{filename}"
        }

settings = {
    'DEPTH_LIMIT': 2,
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)', 
    # descomentar aqui se usar o recurso de insert a cada x dados
    'CONCURRENT_REQUESTS': 100, # default to 16
    # 'CONCURRENT_REQUESTS_PER_DOMAIN': 16, # default to 8
    # 'CONCURRENT_REQUESTS_PER_IP': 0, # default to 0

    'LOG_LEVEL': 'INFO',
    'COOKIES_ENABLED': False,
    # 'SCHEDULER_PRIORITY_QUEUE': 'scrapy.pqueues.DownloaderAwarePriorityQueue',
    # 'REACTOR_THREADPOOL_MAXSIZE': 20,
    # 'RETRY_ENABLED': False,
    'DOWNLOAD_TIMEOUT': 15,
    # 'REDIRECT_ENABLED': False,
    'AJAXCRAWL_ENABLED': True,
    # 'DEPTH_PRIORITY': 1,
    # 'SCHEDULER_DISK_QUEUE': 'scrapy.squeues.PickleFifoDiskQueue',
    # 'SCHEDULER_MEMORY_QUEUE': 'scrapy.squeues.FifoMemoryQueue',
    # 'LOG_FILE': 'crawler.log' # logging file
    'FEEDS': {
        'data.csv': {'format': 'csv'}
    }
}

def main():
    process = CrawlerProcess(settings)
    process.crawl(Infolink)
    process.start()


if __name__ == "__main__":
    main()
