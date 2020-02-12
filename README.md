去哪儿网数据分析和可视化
====================

目标
---

- [x] 根据关键字列表爬取各个城市的酒店信息和相关评论
- [x] 根据关键字列表爬取各个城市的景点信息
- [ ] 对数据进行分析并可视化
    - [ ] 酒店推荐(首页)
    - [ ] 酒店价格分布区间柱状图(酒店列表页)
    - [ ] 酒店好中差评论比例饼图(酒店详情页)
    - [ ] 酒店评论关键字词云(酒店详情页)
    - [ ] 景点热度top排名(首页)
    - [ ] todo
- [ ] 使用Django展示
    - [X] 导航
    - [X] 显示所有酒店列表和详情
    - [X] 显示所有景点列表和景点详情
    - [ ] 首页:推荐热门城市,热门景点
    - [ ] 酒店列表和酒店详情页
    - [ ] 景点列表和景点详情页
    - [ ] todo
    
环境
------
- Python 3.7
- mongodb-community 4.2.3

安装依赖
------
    $ python3 -m pip install -r requirements.txt

运行爬虫
------
    $ python3 crawl.py

备注
---
- NoSQL数据库用于存储爬取下来的数据时会很方便，但是Django默认的数据库backend是不支持MongoDB的，主要的两个开源实现包括[mongodb-engine](https://github.com/django-nonrel/mongodb-engine)和[mongoengine](https://github.com/MongoEngine/mongoengine)，前者依赖的django-norel已经长期没有更新了，后者默认是不支持admin app的；所以决定选取MySQL作为网站的后端数据库。
- 城市列表使用了开源项目[china_regions](https://github.com/wecatch/china_regions)，通过观察去哪儿网url规则发现，网址url和api接口都会讲城市名字转换为拼音，例如三亚市的url为https://hotel.qunar.com/cn/sanya/ ,以下为转换规则：
    1. 所有城市不包含末尾的"市",三亚市 -> sanya
    2. 直辖市增加"_city"后缀:北京 -> beijing_city
    3. 不包含末尾"朝鲜自治州": 延边朝鲜自治州 -> yanbian
    4. 不包含末尾"地区": 大兴安岭地区 -> daxinganling
    5. 土家族苗族自治州
    7. 藏族羌族自治州
    8. 布依族苗族自治州
    9. 苗族侗族自治州
    9. 楚雄彝族自治州
    10. 哈尼族彝族自治州
    11. 壮族苗族自治州
    12. 纳傣族自治州
    13. 白族自治州
    14. 傣族景颇族自治州
    15. 傈僳族自治州
    16. 藏族自治州
    17. 回族自治州
    18. 蒙古族藏族自治州
    19. 蒙古自治州
    20. 哈萨克自治州
    21. 克孜勒苏柯尔克孜自治州 -> 克孜勒苏柯尔克孜





