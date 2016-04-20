import urllib
import time
import json
import MySQLdb
import httplib

import config

def get_data(url):
    values = {
        'apiNameAndVersion' : 'kingdom.kifp.get_all_kind_total,v1.0',
    }
    data = urllib.urlencode(values)
    response = urllib.urlopen(url, data)
    the_page = response.read()
    d = json.loads(the_page) 
    l = [float(item['total']) for item in d['items']]
    register = int(l[0])
    invest = l[1]
    transfer = l[2]
    cash = l[3]
    return register, invest, transfer, cash 


# print(the_page.decode("utf8")) 


if __name__ == '__main__':
    data = get_data(config.url)
    try:
        conn = MySQLdb.connect(host='localhost',user='me',passwd='Helei61881221',db='mydb',port=3306)
        cur=conn.cursor()
        # cur.execute('create table daily_data(time date, people int, invest double(15, 2), transfer double(15, 2), cash double(15, 2))')
        cur.execute('insert into daily_data values(curdate(), %s, %s, %s, %s)', data) 
        count = cur.execute('select * from daily_data')
        print count
        conn.commit()
        cur.close()
        conn.close()
    except MySQLdb.Error,e:
         print "Mysql Error %d: %s" % (e.args[0], e.args[1])
