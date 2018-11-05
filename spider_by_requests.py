# -*- coding:utf -*-
import requests
import json
import MySQLdb
import time
db = MySQLdb.connect("127.0.0.1", "root", "123", "belt_road",charset="utf8")
cursor = db.cursor()
sql_sentence = 'INSERT INTO `huazhuangpin`(`id`, `goldUser`, `class`) VALUES(%s, %s, %s)'

for i in xrange(100,101):
    if i < 100:
        flag = 0
    else:
        flag = 1
    url = 'https://rate.tmall.com/list_detail_rate.htm?itemId=567254872004&spuId=318264107&sellerId=2095455386&order=3&currentPage='+str(i)+'&append=0&content=1&tagId=&posi=&picture=&ua=098%23E1hvspvBvo9vUvCkvvvvvjiPPsFU6jEvRFLpzjEUPmPwtjrPn2qv0j3vR2F9QjrE9phvHnQGyjsqzYswzPoG7MwEzbNw9HuCdphvmpmCC33Cvv2OwT6Cvvyv9O8VaQvvor9tvpvhvvCvp86Cvvyv9LGTM9vvBGhEvpCW9O5ITClrj8TxhplaWf0shB4AVADlYbmr%2BulgEc7Q%2Bu6wd5lwD76Xd346NB3rg8TNjC3ApKFhVEQ4V0Q4S4ZAhCkaU6bnDBvXVC6AxqyCvm9vvhCOvvvvIvvvBxvvvv2%2FvvCHhQvv9pvvvhxpvvvCavvvBxvvvvH6kphvC9hvpy2Ol8yCvv9vvhhygUxTMQhCvvOvChCvvvvPvpvhvv2MMsyCvvpvvhCviQhvCvvvpZojvpvhvUCvpUhCvvswPmCJDrMwznQKEHurvpvEvUHyB9gvvnGWRphvCvvvphv%3D&isg=BEFBvKtA_uKHeRLW263_5yHmUIRbbrVgg8DDTaOWPcinimFc677FMG-oaLZpmU2Y&needFold='+ flag +'&_ksTS=1534249317853_2312'
    print url
    for each in xrange(3):
        try:
            a = requests.get(url)
            json_data = json.loads(a.text.replace('"rateDetail":',''))
            for data in json_data['rateList']:
                id = data['id']
                goldUser = data['goldUser']
                auctionSku = data['auctionSku']
                data = id,goldUser,auctionSku
                try:
                    cursor.execute(sql_sentence, data)
                    db.commit()
                    print 'scussess'
                except Exception as e:
                    print e
                    db.rollback()
            break
        except:
            continue
    time.sleep(2)