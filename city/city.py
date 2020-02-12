import json
from collections import defaultdict
from pprint import pprint

suffix_list = [
    "市",
    "朝鲜族自治州",
    "地区",
    "盟",
    "土家族苗族自治州",
    "藏族羌族自治州",
    "布依族苗族自治州",
    "苗族侗族自治州",
    "哈尼族彝族自治州",
    "壮族苗族自治州",
    "傣族景颇族自治州",
    "蒙古族藏族自治州",
    "傣族自治州",
    "白族自治州",
    "傈僳族自治州",
    "彝族自治州",
    "藏族自治州",
    "回族自治州",
    "蒙古自治州",
    "哈萨克自治州",
    "自治州",
]

def get_province_cities():
    provinces = get_province_cities_dict()
    provinces = clean_city_name(provinces)
    return provinces


def get_province_cities_dict():
    provinces = defaultdict(list)
    with open('city/city.json') as f:
        d = json.loads(f.read())

    for id_, province in d.items():
        for city in province:
            province_name = city['province']
            city_name = city['name']
            if province_name in [
                '北京市', '重庆市', '天津市', '上海市'
            ]:
                provinces['直辖市'].append(province_name)
            elif city_name in ['自治区直辖县级行政区划',
                               '省直辖县级行政区划', ]:
                pass
            else:
                provinces[province_name].append(city_name)
    return provinces


def clean_city_name(provinces):
    new_provinces = defaultdict(list)
    for province, cities in provinces.items():
        for city in cities:
            for suffix in suffix_list:
                if city.endswith(suffix):
                    city = city[:-len(suffix)]
            new_provinces[province].append(city)
    return new_provinces


if __name__ == '__main__':
    provinces = get_province_cities_dict()
    # pprint(provinces)
    provinces = clean_city_name(provinces)
    pprint(provinces)
