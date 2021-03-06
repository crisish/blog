import datetime

from constants import STRING
from functions import partial, url_safe, utf8, import_httplib

httplib = import_httplib()

class RequestClient(object):
    '''
    A simple http client implement.
    '''
    methods = ['GET', 'POST', 'PUT', 'DELETE', 'HEAD']

    def __init__(self, host, port=443):
        self.h, self.p = host, port

    def send_request(self, method, path='', params={}, headers={}, body=''):
        # Start args validate sections.
        assert not params or isinstance(params, dict), 'params must be dict or None'
        assert not params or isinstance(headers, dict), 'headers must be dict or None'

        conn = httplib.HTTPSConnection(self.h, self.p)
        url = self.get_url(path, params)
        conn.request(method, url, body, headers)
        res = conn.getresponse()
        return res

    def __getattr__(self, attr):
        if attr.upper() in self.methods:
            return partial(self.send_request, attr.upper())
        else:
            errs = (self.__class__.__name__, attr)
            raise AttributeError("'%s' object has no attribute '%s'"%errs)

    def get_url(self, path, params):
        '''
        Generates request url according to specified params.
        '''
        p = []
        for (k, v) in params.items():
            k, v = (url_safe(k.replace('_', '-')), url_safe(utf8(v)))
            entry = '%s=%s'%(k, v) if v else '%s'%k
            p.append(entry)
        connector = '&'
        seperator = '?' if p else ''
        return '%s%s%s'%(path, seperator, connector.join(p))
