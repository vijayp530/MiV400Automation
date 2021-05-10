"""
 Custom Expected Wait Conditions which are generally useful within web driver tests.
"""

__author__ = "nitin.kumar-2@mitel.com"

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchFrameException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoAlertPresentException




class length_of_drop_down_is(object):
    """An expectation for checking that a drop down element has a given number of elements.

    locator - used to find the element
    value - expected length of the drop down
    returns the WebElement once it has the particular length
    """
    def __init__(self, locator, value):
        self.locator = locator
        self.value = value

    def __call__(self, driver):
        element = _find_element(driver, self.locator)
        length = len(element.find_elements_by_tag_name('option'))
        print("length is %d" %length)
        if length > self.value:
            return element
        else:
            return False

class drop_down_has_option(object):
    """An expectation for checking that a drop down has a given option.

    locator - used to find the element
    value - expected option in the drop down elements/options
    returns the WebElement once it has the the expected option
    """
    def __init__(self, locator, value):
        self.locator = locator
        self.value = value

    def __call__(self, driver):
        element = _find_element(driver, self.locator)
        options = element.find_elements_by_tag_name('option')
        print(self.value)
        items = [n.text for n in options]
        if self.value in items:
            print("%s in %s" % (self.value,items))
            return element
        else:
            return False

class drop_down_has_option_which_contains(object):
    """An expectation for checking that a drop down has a given option.It will perform a partial match.

    locator - used to find the element
    value - expected string to be searched in the drop down options. e.g. "user" will match "user45678" and "user111" etc.
            first match will terminate the wait
    returns the WebElement once it has the the expected option
    """
    def __init__(self, locator, value):
        self.locator = locator
        self.value = value

    def __call__(self, driver):
        element = _find_element(driver, self.locator)
        options = element.find_elements_by_tag_name('option')
        items = [n.text for n in options]
        for option in items:
            if self.value in option:
                print("%s matches with %s" %(option,self.value))
                return element
        else:
            return False


def _find_element(driver, by):
    """Looks up an element. Logs and re-raises ``WebDriverException``
    if thrown."""
    try:
        return driver.find_element(*by)
    except NoSuchElementException as e:
        raise e
    except WebDriverException as e:
        raise e


def _find_elements(driver, by):
    try:
        return driver.find_elements(*by)
    except WebDriverException as e:
        raise e
