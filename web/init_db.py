import json
import os
import django
from pymongo import MongoClient
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'app.settings')
django.setup()

from qunar.models import Province, City, \
    Hotel, HotelComment, HotelRatingStat, Sight
from django.db.utils import IntegrityError
from qunar.utils import province_cities



def populate_provinces_cities():
    for province_name, cities in province_cities.items():
        try:
            Province.objects.create(name=province_name)
        except IntegrityError:
            print(f'省份{province_name}已经存在!')
        province = Province.objects.get(name=province_name)
        for city_name in cities:
            try:
                City.objects.create(name=city_name,
                                    province=province)
            except IntegrityError:
                print(f'城市{city_name}已经存在!')


def populate_hotels():
    mongo_client = MongoClient()
    hotels = mongo_client.qunar.hotels
    for hotel in hotels.find():
        city = City.objects.get(name=hotel.get('city'))
        try:
            Hotel.objects.create(
                city=city,
                seq_no=hotel.get('seqNo'),
                name=hotel.get('name'),
                price=int(hotel.get('price')),
                gpoint=hotel.get('gpoint'),
                dangci_text=hotel.get('dangciText'),
                dangci=int(hotel.get('dangci')),
                image_url=hotel.get('imageid'),
            )
            print(f'酒店{hotel.get("seqNo")}插入成功!')
        except IntegrityError:
            print(f'酒店{hotel.get("seqNo")}已经存在!')


def populate_ratings():
    mongo_client = MongoClient()
    hotel_rating_stat = mongo_client.qunar.hotel_comment_rating_stat
    for rating in hotel_rating_stat.find():
        hotel = Hotel.objects.get(seq_no=rating.get('seqNo'))
        if hotel:
            try:
                HotelRatingStat.objects.create(
                    hotel=hotel,
                    positive_count=rating.get('positiveCount'),
                    neutral_count=rating.get('neutralCount'),
                    negative_count=rating.get('negativeCount'),
                )
                print(f'酒店{hotel.get("seqNo")}好中差评数量插入成功!')
            except IntegrityError:
                print(f'酒店{hotel.get("seqNo")}的好中差评已经存在!')


def populate_comments():
    mongo_client = MongoClient()
    hotel_comments = mongo_client.qunar.hotel_comments
    for comment in hotel_comments.find():
        try:
            hotel = Hotel.objects.get(seq_no=comment.get('seqNo'))
            content = json.loads(comment.get('content'))
            HotelComment.objects.create(
                hotel=hotel,
                feed_id=comment.get('feedOid'),
                feed_type='qunar',
                nickname=comment.get('nickName'),
                content=content.get('feedContent')
            )
            print(f'成功插入评论{comment.get("feedOid")}')
        except Hotel.DoesNotExist:
            print(f'酒店{comment.get("seqNo")}不存在!')

def populate_sights():
    mongo_client = MongoClient()
    sights = mongo_client.qunar.sights
    for sight in sights.find():
        city = City.objects.get(name=sight.get('city'))
        try:
            Sight.objects.create(
                city=city,
                sight_id=sight.get('sightId'),
                name=sight.get('sightName'),
                score=float(sight.get('score')),
                intro=sight.get('intro'),
                point=sight.get('point'),
                price=float(sight.get('qunarPrice') or '0'),
                image_url=sight.get('sightImgURL'),
            )
            print(f'景点{sight.get("sightName")}插入成功!')
        except IntegrityError:
            print(f'景点{sight.get("sightName")}已经存在!')




if __name__ == '__main__':
    populate_provinces_cities()
    populate_hotels()
    populate_ratings()
    populate_comments()
    populate_sights()
