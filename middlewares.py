from scrapper_boilerplate import setSelenium
from scrapy.http import HtmlResponse
from time import sleep


class SeleniumMiddleware(object):

    def process_request(self, request, spider):
        print(request.url)
        with setSelenium(remote_webdriver=True) as driver:
            driver.get(request.url)
            driver.implicitly_wait(220)
            # sleep(30)
            current_url = driver.current_url
            body = driver.page_source
        print('Done!')

        return HtmlResponse(current_url, body=body, encoding='utf-8', request=request)
