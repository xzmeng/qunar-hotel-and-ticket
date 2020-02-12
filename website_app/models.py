from django.db import models


# Create your models here.
class Province(models.Model):
    name = models.CharField(max_length=100,
                            primary_key=True)


class City(models.Model):
    name = models.CharField(max_length=100,
                            primary_key=True)
    province = models.ForeignKey(Province,
                                 on_delete=models.CASCADE,
                                 related_name='cities')


class Hotel(models.Model):
    city = models.ForeignKey(City,
                             on_delete=models.SET_NULL,
                             blank=True,
                             null=True)
    seq_no = models.CharField(max_length=50,
                              primary_key=True)
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    gpoint = models.CharField(max_length=100)
    dangci_text = models.CharField(max_length=20)
    dangci = models.IntegerField()
    image_url = models.CharField(max_length=1024)


class HotelRatingStat(models.Model):
    hotel = models.OneToOneField(Hotel,
                                 on_delete=models.CASCADE,
                                 related_name='rating_stat')
    positive_count = models.IntegerField()
    neutral_count = models.IntegerField()
    negative_count = models.IntegerField()


class HotelComment(models.Model):
    hotel = models.ForeignKey(Hotel,
                              on_delete=models.CASCADE)
    feed_id = models.CharField(max_length=20,
                               primary_key=True)
    feed_type = models.CharField(max_length=20)
    nickname = models.CharField(max_length=100)
    content = models.TextField()


class Sight(models.Model):
    city = models.ForeignKey(City,
                             on_delete=models.SET_NULL,
                             blank=True,
                             null=True)
    sight_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    score = models.FloatField(default=0.0)
    intro = models.CharField(max_length=1024)
    point = models.CharField(max_length=100)
    price = models.FloatField()
    sale_count = models.IntegerField(default=0)
    image_url = models.CharField(max_length=1024)



