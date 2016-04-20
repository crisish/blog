import urllib
import json

url = 'https://www.zhelitou.com.cn/bonds_list.html'

def get_data(url):
    response = urllib.urlopen(url)
    the_page = response.read()
    return the_page 

if __name__ == '__main__':
    print get_data(url)
