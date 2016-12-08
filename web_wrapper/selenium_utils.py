import sys
import json
import logging
from selenium.common.exceptions import TimeoutException, WebDriverException


logger = logging.getLogger(__name__)


class SeleniumHTTPError(IOError):
    """
    An HTTP error occurred in Selenium
    Mimic requests.exceptions.HTTPError for status_code
    """

    def __init__(self, *args, **kwargs):
        self.response = type('', (), {})()

        # Match how the status code is formatted in requests.exceptions.HTTPError
        self.response.status_code = kwargs.get('status_code')


class SeleniumUtils:

    def __inti__(self):
        pass

    def get_selenium_header(self):
        """
        Return server response headers from selenium request
        Also includes the keys `status-code` and `status-text`
        """
        javascript = """
                     function parseResponseHeaders( headerStr ){
                       var headers = {};
                       if( !headerStr ){
                         return headers;
                       }
                       var headerPairs = headerStr.split('\\u000d\\u000a');
                       for( var i = 0; i < headerPairs.length; i++ ){
                         var headerPair = headerPairs[i];
                         var index = headerPair.indexOf('\\u003a\\u0020');
                         if( index > 0 ){
                           var key = headerPair.substring(0, index);
                           var val = headerPair.substring(index + 2);
                           headers[key] = val;
                         }
                       }
                       return headers;
                     }
                     var req = new XMLHttpRequest();
                     req.open('GET', document.location, false);
                     req.send(null);
                     var header = parseResponseHeaders(req.getAllResponseHeaders().toLowerCase());
                     header['status-code'] = req.status;
                     header['status-text'] = req.statusText;
                     return header;
                     """

        return self.driver.execute_script(javascript)

    def _get_site(self, url, page_format, headers, cookies, timeout, driver_args, driver_kwargs):
        """
        Try and return page content in the requested format using selenium
        """
        try:
            # **TODO**: Find what exception this will throw and catch it and call
            #   self.driver.execute_script("window.stop()")
            # Then still try and get the source from the page
            self.driver.set_page_load_timeout(timeout)

            self.driver.get(url)
            header_data = self.get_selenium_header()
            status_code = header_data['status-code']

            # Set data to access from script
            self.status_code = status_code
            self.url = self.driver.current_url

        except TimeoutException:
            logger.warning("Page timeout: {}".format(url))
            try:
                scraper_monitor.failed_url(url, 'Timeout')
            except (NameError, AttributeError):
                # Happens when scraper_monitor is not being used/setup
                pass
            except Exception:
                logger.exception("Unknown problem with scraper_monitor sending a failed url")

        except Exception as e:
            raise e.with_traceback(sys.exc_info()[2])

        else:
            # If an exception was not thrown then check the http status code
            if status_code < 400:
                # If the http status code is not an error
                rdata = None
                if page_format == 'html':
                    logger.debug("Convert selenium html into soup")
                    rdata = self.get_soup(self.driver.page_source, input_type='html')

                elif page_format == 'json':
                    logger.debug("Convert selenium json response into dict")
                    rdata = json.loads(self.driver.find_element_by_tag_name('body').text)

                elif page_format == 'xml':
                    logger.debug("Convert selenium xml response into soup")
                    rdata = self.get_soup(self.driver.page_source, input_type='xml')

                elif page_format == 'raw':
                    logger.debug("Do not convert the selenium response, return the page source as a string")
                    # Return unparsed html
                    # In this case just use selenium's built in find/parsing
                    rdata = self.driver.page_source

                else:
                    rdata = None

                return rdata
            else:
                # If http status code is 400 or greater
                raise SeleniumHTTPError("Status code >= 400", status_code=status_code)
