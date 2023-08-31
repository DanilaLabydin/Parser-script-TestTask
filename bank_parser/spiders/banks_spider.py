import scrapy
import logging
import time
import re

from bank_parser.psql_ops import insert_bank_info


LOGGER = logging.getLogger(__name__)


BANK_NAME_TAG = "span._1al0wlf"
BANK_ADDRESS_TAG = "div._y10azs"
BANK_RATE_TAG = "div._jspzdm"
BANK_REVIEW_AMOUNT_TAG = "span._14quei"
BANK_LIST_LINKS = "div._1x4k6z7"


class TwoGisBanksSpider(scrapy.Spider):
    name = "banks"
    start_urls = ["https://2gis.ru/spb/search/bank"]

    def parse(self, response):
        if response is None:
            return

        try:
            names = response.css(BANK_NAME_TAG)
            addresses = response.css(BANK_ADDRESS_TAG)
            rates = response.css(BANK_RATE_TAG)
            review_amounts = response.css(BANK_REVIEW_AMOUNT_TAG)

        except Exception as e:
            LOGGER.error(
                f"Error occured when you tried to extract tag from response: {e}"
            )
            return

        if not all([names, addresses, rates, review_amounts]):
            return

        banks_info = []
        for name, rate, review_amount, address in zip(
            names, addresses, rates, review_amounts
        ):
            if not all([name, rate, review_amount, address]):
                return

            try:
                name = name.css("::text").get()
                address = address.css("::text").getall()[1]
                rate = rate.css("::text").get()
                review_amount = re.findall(
                    "^[0-9]*", review_amount.css("::text").get()
                )[0]

            except Exception as e:
                LOGGER.error(
                    f"Error occured when you tried to extract values from tags: {e}"
                )
                return

            if not all([name, address, rate, review_amount]):
                return

            banks_info.append((name, address, rate, int(review_amount)))

        insert_bank_info(banks_info)

        try:
            links_list = response.css(BANK_LIST_LINKS).css("a")
        except Exception as e:
            LOGGER.error(f"Error occured when you tried to get the list of links")
            return

        if links_list is None:
            return

        time.sleep(5)
        for link in links_list:
            try:
                next_link = response.urljoin(link.attrib["href"])
            except Exception as e:
                continue

            yield scrapy.Request(next_link, callback=self.parse)

        return
