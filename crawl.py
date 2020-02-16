from qunar.test import Test
from qunar.crawler import HotelCrawler, SightCrawler
import json

with open('web/content/static/province_cities.json') as f:
    provinces = json.load(f)

def crawl_hotels(crawl_comment=False):
    for province, cities in provinces.items():
        for city in cities:
            HotelCrawler(city, crawl_comment=crawl_comment).crawl()


def crawl_sights():
    for province, cities in provinces.items():
        for city in cities:
            SightCrawler(city).crawl()


if __name__ == '__main__':
    test = Test()

    # 单独测试酒店，评论，景点
    # test.only_hotel()
    # test.only_comment()
    # test.only_sight()

    # 快速爬取全国酒店(不爬评论)
    # crawl_hotels()

    # 爬取全国酒店和评论(附带评论)
    crawl_hotels(crawl_comment=True)

    # 全国景点(很容易被封)
    # crawl_sights()
