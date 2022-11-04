from scrapper_boilerplate import setSelenium
from scrapy.http import HtmlResponse


class SeleniumMiddleware(object):

    # Here you get the request you are making to the urls which your LinkExtractor found and use selenium to get them and return a response.
    def process_request(self, request, spider):
        with setSelenium(remote_webdriver=True) as driver:
            driver.get(request.url)
            driver.implicitly_wait(220)
            body = driver.page_source
            return HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=request)
