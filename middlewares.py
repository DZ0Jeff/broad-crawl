from scrapper_boilerplate import setSelenium, scrolldown
from scrapy.http import HtmlResponse

from selenium.webdriver.common.by import By


class SeleniumMiddleware(object):

    def __init__(self):
        self.driver = setSelenium(remote_webdriver=True)

    def process_request(self, request, spider):
        # print(request.url)
        
        self.driver.get(request.url)
        self.driver.implicitly_wait(220)
        current_url = self.driver.current_url
        body = self.driver.page_source

        # links = self.driver.find_elements(By.TAG_NAME, 'a')
        # links = [link.get_attribute('href') for link in links if link ]

        # print(f'{len(links)} links')

        return HtmlResponse(current_url, body=str(body), encoding='utf-8', request=request)

    def spider_closed(self):
        self.spider.quit()
