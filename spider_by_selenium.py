# -*- coding:utf-8 -*-
import requests
import re
from selenium import webdriver
import time
from lxml import etree
import MySQLdb
def initDriver(executable_path):
    # driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1'])
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(executable_path=executable_path,chrome_options=chrome_options)
    driver.set_page_load_timeout(60)
    driver.set_script_timeout(60)
    return driver
executable_path = '/home/linnankai/PycharmProjects/taobao/chromedriver'
driver = initDriver(executable_path )
url = 'https://s.taobao.com/search'
payload = {
    'q': '内存条',
    's': '1',
    'bcoffset': '6',
    'ntoffset': '6',
    'p4ppushleft': '1%2C48'
}
header = {
    'upgrade-insecure-requests':'1',
    'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/65.0.3325.181 Chrome/65.0.3325.181 Safari/537.36'
}
base_url = 'https://detail.tmall.com/item.htm?id='
db = MySQLdb.connect("127.0.0.1", "root", "123", "belt_road",charset="utf8")
cursor = db.cursor()
for k in range(1, 10):  # 10次，就是10页的商品数据
    payload['s'] = 44 * k
    payload['bcoffset'] = -3 * k + 6
    payload['ntoffset'] = -3 * k + 6
    resp = requests.get(url, params=payload)
    print(resp.url)  # 打印访问的网址
    resp.encoding = 'utf-8'  # 设置编码
    title = re.findall(r'"raw_title":"([^"]+)"', resp.text, re.I)
    price = re.findall(r'"view_price":"([^"]+)"', resp.text, re.I)
    loc = re.findall(r'"item_loc":"([^"]+)"', resp.text, re.I)
    detail_url = re.findall(r'"detail_url":"([^"]+)"', resp.text, re.I)
    nid = re.findall(r'"nid":"([^"]+)"', resp.text, re.I)
    x = len(title)  # 每一页商品的数量
    print x
    print len(detail_url)
    for i in xrange(x):
        print title[i]
        url = base_url + nid[i]
        print url
        temp = requests.get(url)
        if 'tmall' in temp.url:
            driver.get(temp.url)
            if 'login' in driver.current_url:
                time.sleep(20)
            time.sleep(5)
            page_content = driver.page_source
            selector = etree.HTML(page_content)
            try:
                price = selector.xpath('//*[@id="J_PromoPrice"]/dd/div/span/text()')[0]
            except:
                price = selector.xpath('//*[@id="J_StrPriceModBox"]/dd/span/text()')[0]
            other_items = selector.xpath('//*[@id="J_relateGroup"]/dd/ul/li/a/@href')
            hot = selector.xpath('//*[@id="J_DetailMeta"]/div[1]/div[1]/div/ul/li[1]/div/span[2]/text()')[0]
            name = selector.xpath('//h1/text()')[-1].strip()
            sql_sentence = 'INSERT INTO `taobao`(`id`, `items`, `price`, `month_volume`, `class`, `url`) VALUES(%s, %s, %s, %s, %s, %s)'
            data = nid[i], name, price, hot, '内存条',url
            try:
                cursor.execute(sql_sentence, data)
                db.commit()
                print 'scussess'
            except Exception as e:
                print e
                db.rollback()

            for other in other_items:
                id = re.findall(r'id=([^"]+)',other)[0]
                print id
                url = base_url + id
                print url
                driver.get(url)
                if 'login' in driver.current_url:
                    time.sleep(20)
                time.sleep(5)
                page_content = driver.page_source
                selector = etree.HTML(page_content)
                try:
                    price = selector.xpath('//*[@id="J_PromoPrice"]/dd/div/span/text()')[0]
                except:
                    price = selector.xpath('//*[@id="J_StrPriceModBox"]/dd/span/text()')[0]
                other_items = selector.xpath('//*[@id="J_relateGroup"]/dd/ul/li/a/@href')
                hot = selector.xpath('//*[@id="J_DetailMeta"]/div[1]/div[1]/div/ul/li[1]/div/span[2]/text()')[0]
                name = selector.xpath('//h1/text()')[-1].strip()
                sql_sentence = 'INSERT INTO `taobao`(`id`, `items`, `price`, `month_volume`, `class`, `url`) VALUES(%s, %s, %s, %s, %s, %s)'
                data = id, name, price, hot, '内存条', url
                try:
                    cursor.execute(sql_sentence, data)
                    db.commit()
                    print 'scussess'
                except Exception as e:
                    print e
                    db.rollback()




