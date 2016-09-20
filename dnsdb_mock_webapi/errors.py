import web

AUTHENTICATE_FAILED = {'success': False, 'error': 'authenticate_failed', 'message': "Username password does not match"}
UNAUTHORIZED_ERROR = {'success': False, 'error': 'unauthorized', 'message': 'Access token has expired or not existed'}
CREDITS_INSUFFICIENT = {'success': False, 'error': 'credits_insufficient',
                        'message': 'API number of times insufficient, please recharge'}
ACCOUNT_DISABLED_ERROR = {'success': False, 'error': 'account_disabled', 'message': 'Account is disabled'}
NOT_DEVELOPER_ERROR = {'success': False, 'error': 'not_developer', 'message': 'Please apply to become a developer'}
MISSING_QUERY_ERROR = {'success': False, 'error': 'missing_query_error',
                       'message': 'Missing query parameters, please select at least one parameter from "host", "domain", and "ip"'}
FROM_VALUE_ERROR = {'success': False, 'error': 'from_value_error', 'message': '[from] should be an integer(0~9970)'}
IP_VALUE_ERROR = {'success': False, 'error': 'ip_value_error', 'message': '[ip] should be a valid IP address'}
GATEWAY_TIMEOUT_ERROR = {'success': False, 'error': 'gateway_timeout',
                         'message': 'Please contact the dnsdb.io administrator to deal with the problem.'}
INTERNAL_SERVER_ERROR = {'success': False, 'error': 'internal_server_error',
                         'message': 'Please contact the dnsdb.io administrator to deal with the problem.'}
ABUSE_REQUEST_ERROR = {'success': False, 'error': 'abuse_request',
                       'message': 'Server detects your IP presence abuse request'}
NOT_FOUND = {'success': False, 'error': 'not_found', 'message': 'Not found'}
WRONG_SEARCH_ID = {'success': False, 'error': 'wrong_search_id', 'message': 'Wrong search id'}


class UnauthorizedError(web.HTTPError):
    def __init__(self):
        status = '401 Unauthorized'
        headers = {'Content-Type': 'application/json'}
        data = AUTHENTICATE_FAILED
        web.HTTPError.__init__(self, status, headers, data)
