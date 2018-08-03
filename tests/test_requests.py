from web_wrapper import DriverRequests


###
# Headers
###

def _check_header_keys(custom_headers, response, expected_response):
     # Check that the keys are the same
    assert response['headers'].keys() == expected_response['headers'].keys()

    # Check that the custom headers we set are exact matches
    for key, value in custom_headers.items():
        assert response['headers'].get(key) == expected_response['headers'].get(key)


def test_requests_header_init(httpbin):
    expected_response = {'headers': {'Accept': '*/*',
                                     'Accept-Encoding': 'gzip, deflate',
                                     'Connection': 'keep-alive',
                                     'Foo': 'bar',
                                     # The port will always differ, but just checking if the key exists
                                     'Host': '127.0.0.1:37365',
                                     'User-Agent': 'python-test'}}
    custom_headers = {'Foo': 'bar',
                      'User-Agent': 'python-test'}
    web = DriverRequests(headers=custom_headers)
    response = web.get_site(httpbin.url + '/headers', page_format='json')
    _check_header_keys(custom_headers, response, expected_response)


def test_requests_header_update(httpbin):
    expected_response = {'headers': {'Accept': '*/*',
                                     'Accept-Encoding': 'gzip, deflate',
                                     'Connection': 'keep-alive',
                                     'Foo': 'bar',
                                     # The port will always differ, but just checking if the key exists
                                     'Host': '127.0.0.1:37365',
                                     'User-Agent': 'python-test'}}
    custom_headers = {'Foo': 'bar',
                      'User-Agent': 'python-test'}
    web = DriverRequests()
    web.update_headers(custom_headers)
    response = web.get_site(httpbin.url + '/headers', page_format='json')
    _check_header_keys(custom_headers, response, expected_response)


def test_requests_header_set(httpbin):
    # Setting headers will clear the headers `Accept` or `Connection` set by the server on the first connection
    expected_response = {'headers': {'Accept-Encoding': 'gzip, deflate',
                                     'Foo': 'bar',
                                     # The port will always differ, but just checking if the key exists
                                     'Host': '127.0.0.1:37365',
                                     'User-Agent': 'python-test'}}
    custom_headers = {'Foo': 'bar',
                      'User-Agent': 'python-test'}
    web = DriverRequests()
    web.set_headers(custom_headers)
    response = web.get_site(httpbin.url + '/headers', page_format='json')
    _check_header_keys(custom_headers, response, expected_response)


###
# Cookies
###

def _check_cookie_keys(custom_cookies, response, expected_response):
     # Check that the keys are the same
    assert response['cookies'].keys() == expected_response['cookies'].keys()

    # Check that the custom cookies we set are exact matches
    if isinstance(custom_cookies, dict):
        custom_cookies = [custom_cookies]
    for cookies in custom_cookies:
        for key, value in cookies.items():
            assert response['cookies'].get(key) == expected_response['cookies'].get(key)


def test_requests_cookie_init(httpbin):
    expected_response = {'cookies': {'location': 'here'}}
    custom_cookies = {'location': 'here'}
    web = DriverRequests(cookies=custom_cookies)
    response = web.get_site(httpbin.url + '/cookies', page_format='json')
    _check_cookie_keys(custom_cookies, response, expected_response)


def test_requests_cookie_update(httpbin):
    expected_response = {'cookies': {'location': '54'}}
    custom_cookies = {'location': 54}  # Tests non string value in cookie dict
    web = DriverRequests()
    web.update_cookies(custom_cookies)
    response = web.get_site(httpbin.url + '/cookies', page_format='json')
    _check_cookie_keys(custom_cookies, response, expected_response)


def test_requests_cookie_set(httpbin):
    expected_response = {'cookies': {'location': 'here'}}
    custom_cookies = {'location': 'here'}
    web = DriverRequests()
    web.set_cookies(custom_cookies)
    response = web.get_site(httpbin.url + '/cookies', page_format='json')
    _check_cookie_keys(custom_cookies, response, expected_response)


def test_requests_cookies_init(httpbin):
    expected_response = {'cookies': {'location': 'here', 'user_id': '123'}}
    custom_cookies = [{'name': 'location', 'value': 'here'},
                      {'name': 'user_id', 'value': 123}]  # Tests non string value in cookie list
    web = DriverRequests(cookies=custom_cookies)
    response = web.get_site(httpbin.url + '/cookies', page_format='json')
    _check_cookie_keys(custom_cookies, response, expected_response)


def test_requests_cookies_update(httpbin):
    expected_response = {'cookies': {'location': 'here', 'user_id': '123'}}
    custom_cookies = [{'name': 'location', 'value': 'here'},
                      {'name': 'user_id', 'value': 123}]
    web = DriverRequests()
    web.update_cookies(custom_cookies)
    response = web.get_site(httpbin.url + '/cookies', page_format='json')
    _check_cookie_keys(custom_cookies, response, expected_response)


def test_requests_cookies_set(httpbin):
    expected_response = {'cookies': {'location': 'here', 'user_id': '123'}}
    custom_cookies = [{'name': 'location', 'value': 'here'},
                      {'name': 'user_id', 'value': 123}]
    web = DriverRequests()
    web.set_cookies(custom_cookies)
    response = web.get_site(httpbin.url + '/cookies', page_format='json')
    _check_cookie_keys(custom_cookies, response, expected_response)
