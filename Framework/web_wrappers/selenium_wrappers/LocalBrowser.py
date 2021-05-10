"""
This is an updated Browser class that inherits the remote driver version of Browser

"""
__author__ = "nitin.kumar-2@mitel.com"

import os
import sys
import time

#Part of JavaScript console.log modification
import logging
import tempfile


from log import log

from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from robot.api.logger import console
from robot.api import logger
from selenium.webdriver.chrome.options import Options
from Browser import Browser

# todo if the user already has the config for the webdriver enabled then they can use the installed driver

class LocalBrowser(Browser):
    _DEFAULT_TIMEOUT = 15
    _BROWSER_INFO_WIN = {'firefox'       : {'webdriver_path': os.path.join(
                                            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                                            'ext_web_driver','windows', 'geckodriver.exe')},
                     'ie'            : {'webdriver_path': '..\\ext_web_driver\\windows\\IEDriverServer.exe'},
                     'edge'          : {'webdriver_path': '..\\ext_web_driver\\windows\\MicrosoftWebDriver.exe'},
                     'local_chrome'  : {'webdriver_path': os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ext_web_driver','windows', 'chromedriver.exe')},
                     'chrome'        : {'webdriver_path': os.path.join(
                                            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                                            'ext_web_driver','windows', 'chromedriver.exe')},
                     'ghost'         : {'webdriver_path': '..\\ext_web_driver\\windows\\phantomjs.exe'}}

    _BROWSER_INFO_MAC = {'firefox': {'webdriver_path': os.path.join(
                                            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                                            'ext_web_driver','mac', 'geckodriver.exe')},
                     'ie': {'webdriver_path': '..\\ext_web_driver\\mac\\IEDriverServer'},
                     'edge': {'webdriver_path': '..\\ext_web_driver\\mac\\MicrosoftWebDriver'},
                     'local_chrome': {
                         'webdriver_path': os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ext_web_driver','mac',
                                                        'chromedriver')},
                     'chrome': {'webdriver_path': os.path.join(
                         os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                         'ext_web_driver', 'mac','chromedriver')},
                     'ghost': {'webdriver_path': '..\\ext_web_driver\\mac\\phantomjs'}}

    _BROWSER_INFO_LINUX = {'firefox': {'webdriver_path': os.path.join(
                    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                    'ext_web_driver', 'linux', 'geckodriver.exe')},
                    'ie': {'webdriver_path': '..\\ext_web_driver\\linux\\IEDriverServer'},
                    'edge': {'webdriver_path': '..\\ext_web_driver\\linux\\MicrosoftWebDriver'},
                    'local_chrome': {
                        'webdriver_path': os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ext_web_driver', 'linux',
                                                       'chromedriver')},
                    'chrome': {'webdriver_path': os.path.join(
                        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                        'ext_web_driver', 'linux', 'chromedriver')},
                    'ghost': {'webdriver_path': '..\\ext_web_driver\\linux\\phantomjs'}}

    def __init__(self, browser="chrome", crx=None, notifications=None):

        # Part of JavaScript console.log modification
        selenium_logger = logging.getLogger("selenium.webdriver.remote.remote_connection")
        selenium_logger.setLevel(logging.WARNING)
        self.console_log = tempfile.NamedTemporaryFile(delete=False, suffix=".log")

        # initializing based on platform
        if sys.platform == "win32":
            self._BROWSER_INFO = self._BROWSER_INFO_WIN
            self._FIREFOX_DEFAULT_PATH = os.path.join(os.environ["ProgramFiles"], "Mozilla Firefox\\firefox.exe")
            self.user_data_dir = "C:\\Users\\Administrator\\AppData\\Local\\Google\\Chrome\\User Data"
        elif sys.platform == "darwin":
            self._BROWSER_INFO = self._BROWSER_INFO_MAC
            self._FIREFOX_DEFAULT_PATH = "//Applications//Firefox.app//Contents//MacOS//firefox-bin"
            self.user_data_dir = "//Users//administrator//Library//Application Support//Google//Chrome"
        elif sys.platform == "linux2":
            self._BROWSER_INFO = self._BROWSER_INFO_LINUX
            self._FIREFOX_DEFAULT_PATH = "//Applications//Firefox.app//Contents//MacOS//firefox-bin"
            self.user_data_dir = "//Users//administrator//Library//Application Support//Google//Chrome"
        self.browsertype = browser
        if self.browsertype in self._BROWSER_INFO.keys():
            self._browser = self.create_webdriver(self.browsertype,crx, notifications)
        else:
            raise Exception("\nBrowser not supported. Supported browsers: %s\n" %
                            self._BROWSER_INFO.keys())

        # super(LocalBrowser,self).__init__("test")
        self.elements = {
            "id"            : self._browser.find_elements_by_id,
			#"accessibility" : self._browser.find_element_by_accessibility_id,
            "name"          : self._browser.find_elements_by_name,
            "xpath"         : self._browser.find_elements_by_xpath,
            "tag"           : self._browser.find_elements_by_tag_name,
            "css_class"     : self._browser.find_elements_by_class_name,
            "text"          : self._browser.find_element_by_link_text,
            "css_selector"  : self._browser.find_elements_by_css_selector
        }
        log.setLogHandlers()

    def create_webdriver(self, browser="chrome", crx=None, notifications=None):
        """
        Create the webdriver object depending on the browser type
                Args:
                    browser - type of browser. Supported options: chrome, firefox, ie, headless, edge
                Returns:
                    Webdriver(object) depending on the type of the browser
        """
        if browser == 'firefox':
            try:
                firefoxCap = DesiredCapabilities.FIREFOX
                # we need to explicitly specify to use Marionette
                firefoxCap['marionette'] = True
                # and the path to firefox
                firefoxCap['binary'] = self._FIREFOX_DEFAULT_PATH

                testdriver = webdriver.Firefox(capabilities=firefoxCap, firefox_binary=FirefoxBinary(
                    self._FIREFOX_DEFAULT_PATH),
                                               executable_path=self._BROWSER_INFO[browser]['webdriver_path'])
            except Exception as err:
                console(err)

        elif browser == 'ghost':
            testdriver = webdriver.PhantomJS(self._BROWSER_INFO[browser]['webdriver_path'])

        elif browser == 'local_chrome':
            browser_chrome = 'chrome.exe'
            os.system("taskkill /f /im " + browser_chrome)
            options = webdriver.ChromeOptions()
            options.add_argument(r"user-data-dir=%s"%self.user_data_dir)
            if notifications is not None:
                if notifications == "allow":
                    notif_index = 1
                else:
                    notif_index = 2
            prefs = {"profile.default_content_setting_values.notifications": notif_index}
            options.add_experimental_option("prefs", prefs)
            testdriver = webdriver.Chrome(self._BROWSER_INFO[browser]['webdriver_path'], chrome_options=options)

        elif browser == 'chrome' and sys.platform == "linux2":
            options = webdriver.ChromeOptions()
            options.add_argument(r"--no-sandbox")
            testdriver = webdriver.Chrome(self._BROWSER_INFO[browser]['webdriver_path'], chrome_options=options)

        else:
            options = webdriver.ChromeOptions()
            if crx:
                logger.warn("Using crx app '%s'" % crx)
                options.add_extension(crx)

            if notifications:
                if notifications == "allow":
                    notif_index = 1
                else:
                    notif_index = 2
                prefs = {"profile.default_content_setting_values.notifications": notif_index}
            else:
                prefs = {"profile.default_content_setting_values.notifications": 2}
            options.add_experimental_option("prefs", prefs)

            # Part of JavaScript console.log modification
            service_args = []
            if self.console_log:
                service_args.append("--verbose")
                service_args.append("--log-path=" + self.console_log.name)

            testdriver = webdriver.Chrome(self._BROWSER_INFO[browser]['webdriver_path'],
                                          service_args=service_args,
                                          chrome_options=options)
            # testdriver = getattr(webdriver, browser.capitalize())(self._BROWSER_INFO[browser]['webdriver_path'],
            #                                                       chrome_options=options)
        testdriver.implicitly_wait(self._DEFAULT_TIMEOUT)
        return testdriver
