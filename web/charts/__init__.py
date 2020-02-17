import os
import django
import matplotlib.pyplot as plt
import numpy as np

# Fixing random state for reproducibility
plt.rcdefaults()
plt.rcParams['font.sans-serif'] = ['Hiragino Sans GB']

from qunar.models import Sight, HotelRatingStat, Hotel
from django.conf import settings


class Chart:
    save_dir = os.path.join(settings.MEDIA_ROOT, 'charts')
    charts_url = os.path.join(settings.MEDIA_URL, 'charts')

    chart_prefix = None
    identifier = None

    @property
    def filename(self):
        return f'{self.chart_prefix}-{self.identifier}.png'

    @property
    def filepath(self):
        return os.path.join(self.save_dir, self.filename)

    @property
    def file_url(self):
        return os.path.join(self.charts_url, self.filename)

    @property
    def url(self):
        if not os.path.exists(self.filepath):
            self.plot()
        return self.file_url

    def save(self):
        plt.savefig(os.path.join(self.save_dir, self.filename))
        plt.close()



class Top10SaleSightsBar(Chart):
    def __init__(self, city_name='all'):
        self.city_name = city_name
        self.identifier = city_name
        self.chart_prefix = 'top-10-sale-sights-bar'

    def plot(self):
        if self.city_name == 'all':
            sights = Sight.objects.order_by('-sale_count')[:10]
            title = '全国最热门的十大景点'
        else:
            sights = Sight.objects.filter(city__name=self.city_name). \
                         order_by('-sale_count')[:10]
            title = f'{self.city_name}最热门的十大景点'

        fig, ax = plt.subplots()

        # Example data
        sight_names = [sight.name for sight in sights]
        sight_values = [sight.sale_count for sight in sights]

        ax.barh(sight_names, sight_values)
        ax.invert_yaxis()  # labels read top-to-bottom
        ax.set_xlabel('销量')
        ax.set_title(title)

        self.save()



class Top10ScoreSightsBar(Chart):
    def __init__(self, city_name='all'):
        self.city_name = city_name
        self.identifier = self.city_name
        self.chart_prefix = 'top-10-score-sights-bar'

    def plot(self):
        if self.city_name == 'all':
            sights = Sight.objects.order_by('-score')[:10]
            title = '全国评分最高的十大景点'
        else:
            sights = Sight.objects.filter(city__name=self.city_name). \
                         order_by('-score')[:10]
            title = f'{self.city_name}评分最高的十大景点'

        fig, ax = plt.subplots()

        # Example data
        sight_names = [sight.name for sight in sights]
        sight_values = [sight.score for sight in sights]

        ax.barh(sight_names, sight_values)
        ax.invert_yaxis()  # labels read top-to-bottom
        ax.set_xlabel('评分')
        ax.set_title(title)

        self.save()


class HotelRatingPie(Chart):
    def __init__(self, seq_no):
        self.seq_no = seq_no
        self.identifier = seq_no
        self.chart_prefix = 'hotel-rating-pie'

    def plot(self):
        fig, ax = plt.subplots(figsize=(4, 3), subplot_kw=dict(aspect="equal"))
        try:
            rating = HotelRatingStat.objects.get(hotel_id=self.seq_no)
        except HotelRatingStat.DoesNotExist:
            ax.set_title(f'酒店{self.seq_no}的评分信息缺失!')
            self.save()
            return

        data = [rating.positive_count, rating.neutral_count, rating.negative_count]
        labels = ['好评', '中评', '差评']

        def func(pct, allvals):
            absolute = int(pct / 100. * np.sum(allvals))
            return "{:.1f}%\n({:d})".format(pct, absolute)

        wedges, texts, autotexts = ax.pie(data, autopct=lambda pct: func(pct, data),
                                          textprops=dict(color="w"))

        ax.legend(wedges, labels,
                  title="种类",
                  loc="center left",
                  bbox_to_anchor=(1, 0, 0.5, 1))

        plt.setp(autotexts, size=8, weight="bold")

        ax.set_title(f"酒店{self.seq_no}的评分情况")
        self.save()


class Top10ExpensiveHotelsBar(Chart):
    def __init__(self, city_name='all'):
        self.city_name = city_name
        self.identifier = city_name
        self.chart_prefix = 'top-10-expensive-hotels-bar'

    def plot(self):
        if self.city_name == 'all':
            hotels = Hotel.objects.order_by('-price')[:10]
            title = '全国最贵的十个酒店'
        else:
            hotels = Hotel.objects.filter(city__name=self.city_name). \
                         order_by('-price')[:10]
            title = f'{self.city_name}最贵的十个酒店'

        fig, ax = plt.subplots()

        # Example data
        hotel_names = [hotel.name for hotel in hotels]
        hotel_values = [hotel.price for hotel in hotels]

        ax.barh(hotel_names, hotel_values)
        ax.invert_yaxis()  # labels read top-to-bottom
        ax.set_xlabel('最低价格')
        ax.set_title(title)

        self.save()


class HotelPriceHistogram(Chart):
    def __init__(self, city_name):
        self.city_name = city_name
        self.identifier = city_name
        self.chart_prefix = 'hotels-price-histogram'

    def plot(self):
        if self.city_name == 'all':
            hotels = Hotel.objects.order_by('-price')
            title = '全国酒店价格分布直方图'
        else:
            hotels = Hotel.objects.filter(city__name=self.city_name). \
                order_by('-price')
            title = f'{self.city_name}酒店价格分布直方图'

        hotel_prices = [hotel.price for hotel in hotels]
        fig, ax = plt.subplots()
        ax.hist(hotel_prices, bins=30)
        ax.set_xlabel('最低价格')
        ax.set_title(title)
        self.save()
