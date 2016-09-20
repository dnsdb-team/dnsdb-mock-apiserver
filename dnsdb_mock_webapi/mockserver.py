import web
import json
import errors
import random


def generate_access_token():
    charsets = 'abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    token = ''
    for i in range(0, 128):
        token += charsets[random.randint(0, len(charsets) - 1)]
    return token


class ApplicationContext(object):
    def __init__(self):
        self.context = {'tokens': []}

    def has_token(self, token):
        return token in self.context['tokens']

    def put_token(self, token):
        self.context['tokens'].append(token)


dns_data = [
    {'host': 'a.com', 'type': 'a', 'value': '1.1.1.1'},
    {'host': 'b.com', 'type': 'a', 'value': '1.1.1.2'},
    {'host': 'c.com', 'type': 'a', 'value': '1.1.1.3'},
    {'host': 'd.com', 'type': 'a', 'value': '1.1.1.4'},
]

context = ApplicationContext()

urls = (
    '/api/v1', 'Index',
    '/api/v1/authorize', 'Authorize',
    '/api/v1/dns/search', 'SearchDns',
    '/api/v1/dns/search_all', 'SearchAllDns',
    '/api/v1/dns/retrieve', 'RetrieveDns',
    '/api/v1/resources', 'Resources',
)


def api_processor(handler):
    res = handler()
    if res:
        data = json.dumps(res)
        web.header('Content-Type', 'application/json')
        web.header('Server', 'DnsDB Mock API Server')
        web.header('Content-Length', len(data))
        return data


class Index:
    def GET(self):
        api_info = {'message': 'DnsDB Mock Web API', 'version': 1}
        return api_info


class Authorize:
    def POST(self):
        i = web.input()
        username = i.get("username")
        password = i.get("password")
        if username == password:
            data = {
                'success': True,
                'access_token': generate_access_token(),
                'expire_in': 600
            }
            context.put_token(data['access_token'])
            return data
        else:
            raise errors.UnauthorizedError()


class SearchDns:
    def GET(self):
        token = web.ctx.env.get('HTTP_ACCESS_TOKEN')
        return {'success': True, 'data': dns_data, 'remaining_request': 321, 'total': 921}


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.add_processor(api_processor)
    app.run()
