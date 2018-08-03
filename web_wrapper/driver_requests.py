import sys
import requests
from web_wrapper.web import Web
import logging

logger = logging.getLogger(__name__)


class DriverRequests(Web):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.driver_type = 'requests'

        self._create_session()

    # Headers Set/Get
    def get_headers(self):
        return self.driver.headers

    def set_headers(self, headers):
        self.driver.headers = headers

    def update_headers(self, headers):
        self.driver.headers.update(headers)

    # Cookies Set/Get
    def get_cookies(self):
        return self.driver.cookies.get_dict()

    def _format_cookies(self, cookies):
        format_cookies = []

        if isinstance(cookies, dict) is True:
            cookies = [cookies]

        for cookie in cookies:
            if 'name' in cookie and 'value' in cookie:
                cookie['value'] = str(cookie['value'])
                format_cookies.append(cookie)
            else:
                name = list(cookie.keys())[0]
                format_cookies.append({'name': name, 'value': str(cookie[name])})

        return format_cookies

    def set_cookies(self, cookies):
        # Delete all current cookies
        self.driver.cookies.clear()
        self.update_cookies(cookies)

    def update_cookies(self, cookies):
        for cookie in self._format_cookies(cookies):
            name = cookie['name']
            value = cookie['value']
            # Delete the name and value and expand out any other keys in case there
            #   are domain and other values for the cookie
            del cookie['name']
            del cookie['value']
            self.driver.cookies.set(name, value, **cookie)

    # Proxy Set/Get
    def set_proxy(self, proxy):
        """
        Set proxy for requests session
        """
        # TODO: Validate proxy url format

        if proxy is None:
            self.driver.proxies = {'http': None,
                                   'https': None
                                   }
        else:
            self.driver.proxies = {'http': proxy,
                                   'https': proxy
                                   }

        self.current_proxy = proxy

    def get_proxy(self):
        return self.current_proxy

    # Session
    def _create_session(self):
        """
        Creates a fresh session with the default header (random UA)
        """
        self.driver = requests.Session(**self.driver_args)
        # Set default headers
        self.update_headers(self.current_headers)
        self.update_cookies(self.current_cookies)
        self.set_proxy(self.current_proxy)

    def reset(self):
        """
        Kills old session and creates a new one with the default headers
        """
        self.driver = None
        self._create_session()

    def quit(self):
        """
        Generic function to close distroy and session data
        """
        self.driver = None

    # Actions
    def _get_site(self, url, headers, cookies, timeout, driver_args, driver_kwargs):
        """
        Try and return page content in the requested format using requests
        """
        try:
            # Headers and cookies are combined to the ones stored in the requests session
            #  Ones passed in here will override the ones in the session if they are the same key
            response = self.driver.get(url,
                                       *driver_args,
                                       headers=headers,
                                       cookies=cookies,
                                       timeout=timeout,
                                       **driver_kwargs)

            # Set data to access from script
            self.status_code = response.status_code
            self.url = response.url
            self.response = response

            if response.status_code == requests.codes.ok:
                # Return the correct format
                return response.text

            response.raise_for_status()

        except Exception as e:
            raise e.with_traceback(sys.exc_info()[2])
