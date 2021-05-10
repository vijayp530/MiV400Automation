"""
Description: AssertElement module contains methods to verify basic functionality of web applications
"""
__author__ = "Vinay HA"

import sys
import os
import time
import re

# STAF modules
sys.path.append("../log")
from .log import log


class AssertElement():
    '''
    AssertElement class contains methods to verify web elements in the application
    '''

    def __init__(self, browser):
        self._browser = browser

    def element_should_contain_text(self, locator, expected):
        """Verifies element identified by `locator` contains text `expected`.

        It matches substring on the text of the element

        Key attributes for arbitrary elements are `id` and `name`
        """
        self.actual = self._get_text(locator)
        if not expected in self.actual:
            message = "Element '%s' should have contained text '%s' but "\
                          "its text was '%s'." % (locator, expected, self.actual)
            log.mjLog.LogReporter("AssertElement","error",message)
            raise AssertionError(message)
        log.mjLog.LogReporter("AssertElement","debug","Element '%s' contains text '%s'" %(locator, expected))
        
    def element_should_not_contain_text(self, locator, expected):
        """Verifies element identified by `locator` does not contains text `expected`.

        It matches substring on the text of the element
        """
        self.actual = self._get_text(locator)
        if expected in self.actual:
            message = "Element '%s' should not have contained text '%s' but "\
                          "it does." % (locator, expected)
            log.mjLog.LogReporter("AssertElement","error",message)
            raise AssertionError(message)
        log.mjLog.LogReporter("AssertElement","debug","Element '%s' contains text '%s'" %(locator, expected))

    def values_should_be_equal(self, actualValue, expectedValue):
        """Verifies that actualValue is equal to expectedValue
        """
        if actualValue != expectedValue:
            raise AssertionError("Actual value and Expected Values are not equal")
        log.mjLog.LogReporter("AssertElement","debug"," Actual value is equal to Expected Value")        

    def frame_should_contain_text(self, locator, text):
        """Verifies frame identified by `locator` contains `text`.
        """
        if not self._frame_contains(locator, text):
            raise AssertionError("Frame should have contained text '%s' "
                                 "but did not" % text)
        log.mjLog.LogReporter("AssertElement","debug","Frame '%s' contains text '%s'" %(locator, text))

    def page_should_contain_text(self, text):
        """Verifies that current page contains `text`.
        """
        if not self._page_contains(text):
            raise AssertionError("Page should have contained text '%s' "
                                 "but did not" % text)
        log.mjLog.LogReporter("AssertElement","debug","Page contains text '%s'" %( text))

    def page_should_contain_element(self, locator):
        """Verifies element identified by `locator` is found on the current page.
        """
        if not self._page_should_contain_element(locator):
            message = "Page should have contained %s but did not"\
                           % (locator)
            raise AssertionError(message)
        log.mjLog.LogReporter("AssertElement","debug","Current page contains element %s" % (locator))


    def page_should_not_contain_text(self, text):
        """Verifies the current page does not contain `text`.

        """
        if self._page_contains(text):
            raise AssertionError("Page should have not contained text '%s' "
                                 "but it did " % text)
        log.mjLog.LogReporter("AssertElement","debug","Page does not contains text '%s'" %( text))

    def page_should_not_contain_element(self, locator):
        """Verifies element identified by `locator` is not found on the current page.

        """
        if self._page_should_contain_element(locator):
            message = "Page should have not contained %s but did not"\
                           % (locator)
            raise AssertionError(message)
        log.mjLog.LogReporter("AssertElement","debug","Current page does not contains %s" % (locator))
        
    def element_should_be_disabled(self, locator):
        """Verifies that element identified with `locator` is disabled.

        """
        if self._is_enabled(locator):
            raise AssertionError("Element '%s' is enabled." % (locator))
        log.mjLog.LogReporter("AssertElement","debug","Element is disabled as expected - %s" % (locator))

    def element_should_be_disabled_1(self, locator):
        """Verifies that element identified with `locator` is disabled by searching disabled in the class attribute of the element.

        """
        if not self._is_disabled(locator):
            raise AssertionError("Element '%s' is enabled." % (locator))
        log.mjLog.LogReporter("AssertElement","debug","Element is disabled as expected - %s" % (locator))

    def element_should_be_enabled(self, locator):
        """Verifies that element identified with `locator` is enabled.

        """
        if not self._is_enabled(locator):
            raise AssertionError("Element '%s' is disabled." % (locator))
        log.mjLog.LogReporter("AssertElement","debug","Element is enabled as expected - %s" % (locator))

    def element_should_be_displayed(self, locator):
        """Verifies that the element identified by `locator` is displayed.

        Herein, displayed means that the element is logically visible, not optically
        visible in the current browser viewport. For example, an element that carries
        display:none is not logically visible, so using this keyword on that element
        would fail.

        """
        self.visible = self._is_visible(locator)
        if not self.visible:
            message = "The element '%s' should be visible, but it "\
                          "is not." % locator
            raise AssertionError(message)
        log.mjLog.LogReporter("AssertElement","debug","Element is displayed as expected - %s" % (locator))

    def element_should_not_be_displayed(self, locator):
        """Verifies that the element identified by `locator` is NOT displayed.

        This is the opposite of `element_should_be_displayed`.

        """
        self.visible = self._browser.elements_finder(locator)
        if len(self.visible)>0:
            message = "The element '%s' should not be visible, "\
                          "but it is." % locator
            raise AssertionError(message)
        log.mjLog.LogReporter("AssertElement","debug","Element is not displayed as expected - %s" % (locator))

    def element_should_be_selected(self, locator):
        """Verifies element identified by `locator` is selected/checked.

        """
        self.element = self._element_finder(locator)
        if not self.element.is_selected():
            raise AssertionError("Element '%s' should have been selected "
                                 "but was not" % locator)
        log.mjLog.LogReporter("AssertElement","debug","Element is selected as expected - %s" % (locator))

    def element_should_not_be_selected(self, locator):
        """Verifies element identified by `locator` is not selected/checked.
        """
        
        self.element = self._element_finder(locator)
        if self.element.is_selected():
            raise AssertionError("Element '%s' should not have been selected"
                                  % locator)
        log.mjLog.LogReporter("AssertElement","debug","Element is not selected as expected - %s" % (locator))

    def element_text_should_be_exact(self, locator, expected):
        """Verifies element identified by `locator` exactly contains text `expected`.

        In contrast to `element_should_contain_text`, this keyword does not try
        a substring match but an exact match on the element identified by `locator`.

        """
        log.mjLog.LogReporter("AssertElement","debug","Element should contains exact text: %s => %s" % (locator,expected))
        self.element = self._element_finder(locator)
        actual = self.element.text
        if expected != actual:
            message = "The text of element '%s' should have been '%s' but "\
                          "in fact it was '%s'." % (locator, expected, actual)
            raise AssertionError(message)
        log.mjLog.LogReporter("AssertElement","debug","Element contains exact text: %s => %s" % (locator,actual))

    def current_frame_contains_text(self, text):
        """Verifies that current frame contains `text`.

        """
        if not self._is_text_present(text):
            log.mjLog.LogReporter("AssertElement","error","Frame should have contained text '%s' "
                                 "but did not" % text)
            raise AssertionError("Frame should have contained text '%s' "
                                 "but did not" % text)
        log.mjLog.LogReporter("AssertElement","debug","Current Frame contains text '%s'." % text)
        

    def current_frame_should_not_contain_text(self, text):
        """Verifies that current frame contains `text`.


        """
        if self._is_text_present(text):
            log.mjLog.LogReporter("AssertElement","error","Frame should not have contained text '%s' "
                                 "but did contain" % text)
            raise AssertionError("Frame should not have contained text '%s' "
                                 "but it did" % text)
        log.mjLog.LogReporter("AssertElement","debug","Current Frame does not contains text '%s'." % text)

    def verify_element_color(self, locator, expectedColor):
        """
        Verifies element color
        """
        pass
    
    def verify_text_in_dropdown(self, textList, valueToVerify):
        ''' Verifies the value identified by valueToVerify is present in list identified by textList
        
        '''
        try:
            count = 0
            for text in textList:
                if text == valueToVerify:
                    count = count +1
                    log.mjLog.LogReporter("AssertElement", "info", "verify_text_in_dropdown"
                                          " - "+valueToVerify+" is present in list")
                    break
            if count == 0:
                log.mjLog.LogReporter("AssertElement", "error", "%s is not present in list" % valueToVerify)
            
        except:
            raise AssertionError("Error in verify_text_in_dropdown "+str(sys.exc_info()))

    def values_should_not_be_equal(self, actualValue, expectedValue):
        """Verifies that actualValue is not equal to expectedValue
        """
        if actualValue == expectedValue:
            raise AssertionError("Actual value and Expected Values are equal")
        log.mjLog.LogReporter("AssertElement","debug"," Actual value is not equal to Expected Value")

    def page_should_not_contain_javascript_errors(self):
        """
        `Description;`  Verifies the current page does not contain JavaScript errors.

        `Param:`  None

        `Returns:`  status - True/False

        `Created by:` Jim Wendt

        """
        error_recap = []
        keep_phrases = [
            '"description": "EvalError',
            '"description": "InternalError',
            '"description": "RangeError',
            '"description": "ReferenceError',
            '"description": "SyntaxError',
            '"description": "TypeError',
            '"description": "URIError',
            '"description": "ReferenceError',
            '"description": "DOMException'
        ]
        status = False
        if self._browser.console_log:
            for line in self._browser.console_log:
                for phrase in keep_phrases:
                    if phrase in line:
                        line = line.replace("\"description\": ", "")
                        line = line.replace("\\n", "").strip()
                        line = re.sub("\s+", " ", line)
                        line = line[1:-2]
                        if not line in error_recap:
                            error_recap.append(line)
            if len(error_recap):
                for line in error_recap:
                    log.mjLog.LogReporter("AssertElement", "error", line)
                log.mjLog.LogReporter("AssertElement", "error", "Page Contains JavaScript Errors")
                self._browser.console_log.truncate()
                raise AssertionError()
                return status
            else:
                status = True
                return status
        else:
            raise AssertionError("Unable to Validate Javascript Errors")
            log.mjLog.LogReporter("AssertElement", "debug", "Unable to Validate Javascript Errors")
            return status

 #private methods
    def _element_finder(self, locator):
        '''
        _element_finder() - Method to invoke element_finder from browser class
        '''
        return self._browser.element_finder(locator)
        
    def _get_browser_driver(self):
        return self._browser.get_current_browser()
    
    def _frame_contains(self, locator, text):
        self._driver = self._get_browser_driver()
        element = self._element_finder(locator)
        
        self._driver.switch_to_frame(element)
        found = self._is_text_present(text)
        self._driver.switch_to_default_content()
        return found

    def _get_text(self, locator):
        element = self._element_finder(locator)
        if element is not None:
            return element.text
        return None

    def _is_text_present(self, text):
        locator = "//*[contains(., '%s')]" % (text);
        return self._is_element_contains(locator)

    def _is_element_present(self, locator):
        return self._element_finder(locator)
    
    def _is_element_contains(self, locator):
        self._driver = self._browser.get_current_browser()
        return self._driver.find_elements_by_xpath(locator) 

    def _page_contains(self, text):
        self._driver = self._get_browser_driver()
        self._driver.switch_to_default_content()

        if self._is_text_present(text):
            return True

        subframes = self._element_finder("xpath=//frame|//iframe")
        if subframes:
            for frame in subframes:
                self._driver.switch_to_frame(frame)
                found_text = self._is_text_present(text)
                self._driver.switch_to_default_content()
                if found_text:
                    return True

        return False

    def _page_should_contain_element(self, locator):
        return self._is_element_present(locator)
    

    def _get_value(self, locator, tag=None):
        element = self._element_finder(locator, True, False, tag=tag)
        return element.get_attribute('value') if element is not None else None

    def _is_enabled(self, locator):
        element = self._element_finder(locator)
        if not element.is_enabled():
            return False
        read_only = element.get_attribute('readonly')
        if read_only == 'readonly' or read_only == 'true':
            return False
        return True

    def _is_disabled(self, locator):
        element = self._element_finder(locator)
        if "disabled" in element.get_attribute('class').lower():
            return True
        return False

    def _is_visible(self, locator):
        element = self._element_finder(locator)
        if element is not None:
            return element.is_displayed()
        return None

if __name__ == "__main__":
    params = {"name" : "Vinay"}
    myBrowser = Browser(params)
    myBrowser.go_to("http://google.com")
    Webaction = WebElementAction(myBrowser)
    Webaction.input_text("SearchButton","Vinay")
    Webaction.press_key("SearchButton","ENTER")
    AssertMethods = AssertElement(myBrowser)
    AssertMethods.page_should_contain_text("Indian film")
    print((1))
    AssertMethods.element_should_contain_text("SearchTools", "Search tools")
    print((2))
    AssertMethods.page_should_contain_element("SearchIcon")
    print((3))
    AssertMethods.page_should_not_contain_text("ShoreTel")
    print((4))
    AssertMethods.element_should_be_enabled("SearchTools")
    print((5))
   #AssertMethods.element_should_be_disabled("SearchIcon")
    AssertMethods.element_should_be_displayed("SearchIcon")
    #AssertMethods.page_should_not_contain_element("Mapper")
    print(("6 sec"))
    AssertMethods.element_text_should_be_exact("SearchTools", "Search tools")
    time.sleep(3)
    myBrowser.quit()
