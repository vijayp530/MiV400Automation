"""
Module: Browser
File name: Browser.py
Description: Browser module contains methods to control & retrieve information from web Browsers
"""
__author__ = "Vinay HA"

# Selenium Modules
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from robot.api.logger import console, info

# Python Modules
import copy
import time
import sys
import os

# STAF Modules
from log import log

sys.path.append(os.path.join(os.path.dirname((os.path.dirname(os.path.dirname(__file__)))), "utils"))
from mapMgr import mapMgr

from selenium.common.exceptions import (
    NoSuchAttributeException,
    NoSuchElementException,
    NoSuchFrameException,
    NoSuchWindowException,
    StaleElementReferenceException,
    WebDriverException,
)


class Browser:
    """
        Base class for Web Automation uses python selenium Web Driver for this module
    """
    _DEFAULT_TIMEOUT = 15  # confirm with ROBOT expert
    # Below locators are required to use when the shadow root is returned after calling get_shadow_dom()
    # and a web element is
    # returned and below methods can be invoked on it.
    elem_locators = {
        "id": "find_elements_by_id",
        "accessibility": "find_element_by_accessibility_id",
        "name": "find_elements_by_name",
        "xpath": "find_elements_by_xpath",
        "tag": "find_elements_by_tag_name",
        "css_class": "find_elements_by_class_name",
        "text": "find_element_by_link_text",
        "css_selector": "find_elements_by_css_selector"
    }

    def __init__(self, params):
        '''
            Web Automation base class initiator which sets Default browser as Chrome
        '''
        if "server" in params.keys():
            self.server = params["server"]
        else:
            self.server = "localhost"

        log.setLogHandlers()
        self.componentType = params["component_type"].lower()

        self._browser = None

        self.browserName = self.get_browser(params)
        self._browser = self.get_driver_object(self.browserName, self.server, params)

        self.elements = {
            "id": self._browser.find_elements_by_id,
            "name": self._browser.find_elements_by_name,
            "xpath": self._browser.find_elements_by_xpath,
            "tag": self._browser.find_elements_by_tag_name,
            "css_class": self._browser.find_elements_by_class_name,
            "text": self._browser.find_element_by_link_text,
            "css_selector": self._browser.find_elements_by_css_selector
        }

        # Added below if condition to add new element finder methods only for mobility (ukumar: 27-Feb-2018)
        if "platformName" in params.keys() and params["platformName"].lower() in ('android', 'ios'):
            self.elements["accessibility"] = self._browser.find_element_by_accessibility_id
            self.elements["android_uiautomator"] = self._browser.find_element_by_android_uiautomator

        self._browser.implicitly_wait(10)

    def get_component_type(self):
        """
        Returns component type
        """
        return self.componentType

    def get_browser(self, params):
        """
        This method returns projects specific browser to use
        """
        try:
            default_browser_dict = {"manhattancomponent": DesiredCapabilities.CHROME,
                                    "highballcomponent": DesiredCapabilities.FIREFOX,
                                    "smcandroidcomponent": DesiredCapabilities.FIREFOX,
                                    "smcioscomponent": DesiredCapabilities.FIREFOX,
                                    "teamworkandroidcomponent": None,
                                    "smrcomponent": DesiredCapabilities.FIREFOX,
                                    "lyncupcomponent": DesiredCapabilities.FIREFOX,
                                    "cloudlinkcomponent": None
                                    }

            custom_browser_dict = {"chrome": DesiredCapabilities.CHROME, "firefox": DesiredCapabilities.FIREFOX,
                                   "ie": DesiredCapabilities.INTERNETEXPLORER}

            if params["component_type"].lower() == "webagentcomponent":
                if "browserName" in params.keys():
                    return custom_browser_dict[params["browserName"].lower()]
                else:
                    return DesiredCapabilities.FIREFOX
            elif params["component_type"].lower() == "manhattancomponent":
                return self.get_browser_caps_manhattan(custom_browser_dict, params)
            else:
                return default_browser_dict[params["component_type"].lower()]
        except:
            log.mjLog.LogReporter("Browser", "error", "Unable to assign browser name!")

    def get_browser_caps_manhattan(self, custom_browser_dict, params):
        """
        This method returns aut specific capabilities for Manhattan
        Extra Info: aut is Application Under Test (connect client or browser)
        """
        try:
            if params["aut"] == "connect_client":
                # options = webdriver.ChromeOptions()
                # options.binary_location = r'C:\NodeWebKit\ShoreTel.exe'
                # return options.to_capabilities()
                return custom_browser_dict[params["browserName"].lower()]
            else:
                if params["browserName"].lower() == "chrome":
                    return custom_browser_dict[params["browserName"].lower()]
                elif params["browserName"].lower() == "firefox":
                    return custom_browser_dict[params["browserName"].lower()]
                else:
                    # not yet implemented
                    pass
        except:
            log.mjLog.LogReporter("Browser", "error",
                                  "Unable to assign browser capabilities for manhattan application!")

    def get_driver_object(self, browserName, server, params):
        """
        This method returns driver object specific to projects
        """
        try:
            comp_type = params["component_type"].lower()
            self.browserName = browserName
            if comp_type == "lyncupcomponent":
                driverObject = webdriver.Remote(command_executor='http://' + server + ':' + params["port"],
                                                desired_capabilities={
                                                    "app": 'os.path.join(os.environ["ProgramFiles"], "Microsoft Office\\Office15\\lync.exe")'}
                                                )
            # added creating driver for teamwork android, smc ios on 30-Jan-2018 by Parasu
            elif (comp_type == "smcandroidcomponent") or (comp_type == "smcioscomponent") or (
                    comp_type == "teamworkandroidcomponent") or (comp_type == "cloudlinkcomponent"):
                appium = __import__("appium")
                driverObject = appium.webdriver.Remote('http://' + server + ':' + params["port"] + '/wd/hub', params)
            else:
                driverObject = webdriver.Remote(command_executor='http://' + server + ':' + params["port"] + '/wd/hub',
                                                desired_capabilities=self.browserName
                                                )
            return driverObject
        except:
            log.mjLog.LogReporter("Browser", "error", "Unable to create driver object! " + str(sys.exc_info()))

    def get_current_browser(self):
        return self._browser

    def get_locator(self, by):
        '''
        get_locator() will return element identifier object e.g. find_elements_by_id
        '''
        if by is None:
            log.mjLog.LogReporter("Browser", "error", "Attribute to identify element is empty")
            return None

        return self.elements[by.lower()]

    def go_to(self, url):
        '''
            go_to() method goes to the specific URL after the browser instance launches
        '''
        self._browser.get(url)

    def get_screenshot_as_file(self, screenshot_file):
        '''
            get_screenshot_as_file() - Gets the screenshot of the current window.
            Returns False if there is any IOError, else returns True.
             Use full paths in your filename.
        '''
        self._browser.get_screenshot_as_file(screenshot_file)

    def get_elements(self, By=None, ByValue=None, index=None):
        '''
            get_elements() api works for multiple web elements Identification
            on web pages
        '''
        try:
            self.By = By
            self.ByValue = ByValue
            if self.By is None or self.ByValue is None:
                log.mjLog.LogReporter("Browser", "error", "Element by and Element attribute value is empty")
                return None

            # Getting element identifier object
            self.elementObj = self.get_locator(self.By.lower())

            # Returning identified element
            self.elementObjList = self.elementObj(self.ByValue)
            if index is None:
                # print("Index is None, return all elements found")
                return self.elementObjList
            else:
                if index >= len(self.elementObjList):
                    # print("Element index is outside of number of elements found.")
                    log.mjLog.LogReporter("Browser", "error", "Element index is outside of number of elements found")
                    return None
                else:
                    # print("Returning elements at index %d" % index)
                    if (not self.elementObjList[index].is_displayed()) or (not self.elementObjList[index].is_enabled()):
                        log.mjLog.LogReporter("Browser", "error", "The element is found but is not enabled/visible.")
                        return None

                    return [self.elementObjList[index]]

        except (WebDriverException, NoSuchElementException) as e:
            log.mjLog.LogReporter("Browser", "error", "Browser.get_elements: Exception: %s" % str(e))

    def get_element(self, By=None, ByValue=None, index=None):
        '''
            get_element() api works for web element Identification
            on web pages uses get_elements() method and returns single
            element on call
        '''
        try:
            log.mjLog.LogReporter("Browser", "debug", "Browser.get_elements: By=%s, ByValue=%s" % (By, ByValue))
            if index is not None:
                self.elementRef = self.get_elements(By, ByValue, index)
            else:
                self.elementRef = self.get_elements(By, ByValue)

            if len(self.elementRef) == 0:
                raise Exception("0 elements found.")
            elif len(self.elementRef) > 1:
                log.mjLog.LogReporter("Browser", "warning",
                                      ">1 Elements found using : By=%s, ByValue=%s" % (By, ByValue))
                raise AssertionError(">1 element found")

            # elif (not self.elementRef[0].is_displayed()) or (not self.elementRef[0].is_enabled()):
            #     raise Exception("The element is found but is not enabled/visible.")

            else:
                log.mjLog.LogReporter("Browser", "debug", "Element identified: By=%s, ByValue=%s" % (By, ByValue))
                return self.elementRef[0]
        except (WebDriverException, NoSuchElementException) as e:
            import traceback
            raise AssertionError("Exception occured in element identification. Traceback: %s" % traceback.format_exc())

    def quit(self):
        '''
            Close the Browser
        '''
        try:
            self._browser.quit()
        except:
            import time
            time.sleep(2)
            try:
                self._browser.quit()
            except:
                log.mjLog.LogReporter("Browser", "error", "Webdriver was not able to close browser.")
                import traceback
                log.mjLog.LogReporter("Browser", "debug", " %s" % traceback.format_exc())

    def close(self):
        '''
        Close the current browser window
        '''
        try:
            self._browser.close()
        except:
            log.mjLog.LogReporter("Browser", "error", "Webdriver is not able to close corrent browser.")
            import traceback
            log.mjLog.LogReporter("Browser", "debug", " %s" % traceback.format_exc())

    def close_browser(self):
        '''
        Close the current browser window
        '''
        try:
            self._browser.close()
        except:
            import traceback
            log.mjLog.LogReporter("Browser", "error",
                                  "Error in closing current browser: " + str(traceback.format_exc()))

    def _map_converter(self, locator, replace_dict=None):
        '''
        map_converter() - Gets element attributes from map files
        Return dictionary
        '''
        # self.elementAttr = mapMgr.__getitem__(locator)
        self.elementAttr = copy.deepcopy(mapMgr.__getitem__(locator))
        if replace_dict:
            for key in replace_dict:
                xpath = self.elementAttr['BY_VALUE']
                r = '!'+key+'!'
                self.elementAttr['BY_VALUE'] = xpath.replace(r, str(replace_dict[key]))

        info(self.elementAttr)
        return self.elementAttr

    def validate_mapping(self, locator):
        '''
        Exposes the private _map_converter method for use in testing to validate a mapped locator
        return result of _map_converter method
        jim wendt
        '''
        return self._map_converter(locator)

    def waitfor_ajax_complete(self):
        '''
        Executes a jQuery JavaScript snippet that checks for active Ajax Requests
        return boolean of active requests
        jim wendt
        '''
        for x in range(100):
            if self._browser.execute_script("return window.jQuery != undefined && jQuery.active == 0"):
                return True
            time.sleep(.25)
            print("Waiting for AJAX to complete")
        return False

    def element_finder(self, locator, replace_dict=None):
        '''
        element_finder() - locates the element in the web application
        return element object
        '''
        try:
            if locator[0:2] == "//":
                self.elementAttr = {
                    "ELEMENT_TYPE": "unused placeholder",
                    "BY_TYPE": "xpath",
                    "BY_VALUE": locator
                }
            else:
                self.elementAttr = self._map_converter(locator, replace_dict)

            if self.elementAttr:
                if len(self.elementAttr.keys()) == 3:
                    self.element = self.get_element(By=self.elementAttr["BY_TYPE"],
                                                    ByValue=self.elementAttr["BY_VALUE"])
                elif len(self.elementAttr.keys()) == 4:
                    self.element = self.get_element(By=self.elementAttr["BY_TYPE"],
                                                    ByValue=self.elementAttr["BY_VALUE"],
                                                    index=self.elementAttr["INDEX"])
                else:
                    log.mjLog.LogReporter("WebUIOperation", "error",
                                          "Element property in map file are not proper  - %s" % (locator))
                    raise AssertionError("Element property in map file are not proper  - %s" % (locator))
                return self.element
            else:
                raise Exception("No element returned for provided locator <%s>"%locator)
        except:
            log.mjLog.LogReporter("Browser", "error",
                                  "element_finder - No or more than 1 element returned for provided locator" + str(sys.exc_info()))
            raise AssertionError("Browser- element_finder - No or more than 1 element returned for provided locator")

    def elements_finder(self, locator, replace_dict=None):
        '''
        elements_finder() - locates multiple elements in the web application
        return element object
        '''

        try:
            if locator[0:2] == "//":
                self.elementAttr = {
                    "ELEMENT_TYPE": "unused placeholder",
                    "BY_TYPE": "xpath",
                    "BY_VALUE": locator
                }
            else:
                self.elementAttr = self._map_converter(locator, replace_dict)

            if self.elementAttr:
                if len(self.elementAttr.keys()) == 3:
                    self.elementlist = self.get_elements(By=self.elementAttr["BY_TYPE"],
                                                         ByValue=self.elementAttr["BY_VALUE"])
                elif len(self.elementAttr.keys()) == 4:
                    self.elementlist = self.get_elements(By=self.elementAttr["BY_TYPE"],
                                                         ByValue=self.elementAttr["BY_VALUE"],
                                                         index=self.elementAttr["INDEX"])
                else:
                    log.mjLog.LogReporter("WebUIOperation", "error",
                                          "Element property in map file are not proper  - %s" % (locator))
                    raise AssertionError("Element property in map file are not proper  - %s" % (locator))
                return self.elementlist
            else:
                raise Exception("No element returned for provided locator <%s>" % locator)
        except:
            log.mjLog.LogReporter("Browser", "error",
                                  "elements_finder - No element returned for provided locator" + str(sys.exc_info()))
            raise AssertionError("Browser- elements_finder - No element returned for provided locator")

    def select_item_from_table(self, locator, Search_Item):
        try:
            self.varlist = self.elements_finder(locator)
            for item in self.varlist:
                name_list = item.text
                if Search_Item == name_list:
                    time.sleep(1)
                    item.click()
                break
        except:
            log.mjLog.LogReporter("Browser", "error", "Selecting item from table failed  - %s" % (locator))
            raise AssertionError("Selecting item from table failed  - %s" % (locator))

    def get_shadow_dom(self, element):
        """
        This function will return the shadow root of a web element
        :param element: a web element e.g. return of methods like find_elements_by_id() or find_elements_by_css_selector()
        :return: the shadow root which can then be use to find other web elements inside it

        e.g.
        root1 = driver.find_element_by_css_selector('some css')
        shadow_root1 = get_shadow_dom(root1)
        el = shadow_root1.find_element_by_css_selector('some other css')
        el.click()
        """
        shadow_root = self._browser.execute_script('return arguments[0].shadowRoot', element)
        return shadow_root


if __name__ == "__main__":
    browserDict = {"remote": "local"}
    driver = Browser(browserDict)
    driver.go_to("http://www.google.com")
    ElemntRef = driver.get_element(By="name", ByValue="q")
    ElemntRef.send_keys("Vinay")
    time.sleep(2)
    driver.quit()

