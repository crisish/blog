import urllib
from http import RequestClient

url = 'www.zhelitou.com.cn'


if __name__ == '__main__':
    clnt = RequestClient(url)
    # response = clnt.get('/bonds_list.html')
    # print response.status
    values = {
        'apiNameAndVersion' : 'kingdom.kifp.get_all_kind_total,v1.0',
    }
    data = urllib.urlencode(values)
    headers = {
        "Content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Accept": "application/json, text/javascript, */*; q=0.01"
    }

    response = clnt.post('/mall/zjv2commonaction!zjCommonMethod.do', body=data, headers=headers)
    print response.status
    print response.read()
