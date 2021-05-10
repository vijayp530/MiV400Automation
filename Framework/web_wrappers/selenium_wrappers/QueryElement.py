"""
Description: QueryElement module contains methods to retrieve basic information of web applications
"""

__author__ = "Vinay HA"

#Python modules
import sys
import re
from cgitb import text

#STAF Modules
sys.path.append("../log")
from log import log


class QueryElement():
    '''
    Query class contains methods to query elements details from web application
    '''

    def __init__(self, browser):
        self._browser = browser

    
    def verify_element_visible_and_enabled(self, locator):
        """Checks that the element is visible and enabled 
         identified by `locator`.
        """
        if self._is_visible(locator) and self._is_enabled(locator):
            return True
        raise AssertionError("Verify_element_visible_and_enabled failed for '%s'" % (locator))
                
    def verify_element_visible_and_disabled(self, locator):
        """Checks that the element is visible but disabled 
         identified by `locator`.
        """
        if self._is_visible(locator) and not self._is_enabled(locator):
            return True
        raise AssertionError("Verify_element_visible_and_disabled failed for '%s'" % (locator))
        
    def verify_checkbox(self, locator):
        """Checks the status of checkbox identified by `locator`
         whether it is selected or not.
        """
        self.element = self._element_finder(locator)
        if self.element.is_selected():
            log.mjLog.LogReporter("WebUIOperation","debug","verify_checkbox verified \
                                    successfully- %s" %(locator))
            return True
        else:
            log.mjLog.LogReporter("WebUIOperation","debug","verify_checkbox verified \
                                    successful- %s" %(locator))
            return False
    
    def get_element_attribute(self, locator, attribute):
        """Return value of element attribute.
        """
        return self._get_attribute(locator,attribute)
      

    def get_horizontal_position(self, locator):
        """Returns horizontal position of element identified by `locator`.
        """
        self.element = self._element_finder(locator)
        if self.element is None:
            raise AssertionError("Could not determine horizontal position for '%s'" % (locator))
        return self.element.location['x']


    def get_value(self, locator):
        """Returns the value attribute of element identified by `locator`.
        """
        return self._get_attribute(locator, "value")

    def get_text(self, locator):
        """Returns the text value of element identified by `locator`.
        """
        return self._get_text(locator)
        
    def get_value_execute_javascript(self, script_name):
        '''
          execute java script and get return value
        '''
        return self._browser.get_current_browser().execute_script("return "+script_name)

    def get_vertical_position(self, locator):
        """Returns vertical position of element identified by `locator`.

        The position is returned in pixels offset the top of the page,
        as an integer. Fails if a matching element is not found.

        See also `get_horizontal_position`.
        """
        element = self._element_finder(locator)
        if element is None:
            raise AssertionError("Could not determine position for '%s'" % (locator))
        return element.location['y']
    
    def get_color(self, locator):
        """
            returns color of the object
        """
        self.element = self._element_finder(locator)
        rgb = self.element.value_of_css_property("background-color")
        r,g,b = map(int, re.search(r'rgba\((\d+),\s*(\d+),\s*(\d+).*', rgb).groups())
        hex_color = '#%02x%02x%02x' % (r, g, b)
            
        if "#09cf94" in hex_color:
            return "green"
        elif "#ffd500" in hex_color:
            return "yellow"
        elif "#ff5550" in hex_color:
            return "red"
        elif "#d9d9d9" in hex_color:
            return "gray"
        elif "#F49300":
            return "orange"
        else:
            raise AssertionError("Error in finding color, verify that it is an HTML color")
    
    
#private method
    def _element_finder(self, locator, replace_dict=None):
        '''
        _element_finder() - Method to invoke element_finder from browser class
        '''
        return self._browser.element_finder(locator, replace_dict)
    
    def _get_attribute(self, locator, attribute):
        self.element = self._element_finder(locator)
        if self.element:
            self._actualattrib = self.element.get_attribute(attribute)
            log.mjLog.LogReporter("Query","debug","Element %s has attribute %s" % (locator, self._actualattrib))
            return self._actualattrib
    
    def _get_text(self, locator):
        element = self._element_finder(locator)
        if element is not None:
            return element.text
        return None

    def element_displayed(self, locator, replace_dict=None):
        """Verifies that the element identified by `locator` is displayed.

        Herein, displayed means that the element is logically visible, not optically
        visible in the current browser viewport. For example, an element that carries
        display:none is not logically visible, so using this keyword on that element
        would fail.

        """
        return self._is_visible(locator, replace_dict)


    def _is_visible(self, locator, replace_dict=None):
        try:
            element = self._element_finder(locator, replace_dict)
            if element is not None:
                return element.is_displayed()
            return False
        except:
            return False

    def _is_enabled(self,locator):
        element=self._element_finder(locator)
        if element is not None:
            return element.is_enabled()
        return None

    def _get_selected_option_from_dropdown(self, locator):
        dropDown = self._element_finder(locator)
        if dropDown is not None:
            optionList = dropDown.find_elements_by_tag_name('option')
            for option in optionList:
                if option.is_selected():
                    return option

    def get_table_cell_data(self,locator, row, col):
        """Returns cell data of a table using row & col number.
        your xpath for table should be something like : //form[2]/table/tbody

        """
        try:
            self.table = self._element_finder(locator)
            if self.table:
                self.rowlist = self.table.find_elements_by_tag_name('tr')
                log.mjLog.LogReporter("Query","info","get_table_cell_data - Total row count %s " % (str(len(self.rowlist))))
                print("1st log")
                #check row count                
                if (len(self.rowlist)< row ):
                    log.mjLog.LogReporter("Query","error","get_table_cell_data - Expected row no %s " \
                                          "total no of rows in table %s" % (str(row), str(len(self.rowlist))))
                    raise AssertionError("Expected row no is not present in table")
                
                #get coloumn list
                self.expectedrow = self.rowlist[row]
                self.colList = self.expectedrow.find_elements_by_tag_name('td')
                log.mjLog.LogReporter("Query","info","get_table_cell_data - Total col count %s " % (str(len(self.colList))))
                
                #check col count
                if (len(self.colList)< col ):
                    log.mjLog.LogReporter("Query","error","get_table_cell_data - Expected" \
                                          "col no %s total no of cols in table %s" % (str(col), str(len(self.colList))))
                    raise AssertionError("Expected row no is not present in table")
                
                log.mjLog.LogReporter("Query","info","get_table_cell_data - expected cell " \
                                      "data -  %s " % (str(self.colList[col].text)))
                return self.colList[col].text
        except:
            raise AssertionError("Error in get_table_cell_data - Check table xpath" \
                                 "or row count or col count")
        
    def get_table_cell_data_using_primaryId_modified(self,locator, primaryCol, primaryId, elementCol, looseSearch=False):
        """Returns cell data of a table using primary Id  & element col number.
        PrimaryID is the text that we are using to search the row 
        primaryCol is the coloumn where PrimaryId is located
        your xpath for table should be something like : //form[2]/table/tbody
        
        e.g. get_table_cell_data_using_primaryId("TenantTable",1,"PaxshoreTxt1",6)

        """
        try:
            self.flag = 0
            self.table = self._element_finder(locator)
            if self.table:
                for row in self.table.find_elements_by_tag_name('tr'):
                    self.colList = row.find_elements_by_tag_name('td')
                    if (len(self.colList) > primaryCol ):
                        if looseSearch==False:
                            if self.colList[primaryCol].text == primaryId:
                                self.flag=1
                                break
                        else:
                            if primaryId in self.colList[primaryCol].text:
                                self.flag=1
                                break
                if self.flag:
                    if (len(self.colList) >= elementCol ):
                        log.mjLog.LogReporter("Query","info","get_table_cell_data_using_primaryId -" \
                                              "expected cell data -  %s " % (str(self.colList[elementCol].text)))
                        
                        return self.colList[elementCol].text
                    else:
                        log.mjLog.LogReporter("Query","error","get_table_cell_data_using_primaryId" \
                                              "- Expected element col  %s is not found in the table" % (str(elementCol)))
                        raise AssertionError("Expected primary Id is not present in table")
                else:             
                    log.mjLog.LogReporter("Query","error","get_table_cell_data_using_primaryId" \
                                          "- Expected primaryID %s is not found in the table" % (primaryId))
                    raise AssertionError("Expected primary Id is not present in table")

        except Exception as inst :
            if str(inst) == 'The element is found but is not enabled/visible.':
                log.mjLog.LogReporter("Query","info","get_table_cell_data_using_primaryId -" \
                                              "expected cell data" )
                return False
            else:
                raise AssertionError("Error in get_table_cell_data_using_primaryId" \
                                  "- Check table xpath or primaryID or element col no")
    
    def get_table_cell_data_using_primaryId(self,locator, primaryCol, primaryId, elementCol, looseSearch=False):
        """Returns cell data of a table using primary Id  & element col number.
        PrimaryID is the text that we are using to search the row 
        primaryCol is the coloumn where PrimaryId is located
        your xpath for table should be something like : //form[2]/table/tbody
        
        e.g. get_table_cell_data_using_primaryId("TenantTable",1,"PaxshoreTxt1",6)

        """
        try:
            self.flag = 0
            self.table = self._element_finder(locator)
            if self.table:
                for row in self.table.find_elements_by_tag_name('tr'):
                    self.colList = row.find_elements_by_tag_name('td')
                    if (len(self.colList) > primaryCol ):
                        if looseSearch==False:
                            if self.colList[primaryCol].text == primaryId:
                                self.flag=1
                                break
                        else:
                            if primaryId in self.colList[primaryCol].text:
                                self.flag=1
                                break
                if self.flag:
                    if (len(self.colList) >= elementCol ):
                        log.mjLog.LogReporter("Query","info","get_table_cell_data_using_primaryId -" \
                                              "expected cell data -  %s " % (str(self.colList[elementCol].text)))
                        
                        return self.colList[elementCol].text
                    else:
                        log.mjLog.LogReporter("Query","error","get_table_cell_data_using_primaryId" \
                                              "- Expected element col  %s is not found in the table" % (str(elementCol)))
                        raise AssertionError("Expected primary Id is not present in table")
                else:             
                    log.mjLog.LogReporter("Query","error","get_table_cell_data_using_primaryId" \
                                          "- Expected primaryID %s is not found in the table" % (primaryId))
                    raise AssertionError("Expected primary Id is not present in table")

        except:
            raise AssertionError("Error in get_table_cell_data_using_primaryId" \
                                  "- Check table xpath or primaryID or element col no")

    def get_table_cell_obj_using_primaryId(self,locator, primaryCol, primaryId, elementCol):
        """Returns cell obj of a table using primary Id  & element col number.
        your xpath for table should be something like : //form[2]/table/tbody

        """
        try:
            self.flag = 0
            self.table = self._element_finder(locator)
            if self.table:
                for row in self.table.find_elements_by_tag_name('tr'):
                    self.colList = row.find_elements_by_tag_name('td')
                    if (len(self.colList) > primaryCol ):
                        if self.colList[primaryCol].text == primaryId:
                            self.flag=1
                            break
                if self.flag:
                    if (len(self.colList) >= elementCol ):
                        log.mjLog.LogReporter("Query","info","get_table_cell_obj_using_primaryId -" \
                                              "returning expected cell obj " )
                        return self.colList[elementCol]
                    else:
                        log.mjLog.LogReporter("Query","error","get_table_cell_obj_using_primaryId" \
                                               "- Expected element col  %s is not found in the table" % (str(elementCol)))
                        raise AssertionError("Expected primary Id is not present in table")
                else:             
                    log.mjLog.LogReporter("Query","error","get_table_cell_obj_using_primaryId" \
                                           "- Expected primaryID %s is not found in the table" % (primaryId))
                    raise AssertionError("Expected primary Id is not present in table")

        except:
            raise AssertionError("Error in get_table_cell_obj_using_primaryId" \
                                 "- Check table xpath or primaryID or element col no")
        
    ### number of rows in the given table.
    def get_row_count(self,locator):
        """
        return number of rows in the given table
        """
        try:
            self.table = self._element_finder(locator)
            if self.table:
                return (len(self.table.find_elements_by_tag_name('tr')))
            else:
                log.mjLog.LogReporter("Query","error","get_row_count - Check table xpath")
                raise AssertionError("Error in get_row_count - Check table xpath")
        except:
            raise AssertionError("Error in get_row_count - Check table xpath ")

    ### number of columns in the given table. Hope your table has TH row in it.

    def get_col_count(self,locator):
        """
        return number of columns in the given table. Hope your table has TH row in it.
        """
        try:
            self.table = self._element_finder(locator)
            if self.table:
                self.tr = self.table.find_elements_by_tag_name('tr')
                return (len(self.tr[0].find_elements_by_tag_name('th')))
            else:
                log.mjLog.LogReporter("Query","error","get_col_count - Check table xpath")
                raise AssertionError("Error in get_col_count - Check table xpath")
        except:
            raise AssertionError("Error in get_col_count - Check table xpath ")
    
    def element_not_displayed(self,locator):
        """Verifies that element identified by `locator` is not displayed."""
        try:
            lengthOfElements = len(self._browser.elements_finder(locator))
            print(("element_not_displayed len -- ", lengthOfElements))
            if lengthOfElements > 0:
                return False
            else:
                return True
        except:
            raise AssertionError("Error in element_not_displayed - error in"
                                 " element_not_displayed "+str(sys.exc_info()))
        
    def element_enabled(self,locator): 
        """
        Verifies that element identified by `locator` is enabled or not.
        """
        try:
            self.elemlist = self._browser.elements_finder(locator)
            if (len(self.elemlist) == 1):
                if not self.elemlist[0].is_enabled():
                    log.mjLog.LogReporter("Query","info","element_enabled - element is disabled")
                    return False
                else:
                    log.mjLog.LogReporter("Query","info","element_enabled - element is enabled")
                    return True
            else:
                log.mjLog.LogReporter("Query","info","element_enabled - element is enabled")
                return True
        except:
            raise AssertionError("Error in checking enablity of element "+str(sys.exc_info()))
        
    def text_present(self, text):
        """
        Verifies that text is present on the page or not
        """
        try:
            from AssertElement import AssertElement
            self.assertElement = AssertElement(self._browser)
            if self.assertElement._page_contains(text):
                return text
            else:
                log.mjLog.LogReporter("WebUIOperation","debug","text_present verified \
                                        successful- %s" %(text))
                return False
        except:
            raise AssertionError("Error in checking presence of text "+str(sys.exc_info()))

    def get_text_list_from_dropdown(self,locator):
        ''' Selecting item from dropdownlist by using the option itemindex
        
        '''
        try:
            selectionlist=self._element_finder(locator)
            text_list = list()
            for option in selectionlist.find_elements_by_tag_name('option'):
                text_list.append(option.get_attribute("text"))
            return text_list
        except:
            raise AssertionError("Error in get_text_list_from_dropdown -"+str(sys.exc_info()))

    def get_text_of_selected_dropdown_option(self,locator):
        """
        return text of selected option from drop down list
        """
        try:
            selected_option = self._get_selected_option_from_dropdown(locator)
            if selected_option is not None:
                return selected_option.get_attribute("text")
            else:
                log.mjLog.LogReporter("Query","error","get_text_of_selected_dropdown_option-"\
                                              "- Check table xpath")
                raise AssertionError("Error in get_text_of_selected_dropdown_option - Check ddl xpath")
        except:
            raise AssertionError("Error in get_text_of_selected_dropdown_option - Check ddl xpath ")

    def verify_text_in_dropdown(self, textList, valueToVerify):
        ''' Verifies the value identified by valueToVerify is present in list identified by textList
        
        '''
        try:
            for text in textList:
                if text == valueToVerify:
                    log.mjLog.LogReporter("Query","info","verify_text_in_dropdown - "+valueToVerify+" is present in list")
                    break
        except:
            raise AssertionError("Error in verify_text_in_dropdown "+str(sys.exc_info()))


    def get_table_header_columns_text_list(self,locator):
        """Returns list of text in table header 
        your xpath for table should be something like : //form[2]/table/tbody
        
        e.g. get_table_header_columns_text_list("TenantTable")

        """
        try:
            self.table = self._element_finder(locator)
            if self.table:
                row=self.table.find_elements_by_tag_name('tr')
                self.colList = row[0].find_elements_by_tag_name('th')
                textList=list()
                for header in self.colList:
                    textList.append(header.text)
                log.mjLog.LogReporter("Query","info","get_table_header_columns_text_list -" \
                                              "executed successfully,table header text list returned")
                return textList
            else:
                raise AssertionError("Error in getting table - Check table xpath")
            
        except:
            raise AssertionError("Error in get_table_header_columns_text_list" \
                                  "- Check table xpath")

    def get_table_column_value(self,locator,col):
        """Returns list of text in table header 
        your xpath for table should be something like : //form[2]/table/tbody
        
        e.g. get_table_header_columns_text_list("TenantTable")
        """
        try:
          self.table = self._element_finder(locator)
          if self.table:
              rowList=self.table.find_elements_by_tag_name('tr')
              textList=list()
              for row in rowList:
                  self.colList = row.find_elements_by_tag_name('td')
                  textList.append(self.colList[col].text)
              log.mjLog.LogReporter("Query","info","get_table_column_value -" \
                                              "executed successfully,table column text list returned")
              return textList
          else:
              raise AssertionError("Error in getting table - Check table xpath")
            
        except:
            raise AssertionError("Error in get_table_column_value" \
                                  "- Check table xpath")

# if __name__ == "__main__":
#     params = {"name" : "Vinay"}
#     myBrowser = Browser(params)
#     myBrowser.go_to("http://google.com")
#     myBrowser.go_to("https://10.196.4.151/site/?page=MEETINGS&PHPSESSID=cb571e83ecad851fd8fe954fe955db0a")
#     #Webaction = WebElementAction(myBrowser)
#     Webaction.input_text("SearchButton","Vinay")
#     Webaction.press_key("SearchButton","ENTER")
#     AssertMethods = AssertElement(myBrowser)
#     AssertMethods.page_should_contain_text("Indian film")
#     Query = QueryElement(myBrowser)
#     print(Query.get_table_cell_data("join_conference_meetingtable",1,1))
#     print((Query.get_element_attribute("SearchIcon", "class")))
#     print((Query.get_text("SearchTools")))
#     print((Query.get_horizontal_position("SearchIcon")))
#     print((Query.get_vertical_position("SearchIcon")))
#     myBrowser.quit()

