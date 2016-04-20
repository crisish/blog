#encoding=utf-8
import urllib
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import time
import MySQLdb
from bs4 import BeautifulSoup
from http import RequestClient

DB_HOST = "localhost"
DB_PORT = 3306
DB_NM = "financial_data"
DB_USER = "me"
PASSWD = "Helei61881221"

url = 'www.zhelitou.com.cn'

def format_name(raw_name):
    name = raw_name.encode('utf-8')
    return name

def format_cycle(raw_cycle):
    cycle = 0
    if u"季" in raw_cycle:
        cycle = 3 
    elif  u"半年" in raw_cycle:
        cycle = 6 
    else:
        cycle = 12
    return cycle

def format_rate(raw_rate):
    rate = 0
    rate = float(raw_rate.strip(u'%')) / 100
    return round(rate, 6)

def format_deadline(raw_deadline):
    deadline = 0
    deadline = int(raw_deadline.strip(u"天"))
    return deadline

def format_status(raw_status):
    status = False 
    if u"已转让" in raw_status:
        status = True 
    else:
        status = False 
    return status

def format_amount(raw_amount):
    amount = float(raw_amount)
    return round(amount, 6)

def get_connection():
    conn = MySQLdb.connect(host=DB_HOST,user=DB_USER,passwd=PASSWD,db=DB_NM,port=DB_PORT, charset="utf8")
    return conn

def table_exist(table_name):
    conn = get_connection()
    curr = conn.cursor()
    sql = "select TABLE_NAME from INFORMATION_SCHEMA.TABLES where TABLE_SCHEMA='financial_data' and TABLE_NAME='%s' ;" % table_name
    curr.execute(sql)
    if curr.fetchall():
        return True
    else:
        return False

def create_table(table_name):
    if not table_exist(table_name):
        conn = get_connection()
        sql = """CREATE TABLE bond_data (
                 transfer_id NCHAR(40),
                 product NCHAR(40) NOT NULL,
                 cycle INT,
                 rate DOUBLE(15, 4),
                 deadline INT,
                 status BOOL,
                 amount DOUBLE(15, 2),
                 insert_time date) character set = utf8;"""
        curr = conn.cursor()
        curr.execute(sql)
        conn.commit()
        conn.close()

def get_bond(max_page=100, interval=1):
    clnt = RequestClient(url)
    for page_num in xrange(1, max_page+1):
        time.sleep(interval)
        params = {
            "type": "zjv20transfer",
            "page": str(page_num),
        }
        response = clnt.get('/transfer.html', params=params)
        if response.status/100 == 2:
            data = response.read()
            souped = BeautifulSoup(data, "html.parser")
            table = souped.find('table')
            for row in table.find_all('tr'):
                row_l = []
                attrs = row.find(class_='kdmall-btn')
                transfer_id = attrs['attrtwo'] if attrs else ""
                for col in row.find_all('td'):
                    value = col.strings
                    if value:
                        column_value = ''.join([tag_str.strip() for tag_str in value])
                        row_l.append(column_value)
                name, cycle, rate, deadline, status, amount, _= row_l
                name = format_name(name)
                cycle = format_cycle(cycle)
                rate = format_rate(rate)
                deadline = format_deadline(deadline)
                status = format_status(status)
                amount = format_amount(amount)
                yield (transfer_id, name, cycle, rate, deadline, status, amount)
    

if __name__ == '__main__':
    table_name = "bond_data"
    create_table(table_name)
    conn = get_connection()
    curr = conn.cursor()
    for (transfer_id, name, cycle, rate, deadline, status, amount) in get_bond(2):
        sql = u'''select * from bond_data where transfer_id = %s and product = %s'''
        curr.execute(sql, (transfer_id, name, ))
        if not curr.fetchall():
            print "insert", transfer_id, name, cycle, rate, deadline, status, amount
            sql = u'''insert into bond_data values (%s, %s, %s, %s, %s, %s, %s, curdate())'''
            data = (transfer_id, name, cycle, rate, deadline, status, amount)
            curr.execute(sql, data)
        else:
            print 
    conn.commit()
    curr.close()
    conn.close()
