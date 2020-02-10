from .crawler import HotelCrawler, HotelCommentCrawler, SightCrawler


class Test:

    def only_hotel(self):
        keyword_list = [
            '郑州', '武汉', '南京',
        ]
        for keyword in keyword_list:
            HotelCrawler(keyword).crawl()

    def only_comment(self):
        hotel_list = [
            'zhengzhou_5307', 'zhengzhou_14833', 'zhengzhou_5340',
        ]
        for hotel in hotel_list:
            HotelCommentCrawler(hotel).crawl()

    def hotel_with_comment(self):
        pass

    def only_sight(self):
        keyword_list = [
            '西安', '日本', '挪威',
        ]
        for keyword in keyword_list:
            SightCrawler(keyword).crawl()
