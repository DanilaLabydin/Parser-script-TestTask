import scrapy
import time
import re
from tutorial.psql_ops import insert_bank_info

from pathlib import Path


class TwoGisBanksSpider(scrapy.Spider):
    name = "banks"
    start_urls = ["https://2gis.ru/spb/search/bank"]

    def parse(self, response):
        banks_info = []
        for bank_name, bank_rate, review_amount, bank_adres in zip(
            response.css("span._1al0wlf"),
            response.css("div._y10azs"),
            response.css("div._jspzdm"),
            response.css("span._14quei"),
        ):
            # print(
            #     bank_name.css("::text").get(),
            #     bank_rate.css("::text").get(),
            #     review_amount.css("::text").get(),
            #     bank_adres.css("::text").getall()[1],
            # )
            banks_info.append(
                (
                    bank_name.css("::text").get(),
                    bank_adres.css("::text").getall()[1],
                    bank_rate.css("::text").get(),
                    int(re.findall("^[0-9]*", review_amount.css("::text").get())[0]),
                )
            )
        print(insert_bank_info(banks_info))

        links_list = response.css("div._1x4k6z7").css("a")

        time.sleep(5)
        for link in links_list:
            next_link = response.urljoin(link.attrib["href"])
            yield scrapy.Request(next_link, callback=self.parse)
