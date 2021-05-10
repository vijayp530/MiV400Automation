# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
#from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import unittest, time, re, sys


class BOSS():
    
    def __init__(self,logFile):
		
		print("BOSS STARTED...")
		self.driver = webdriver.Chrome()
		self.verificationErrors = []
		self.accept_next_alert = True
		self.log = logFile
		self.errorCode = ""
		self.testResult = "PASSED"
    
    def addNewUser(self, userInfo,config ):

		print(config)
		print(userInfo['Cluster'])
		self.paramsDict = config[userInfo['Cluster']]
		print(self.paramsDict)
		self.base_url = self.paramsDict['bossURL']	
		firstName = userInfo['FirstName']
		lastName = userInfo['LastName']
		email = userInfo['UserID']
		extn = userInfo['Extn']
		did = userInfo['did']
		passwd = userInfo['Password']
		
		driver = self.driver
		# Open BOSS portal
		driver.get(self.base_url + "/UserAccount/LogOn?ReturnUrl=%2f")
		driver.maximize_window()

		# Login to portal
		print("Login to Portal")
		driver.find_element_by_id("UserName").send_keys(self.paramsDict['bossLoginID'])
		driver.find_element_by_id("Password").send_keys(self.paramsDict['bossPassword'])  
		driver.find_element_by_id("main_login").click()			
		#driver.find_element_by_xpath("//input[@type='submit' and @value='Log In']").click()
        
		try:
			# Switch to Tenant in which you want to add the user
			print("Switching Account")
			elem3=driver.find_element_by_xpath("//div[@id='userOptions']/a")
			#elem3=driver.find_element_by_id("userOptions")
			actions = ActionChains(driver)
			actions.move_to_element(elem3)
			actions.perform()
			driver.find_element_by_xpath("//a[contains(text(),'Switch Account')]").click()  
			#driver.find_element_by_id("Switch Account").click() 			
			self.explicit_wait("//input[@id='companiesAutocomplete']")
			accountName = self.paramsDict['bossAccount']
			driver.find_element_by_xpath("//input[@id='companiesAutocomplete']").send_keys(accountName)  
			time.sleep(2)
			driver.find_element_by_xpath("//strong[contains(text(),'"+accountName+"')]").click()

			time.sleep(2)
			select=Select(driver.find_element_by_id("peopleForSelectedAccount"))
			select.select_by_index(1)
			driver.find_element_by_id("SwitchAccount_OK").click()

			time.sleep(2)

			elem6=driver.find_element_by_xpath("//a[contains(text(),'Phone System')]")
			actions = ActionChains(driver)
			actions.move_to_element(elem6)
			actions.perform()
			
			# added by Raja
			if 'bossAccountPartition' in self.paramsDict.keys() :
				partition = "("+self.paramsDict['bossAccountPartition']+") "+self.paramsDict['bossAccount']
				print(partition)
				elem7 = driver.find_element_by_xpath("//span[contains(text(),'"+partition+"')]")
				actions = ActionChains(driver)
				actions.move_to_element(elem7)
				actions.perform()
				print("moved to partition: "+ partition)
				time.sleep(3)
			#####
			
			driver.find_element_by_xpath("//a[contains(text(),'Users')]").click()
			time.sleep(5)

			# Filling user info
			print("Going To Create User %s- %s" %(firstName,lastName))
			#driver.find_element_by_link_text("Users").click()
			driver.find_element_by_id("usersDataGridNewPersonButton").click()
			print("Entered new User page %s %s" %(firstName,lastName))
			time.sleep(10)
			#self.explicit_wait("//input[@id='Person_FirstName']")
			driver.find_element_by_id("Person_FirstName").clear()
			driver.find_element_by_id("Person_FirstName").send_keys(firstName)
			driver.find_element_by_id("Person_LastName").clear()
			driver.find_element_by_id("Person_LastName").send_keys(lastName)
			driver.find_element_by_id("Person_BusinessEmail").clear()
		
			driver.find_element_by_id("Person_BusinessEmail").send_keys(email)
			time.sleep(2)
			
			self.select_list_item_using_index(driver.find_element_by_id("Person_LocationId"), "1")
			
			time.sleep(2)
			driver.find_element_by_id("Person_Username").clear()
			driver.find_element_by_id("Person_Username").send_keys(email)
			time.sleep(2)
			driver.find_element_by_id("Person_Password").clear()
			driver.find_element_by_id("Person_Password").send_keys(passwd)
			driver.find_element_by_id("confirmPassword").clear()
			driver.find_element_by_id("confirmPassword").send_keys(passwd)
			time.sleep(3)
			driver.find_element_by_id("addEditPersonWizard_next").click()
			print("Entered new User passwd  %s %s" %(firstName,lastName))
			time.sleep(3)
			#self.explicit_wait("//select[@id='PhoneType']")
			

			self.select_list_item_using_index(driver.find_element_by_id("Phone_LocationId"), "1")
			self.select_list_item_using_index(driver.find_element_by_id("PhoneType"), "2")
			
			driver.find_element_by_id("allLocations").click()
			time.sleep(3)
			did = str(did)[-11:]
			did = did[0]+' ('+did[1:4]+') '+did[4:7]+'-'+did[7:11]
			print(did)
			#self.select_list_item_using_index(driver.find_element_by_id("Profile_TnId"), "1")
			
			# Added by Raja			
			select = Select(driver.find_element_by_id("Profile_TnId"))
			select.select_by_visible_text(did)
			#self.select_from_dropdown_using_text(driver.find_element_by_id("Profile_TnId"), did)

			driver.find_element_by_id("Person_Profile_Extension").clear()
			driver.find_element_by_id("Person_Profile_Extension").send_keys(extn)
			print("Entered new User extn  %s %s" %(firstName,lastName))
			time.sleep(2)
			#driver.find_element_by_css_selector("img.ui-datepicker-trigger").click()
			driver.find_element_by_id("ActivationDate").clear()
			date = time.strftime("%x")
			print(date)
			driver.find_element_by_id("ActivationDate").send_keys(date)
			time.sleep(5)
			#driver.find_element_by_link_text(str(self.get_current_date())).click()
			print("Completed  new   User last page %s %s" %(firstName,lastName))
			time.sleep(2)
			driver.find_element_by_id("addEditPersonWizard_next").click()
			time.sleep(2)
			driver.find_element_by_id("addEditPersonWizard_next").click()
			time.sleep(2)
			driver.find_element_by_id("addEditPersonWizard_next").click()
			time.sleep(2)
			
			# Added by Raja			
			select = Select(driver.find_element_by_id("RequestedBy"))
			select.select_by_index(1)
			select = Select(driver.find_element_by_id("RequestSources"))
			select.select_by_visible_text("Email")
			#self.select_list_item_using_index(driver.find_element_by_id("RequestedBy"), "1")
			#self.select_from_dropdown_using_text(driver.find_element_by_id("RequestSources"), "Email")
			
			time.sleep(2)
			#driver.find_element_by_id("addEditPersonWizard_finish").click()
			time.sleep(100)
			#self.explicit_wait("//button[@id='usersDataGridNewPersonButton']")
			print("Created  User %s %s" %(firstName,lastName))
			# Validating user creation
			# print("Validating user creation")
			driver.find_element_by_id("headerRow_BusinessEmail").clear()
			driver.find_element_by_id("headerRow_BusinessEmail").send_keys(email)
			self.is_element_contains_text(driver.find_element_by_xpath("//div[@style='display:inline-block;position:absolute;']"), email)

			driver.find_element_by_id("headerRow_BusinessEmail").clear()
			print("*** "+firstName+" "+lastName+" CREATED***")
			
			print("Logging Out of BOSS Portal")
			elem3=driver.find_element_by_xpath("//div[@id='userOptions']/a")
			actions = ActionChains(driver)
			actions.move_to_element(elem3)
			actions.perform()
			driver.find_element_by_xpath("//a[contains(text(),'Log Off')]").click()  
			time.sleep(5)
			print("Logout Successfully")
			time.sleep(2)
		except:
			raise AssertionError("Error : "+str(sys.exc_info()))
        
    def explicit_wait(self, element, waittime=60):
        driver = self.driver
        wait = WebDriverWait(driver, waittime)
        elementStatus = wait.until(EC.element_to_be_clickable((By.XPATH, element)))
        return elementStatus
        
    def get_current_date(self):
        try:
            date = time.strftime("%x")
            print(date)
            return date.split("/")[1].lstrip('0')
        except NoSuchElementException, e: return False
        return True
    
    def get_params(self):
        try:
            tempDict = {}
            fObj = open("ConfigParams.txt")
            paramsList = fObj.readlines()
            fObj.close()
            
            for line in paramsList:
                if "###" in line or "\n" == line:
                    continue
                key = line.split("=")[0]
                value = line.split("=")[1].rstrip("\n")
                tempDict[key] = value
            
            return tempDict
        except:
            raise AssertionError("ERROR "+str(sys.exc_info()))
    
    def select_from_dropdown_using_text(self,selectionlist,itemtext):
        try:
            for option in selectionlist.find_elements_by_tag_name('option'):
                if option.text == itemtext :
                    option.click()
        except NoSuchElementException, e: return False
        return True
    
    def select_list_item_using_index(self,selectionlist, itemindex):
        try:
            for option in selectionlist.find_elements_by_tag_name('option'):
                if option.get_attribute("index") == str(itemindex):
                    option.click()
        except NoSuchElementException, e: return False
        return False
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
    
    def is_element_contains_text(self, locator, itemtext):
        actualText = locator.text
        if actualText != itemtext:
            raise AssertionError("Element '%s' does not contains %s." % (locator, itemtext))
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def __del__(self):
        self.driver.quit()
        #self.assertEqual([], self.verificationErrors)