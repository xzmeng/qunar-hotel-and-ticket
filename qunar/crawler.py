import traceback

import pymongo
import requests

from qunar import logging, settings
import time
from datetime import date, timedelta
from urllib.parse import quote
from pypinyin import lazy_pinyin


class Crawler:
    """Crawler实现了所有爬虫的通用功能"""

    mongo_client = pymongo.MongoClient(settings.MONGO_HOST, settings.MONGO_PORT)
    mongo_database = mongo_client.qunar

    def __init__(self, prefix):
        self.log = logging.Logger(prefix=prefix)
        self.collection = None

        self.crawled_count = 0
        self.saved_count = 0

        self.keyword = None
        self.method = 'GET'
        self.api_url = None
        self.params = None
        self.json = None
        self.headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
        }

    def crawl(self):
        try:
            self._crawl()
        except Exception as e:
            traceback.print_exc()

    def summary(self):
        self.log.info(f'爬取结束,共爬取{self.crawled_count}条数据,保存{self.saved_count}条数据.')

    def get_json(self):
        json = None
        try:
            if self.method == 'GET':
                r = requests.get(self.api_url,
                                 headers=self.headers,
                                 params=self.params)
            else:
                r = requests.post(self.api_url,
                                  headers=self.headers,
                                  json=self.json)
            json = r.json()
            assert json.get('data') is not None
        except KeyError:
            self.log.info(str('返回的json数据有误: ' + str(json)))
        return json

    def save_one_to_mongo(self, document, pk):
        self.crawled_count += 1
        if self.collection.count_documents({pk: document[pk]}) == 0:
            document['keyword'] = self.keyword
            self.collection.insert_one(document)
            self.saved_count += 1
        else:
            self.log.debug(f'去重丢弃, {pk}: {document[pk]}')
        pass

    def save_list_to_mongo(self, documents, pk):
        for document in documents:
            self.save_one_to_mongo(document, pk)


class HotelCrawler(Crawler):
    """根据城市名字爬取酒店列表"""

    def __init__(self, city, crawl_comment=False):
        super().__init__(city)
        self.api_url = 'https://hotel.qunar.com/napi/list'
        self.city = city
        self.keyword = city
        self.crawl_comment = crawl_comment
        self.num = 20  # hotels per page
        self.collection = self.mongo_database.hotels

    def _crawl(self):
        limit = settings.HOTEL_CRAWLER_MAX_COUNT_PER_KEYWORD
        try:
            total_count = self.get_hotel_count()
        except Exception as e:
            self.log.info(f'获取{self.city}酒店数量失败:{str(e)},'
                          + '取默认值1000')
            total_count = 1000

        if limit > 0:
            hotel_count = min(total_count, limit)
        else:
            hotel_count = total_count

        self.log.info(f'一共找到{total_count}个酒店,将要爬取前{hotel_count}个.')
        for start in range(0, hotel_count, self.num):
            try:
                self.log.info(f'正在爬取第{start}-{start + self.num}个(共{hotel_count}个).')
                hotels = self.get_hotels(start)
                self.save_list_to_mongo(hotels, 'seqNo')
                time.sleep(settings.REQUEST_DELAY)
                # comment
                if self.crawl_comment:
                    for hotel in hotels:
                        HotelCommentCrawler(hotel['seqNo']).crawl()
            except KeyError as e:
                self.log.info(f'第{start}-{start + self.num}爬取失败: 返回数据格式错误')
            except Exception as e:
                self.log.info(f'第{start}-{start + self.num}爬取失败:,调用栈如下:')
                traceback.print_exc()

    def get_hotel_count(self):
        try:
            json = self.get_hotels_json(0)
            count = json['data']['tcount']
        except KeyError:
            self.log.info(str(json))
            raise KeyError
        return count

    def get_hotels(self, start):
        json = self.get_hotels_json(start)
        hotels = json['data']['hotels']
        for hotel in hotels:
            hotel['city'] = self.city
        return hotels

    def get_hotels_json(self, start):
        city_pinyin = ''.join(lazy_pinyin(self.city))
        if city_pinyin in [
            'beijing', 'shanghai', 'chongqing', 'tianjin'
            ]:
            city_pinyin += '_city'
        today = date.today()
        tomorrow = date.today() + timedelta(days=1)
        from_date = str(today)
        to_date = str(tomorrow)
        self.json = {
            "b": {
                "bizVersion": "17",
                "cityUrl": city_pinyin,
                "fromDate": from_date,
                "toDate": to_date,
                "q": "",
                "qFrom": 3,
                "start": start,
                "num": self.num,
                "minPrice": 0,
                "maxPrice": -1,
                "level": "",
                "sort": 0,
                "cityType": 1,
                "fromForLog": 1,
                "uuid": "",
                "userName": "",
                "userId": "",
                "fromAction": "",
                "searchType": 0,
                "locationAreaFilter": [],
                "comprehensiveFilter": []
            },
            "qrt": "h_hlist",
            "source": "website"
        }
        headers = {
            'content-type': 'application/json;charset=UTF-8',
            'origin': 'https://hotel.qunar.com',
            'referer': f'https://hotel.qunar.com/cn/{city_pinyin}/?fromDate={from_date}&toDate={to_date}&cityName={quote(self.city)}',
        }
        self.headers.update(headers)
        self.method = 'POST'
        json = self.get_json()
        return json


# HotelCrawler('南京').crawl()

class HotelCommentCrawler(Crawler):
    """酒店评论爬虫"""

    def __init__(self, seq_no):
        super().__init__(seq_no)
        self.seq_no = seq_no
        self.keyword = seq_no
        self.collection = self.mongo_database.hotel_comments
        self.rating_stat_collection = self.mongo_database.hotel_comment_rating_stats

    def _crawl(self):
        try:
            first_page = self.get_comment_page_json(1)
            rating_stat = first_page['data']['ratingStat']
            total_count = first_page['data']['count']
            page_count = (total_count + 9) // 10
        except:
            self.log.info(f'获取评论页数失败,将使用默认值2页')
            page_count = 2
        max_page = settings.HOTEL_COMMENT_CRAWLER_MAX_PAGE
        if max_page > 0:
            page_count = min(max_page, page_count)
        self.save_rating_stat(rating_stat)
        self.log.info(f'酒店{self.seq_no}一共有{total_count}条评论,将爬取前{page_count}页.')
        for i in range(1, page_count + 1):
            try:
                self.log.info(f'正在爬取第{i}/{page_count}页...')
                json = self.get_comment_page_json(i)
                for comment in json['data']['list']:
                    comment['seqNo'] = self.seq_no
                self.save_list_to_mongo(json['data']['list'], 'feedOid')
            except KeyError as e:
                self.log.info(f'第{i}页爬取失败: 返回数据格式错误')
            except Exception as e:
                self.log.info(f'第{i}页爬取失败:,调用栈如下:')
                traceback.print_exc()


    def save_rating_stat(self, document):
        document['seqNo'] = self.seq_no
        if self.rating_stat_collection.count_documents({'seqNo': self.seq_no}) == 0:
            self.rating_stat_collection.insert_one(document)
        else:
            self.log.debug(f'去重丢弃, seqNo: {self.seq_no}')

    def save_one_to_mongo(self, document, pk):
        self.crawled_count += 1
        if self.collection.count_documents({pk: document[pk]}) == 0:
            self.collection.insert_one(document)
            self.saved_count += 1
        else:
            self.log.debug(f'去重丢弃, {pk}: {document[pk]}')
        pass

    def get_rating_stat(self):
        json = self.get_comment_page_json(1)
        return json['data']['ratingStat']

    def get_comment_page_json(self, page_num):
        url_template = 'https://hotel.qunar.com/napi/ugcCmtList?hotelSeq={seq_no}' \
                       '&page={page_num}&onlyGuru=false&rate=all&sort=hot'
        self.api_url = url_template.format(seq_no=self.seq_no, page_num=page_num)
        return self.get_json()


# HotelCommentCrawler('zhengzhou_5307').crawl()


class SightCrawler(Crawler):
    """根据关键字爬取景点"""

    def __init__(self, keyword):
        super().__init__(keyword)
        self.api_url = 'https://piao.qunar.com/ticket/list.json'
        self.keyword = keyword
        self.collection = self.mongo_database.sights

    def _crawl(self):
        self.log.info(f'开始爬取关键字"{self.keyword}"...')
        try:
            total_count, page_count = self.get_total_count_and_page_count()
        except:
            self.log.info(f'获取关键字景点数量失败，将使用默认值: 150条, 10页')
            total_count, page_count = 150, 10
        self.log.info(f'共找到{total_count}条记录,将分{page_count}页爬取.')
        max_page = settings.SIGHT_CRAWLER_MAX_PAGE
        if max_page > 0:
            end_page = min(max_page, page_count)
            self.log.info(f'检测到max_page={max_page},将只爬取前{max_page}页.')
        else:
            end_page = page_count
        for i in range(1, end_page + 1):
            try:
                self.log.info(f'正在爬取第{i}/{end_page}页...')
                sights = self.get_sights(i)
                self.save_list_to_mongo(sights, 'sightId')
                time.sleep(settings.REQUEST_DELAY)
            except:
                self.log.info(f'第{i}页爬取失败,失败原因:')
                traceback.print_exc()

    def get_total_count_and_page_count(self):
        json = self.get_sights_json(page_num=1)
        total_count = json['data']['totalCount']
        count_per_page = len(json['data']['sightList'])
        page_count = (total_count + count_per_page - 1) // count_per_page
        return total_count, page_count

    def get_sights_json(self, page_num):
        self.params = {
            'from': 'mps_search_suggest',
            'keyword': self.keyword,
            'page': page_num,
        }
        return self.get_json()

    def get_sights(self, page_num):
        json = self.get_sights_json(page_num)
        sights = json['data']['sightList']
        for sight in sights:
            sight['city'] = self.keyword
        return sights



# def crawl():
#     keyword_list = ['加拿大', '青海', '青岛', '日照']
#     for keyword in keyword_list:
#         crawler = SightCrawler(keyword)
#         crawler.crawl()
#
# crawl()