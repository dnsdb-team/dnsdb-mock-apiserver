import json
import random
import thread
import web
import errors
from utils import validate_ip

default_remaining_request = 10
max_page_size = 100
total = 100
default_access_token = None
default_search_id = None
users = {
    'admin': {'password': '12345', 'remaining_request': 10},
}


def generate_random_string():
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

    def put_retrieve_context(self, search_id, retrieve_context):
        self.context[search_id] = retrieve_context

    def get_retrieve_ctx(self, search_id):
        return self.context[search_id]


class RetrieveContext(object):
    def __init__(self, data, remaining_request):
        self.data = data
        self.total = len(data)
        self.remaining_request = remaining_request


dns_data = [
    {'host': 'a.com', 'type': 'a', 'value': '1.1.1.1'},
    {'host': 'b.com', 'type': 'a', 'value': '1.1.1.2'},
    {'host': 'c.com', 'type': 'a', 'value': '1.1.1.3'},
    {'host': 'd.com', 'type': 'a', 'value': '1.1.1.4'},
]

all_dns_data = dns_data * 100

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


class Index(object):
    def GET(self):
        api_info = {'message': 'DnsDB Mock Web API', 'version': 1}
        return api_info


class Authorize(object):
    def POST(self):
        i = web.input()
        username = i.get("username")
        password = i.get("password")
        if default_access_token:
            token = default_access_token
        else:
            token = generate_random_string()
        if users.get(username, None) == password:
            data = {
                'success': True,
                'access_token': token,
                'expire_in': 600
            }
            context.put_token(data['access_token'])
            return data
        else:
            raise errors.UnauthorizedError()


class SearchDns(object):
    def GET(self):
        token = web.ctx.env.get('HTTP_ACCESS_TOKEN')
        if not context.has_token(token):
            raise errors.UnauthorizedError()
        i = web.input()
        domain = i.get('domain')
        host = i.get('host')
        ip = i.get('ip')
        dns_type = i.get('type')
        start_position = i.get('from')
        if start_position == '':
            start_position = 0
        try:
            start_position = int(start_position)
        except ValueError:
            raise errors.BadRequestError(errors.FROM_VALUE_ERROR)
        if start_position < 0 or start_position > 9970:
            raise errors.BadRequestError(errors.FROM_VALUE_ERROR)

        if ip:
            if not validate_ip(ip):
                raise errors.BadRequestError(errors.IP_VALUE_ERROR)
        if domain is None and ip is None and host is None:
            raise errors.BadRequestError(errors.MISSING_QUERY_ERROR)
        return {'success': True, 'data': dns_data, 'remaining_request': 321, 'total': 921}


class SearchAllDns(object):
    def GET(self):
        token = web.ctx.env.get('HTTP_ACCESS_TOKEN')
        if not context.has_token(token):
            raise errors.UnauthorizedError()
        if default_search_id:
            search_id = default_search_id
        else:
            search_id = generate_random_string()
        dns_set = [{"host": "a.com", "type": "a", "value": "1.1.1.1"}]
        retrieve_ctx = RetrieveContext(data=dns_set * total, remaining_request=default_remaining_request)
        context.put_retrieve_context(search_id, retrieve_ctx)
        data = {
            "success": True,
            "total": retrieve_ctx.total,
            "id": search_id
        }
        return data


class RetrieveDns(object):
    def GET(self):
        i = web.input()
        search_id = i.get("id")
        retrieve_ctx = context.get_retrieve_ctx(search_id)
        if retrieve_ctx.remaining_request <= 0:
            raise errors.CreditsInsufficientError()
        data = retrieve_ctx.data[:max_page_size]
        for record in data:
            retrieve_ctx.data.remove(record)
        if len(data) > 0:
            retrieve_ctx.remaining_request -= 1
            return {
                "success": True,
                "total": retrieve_ctx.total,
                "data": data,
                'remaining_request': retrieve_ctx.remaining_request
            }
        else:
            raise errors.NotFoundError()


class Resources(object):
    def GET(self):
        pass


app = web.application(urls, globals())
app.add_processor(api_processor)


def start():
    thread.start_new_thread(app.run, ())


def stop():
    app.stop()


def restart():
    stop()
    start()
