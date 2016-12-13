import re
import logging
from selenium import webdriver
from web_wrapper.web import Web
from web_wrapper.selenium_utils import SeleniumUtils


logger = logging.getLogger(__name__)

# Have all compiles up here to run once
# TODO: Move to cuil, have a section for regex's
proxy_pattern = re.compile('(?:(?P<schema>\w+):\/\/)(?:(?P<user>.*):(?P<password>.*)@)?(?P<address>.*)')


class DriverSeleniumChrome(Web, SeleniumUtils):

    def __init__(self, headers={}, proxy=None):
        super().__init__()
        self.driver = None
        self.driver_type = 'selenium_chrome'
        self.opts = webdriver.ChromeOptions()
        self.current_headers = {**self._get_default_header(), **headers}
        self.current_proxy = proxy
        self.set_headers(self.current_headers, update=False)
        # self.set_proxy(self.current_proxy, update=False)
        self._create_session()

    # Headers Set/Get
    def set_headers(self, headers, update=True):
        logger.debug("Set chrome headers")

        self.current_headers = headers

        # Clear headers
        # TODO

        for key, value in headers.items():
            self.opts.add_argument("--{}={}".format(key.lower(), value))

        if update is True:
            # Recreate webdriver with new header
            self._update()

    def get_headers(self):
        # TODO: Try and get from chrome directly to be accurate
        return self.current_headers

    def add_headers(self, headers):
        self.current_headers.update(headers)
        self.set_headers(self.current_headers)

    # def set_proxy(self, proxy_parts):
    #     """
    #     Set proxy for chrome session
    #     """
    #     if proxy_parts is None:
    #         proxy_parts = {}

    #     proxy = proxy_parts.get('curl')
    #     # Did we change proxies?
    #     update_web_driver = False
    #     if self.last_proxy_value != proxy:
    #         update_web_driver = True
    #         self.last_proxy_value = proxy

    #     self.opts.add_argument('--proxy-server={}'.format(proxy))

    #     # Recreate webdriver with new proxy settings
    #     if update_web_driver is True:
    #         self._update()

    def _create_session(self):
        """
        Creates a fresh session with no/default headers and proxies
        """
        self.driver = webdriver.Chrome(chrome_options=self.opts)
        self.driver.set_window_size(1920, 1080)

    def _update(self):
        """
        Re create the web driver with the new proxy or header settings
        """
        logger.debug("Update chrome web driver")
        self.quit()
        self._create_session()

    def reset(self):
        """
        Kills old session and creates a new one with no proxies or headers
        """
        # Kill old connection
        self.quit()
        # Clear chrome configs
        self.opts = webdriver.ChromeOptions()
        # Create new web driver
        self._create_session()

    def quit(self):
        """
        Generic function to close distroy and session data
        """
        if self.driver is not None:
            self.driver.quit()
        self.driver = None
