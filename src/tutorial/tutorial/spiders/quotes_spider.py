import scrapy

from pathlib import Path


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        "https://quotes.toscrape.com/page/1/",
    ]

    def parse(self, response):
        for quote in response.css("div.quote"):
            yield {
                "text": quote.css("span.text::text").get(),
                "author": quote.css("small.author::text").get(),
                "tags": quote.css("div.tags a.tag::text").getall(),
            }

        next_page = response.css("li.next a::attr(href)").get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)


class TwoGisBanksSpider(scrapy.Spider):
    name = "banks"
    start_urls = ["https://2gis.ru/spb/search/bank"]

    def parse(self, response):
        # page = response.url.split("/")[-2]
        # filename = f"banks-{page}.html"
        # Path(filename).write_bytes(response.body)

        # for bank in response.css("div._awwm2v"):
        #     yield bank
        #     # yield {
        #     #     "name": bank.css("span._1al0wlf::text").get()
        #     # }
        test = []
        for bank_name, bank_rate, review_amount, bank_adres in zip(
            response.css("span._1al0wlf"),
            response.css("div._y10azs"),
            response.css("div._jspzdm"),
            response.css("span._14quei"),
        ):
            print(
                bank_name.css("::text").get(),
                bank_rate.css("::text").get(),
                review_amount.css("::text").get(),
                bank_adres.css("::text").getall()[1],
            )
            test.append(
                (
                    bank_name.css("::text").get(),
                    bank_rate.css("::text").get(),
                    review_amount.css("::text").get(),
                    bank_adres.css("::text").getall()[1],
                )
            )

        return test
        # yield bank_name.css("::text").get(), bank_rate.css("::text").get(), review_amount.css("::text").get(), bank_adres.css('::text').getall()[1]


a = response.css("div._1x4k6z7").get()
b = a.css("a")
bb = b[0]
bb.attrib["href"]
