# -*- coding: utf-8 -*-

import xlwt
import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
from selenium import webdriver
from Premium.dataprocess import DataProcess


from Premium.items import PremiumItem


class PremiumSpider(scrapy.Spider):
    name = 'jd'
    allowed_domains = ['jd.com']
    search_base_url = 'https://search.jd.com/'
    search_end_url = '&enc=utf-8.html'
    # start_urls = ['https://search.jd.com/Search?keyword=iPhone8plus']
    kw = ['奥克斯']

    def start_requests(self):
        # return None
        # 启动selenium服务端
        option = webdriver.ChromeOptions()
        option.add_argument('headless')
        self.driver = webdriver.Chrome(chrome_options=option)
        # 爬虫起始链接
        for i in self.kw:
            url = '{}Search?keyword={}{}'.format(self.search_base_url, i, self.search_end_url)
            yield Request(url, self.parse, meta={'origin': i})

    def close(self, spider, reason):
        self.driver.close()
        # dp = DataProcess()
        # dp.db = 'jd_copy'
        # dp.search()

    def parse(self, response):
        html = BeautifulSoup(response.text, 'lxml')
        # 品牌
        self.origin = response.meta['origin']
        categories = html.find_all('div', class_='J_selectorLine s-category')
        categories = sum([i.find_all('li') for i in categories], [])
        categories = sum([i.find_all('a') for i in categories], [])
        ''''''
        # categories = categories[:1]
        ''''''
        for i in categories:
            url = '{}{}'.format(self.search_base_url, i['href'])
            category = i['title']
            yield Request(url, callback=self.aux_categories, meta={'category': category})

    def aux_categories(self, response):
        html = BeautifulSoup(self.get_undisplay_page(response.url), 'lxml')
        try:
            max_num = int(html.find('span', class_='p-skip').find('b').text) + 1
            # max_num = 1
        except:
            max_num = 1
        for i in range(max_num):
            url = '{}&page={}'.format(response.url, (2 * i - 1))
            yield Request(url, callback=self.aux_all_page, meta=response.meta)

    def aux_all_page(self, response):
        html = BeautifulSoup(response.text, 'lxml')
        categories = html.find('ul', class_='gl-warp clearfix').find_all('li')
        categories = [i.find('div', class_='p-img').find('a') for i in categories]

        ''''''
        # categories = categories[:1]
        # url = 'https://item.jd.com/28427742841.html'
        # yield Request(url, callback=self.aux_get_details)
        ''''''
        # url
        for category in categories:
            url = '{}{}'.format('https:', category['href'])
            yield Request(url, callback=self.aux_get_details, meta=response.meta)

    def aux_get_details(self, response):
        item = PremiumItem()
        html = BeautifulSoup(self.get_undisplay_page(response.url), 'lxml')

        # 品牌
        try:
            origin = html.find('ul', id='parameter-brand').find('li')['title']
        except:
            origin = ''
        if self.origin not in origin:
            return None
        # 类别
        category = response.meta['category']
        # 价格
        price = html.find('div', class_='summary-price J-summary-price').find('span', class_='p-price')
        price = price.find_all('span')[1].text
        # 链接
        url = response.url

        # 增值保障，保费
        sss = html.find('div', class_='summary p-choose-wrap').find_all('div', id=True)
        sss = [i.find('div', class_='dt') for i in sss]
        other = ''
        for i in sss:
            try:
                if '特色' in i.text or '特殊' in i.text:
                    other = response.url
            except:
                pass
        premium = []
        try:
            ser = html.find('div', id='choose-service').find_all('div', class_='yb-item-cat')
            ser = [i.find('div', class_='more-item').find_all('div', class_='title') for i in ser]
        except:
            ser = []
        # 京东服务 TODO: 京东服务和特殊服务
        try:
            ser1 = html.find('div', id='choose-service+').find_all('div', class_='service')
            ser1 = sum([i.find('div', class_='service__body').find_all('div', class_='title') for i in ser1], [])
        except:
            ser1 = []

        premium.append(
            [
                [
                    (
                        i.find('span', class_='name').text,
                        i.find('span', class_='price').text.replace('￥', '')
                    )
                    for i in service
                ]
                for service in ser
            ]
        )
        premium.append(
            [
                (
                    service.find('span', class_='name').text,
                    service.find('span', class_='price').text.replace('￥', '')
                )
                for service in ser1
            ]
        )
        premium = str(premium).replace("'", '"')

        # 商品信息：型号/货号，商品编号
        '''去除提示问号'''
        try:
            model = html.find_all('div', class_='Ptable-item')[0].find('dl').find_all(['dt', 'dd'])
            for i in model:
                if i.has_attr("class"):
                    del (model[model.index(i)])
        except:
            model=[]
        '''选择型号后面的文字'''
        _ = '0'
        for i in model:
            if i.text == '型号':
                _ = model[model.index(i) + 1].text
                break
        model = _
        '''如果型号没有，就去取货号'''
        all_info = html.find('ul', class_='parameter2 p-parameter-list').find_all('li')
        if model == '0':
            for i in all_info:
                if '货号' in i.text:
                    model = i['title']
                    break
        model = model.split()[0]

        name = all_info[0]['title']
        name_id = all_info[1]['title']

        # 填充数据库，origin, category, model, price, premium, url, name_id
        item['origin'] = origin
        item['category'] = category
        item['name'] = name
        item['model'] = model
        item['price'] = price
        item['premium'] = premium
        item['url'] = url
        item['name_id'] = name_id
        item['other'] = other
        return item

    def get_undisplay_page(self, url):
        self.driver.get(url)
        page = self.driver.page_source
        return page


