# -*- coding: utf-8 -*-
import scrapy
from fang.items import NewhouseItem
from fang.items import EsfItem
import re


class FangspiderSpider(scrapy.Spider):
    name = 'fangspider'
    allowed_domains = ['fang.com']
    start_urls = ['http://www.fang.com/SoufunFamily.htm']
    # 设置起始的 url

    def parse(self, response):
        num = 0  # 计数获取了多少个城市时使用 num += 1 .
        # trs = response.xpath('//table[@id="senfe"]//tr')  # 省份列表
        # for tr in trs:  # 对于每个省份进行处理
        #     print(tr.xpath('./@id').get())
        for count in range(1, 32):
            trs = response.xpath('//tr[@id="sffamily_B03_%02d"]' % count)  # %02d 一位数的时候在左侧补0
            # print(len(trs))
            province = trs[0].xpath('.//strong/text()').get()
            print('******' + province)
            for tr in trs:
                citys = tr.xpath('.//a')
                for city in citys:
                    num += 1
                    city_name = city.xpath('./text()').get()
                    if city_name == '北京':
                        newhouse_url = 'http://newhouse.fang.com/house/s/?from=db'
                        esf_url = 'http://esf.fang.com/house/s/?from=db'
                        print(city_name, newhouse_url, esf_url)
                    else:
                        city_url = city.xpath('./@href').get()  # http://huainan.fang.com/
                        city_url_city = city_url.split('.')[0].split('/')[-1]
                        newhouse_url = 'http://{}.newhouse.fang.com/'.format(city_url_city)
                        esf_url = 'http://{}.esf.fang.com/'.format(city_url_city)
                        print(city_name, newhouse_url, esf_url)
                    yield scrapy.Request(url=newhouse_url,
                                         callback=self.parse_newhouse,
                                         meta={'info': (province, city_name )}
                                         # 使用meta，传递后续使用到的参数，在下边的函数里可见。
                                         )
                    yield scrapy.Request(url=esf_url,
                                         callback=self.parse_esf,
                                         meta={'info': (province, city_name)}
                                         )
                    break
                break
            break
            # print('\n')  # 输出显示时用于在每个省份后加一个空行，便于查看。
        print(num)

    def parse_newhouse(self, response):
        province, city_name = response.meta.get('info')
        lis = response.xpath('//div[@id="newhouse_loupai_list"]//li')
        for li in lis:
            if li.xpath('./div/div/@class').get() == 'nlc_img':
                # 加这个判断是为了去掉lis中那个不是房屋信息的li
                name = li.xpath('.//div[@class="nlcd_name"]/a/text()').get().strip()
                price = ''.join(li.xpath('.//div[@class="nhouse_price"]//text()').getall()[:3]).strip()
                if not price:
                    price = '推荐楼盘'
                parts = li.xpath('.//div[@class="house_type clearfix"]//text()').getall()
                room_list = list(map(lambda x: x.strip().replace('\t', '').replace('\n', ''), parts))
                # 对于小规模的 for 循环，可以用 lambda 函数来处理，显得更加精简
                # 后边的 replace 也可以用正则的 re.sub('\s', '', part) 来处理
                rooms = ''.join(room_list).split('－')[0]
                area = ''.join(room_list).split('－')[-1]
                district = re.findall(r'\[(.+)\]', li.xpath('.//div[@class="address"]/a/@title').get())[0]
                address = li.xpath('.//div[@class="address"]/a/@title').get().split(']')[-1]
                # sale = li.xpath('.//span[@class="inSale"]/text()').get()
                sale = li.xpath('.//div[@class="fangyuan"]/span//text()').get()
                # 此时注意，class的值是在页面源代码里找到的，在页面元素里找到不对。
                origin_url = 'http:' + li.xpath('.//div[@class="nlcd_name"]/a/@href').get()
                item = NewhouseItem(name=name,
                                    price=price,
                                    rooms=rooms,
                                    area=area,
                                    sale=sale,
                                    district=district,
                                    address=address,
                                    origin_url=origin_url,
                                    province=province,
                                    city=city_name
                                    )
                yield item
                # print(district)
        # 查找下一页的链接：
        next_page = 'http://newhouse.fang.com' + response.xpath('//a[@class="next"]/@href').get()
        yield scrapy.Request(url=next_page,
                             callback=self.parse_newhouse,
                             meta={'info': (province, city_name)}
                             )
        # print(next_page)

    def parse_esf(self, response):
        province, city_name = response.meta.get('info')
        item = EsfItem(province=province, city=city_name)
        dls = response.xpath('//div[@class="shop_list shop_list_4"]//dl')
        for dl in dls:
            if dl.xpath('./dt/@class').get() == 'floatl':
                print(dl.xpath('./@id').get())
                item['name'] = dl.xpath('.//p[@class="add_shop"]/a/@title').get()
                infos = list(map(lambda x: x.strip(), dl.xpath('.//p[@class="tel_shop"]//text()').getall()))
                # 对获取列表的每一项进行 lambda 处理去空白符。
                for info in infos:
                    if '厅' in info:
                        item['rooms'] = info
                    elif '层' in info:
                        item['floor'] = info
                    elif '向' in info:
                        item['toward'] = info
                    elif '年' in info:
                        item['year'] = info
                item['address'] = dl.xpath('.//p[@class="add_shop"]/span/text()').get()
                item['area'] = infos[2]
                item['price'] = ''.join(dl.xpath('.//span[@class="red"]//text()').getall())
                item['unit'] = dl.xpath('.//dd[@class="price_right"]/span[2]/text()').get()
                item['origin_url'] = 'http://esf.fang.com' + dl.xpath('.//h4[@class="clearfix"]/a/@href').get()
                yield item
        next_page = 'http://esf.fang.com' + response.xpath('//div[@id="list_D10_15"]/p/a/@href').get()
        yield scrapy.Request(url=next_page,
                             callback=self.parse_esf,
                             meta={'info': (province, city_name)}
                             )
        # print(next_page)
