"""
Description: WebElementAction module contains methods to perform action on web applications
"""

__author__ = "Vinay HA"


from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 

import custom_expected_conditions as CEC

import sys
import os
import time
import inspect

from log import log
import datetime
from time import gmtime, strftime


class WebElementAction:
    '''
    Methods to perform web operations are implemented in this class
    '''
    def __init__(self, browser):
        self._browser = browser

    def click_element(self, locator, replace_dict=None, value=None, index=None):
        """Click element identified by `locator`.
        replace_dict: For dynamically changing the xpath
        value: If you have multiple elements identified by locator and you want to click on a
               particular element where some text is written, then pass value=text_on_element,
               it will match value with text written on the element and click on that.
        index : the index of the element to click. If you have multiple elements with same locator and an element at a particular
                index must be accessed, then this index parameter must be used. e.g. a web page having 5 save buttons with same locator
                (id, xpath etc.). In this case either 5 separate entries in map file should be made(using the last # e.g. #2,#3 etc) but this
                approach will make map file huge so, using this index param in this type of cases will be helpful.


        """
        # if a locator returns more than 1 element and no value to match is supplied
        if index is not None and not value:
            self.elements = self._elements_finder(locator, replace_dict)
            if self.elements:
                self.elements[index].click()
                log.mjLog.LogReporter("WebUIOperation", "debug", "Click operation \
                                    successful for locator %s at index %s with no value to match" % (locator, str(index)))
                # returning as the element has already been clicked
                return
        # if a locator returns more than 1 element and some value to match is supplied
        if value:
            self.elements = self._elements_finder(locator, replace_dict)
            elements = [] # to store elements which has value(passed from param)
            if self.elements:
                for i in self.elements:
                    match_text = i.text.strip()
                    if "\n" in match_text:
                        match_text = map(str.strip, match_text.split("\n"))
                    if value in match_text:
                        elements.append(i)
                # if a locator returns more than 1 element and some value to match is supplied along with some index
                if index is not None:
                    elements[index].click()
                    log.mjLog.LogReporter("WebUIOperation", "debug", "Click operation \
                                        successful for locator %s with value %s and index %s" % (locator, value, str(index)))
                else:
                    elements[0].click()
                    log.mjLog.LogReporter("WebUIOperation", "debug", "Click operation \
                                successful for locator %s with value %s and no index, so clicking the first occurrence" % (locator, value))
        else:
            self.element = self._element_finder(locator, replace_dict)
            if self.element:
                self.element.click()
                log.mjLog.LogReporter("WebUIOperation", "debug", "Click operation \
                                         successful- %s" % (locator))

    def input_text(self,locator, Text):
        """Types the given `text` into text field identified by `locator`.

        """
        self.element = self._element_finder(locator)
        if self.element:
            self.element.clear()
            self.element.send_keys(Text)
            log.mjLog.LogReporter("WebUIOperation","debug","Input_text operation \
                                    successful- %s" %(locator))
            
    def submit_form(self, locator):
        """Submits a form identified by `locator`.
        """
        self.element = self._element_finder(locator)
        if self.element:
            self.element.submit()

    def clear_input_text(self,locator):
        """
        clear the given text field identified by `locator`.
        """
        self.element = self._element_finder(locator)
        if self.element:
            self.element.clear()
            log.mjLog.LogReporter("WebUIOperation","debug","clear_input_text operation \
                                     successful- %s" %(locator))

    def select_checkbox(self, locator):
        """Selects checkbox identified by `locator`.

        Does nothing if checkbox is already selected. Key attributes for
        checkboxes are `id` and `name`.
        """
        self.element = self._element_finder(locator)
        if not self.element.is_selected():
            self.element.click()
            log.mjLog.LogReporter("WebUIOperation","debug","select_checkbox operation \
                                    successful- %s" %(locator))

    def unselect_checkbox(self, locator):
        """Un-selects checkbox identified by `locator`.

        Does nothing if checkbox is already un-selected. Key attributes for
        checkboxes are `id` and `name`.
        """
        self.element = self._element_finder(locator)
        if self.element.is_selected():
            self.element.click()
            log.mjLog.LogReporter("WebUIOperation","debug","unselect_checkbox operation \
                                    successful- %s" %(locator))

    def select_radio_button(self, locator):
        """Sets selection of radio button .

        The XPath used to locate the correct radio button then looks like this:
        //input[@type='radio' and @name='group_name' and (@value='value' or @id='value')]

        """
        self.element = self._element_finder(locator)
        if not self.element.is_selected():
            self.element.click()
            log.mjLog.LogReporter("WebUIOperation","debug","unselect_checkbox operation \
                                    successful- %s" %(locator))
    
    def execute_javascript(self, script_name):
        '''
          execute java script
        '''
        self._browser.get_current_browser().execute_script(script_name)
            
    def choose_file(self, locator, file_path):
        """Inputs the `file_path` into file input field found by `locator`.

        This keyword is most often used to input files into upload forms.
        The file specified with `file_path` must be available on the same host 
        where the Selenium is running.

        """
        if not os.path.isfile(file_path):
            log.mjLog.LogReporter("WebUIOperation","debug","choose_file - File '%s' does not exist on the \
                                    local file system" % file_path)
        self.element = self._element_finder(locator)
        if self.element:
            self.element.send_keys(file_path)
            log.mjLog.LogReporter("WebUIOperation","debug","choose_file - File '%s' selected" % file_path)

    def double_click_element(self, locator):
        """Double click element identified by `locator`.

        Key attributes for arbitrary elements are `id` and `name`
        """
        self.element = self._element_finder(locator)
        if self.element:
            ActionChains(self._browser.get_current_browser()).double_click(self.element).perform()
            log.mjLog.LogReporter("WebUIOperation","debug","double_click_element operation \
                                     successful- %s" %(locator))                
      
    def drag_and_drop(self, source, target):
        """Drags element identified with `source` which is a locator.

        Element can be moved on top of another element with `target`
        argument.

        `target` is a locator of the element where the dragged object is
        dropped.
        """
        self.source_ele = self._element_finder(source)
        self.target_ele = self._element_finder(target)
        
        if self.source_ele and self.target_ele:
            ActionChains(self._browser.get_current_browser()).drag_and_drop(self.source_ele, self.target_ele).perform()
            log.mjLog.LogReporter("WebUIOperation","debug","drag_and_drop operation \
                                    successful: %s -> %s" %(source, target))
                                    
    def drag_and_move(self, source, target):
        """Drags element identified with `source` which is a locator.
        Element can be moved on top of another element with `target`
        argument.
        `target` is a locator of the element where the dragged object is
        dropped.
        """
        self.source_ele = self._element_finder(source)
        self.target_ele = self._element_finder(target)
        
        if self.source_ele and self.target_ele:
          
            ActionChains(self._browser.get_current_browser()).click_and_hold(self.source_ele).move_to_element(self.target_ele).perform()

    def right_click(self, locator):
        '''Right Click on element identified by `locator`.

        Key attributes for arbitrary elements are `id` and `name`
        '''
        self.element = self._element_finder(locator)
        if self.element:
            ActionChains(self._browser.get_current_browser()).context_click(self.element).perform()
            log.mjLog.LogReporter("WebUIOperation", "debug", "right_click operation \
                                     successful- %s" % (locator))

    def explicit_wait(self, element, waittime=20, replace_dict=None, ec='visibility_of_element_located', msg=None, msg_to_verify=None, condition_category="until"):
        """
        explicit_wait() is used to wait until element is displayed & enabled
        element: the web element
        waittime: max time to wait
        replace_dict: to replace variables in the value in map file. Refer _map_converter function in browser.py for more info
        ec: expected condition to wait on
        msg: msg to be validated irrespective of the element e.g. title_is or title_contains
        msg_to_verify: msg to be validated on a web element e.g. text_to_be_present_in_element
        condition_category = category of conditions to verify with until being default. To make the condition checking to until_not pass this
        parameter as until_not while calling this function. Example below

        e.g.
        For a map file entry as below
        comp_name==span#xpath#//*[@id="companyName"]

        some example calls to this function could be
        r = self.action_ele.explicit_wait("comp_name")
        r = self.action_ele.explicit_wait("comp_name",ec="title_contains",msg="Account") # "comp_name" i.e. element is not required
        in this call but it is required as it is a mandatory argument. It is this way to make this function backward compatible
        r = self.action_ele.explicit_wait("comp_name", ec="text_to_be_present_in_element", msg_to_verify="M5Portal Company")

        There are some custom expected conditions as well. They are implemented in the custom_expected_conditions.py file.
        Some of the custom wats are length_of_drop_down_is,drop_down_has_option etc.

        Example usage is given below:
        # to wait till the length of drop down grows more than 5
        mydrop_down = self.action_ele.explicit_wait('Peopleselect_dropbox', ec="length_of_drop_down_is", msg_to_verify=5)
        # to wait till the given drop down has an option "ff ll"
        mydrop_down = self.action_ele.explicit_wait('Peopleselect_dropbox', ec="drop_down_has_option", msg_to_verify="ff ll")
        self.action_ele.explicit_wait('SwitchAcc_ok', ec="visibility_of_element_located",condition_category="until_not")
        """
        if element[0:2] == "//":
            self.elementAttr = {
                "ELEMENT_TYPE": "unused placeholder",
                "BY_TYPE": "xpath",
                "BY_VALUE": element
            }
        else:
            self.elementAttr = self._browser._map_converter(element, replace_dict)

        if 'not' in condition_category:
            wait = WebDriverWait(self._browser.get_current_browser(), waittime).until_not
            error_msg = "The element <%s> can still be located after explicit wait." % element
        else:
            wait = WebDriverWait(self._browser.get_current_browser(), waittime).until
            error_msg = "Could not locate element <%s> during explicit wait." % element
        result = None
        try:
            condition = getattr(EC, ec)
        except AttributeError as e:
            condition = getattr(CEC, ec)
        locator = getattr(By, self.elementAttr['BY_TYPE'].upper())
        try:
            if msg:
                result = wait(condition(msg))
            elif msg is None and msg_to_verify is None:
                result = wait(condition((locator, self.elementAttr["BY_VALUE"])))
            elif msg_to_verify:
                result = wait(condition((locator, self.elementAttr["BY_VALUE"]), msg_to_verify))
        except Exception as e:
            raise Exception(error_msg + str(e))

        return result

    def focus(self, locator):
        """Sets focus to element identified by `locator`."""
        
        self.element = self._element_finder(locator)
        self._current_browser().execute_script("arguments[0].focus();", self.element)
        log.mjLog.LogReporter("WebUIOperation","debug","focus operation successful: %s" %(locator))
        
    def alert_action(self, Cancel= False):
        """Dismisses currently shown alert dialog and returns it's message.

        By default, this keyword chooses 'OK' option from the dialog. If
        'Cancel' needs to be chosen, set keyword ` Cancel = True'
        """
        self.text = self._alert(Cancel)
        log.mjLog.LogReporter("WebUIOperation","debug","alert_action successful:Text => %s" %(self.text))
        return self.text
        
    def press_key(self, locator, key):
        """Simulates user pressing key on element identified by `locator`.

        `key` is a single character.

        Examples:
        press_key ("GoogleSearch", "BACKSPACE")
        """
        if len(key) < 1:
            log.mjLog.LogReporter("WebUIOperation","error","press_key - Key value \
                                    not present  - %s" %(key))
            return None
        keydict = self._map_ascii_key_code_to_key(key)
        #if len(key) > 1:
        #    raise ValueError("Key value '%s' is invalid.", key)
        self.element = self._element_finder(locator)
        #select it
        if self.element:
            self.element.send_keys(keydict)
            log.mjLog.LogReporter("WebUIOperation","debug","press_key - Key %s sent \
                                    successfully " %(key))
    
    def mouse_hover(self, locator):
        '''Mouse hover on element identified by `locator`.

        Key attributes for arbitrary elements are `id` and `name`
        '''
        self.element = self._element_finder(locator)
        if self.element:
            ActionChains(self._browser.get_current_browser()).move_to_element(self.element).perform()
            log.mjLog.LogReporter("WebUIOperation","debug","mouse_hover operation \
                                     successful- %s" %(locator))
    def switch_to_frame(self,frameno):
        '''
          switch to frame('frameno') 
        '''
        self.framelist=self._browser.elements_finder("UCB_Frame")
        self.browserdriver=self._browser.get_current_browser()
        self.browserdriver.switch_to_frame(self.framelist[frameno])

    def select_from_dropdown_using_text(self,locator,itemtext):
        ''' Selecting item from dropdownlist by using the option itemtext
        
        '''
        selectionlist=self._element_finder(locator)
        for option in selectionlist.find_elements_by_tag_name('option'):
            if option.text.strip() == itemtext :
                option.click()
                log.mjLog.LogReporter("WebUIOperation","debug","select_form_dropdown using text \
                                    successful- %s" %(itemtext))

    def select_from_dropdown_using_index(self,locator,itemindex):
        ''' Selecting item from dropdownlist by using the option itemindex
        
        '''
        selectionlist=self._element_finder(locator)
        sel = Select(selectionlist)
        for option in selectionlist.find_elements_by_tag_name('option'):
            if option.get_attribute("index") == str(itemindex):
                #self._setSelected(option)
                sel.select_by_index(itemindex)
                log.mjLog.LogReporter("WebUIOperation","debug","select_form_dropdown using index \
                                    successful- %s" %(itemindex))

    def select_list_item_using_text(self,locator,itemtext):
        '''
           select item from list by using itemtext
        '''
        # below change is to take care of new dropdown implementation
        selectlist=self._browser.elements_finder(locator)
        for item in selectlist:
            if item.text==itemtext:
                item.click()
                log.mjLog.LogReporter("WebUIOperation","debug","select_list_item form list \
                                    successful- %s" %(itemtext))
                break

    def select_list_item_using_index(self,locator,itemindex):
        '''
         select item from list by using itemindex
        '''
        selectlist=self._element_finder(locator)
        for item in selectlist:
            if item[index]==itemindex:
                item[index].click()
                log.mjLog.LogReporter("WebUIOperation","debug","select_list_item form list \
                                    successful- %s" %(itemindex))
    
    def close_window(self):
        '''
          closes the current window
        '''
        self.browserdriver = self._browser.get_current_browser()
        self.browserdriver.close()
        self.window_list = self.browserdriver.window_handles


    def switch_to_window(self,window):
        '''
          switch to window('window')  or
          can be used to switch to a tab
          switch_to_window(1)
          switch_to_window(2)

          the index number is the index of tab based on the order of tab opening

        '''
        self.browserdriver = self._browser.get_current_browser()
        self.window_list = self.browserdriver.window_handles
        self.browserdriver.switch_to.window(self.window_list[window])
    
    
    def scroll(self, locator, position=1000):
        '''Scrolls from top to desired position at bottom
           locator is the id or class of scroll bar not exactly xpath
           position is the value of the place till where you want to scroll
           pass position=0 for scrolling from bottom to top
        '''
        self.xpath = self._browser._map_converter(locator)["BY_VALUE"]
        self.type = self._browser._map_converter(locator)["ELEMENT_TYPE"]
        if self.type == "id" :
            scriptName = "$(document).ready(function(){$('#"+self.xpath+"').scrollTop("+str(position)+");});"
            self._browser.get_current_browser().execute_script(scriptName)
        else:
            scriptName = "$(document).ready(function(){$('."+self.xpath+"').scrollTop("+str(position)+");});"
            self._browser.get_current_browser().execute_script(scriptName)
    
    def input_text_basic(self, locator, text):
        """sets the given 'text' into the field identified by 'locator'
           extra info: This method performs operation on HTML element called time
           Eg: if you want to set time then pass the time parameter in form of 'hhmm'
        """
        self.element = self._element_finder(locator)
        if self.element:
            self.element.send_keys(text)
            log.mjLog.LogReporter("WebUIOperation","debug","input_text_basic operation successful- %s" %(locator))

    def window_handles_count(self):
        '''
          Get window handles count 
        '''
        self.browserdriver=self._browser.get_current_browser()
        self.window_list = self.browserdriver.window_handles
        return len(self.window_list)

    def check_checkbox(self, locator):
        """Checks if checkbox identified by `locator` is selected or unselected
        """
        self.element = self._element_finder(locator)
        if self.element.is_selected():
            log.mjLog.LogReporter("WebUIOperation","debug","check_checkbox operation successful- %s" %(locator))
            return True
        else:
            return False

    def clear_input_text_new(self,locator):
        """
        clear the given text field identified by `locator`.
        clear_input_text() does not work if text is right aligned,this new api works.

        """
        self.element = self._element_finder(locator)
        if self.element:
            self.element.send_keys(Keys.CONTROL + "a")
            self.element.send_keys(Keys.DELETE)
            log.mjLog.LogReporter("WebUIOperation","debug","clear_input_text operation \
                                         successful- %s" %(locator))

    def maximize_browser_window(self):
        """Maximizes the currently opened browser window
        """
        self._current_browser().maximize_window()
        log.mjLog.LogReporter("WebUIOperation","debug","maximize_browser_window - operation successfull")
        
    def minimize_browser_window(self):
        """minimizes the currently opened browser window
        """
        self._current_browser().set_window_position(-2000, 0)
        log.mjLog.LogReporter("WebUIOperation","debug","minimize_browser_window - operation successfull")


    def takeScreenshot(self, funcName, location=None):
        """
        Method to save screen shot to a given path with the function name
        :param funcName: Function name
        :param location: is an optional parameter.If present, the provided location will be used for saving the screen shot
        :return: None
        """
        # trying to figure out the report location
        if location is None:
            for frame in inspect.stack():
                if "page" in frame[1] and "Component" in frame[1]:
                    feature_file = frame[1]
                    location = feature_file.split("page")[0]
                    break
                elif "lib" in frame[1] and "Component" in frame[1]:
                    feature_file = frame[1]
                    location = feature_file.split("lib")[0]
                    break
            else:
                # falling back to framework location
                location = os.path.dirname(os.path.dirname(__file__))
        path = location+"\\reports\\report_"+str(datetime.datetime.now().date())+os.sep
        try:
            if not os.path.exists(path):
                print("Report path not found.Creating...")
                os.makedirs(path)
            name = path+funcName+str(datetime.datetime.now().time()).replace(":","_")+".png"
            print(name)
            self._browser.get_screenshot_as_file(name)
        except Exception as e:
            print(e)

    def sg_get_rows(self, locator):
        """
        returns all the visible rows in a slick grid.

        """
        slick_grid = self._element_finder(locator)
        grid_data = []
        row_data = []
        if self.element:
            rows = slick_grid.find_elements_by_class_name("slick-row")
            for row in rows:
                cells = row.find_elements_by_class_name("slick-cell")
                for cell in cells:
                    row_data.append(cell.text)
                grid_data.append(row_data)
                row_data = []
            log.mjLog.LogReporter("WebUIOperation","debug","sg_get_rows operation \
                                         successful- %s" %(locator))
            return grid_data

    def sg_select_row_containing_text(self, locator, text, all=False):
        """
        text : select a row by clicking on its check box if it has a given text in any of its cells
        all : if true, all rows containing the given text will be selected

        """
        slick_grid = self._element_finder(locator)
        selected = False
        if self.element:
            rows = slick_grid.find_elements_by_class_name("slick-row")
            for row in rows:
                cells = row.find_elements_by_class_name("slick-cell")
                for cell in cells:
                    if cell.text == text:
                        cells[0].click()
                        log.mjLog.LogReporter("WebUIOperation", "debug", "sg_select_row_containing_text operation \
                                                                 successful- %s" % (locator))
                        selected = True
                        break
                if selected and not all:
                    break
            if not selected:
                log.mjLog.LogReporter("WebUIOperation", "error", "sg_select_row_containing_text operation \
                                                         unsuccessful- %s" % (locator))

    def sg_select_rows_by_index(self, locator, indexes):
        """
        indexes : list of row index to be selected

        """
        slick_grid = self._element_finder(locator)
        if self.element:
            rows = slick_grid.find_elements_by_class_name("slick-row")
            for index in indexes:
                rows[index].find_elements_by_class_name("slick-cell")[0].click()
                log.mjLog.LogReporter("WebUIOperation", "debug", "sg_select_row_by_index operation successful for index %d" % (index))

    def sg_get_grid_columns_header(self, locator):
        """
        locator : locator for the slick grid

        """
        slick_grid = self._element_finder(locator)
        if self.element:
            headers = slick_grid.find_elements_by_class_name("slick-column-name")
            names = [x.get_attribute('title') for x in headers]
            if len(names):
                log.mjLog.LogReporter("WebUIOperation", "debug", "sg_get_grid_columns_header operation successful")
                return names
            return False


# Private method
    def _element_finder(self, locator, replace_dict=None):
        '''
        _element_finder() - Method to invoke element_finder from browser class
        '''
        return self._browser.element_finder(locator, replace_dict)

    def _elements_finder(self, locator, replace_dict=None):
        '''
        _elements_finder() - Method to invoke elements_finder from browser class
        '''
        return self._browser.elements_finder(locator, replace_dict)
    
    def _map_ascii_key_code_to_key(self, key_code):
        map = {
            "NULL": Keys.NULL,
            "BACKSPACE": Keys.BACK_SPACE,
            "TAB": Keys.TAB,
            "RETURN": Keys.RETURN,
            "ENTER": Keys.ENTER,
            "CANCEL": Keys.CANCEL,
            "ESCAPE": Keys.ESCAPE,
            "SPACE": Keys.SPACE,
            "MULTIPLY": Keys.MULTIPLY,
            "ADD": Keys.ADD,
            "SUBTRACT": Keys.SUBTRACT,
            "DECIMAL": Keys.DECIMAL,
            "DIVIDE": Keys.DIVIDE,
            "SEMICOLON": Keys.SEMICOLON,
            "EQUALS": Keys.EQUALS,
            "SHIFT": Keys.SHIFT,
            "ARROW_UP": Keys.ARROW_UP,
            "ARROW_DOWN": Keys.ARROW_DOWN,
            "ARROW_LEFT": Keys.ARROW_LEFT,
            "ARROW_RIGHT": Keys.ARROW_RIGHT,
            "INSERT": Keys.INSERT,
            "DELETE": Keys.DELETE,
            "END": Keys.END,
            "HOME": Keys.HOME,
            "F12": Keys.F12,
            "ALT": Keys.ALT

        }
        key = map.get(key_code)
        if key is None:
            log.mjLog.LogReporter("WebUIOperation","info","Key not present, returning same string - %s" %(key_code))
            key = chr(key_code)
        return key

    def _alert(self, Cancel=False):
        alert = None
        try:
            
            alert = self._browser.get_current_browser().switch_to_alert()
            text = ' '.join(alert.text.splitlines()) # collapse new lines chars
            if Cancel: alert.dismiss()
            else: alert.accept()
            return text
        except WebDriverException:
            log.mjLog.LogReporter("WebUIOperation","info","Alert not present" )
            return None

    def _current_browser(self):
        return self._browser.get_current_browser()
                
    def _get_list_item_using_text(self, locator, itemtext):
        selectlist=self._element_finder(locator)
        print(selectlist)
        for item in selectlist:
            print(item.text)
            if item.text==itemtext:
                return item
            
    def _get_parent_obj(self, obj):
        return obj.find_element_by_xpath('..')
                


if __name__ == "__main__":
    params = {"name" : "Vinay"}
    myBrowser = Browser(params)
    myBrowser.go_to("http://google.com")
    Webaction = WebElementAction(myBrowser)
    Webaction.input_text("SearchButton","Vinay")
    Webaction.submit_form("SearchButton")
    #Webaction.press_key("SearchButton","ENTER")
    time.sleep(3)
    myBrowser.quit()
    
