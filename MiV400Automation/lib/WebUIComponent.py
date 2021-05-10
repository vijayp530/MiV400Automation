import sys
import os
import time
import yaml
import csv
import logging
import pysftp

# framework_path = os.path.join(os.path.dirname((os.path.dirname(os.path.dirname(__file__)))), "Framework")
# sys.path.append(os.path.join(framework_path, "phone_wrappers"))

# from PhoneInterface import PhoneInterface
from robot.api.logger import console
from robot.api import logger
from selenium import webdriver
# from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
# from Var import *
from selenium.common.exceptions import *
# from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import *
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.remote_connection import LOGGER as seleniumLogger
from urllib3.connectionpool import log as urllibLogger

seleniumLogger.setLevel(logging.WARNING)
urllibLogger.setLevel(logging.WARNING)


class WebUIComponent(object):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    driver = 'GLOBAL'
    yaml_path = os.path.join(os.path.dirname((os.path.dirname(__file__))), "Variables/WebUIDetails.yaml")
    yaml_file = yaml.load(open(yaml_path), Loader=yaml.FullLoader)
    webUIDetails = {}
    for k, v in yaml_file.items():
        if isinstance(v, dict):
            for k1, v1 in v.items():
                webUIDetails[k1] = v1
        else:
            webUIDetails[k] = v
    # console(webUIDetails)

    def browser(self):
        """
        Browser Handler for execution.

        :return: None
        :created by: Ramkumar. G
        :creation date:
        :last update by: Ramkumar. G
        :last update date: 04/09/2020
        """
        # check chrome driver version with chrome if you are facing some issue in opening chrome
        chromepath = os.path.join(os.path.dirname((os.path.dirname(__file__))), "Browser_driver/chromedriver.exe")
        # edgepath = os.path.join(os.path.dirname((os.path.dirname(__file__))), "Browser_driver/MicrosoftWebDriver.exe")
        downloadPath = os.path.join(os.path.dirname((os.path.dirname(__file__))), "Downloads")
        options = webdriver.ChromeOptions()
        # options = webdriver.Edge()
        # This "prefs" parameter is used for downloading files in desired folder
        prefs = {
            "download.default_directory": downloadPath,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "download.extensions_to_open": 'cfg',
            "safebrowsing.enabled": 'false'
        }
        # options.desired_capabilities('prefs', prefs)
        options.add_experimental_option('prefs', prefs)
        options.add_argument('--disable-download-notification')
        options.add_argument('--ignore-certificate-errors')

        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(chromepath, chrome_options=options)
        # self.driver = webdriver.Edge(edgepath, prefs)

    def loginWebUI(self, **kwargs):
        """
        This method is used to login to the WebUI of the phone.

        Keyword Args:
            :phone: PhoneComponent Object of the phone to login to.
            :UserName: Username to be used for login (Optional)
            :password: Password to be used for login (Optional)
            :secured: Login securely (using https) (Optional)

        :return: None
        :created by: Ramkumar G.
        :creation date:
        :last update by: Sharma
        :last update date: 07/09/2020
        """
        try:
            phone = kwargs['phone']
            userName = kwargs.get('UserName', self.yaml_file['userid'])
            accessCode = kwargs.get('password', self.yaml_file['passcode'])
            secured = bool(kwargs.get("secured", False))
            ip = phone.phone_obj.phone_obj.phone.ipAddress
            # console("IPADDRESS: " + ip)
            # ip = phone
            if secured:
                if userName == 'user':
                    url = str("https://" + str(userName) + "@" + ip + "/")
                    console(url)
                else:
                    url = str("https://" + str(userName) + ":" + str(accessCode) + "@" + ip + "/")
                # self.browser()
                # self.driver.maximize_window()
                # time.sleep(1)
                # self.driver.get(url)
                # self.driver.find_element_by_xpath('//*[@id="details-button"]').click()
                # self.driver.find_element_by_xpath('//*[@id="proceed-link"]').click()
                # try:
                #     WebDriverWait(self.driver, 5).until(EC.alert_is_present(),
                #                                         'Timed out waiting for PA creation ' +
                #                                         'confirmation popup to appear.')
                #     loginPopup = self.driver.switch_to.active_element
                #     console("Text of Login Popup")
                #     console(loginPopup.text)
                # except TimeoutException:
                #     print("no alert")
            else:
                # print str("http://" + str(userName) + ":" + str(accessCode) + "@" + ip + "/")
                if userName == 'user':
                    url = str("http://" + str(userName) + ":" + "@" + ip + "/")
                else:
                    url = str("http://" + str(userName) + ":" + str(accessCode) + "@" + ip + "/")
            self.browser()
            self.driver.maximize_window()
            time.sleep(1)
            self.driver.get(url)
            time.sleep(5)
        except SessionNotCreatedException as e:
            version = str(e)[str(e).rfind(' ')+1:]
            raise Exception("The supported Chrome Version is " + version + ". If you are not using this version, "
                            + "read README.txt from the ProjectFolder/lib/ directory.")
        except Exception as e:
            console("LOGIN EXCEPT")
            raise e

    def goToSection(self, **kwargs):
        """

        :param:
                :option: Option to navigate to (xpath)

        :return: None
        :created by: Ramkumar G.
        :creation date:
        :last update by:
        :last update date:
        """
        try:
            # console(kwargs)
            options = str(kwargs['option'])
            # value = kwargs.get('value', '')
            self.click(options)
            time.sleep(2)
            # if value:
            #     if type(value) is dict:
            #         console("in value")
            #         for k, v in value.items():
            #             value = v
            #     self.click(value)
            #     time.sleep(5)
        except:
            self.LogOff()
            raise Exception

    def LogOff(self, deleteConfig=True):
        """
        This method is used to log off the Phone's Web UI portal.

        :return: None
        :created by: Ramkumar G.
        :creation date:
        :last update by: Vikhyat Sharma
        :last update date: 20/11/2020
        """
        try:
            logger.info("Logging off the Web UI of phone")
            console("Logging off phone")
            import shutil
            self.driver.find_element(By.XPATH, '//*[@id="header"]//ul//a').click()
            time.sleep(3)
            self.driver.quit()
            if deleteConfig:
                downloadPath = os.path.join(os.path.dirname((os.path.dirname(__file__))), "Downloads")
                isDir = os.path.isdir(downloadPath)
                if isDir:
                    shutil.rmtree(downloadPath)
        except NoSuchElementException as e:
            logger.error("----ELEMENT NOT FOUND----")
            raise Exception(e)
        except (TimeoutException, ElementNotVisibleException) as e:
            console(e)
        except WebDriverException:
            logger.warn("Web Browser window is already closed!!")
        except AttributeError:
            logger.warn("Web Browser window is already closed!!")
        # except ElementNotVisibleException as e:
        #     logger.error(e)
        # finally:
        #     self.driver.quit()

    def isChecked(self, **kwargs):
        """
        Below method is used to check if the passed element is checked/selected or not.

        :param:
            :kwargs:
                :option: Option on the webpage to check
                :value: Condition to check i.e., Checked/Selected/Unchecked/Unselected

        :return: None
        :created by: Vikhyat Sharma
        :creation date:
        :last update by:
        :last update date:
        """
        try:
            option = str(kwargs['option'])
            value = kwargs['value']
            checked = self.driver.find_element(By.XPATH, option).is_selected()
            console(checked)
            if value == "selected" or value == "Checked":
                if not checked:
                    self.LogOff()
                    raise Exception("CheckBox for " + self.yaml_file.get(option) + " is not selected.")
                else:
                    logger.info("The checkbox is selected.", also_console=True)
            elif value == "unselected" or value == "Unchecked":
                if checked:
                    self.LogOff()
                    raise Exception("CheckBox is selected.")
                else:
                    logger.info("The checkbox is not selected.", also_console=True)
        except NoSuchElementException as e:
            self.LogOff()
            raise NoSuchElementException(e)

    def click(self, args):
        """
        This method is used to click on the specified option.

        :param:
            :args: Option to click (xpath)

        :return: None
        :created by: Ramkumar G.
        :creation date:
        :last update by:
        :last update date:
        """
        # try:
        console("Clicking option")
        self.driver.find_element(By.XPATH, args).click()
        time.sleep(3)
        # except:
        #     console("CLICK EXCEPT")
        #     self.LogOff()

    def verifyFileDownloaded(self,**kwargs):
        """

        :param kwargs:
        :return:
        :created by: Ramkumar G.
        :creation date:
        :last update by:
        :last update date:
        """
        # try:
        filename = str(kwargs['fileName'])
        console('FileName:' + filename)
        downloadPath = os.path.join(os.path.dirname((os.path.dirname(__file__))), "Downloads")
        time.sleep(15)
        isDir = os.path.isdir(downloadPath)
        if isDir:
            files = (os.listdir(downloadPath))
        else:
            console("Download folder is not available")
            raise Exception
        # console("Files stored: ")
        # console(files)
        # console(downloadPath + '/' + filename)
        if filename in files:
            # console("File Size: " + str(os.stat(downloadPath + '/' + filename).st_size))
            if os.stat(downloadPath + '/' + filename).st_size > 0:
                logger.info(filename + " File is present in the Downloads Folder", also_console=True)
        else:
            self.LogOff()
            raise Exception("File not Found")

    def selectOption(self, **kwargs):
        """

        :param kwargs:
        :return:
        :created by: Ramkumar G.
        :creation date:
        :last update by:
        :last update date:
        """
        try:
            from selenium.webdriver.support.ui import Select
            givenOption = kwargs['option']
            value = kwargs['value']
            option = Select(self.driver.find_element(By.XPATH, givenOption))
            option.select_by_visible_text(value)
        except Exception:
            self.LogOff()

    # def createFile(self, **kwargs):
    #     """
    #
    #     :param kwargs:
    #     :return:
    #     :created by: Ramkumar G.
    #     :creation date:
    #     :last update by:
    #     :last update date:
    #     """
    #     try:
    #         downloadPath = os.path.join(os.path.dirname((os.path.dirname(__file__))), "Downloads")
    #         phone = str(kwargs['phone'].phone_obj.phone_obj.phone.extensionNumber)
    #         filename = str(kwargs['fileName'])
    #         time.sleep(10)
    #         if not os.path.exists(downloadPath):
    #             os.mkdir(os.path.join(os.path.dirname((os.path.dirname(__file__))), "Downloads/"))
    #             console("Directory Created ")
    #         else:
    #             console("Directory already exists")
    #
    #         csvFilePath = os.path.join(os.path.dirname((os.path.dirname(__file__))), "Downloads/" + filename)
    #         with open(csvFilePath, 'w+') as csvfile:
    #             csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    #             rows = ['A', '', '', '','', '','', '','', '','', '','', '','', '','','1','1','1',phone,'-1','V2']
    #             csvwriter.writerow(rows)
    #     except:
    #         self.LogOff()
    #         raise Exception

    def uploadFile(self,**kwargs):
        """

        :param kwargs:
        :return:
        :created by: Ramkumar G.
        :creation date:
        :last update by:
        :last update date:
        """
        try:
            filename = str(kwargs['fileName'])
            uploadPath = os.path.join(os.path.dirname((os.path.dirname(__file__))), "Downloads/" + filename)
            self.driver.send_keys(uploadPath)
            self.driver.send_keys(Keys.RETURN)
        except:
            self.LogOff()
            raise Exception

    def clearLineEntries(self, **kwargs):
        """

        :param kwargs:
        :return:
        :created by: Vikhyat Sharma
        :creation date:
        :last update by:
        :last update date:
        """
        line = kwargs['line']
        deleteLimit = kwargs['deleteLimit']
        if line == 'all':
            # while row < 20:
            screen_name = self.driver.find_element_by_xpath('//*[@id="globalSIPform"]//tr[2]/td[2]/input')
            screen_name.click()
            screen_name.clear()
            time.sleep(1)

            screen_name2 = self.driver.find_element_by_xpath('//*[@id="globalSIPform"]//tr[3]/td[2]/input')
            screen_name2.click()
            screen_name2.clear()
            time.sleep(1)

            phoneNumber = self.driver.find_element_by_xpath('//*[@id="globalSIPform"]//tr[4]/td[2]/input')
            phoneNumber.click()
            phoneNumber.clear()
            time.sleep(1)

            callerID = self.driver.find_element_by_xpath('//*[@id="globalSIPform"]//tr[5]/td[2]/input')
            callerID.click()
            callerID.clear()
            time.sleep(1)

            authName = self.driver.find_element_by_xpath('//*[@id="globalSIPform"]//tr[6]/td[2]/input')
            authName.click()
            authName.clear()
            time.sleep(1)

            password = self.driver.find_element_by_xpath('//*[@id="globalSIPform"]//tr[7]/td[2]/input')
            password.click()
            password.clear()
            time.sleep(1)

            if deleteLimit == 'Fully':
                proxyServer = self.driver.find_element_by_xpath('//*[@id="globalSIPform"]//tr[13]/td[2]/input')
                proxyServer.click()
                proxyServer.clear()
                time.sleep(1)

                proxyPort = self.driver.find_element_by_xpath('//*[@id="globalSIPform"]//tr[14]/td[2]/input')
                proxyPort.click()
                proxyPort.clear()
                time.sleep(1)

                outProxy = self.driver.find_element_by_xpath('//*[@id="globalSIPform"]//tr[17]/td[2]/input')
                outProxy.click()
                outProxy.clear()
                time.sleep(1)

                outProxyPort = self.driver.find_element_by_xpath('//*[@id="globalSIPform"]//tr[18]/td[2]/input')
                outProxyPort.click()
                outProxyPort.clear()
                time.sleep(1)

                registrarServer = self.driver.find_element_by_xpath('//*[@id="globalSIPform"]//tr[21]/td[2]/input')
                registrarServer.click()
                registrarServer.clear()
                time.sleep(1)

                registrarPort = self.driver.find_element_by_xpath('//*[@id="globalSIPform"]//tr[22]/td[2]/input')
                registrarPort.click()
                registrarPort.clear()
                time.sleep(1)
            else:
                proxyServer = self.driver.find_element_by_xpath('//*[@id="globalSIPform"]//tr[13]/td[2]/input')
                proxyServer.click()
                proxyServer.clear()
                proxyServer.send_keys('0.0.0.0')
                time.sleep(1)

                proxyPort = self.driver.find_element_by_xpath('//*[@id="globalSIPform"]//tr[14]/td[2]/input')
                proxyPort.click()
                proxyPort.clear()
                proxyPort.send_keys('0')
                time.sleep(1)

                backupProxyServer = self.driver.find_element_by_xpath('//*[@id="globalSIPform"]//tr[15]/td[2]/input')
                backupProxyServer.click()
                backupProxyServer.clear()
                backupProxyServer.send_keys('0.0.0.0')

                backupProxyPort = self.driver.find_element_by_xpath('//*[@id="globalSIPform"]//tr[16]/td[2]/input')
                backupProxyPort.click()
                backupProxyPort.clear()
                backupProxyPort.send_keys('0')
                time.sleep(1)

                outProxy = self.driver.find_element_by_xpath('//*[@id="globalSIPform"]//tr[17]/td[2]/input')
                outProxy.click()
                outProxy.clear()
                outProxy.send_keys('0.0.0.0')
                time.sleep(1)

                outProxyPort = self.driver.find_element_by_xpath('//*[@id="globalSIPform"]//tr[18]/td[2]/input')
                outProxyPort.click()
                outProxyPort.clear()
                outProxyPort.send_keys('0')
                time.sleep(1)

                backupOutboundProxyServer = self.driver.find_element_by_xpath('//*[@id="globalSIPform"]//tr[19]/td[2]/input')
                backupOutboundProxyServer.click()
                backupOutboundProxyServer.clear()
                backupOutboundProxyServer.send_keys('0.0.0.0')
                time.sleep(1)

                backupOutboundProxyPort = self.driver.find_element_by_xpath('//*[@id="globalSIPform"]//tr[20]/td[2]/input')
                backupOutboundProxyPort.click()
                backupOutboundProxyPort.clear()
                backupOutboundProxyPort.send_keys('0')
                time.sleep(1)

                registrarServer = self.driver.find_element_by_xpath('//*[@id="globalSIPform"]//tr[21]/td[2]/input')
                registrarServer.click()
                registrarServer.clear()
                registrarServer.send_keys('0.0.0.0')
                time.sleep(1)

                registrarPort = self.driver.find_element_by_xpath('//*[@id="globalSIPform"]//tr[22]/td[2]/input')
                registrarPort.click()
                registrarPort.clear()
                registrarPort.send_keys('0')
                time.sleep(1)

                backupRegistrarServer = self.driver.find_element_by_xpath('//*[@id="globalSIPform"]//tr[23]/td[2]/input')
                backupRegistrarServer.click()
                backupRegistrarServer.clear()
                backupRegistrarServer.send_keys('0.0.0.0')
                time.sleep(1)

                backupRegistrarPort = self.driver.find_element_by_xpath('//*[@id="globalSIPform"]//tr[24]/td[2]/input')
                backupRegistrarPort.click()
                backupRegistrarPort.clear()
                backupRegistrarPort.send_keys('0')
                time.sleep(1)

                # saving the settings
            self.driver.find_element_by_xpath('//*[@id="globalSIPform"]/p/input').click()
        else:
            screen_name = self.driver.find_element_by_xpath('//*[@id="mainTable"]//tr[2]/td[2]/input')
            screen_name.click()
            screen_name.clear()
            time.sleep(1)

            screen_name2 = self.driver.find_element_by_xpath('//*[@id="mainTable"]//tr[3]/td[2]/input')
            screen_name2.click()
            screen_name2.clear()
            time.sleep(1)

            phoneNumber = self.driver.find_element_by_xpath('//*[@id="mainTable"]//tr[4]/td[2]/input')
            phoneNumber.click()
            phoneNumber.clear()
            time.sleep(1)

            callerID = self.driver.find_element_by_xpath('//*[@id="mainTable"]//tr[5]/td[2]/input')
            callerID.click()
            callerID.clear()
            time.sleep(1)

            authName = self.driver.find_element_by_xpath('//*[@id="mainTable"]//tr[6]/td[2]/input')
            authName.click()
            authName.clear()
            time.sleep(1)

            password = self.driver.find_element_by_xpath('//*[@id="mainTable"]//tr[7]/td[2]/input')
            password.click()
            password.clear()
            time.sleep(1)

            if deleteLimit == 'Fully':
                proxyServer = self.driver.find_element_by_xpath('//*[@id="mainTable"]//tr[13]/td[2]/input')
                proxyServer.click()
                proxyServer.clear()
                time.sleep(1)

                proxyPort = self.driver.find_element_by_xpath('//*[@id="mainTable"]//tr[14]/td[2]/input')
                proxyPort.click()
                proxyPort.clear()
                time.sleep(1)

                outProxy = self.driver.find_element_by_xpath('//*[@id="mainTable"]//tr[17]/td[2]/input')
                outProxy.click()
                outProxy.clear()
                time.sleep(1)

                outProxyPort = self.driver.find_element_by_xpath('//*[@id="mainTable"]//tr[18]/td[2]/input')
                outProxyPort.click()
                outProxyPort.clear()
                time.sleep(1)

                registrarServer = self.driver.find_element_by_xpath('//*[@id="mainTable"]//tr[21]/td[2]/input')
                registrarServer.click()
                registrarServer.clear()
                time.sleep(1)

                registrarPort = self.driver.find_element_by_xpath('//*[@id="mainTable"]//tr[22]/td[2]/input')
                registrarPort.click()
                registrarPort.clear()
                time.sleep(1)
            else:
                proxyServer = self.driver.find_element_by_xpath('//*[@id="mainTable"]//tr[13]/td[2]/input')
                proxyServer.click()
                proxyServer.clear()
                proxyServer.send_keys('0.0.0.0')
                time.sleep(1)

                proxyPort = self.driver.find_element_by_xpath('//*[@id="mainTable"]//tr[14]/td[2]/input')
                proxyPort.click()
                proxyPort.clear()
                proxyPort.send_keys('0')
                time.sleep(1)

                backupProxyServer = self.driver.find_element_by_xpath('//*[@id="mainTable"]//tr[15]/td[2]/input')
                backupProxyServer.click()
                backupProxyServer.clear()
                backupProxyServer.send_keys('0.0.0.0')

                backupProxyPort = self.driver.find_element_by_xpath('//*[@id="mainTable"]//tr[16]/td[2]/input')
                backupProxyPort.click()
                backupProxyPort.clear()
                backupProxyPort.send_keys('0')
                time.sleep(1)

                outProxy = self.driver.find_element_by_xpath('//*[@id="mainTable"]//tr[17]/td[2]/input')
                outProxy.click()
                outProxy.clear()
                outProxy.send_keys('0.0.0.0')
                time.sleep(1)

                outProxyPort = self.driver.find_element_by_xpath('//*[@id="mainTable"]//tr[18]/td[2]/input')
                outProxyPort.click()
                outProxyPort.clear()
                outProxyPort.send_keys('0')
                time.sleep(1)

                backupOutboundProxyServer = self.driver.find_element_by_xpath('//*[@id="mainTable"]//tr[19]/td[2]/input')
                backupOutboundProxyServer.click()
                backupOutboundProxyServer.clear()
                backupOutboundProxyServer.send_keys('0.0.0.0')
                time.sleep(1)

                backupOutboundProxyPort = self.driver.find_element_by_xpath('//*[@id="mainTable"]//tr[20]/td[2]/input')
                backupOutboundProxyPort.click()
                backupOutboundProxyPort.clear()
                backupOutboundProxyPort.send_keys('0')
                time.sleep(1)

                registrarServer = self.driver.find_element_by_xpath('//*[@id="mainTable"]//tr[21]/td[2]/input')
                registrarServer.click()
                registrarServer.clear()
                registrarServer.send_keys('0.0.0.0')
                time.sleep(1)

                registrarPort = self.driver.find_element_by_xpath('//*[@id="mainTable"]//tr[22]/td[2]/input')
                registrarPort.click()
                registrarPort.clear()
                registrarPort.send_keys('0')
                time.sleep(1)

                backupRegistrarServer = self.driver.find_element_by_xpath('//*[@id="mainTable"]//tr[23]/td[2]/input')
                backupRegistrarServer.click()
                backupRegistrarServer.clear()
                backupRegistrarServer.send_keys('0.0.0.0')
                time.sleep(1)

                backupRegistrarPort = self.driver.find_element_by_xpath('//*[@id="mainTable"]//tr[24]/td[2]/input')
                backupRegistrarPort.click()
                backupRegistrarPort.clear()
                backupRegistrarPort.send_keys('0')
                time.sleep(1)
            # saving the settings
            self.driver.find_element_by_xpath('//*[@id="sipLineSettingsForm"]/p/input').click()

    def unRegisterPhone(self, **kwargs):
        """
        This method is used to unregister the phone using its Web UI.

        This method needs the Web UI to be login in a new browser window beforehand.
        :param:
             :linesToUnregister: The line to unregister i.e., 1 - 24
             :deleteLimit: Fully or Partially
                           Fully will delete the SIP network settings along with the authentication settings
                           but Partially will change network settings to default ones.
             :phone: Phone to unregister
        :return: None
        :created by: Sharma
        :creation date:
        :last update by:
        :last update date:
        """
        line = str(kwargs['lineToUnregister'])
        deleteLimit = kwargs.get('deleteLimit', 'Fully')
        phone = kwargs['phone'].phone_obj.phone_obj.phone.extensionNumber

        logger.info("Unregistered Line: <b>" + line + "</b> using the Web UI of extension: " + phone, html=True)
        console("Unregistered Line: " + line + " using the Web UI of extension: " + phone)
        try:
            if line == 'all' or line == 'All':
                globalSIP = self.driver.find_element_by_xpath('//*[@id="sidebar"]/ul[4]/li[2]/a')
                globalSIP.click()
                self.clearLineEntries(line=line, deleteLimit=deleteLimit)
                logger.info("Unregistering global SIP entries on " + phone)
            elif line == '1':
                self.driver.find_element_by_xpath('//*[@id="sidebar"]/ul[4]/li[3]/a').click()
                self.clearLineEntries(line=line, deleteLimit=deleteLimit)
            elif line == '2':
                self.driver.find_element_by_xpath('//*[@id="sidebar"]/ul[4]/li[4]/a').click()
                self.clearLineEntries(line=line, deleteLimit=deleteLimit)
            elif line == '3':
                self.driver.find_element_by_xpath('//*[@id="sidebar"]/ul[4]/li[5]/a').click()
                self.clearLineEntries(line=line, deleteLimit=deleteLimit)
            elif line == '4':
                self.driver.find_element_by_xpath('//*[@id="sidebar"]/ul[4]/li[6]/a').click()
                self.clearLineEntries(line=line, deleteLimit=deleteLimit)
            elif line == '5':
                self.driver.find_element_by_xpath('//*[@id="sidebar"]/ul[4]/li[7]/a').click()
                self.clearLineEntries(line=line, deleteLimit=deleteLimit)
            elif line == '6':
                self.driver.find_element_by_xpath('//*[@id="sidebar"]/ul[4]/li[8]/a').click()
                self.clearLineEntries(line=line, deleteLimit=deleteLimit)
            elif line == '7':
                self.driver.find_element_by_xpath('//*[@id="sidebar"]/ul[4]/li[9]/a').click()
                self.clearLineEntries(line=line, deleteLimit=deleteLimit)
            elif line == '8':
                self.driver.find_element_by_xpath('//*[@id="sidebar"]/ul[4]/li[10]/a').click()
                self.clearLineEntries(line=line, deleteLimit=deleteLimit)
            elif line == '9':
                self.driver.find_element_by_xpath('//*[@id="sidebar"]/ul[4]/li[11]/a').click()
                self.clearLineEntries(line=line, deleteLimit=deleteLimit)
            logger.info("Unregistered Line: <b>" + line + "</b> using the Web UI of extension: " + phone)
            console("Unregistered Line: " + line + " line using the Web UI of extension: " + phone)
        except Exception as e:
            self.LogOff()
            raise Exception('Could not unregister ' + line + 'line on extension: ' + phone + '. \nDETAILS: ' + e)

    def fillLineEntries(self, **kwargs):
        """
        Below method is used to fill the entries in the registration page of the phone.

        Keyword Args:
            linesToRegister: Line to Register
            phoneToEnter: Phone whose details should be entered

        :return:
        :created by: Vikhyat Sharma
        :creation date:
        :last update by:
        :last update date:
        """
        line = kwargs['linesToRegister']
        phone = kwargs['phoneToEnter']
        number = phone.phone_obj.phone_obj.phone.extensionNumber
        # number = '4165142501'
        pbxUsed = self.yaml_file.get((kwargs['pbx']) + 'IP')
        # pbx = '10.112.123.89'
        if line == 'all' or line == 'All':
            screen_name = self.driver.find_element_by_xpath('//*[@id="globalSIPform"]//tr[2]/td[2]/input')
            screen_name.click()
            screen_name.clear()
            time.sleep(1)
            screen_name.send_keys(number)
            time.sleep(1)

            screen_name2 = self.driver.find_element_by_xpath('//*[@id="globalSIPform"]//tr[3]/td[2]/input')
            screen_name2.click()
            screen_name2.clear()
            time.sleep(1)
            screen_name2.send_keys(number)
            time.sleep(1)

            phoneNumber = self.driver.find_element_by_xpath('//*[@id="globalSIPform"]//tr[4]/td[2]/input')
            phoneNumber.click()
            phoneNumber.clear()
            time.sleep(1)
            phoneNumber.send_keys(number)
            time.sleep(1)

            callerID = self.driver.find_element_by_xpath('//*[@id="globalSIPform"]//tr[5]/td[2]/input')
            callerID.click()
            callerID.clear()
            time.sleep(1)
            callerID.send_keys(number)
            time.sleep(1)

            authName = self.driver.find_element_by_xpath('//*[@id="globalSIPform"]//tr[6]/td[2]/input')
            authName.click()
            authName.clear()
            time.sleep(1)
            authName.send_keys(number)
            time.sleep(1)

            password = self.driver.find_element_by_xpath('//*[@id="globalSIPform"]//tr[7]/td[2]/input')
            password.click()
            password.clear()
            time.sleep(1)
            password.send_keys(number)
            time.sleep(1)

            proxyServer = self.driver.find_element_by_xpath('//*[@id="globalSIPform"]//tr[13]/td[2]/input')
            proxyServer.click()
            proxyServer.clear()
            time.sleep(1)
            proxyServer.send_keys(pbxUsed)
            time.sleep(1)

            proxyPort = self.driver.find_element_by_xpath('//*[@id="globalSIPform"]//tr[14]/td[2]/input')
            proxyPort.click()
            proxyPort.clear()
            time.sleep(1)
            proxyPort.send_keys('5060')
            time.sleep(1)

            outProxy = self.driver.find_element_by_xpath('//*[@id="globalSIPform"]//tr[17]/td[2]/input')
            outProxy.click()
            outProxy.clear()
            time.sleep(1)
            outProxy.send_keys(pbxUsed)
            time.sleep(1)

            outProxyPort = self.driver.find_element_by_xpath('//*[@id="globalSIPform"]//tr[18]/td[2]/input')
            outProxyPort.click()
            outProxyPort.clear()
            time.sleep(1)
            outProxyPort.send_keys('5060')
            time.sleep(1)

            registrarServer = self.driver.find_element_by_xpath('//*[@id="globalSIPform"]//tr[21]/td[2]/input')
            registrarServer.click()
            registrarServer.clear()
            time.sleep(1)
            registrarServer.send_keys(pbxUsed)
            time.sleep(1)

            registrarPort = self.driver.find_element_by_xpath('//*[@id="globalSIPform"]//tr[22]/td[2]/input')
            registrarPort.click()
            registrarPort.clear()
            time.sleep(1)
            registrarPort.send_keys('5060')
            time.sleep(1)

            # saving the settings
            self.driver.find_element_by_xpath('//*[@id="globalSIPform"]/p/input').click()
        else:
            screen_name = self.driver.find_element_by_xpath('//*[@id="mainTable"]//tr[2]/td[2]/input')
            screen_name.click()
            screen_name.clear()
            time.sleep(1)
            screen_name.send_keys(number)
            time.sleep(1)

            screen_name2 = self.driver.find_element_by_xpath('//*[@id="mainTable"]//tr[3]/td[2]/input')
            screen_name2.click()
            screen_name2.clear()
            time.sleep(1)
            screen_name2.send_keys(number)
            time.sleep(1)

            phoneNumber = self.driver.find_element_by_xpath('//*[@id="mainTable"]//tr[4]/td[2]/input')
            phoneNumber.click()
            phoneNumber.clear()
            time.sleep(1)
            phoneNumber.send_keys(number)
            time.sleep(1)

            callerID = self.driver.find_element_by_xpath('//*[@id="mainTable"]//tr[5]/td[2]/input')
            callerID.click()
            callerID.clear()
            time.sleep(1)
            callerID.send_keys(number)
            time.sleep(1)

            authName = self.driver.find_element_by_xpath('//*[@id="mainTable"]//tr[6]/td[2]/input')
            authName.click()
            authName.clear()
            time.sleep(1)
            authName.send_keys(number)
            time.sleep(1)

            password = self.driver.find_element_by_xpath('//*[@id="mainTable"]//tr[7]/td[2]/input')
            password.click()
            password.clear()
            time.sleep(1)
            password.send_keys(number)
            time.sleep(1)

            proxyServer = self.driver.find_element_by_xpath('//*[@id="mainTable"]//tr[13]/td[2]/input')
            proxyServer.click()
            proxyServer.clear()
            time.sleep(1)
            proxyServer.send_keys(pbxUsed)
            time.sleep(1)

            proxyPort = self.driver.find_element_by_xpath('//*[@id="mainTable"]//tr[14]/td[2]/input')
            proxyPort.click()
            proxyPort.clear()
            time.sleep(1)
            proxyPort.send_keys('5060')
            time.sleep(1)

            outProxy = self.driver.find_element_by_xpath('//*[@id="mainTable"]//tr[17]/td[2]/input')
            outProxy.click()
            outProxy.clear()
            time.sleep(1)
            outProxy.send_keys(pbxUsed)
            time.sleep(1)

            outProxyPort = self.driver.find_element_by_xpath('//*[@id="mainTable"]//tr[18]/td[2]/input')
            outProxyPort.click()
            outProxyPort.clear()
            time.sleep(1)
            outProxyPort.send_keys('5060')
            time.sleep(1)

            registrarServer = self.driver.find_element_by_xpath('//*[@id="mainTable"]//tr[21]/td[2]/input')
            registrarServer.click()
            registrarServer.clear()
            time.sleep(1)
            registrarServer.send_keys(pbxUsed)
            time.sleep(1)

            registrarPort = self.driver.find_element_by_xpath('//*[@id="mainTable"]//tr[22]/td[2]/input')
            registrarPort.click()
            registrarPort.clear()
            time.sleep(1)
            registrarPort.send_keys('5060')
            time.sleep(1)

            # saving the settings
            self.driver.find_element_by_xpath('//*[@id="sipLineSettingsForm"]/p/input').click()

    def registerPhone(self, **kwargs):
        """
        This method is used to register phones' lines with an extension of same number or other number.

        Keyword Args:
            phoneToOpen: Phone To Edit
            phoneToEnter: Phone with which the line will be registered
            lineToRegister: Line to Register i.e., 1, 2, or 3 or 4-9.

        :return: None
        :created by: Vikhyat Sharma
        :creation date:
        :last update by: Ramkumar G.
        :last update date: 10/06/2020
        """
        lineToRegister = str(kwargs['linesToRegister'])
        phone = kwargs['phoneToOpen']
        phoneToEnter = kwargs['phoneToEnter']
        try:
            if lineToRegister == 'all':
                logger.info("Registering all the lines on the extension "
                            + phone.phone_obj.phone_obj.phone.extensionNumber + " with IP: "
                            + phone.phone_obj.phone_obj.phone.ipAddress + " with extension: "
                            + phoneToEnter.phone_obj.phone_obj.phone.extensionNumber)
                console("Registering all the lines on the extension "
                        + phone.phone_obj.phone_obj.phone.extensionNumber + " with IP: "
                        + phone.phone_obj.phone_obj.phone.ipAddress + " with extension: "
                        + phoneToEnter.phone_obj.phone_obj.phone.extensionNumber)
                globalSIP = self.driver.find_element_by_xpath('//*[@id="sidebar"]/ul[4]/li[2]/a')
                globalSIP.click()
                self.fillLineEntries(**kwargs)
            elif "-" in lineToRegister:
                line = int(lineToRegister[-1])
                for i in range(1, int(line) + 1):
                    lines = i + 2
                    xpath = '//*[@id="sidebar"]/ul[4]/li[' + str(lines) + ']/a'
                    self.driver.find_element_by_xpath(xpath).click()
                    self.fillLineEntries(**kwargs)
            else:
                logger.info("Registering Line: " + lineToRegister + " on the extension "
                            + phone.phone_obj.phone_obj.phone.extensionNumber + " with IP: "
                            + phone.phone_obj.phone_obj.phone.ipAddress + " with extension: "
                            + phoneToEnter.phone_obj.phone_obj.phone.extensionNumber)
                console("Registering Line: " + lineToRegister + " on the extension "
                        + phone.phone_obj.phone_obj.phone.extensionNumber + " with IP: "
                        + phone.phone_obj.phone_obj.phone.ipAddress + " with extension: "
                        + phoneToEnter.phone_obj.phone_obj.phone.extensionNumber)
                line = int(lineToRegister[-1]) + 2
                xpath = '//*[@id="sidebar"]/ul[4]/li[' + str(line) + ']/a'
                self.driver.find_element_by_xpath(xpath).click()
                self.fillLineEntries(**kwargs)
            logger.info("Registered Line: <b>" + lineToRegister + "</b> on extension: <b>"
                        + phone.phone_obj.phone_obj.phone.extensionNumber + "</b>", html=True)
            console("Registered Line: " + lineToRegister + " on extension: "
                    + phone.phone_obj.phone_obj.phone.extensionNumber)
        except Exception:
            self.LogOff()
            # raise Exception("Could not register Phone.")

    def verifyRegisteredLine(self, **kwargs):
        """
        Below method is used to verify the passed line is registered on the phone.

        :param:
            :kwargs:
                :lineToVerify: Line to Verify for registration
                :phone: Phone To Open
        :return: None
        :created by: Vikhyat Sharma
        :creation date:
        :last update by: Sharma
        :last update date: 07/09/2020
        """
        lineToVerify = kwargs['lineToVerify']
        phone = kwargs['phone']
        phoneNumber = str(kwargs['phone'].phone_obj.phone_obj.phone.extensionNumber)
        # phoneNumber = phone

        sysInfo = self.yaml_file.get('SystemInfoMenu')
        logger.info("Verifying Line: <b>" + lineToVerify + "</b> is registered on Web UI of extension: <b>"
                    + phoneNumber + "</b>", html=True)
        console("Verifying Line: " + lineToVerify + " is registered on Web UI of extension: " + phoneNumber)
        try:
            statusRow = 21
            if phone.phone_obj.phone_type == 'Mitel6930':
                statusRow = 22
            self.goToSection(option=sysInfo)
            if lineToVerify.isdigit():
                lineStatus = self.driver.find_element_by_xpath('//*[@id="content"]//tr['
                                                               + str(statusRow + int(lineToVerify)) + ']/td[3]')
            else:
                raise Exception("INVALID ARGUMENT PASSED FOR 'lineToVerify'")
            # if lineToVerify == '1':
            #     lineStatus = self.driver.find_element_by_xpath('//*[@id="content"]//tr[' + str(lineStatus+1) + ']/td[3]')
            # elif lineToVerify == '2':
            #     lineStatus = self.driver.find_element_by_xpath('//*[@id="content"]//tr[24]/td[3]')
            # elif lineToVerify == '3':
            #     lineStatus = self.driver.find_element_by_xpath('//*[@id="content"]//tr[25]/td[3]')
            # else:
            #     raise Exception("INVALID ARGUMENT PASSED FOR 'lineToVerify'")
            # console("----------------------LINE--------------------------")
            # console(lineStatus)
            # console(lineStatus.is_displayed())
            # console(lineStatus.text)
            if lineStatus.is_displayed() and lineStatus.text == 'Registered':
                logger.info("Verified Line <b>" + lineToVerify + "</b> is registered on phone: <b>" + phoneNumber
                            + "</b>", html=True)
                console("Verified Line " + lineToVerify + " is registered on phone: " + phoneNumber)
            else:
                raise Exception("Could not verify line " + lineToVerify + " is registered on phone: " + phoneNumber
                                + ". Got line status as '" + lineStatus.text + "'")
        except ElementNotVisibleException:
            logger.error("ELEMENT NOT INTRACTABLE")
            self.LogOff()
            raise Exception("ELEMENT NOT INTRACTABLE")
        except NoSuchElementException:
            self.LogOff()
            raise Exception("ELEMENT NOT PRESENT")
        except Exception as e:
            self.LogOff()
            raise Exception(e)

    def findPageElement(self, xpath):
        """

        :param xpath:
        :return:
        :created by: Vikhyat Sharma
        :creation date:
        :last update by:
        :last update date:
        """
        try:
            if xpath == 'Forbidden Page Title':
                if self.driver.title == '403 Forbidden':
                    logger.info("Phone Web UI is locked.")
                else:
                    raise Exception("Phone Web UI is not locked.")
            else:
                present = self.driver.find_element_by_xpath(xpath).is_displayed()
                if present:
                    logger.info("Element is present on the page.", also_console=True)
                    # console("Element is present on the page.")
                else:
                    raise Exception("Element is not present on the page.")
        except:
            self.LogOff()
            raise Exception("Exception occurred while finding element on the page.")

    def verifyElementIsFound(self, element):
        """
        This method is used to verify the presence of element on the Web UI of the phone.

        :param:
            :element: Text to verify or Element's xpath

        :return: None
        :created by: Sharma
        :creation date:
        :last update by:
        :last update date:
        """
        try:
            if element.startswith("//*"):
                if self.driver.find_element_by_xpath(element).is_displayed():
                    console("Element is present on the Web UI.")
                else:
                    raise NoSuchElementException
            else:
                if element in self.driver.page_source:
                    console(element + " is present on the Page.")
                else:
                    raise NoSuchElementException
        except NoSuchElementException as e:
            print(e.__class__)
            self.LogOff()
            raise Exception("Element is not present on the page !!!")
        except Exception:
            self.LogOff()
            raise Exception("Could not verify the presence of the element !!")

    def verifyElementNotFound(self, element):
        """
        This method is used to verify the negative presence of the element on the Web UI of the phone.

        :param:
            :element: Text or Element to verify

        :return: None
        :created by: Vikhyat Sharma
        :creation date:
        :last update by:
        :last update date:
        """
        try:
            if element == 'Forbidden Page Title':
                console("Verifying Forbidden Page Title")
                if self.driver.title == '403 Forbidden':
                    logger.error("Phone Web UI is locked.")
                else:
                    logger.info("Phone Web UI is not locked.", also_console=True)
            else:
                console("Verifying Element is not present on the screen")
                present = self.driver.find_element_by_xpath(element).is_displayed()
                if not present:
                    logger.info("Element is not present on the page.", also_console=True)
                else:
                    raise Exception
        except NoSuchElementException:
            logger.info("Element is not present on the screen.", also_console=True)
        except WebDriverException:
            self.LogOff()
            raise Exception("Try to do something")
        except Exception:
            raise Exception("Could not verify the presence of the element on the Web UI.")

    def clearKeys(self,**kwargs):
        """

        :param kwargs:
        :return:
        :created by: Ramkumar G.
        :creation date:
        :last update by:
        :last update date:
        """
        try:
            option = kwargs['option']
            self.driver.find_element(By.XPATH, option).clear()
            time.sleep(3)
        except:
            console("clearKeys EXCEPT")
            self.LogOff()

    def sendKeys(self,**kwargs):
        """

        :param kwargs:
        :return:
        :created by: Ramkumar G.
        :creation date:
        :last update by:
        :last update date:
        """
        try:
            option = kwargs['option']
            value = str(kwargs['value'])
            self.clearKeys(**kwargs)
            self.driver.find_element(By.XPATH, option).send_keys(value)
            time.sleep(3)
        except:
                console("clearSendKeys EXCEPT")
                self.LogOff()

    def verifyText(self, **kwargs):
        """
        The method is used to verify the value passed against the option available on the Web UI of the phone.

        Keyword Args:
              :option: Option on the Web UI of the phone
              :value: The value to verify against the option.

        :return: None
        :created by: Vikhyat Sharma
        :created on:
        :updated on: 03/02/2021
        :updated by: Milind Patil
        """
        try:
            option = str(kwargs.get('option'))
            value = str(kwargs['value'])
            onPage = bool(kwargs.get('OnPage', False))

            console("Verifying " + value + " on the phone WEB UI.")
            time.sleep(1)

            if onPage:
                if value in self.driver.page_source:
                    logger.info("Value: " + value + " is present on the WEB UI.")
                else:
                    raise Exception("The specified value: '" + value + "' could not be found on the phone WUI !!!")
            else:
                element = self.driver.find_element_by_xpath(option)
                if element.tag_name == 'select':
                    console('Element is dropdown')
                    element = Select(self.driver.find_element_by_xpath(option))
                    text = element.first_selected_option.text
                else:
                    text = self.driver.find_element(By.XPATH, option).text

                if len(text) == 0:
                    text = str(self.driver.find_element(By.XPATH, option).get_attribute('value'))

                if 'verifiedPhone' in kwargs:
                    phoneDetails = self.yaml_file.get('PhoneDetails')
                    for key, val in phoneDetails.items():
                        if value == key:
                            verifiedPhone = kwargs['verifiedPhone']
                            value = getattr(verifiedPhone.phone_obj.phone_obj.phone, val)
                            if key == "PhoneModel":
                                value = value[-4:]
                            break

                if text == value:
                    logger.info("'<b>" + value + "</b>' is verified on the phone WEB UI.", html=True)
                    console("'" + value + "' is verified on the phone WEB UI.")
                else:
                    raise Exception("The specified value: '" + value + "' could not be found on the phone WUI !!!. Got "
                                    + text + " instead.")
        except NoSuchElementException as e:
            self.LogOff()
            raise Exception(e)
        except ElementNotVisibleException as e:
            self.LogOff()
            raise Exception(e)

    def sendFileToUpload(self, **kwargs):
        """

        :param kwargs:
        :return:
        :created by: Ramkumar G.
        :creation date:
        :last update by: Sharma
        :last update date:
        """
        console(kwargs)
        try:
            option = kwargs['option']
            filename = kwargs['fileName']
            filePath = 'configuration/' + filename
            # actions = ActionChains(self.driver)
            # elementLocator = self.driver.find_element(By.XPATH, option)
            # actions.double_click(elementLocator).click().perform()
            # time.sleep(3)
            # directoryFilePath = r'..\configuration\directoryFile.csv'
            directoryFilePath = os.path.join(os.path.dirname(os.path.dirname(__file__)), filePath)
            # os.system(directoryFilePath)
            time.sleep(5)
            # if filename =="Directory"
            self.driver.find_element_by_xpath(option).send_keys(directoryFilePath)
            self.driver.find_element(By.XPATH, '//*[@id="content"]//tr[6]/td[2]/input').click()
            time.sleep(10)
        except Exception as e:
            console("CLICK EXCEPT")
            self.LogOff()
            raise e

    def closeWindow(self):
        """
        Below method is used to close the opened browser windows.
        :return: None
        :created by: Vikhyat Sharma
        :creation date: 16/03/2020
        :last update by:
        :last update date:
        """
        self.driver.quit()

    def serverConnection(self,**kwargs):
        """

        :param kwargs:
        :return:
        :created by: Ramkumar G.
        :creation date:
        :last update by:
        :last update date:
        """
        console(kwargs)
        hostname = kwargs["parameter"]['Hostname']
        Username = kwargs["parameter"]['Username']
        Password = kwargs["parameter"]['Password']
        fileName = kwargs['fileName']
        console(fileName)
        remoteFilePath = self.yaml_file['remoteFilePath']+"/"+fileName
        console(remoteFilePath)
        localFilePath = os.path.join(os.path.dirname((os.path.dirname(__file__))), "Downloads/" + fileName)
        console(localFilePath)
        sftp = pysftp.Connection(host=hostname, username=Username, password=Password)
        directory_structure = sftp.listdir_attr()
        sftp.cwd('/var/www/html/configuration/')
        directory_structure = sftp.listdir_attr()
        sftp.put(localFilePath, remoteFilePath)
        for attr in directory_structure:
            print ("file has moved")

    def addParamtersToCfgfile(self,**kwargs):
        """

        :param kwargs:
        :return:
        :created by: Ramkumar G.
        :creation date:
        :last update by:
        :last update date:
        """
        fileName = kwargs['fileName']
        parameter = kwargs['parameter']
        if not os.path.exists("C:/Robo_SVN_5.1/Desktop_Automation/Downloads/"):
            os.makedirs("C:/Robo_SVN_5.1/Desktop_Automation/Downloads/")
        write_file = open("C:/Robo_SVN_5.1/Desktop_Automation/Downloads/" +fileName, "wb")
        write_file.write("$telnet enabled: Telnet for support1410!$\n")
        write_file.write("sip register blocking: 0\n")
        for k,v in parameter.items():
            write_file.write(k + '\n')
            write_file.write(v + '\n')

    def delete_file(self,**kwargs):
        """

        :param kwargs:
        :return:
        :created by: Ramkumar G.
        :creation date:
        :last update by:
        :last update date:
        """
        fileName = kwargs['fileName']
        if os.path.exists("C:/Robo_SVN_5.1/Desktop_Automation/Downloads"+"/"+fileName):
            os.remove("C:/Robo_SVN_5.1/Desktop_Automation/Downloads"+"/"+fileName)

    def verifyOpenedURL(self, **kwargs):
        """
        This method verifies the currently opened URL with the passed URL entry.

        :param
            :kwargs:
                :url: URL to verify on the browser window
        :return: None
        :created by: Vikhyat Sharma
        :creation date: 07/05/2020
        :last update by:
        :last update on:
        """
        url = kwargs['url']
        currentURL = self.driver.current_url
        if url in currentURL:
            logger.info("Correct URL is opened.")
        else:
            raise Exception("Incorrect URL opened.")

    def capturePackets(self, **kwargs):
        """
        This method can start/stop the packets capturing and download the captured file using phone's Web UI.

        Keyword Args:
            action: action to perform i.e., Start/Stop the capture or Download
            phoneObj: PhoneComponent object of the phone
            portNumber: PortNumber of the protocol for filtering or all for every protocol
            timeout: Automatic Timeout period for the capture

        :return: None
        :created by: Vikhyat Sharma
        :creation date: 11/05/2020
        :last update by:
        :last update date:
        """
        # console(kwargs)
        action = str(kwargs.get('action'))
        phoneObj = kwargs.get('phoneObj')
        captureOptions = self.yaml_file.get("CaptureLink")

        self.goToSection(option=self.yaml_file.get("CaptureMenu"))
        port = self.driver.find_element_by_xpath(captureOptions['Port'])
        saveSettings = self.driver.find_element_by_xpath(captureOptions['SaveSetting'])
        if action == 'Download':
            pcapFilePath = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                                        'Downloads\\captureFile.pcap'))
            convertedFilePath = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                                             'Downloads\\convertedFile.txt'))
            downloadPath = os.path.join(os.path.dirname((os.path.dirname(__file__))), "Downloads")
            if os.path.isdir(downloadPath):
                if os.path.exists(pcapFilePath):
                    os.remove(pcapFilePath)
                if os.path.exists(convertedFilePath):
                    os.remove(convertedFilePath)
            self.driver.find_element_by_xpath(captureOptions['GetCapture']).click()
            time.sleep(10)
            logger.info("Successfully downloaded the capture file.", also_console=True)
        else:
            timeout = kwargs.get('timeout')
            if timeout is not None:
                self.driver.find_element_by_xpath(captureOptions['TimeOut']).clear()
                self.driver.find_element_by_xpath(captureOptions['TimeOut']).send_keys(timeout)

            portNumber = str(kwargs.get('portNumber', ''))
            if portNumber == 'default':
                portNumber = 5060

            if portNumber == 'all':
                port.click()
                port.clear()
                saveSettings.click()
                time.sleep(3)
                self.goToSection(option=self.yaml_file.get('CaptureMenu'))
            else:
                port.click()
                port.clear()
                time.sleep(2)
                port.send_keys(portNumber)

            startStopButton = self.driver.find_element_by_xpath(captureOptions['Start'])

            if action == 'Start':
                if startStopButton.text == 'Stop':
                    logger.warn("Capture is already going on IP: {}!! Stopping the current capture and "
                                "starting again.".format(phoneObj.phone_obj.phone_obj.phone.ipAddress))
                    startStopButton.click()
                    self.capturePackets(action='Start', phoneObj=phoneObj, portNumber=portNumber)
                logger.info("Started the capture on extension: " + phoneObj.phone_obj.phone_obj.phone.extensionNumber)
            elif action == 'Stop':
                if startStopButton.text == 'Start':
                    raise Exception("Capture was not running on extension: {} with IP: {}".format(
                                    phoneObj.phone_obj.phone_obj.phone.extensionNumber,
                                    phoneObj.phone_obj.phone_obj.phone.ipAddress))
                else:
                    logger.info('Stopped capture on extension: ' + phoneObj.phone_obj.phone_obj.phone.extensionNumber)
            startStopButton.click()

    def verifyElementIsClickable(self, **kwargs):
        """
        This method is used to verify the passed element is clickable/enabled or not on the web page.

        :param:
            :kwargs:
                :element: Element to verify on the web page.
                :clickable: Verify enabled/not enabled i.e., True to verify element is enabled
                            and False to verify element is not enabled.
        :return: None
        :created by: Vikhyat Sharma
        :creation date: 18/05/2020
        :last update by:
        :last update date:
        """
        element = kwargs['element']
        clickable = str(kwargs['clickable'])

        elementToVerify = self.driver.find_element_by_xpath(element)
        if clickable == 'True':
            if elementToVerify.is_enabled():
                logger.info("The " + self.webUIDetails.keys()[self.webUIDetails.values().index(element)] +
                            " element is enabled on the Web UI.", also_console=True)
            else:
                raise Exception("The " + self.webUIDetails.keys()[self.webUIDetails.values().index(element)] +
                                " element should be enabled but is not enabled.")
        else:
            if not elementToVerify.is_enabled():
                logger.info("The " + self.webUIDetails.keys()[self.webUIDetails.values().index(element)] +
                            " element is not enabled on the Web UI.", also_console=True)
            else:
                raise Exception("The " + self.webUIDetails.keys()[self.webUIDetails.values().index(element)] +
                                " element should not be enabled, but is enabled.")

    def verifyTextNotPresent(self, **kwargs):
        """
        This method is used to verify the passed option is not present on the Web UI of the phone.

        This method should be used if the option is not present anytime on the Web UI. If the option can be
        made available or unavailable on the Web UI, then see method:
            self.verifyElementIsFound or self.verifyElementNotFound

        :param:
            :kwargs:
                :text: Text/Option to Verify on the display

        :return: None
        :created by: Sharma
        :creation date: 14/08/2020
        :last update by:
        :last update date:
        """
        textToVerify = kwargs['text']
        if textToVerify not in self.driver.page_source:
            logger.info("The option: " + textToVerify + " is not present on the Web UI.")
        else:
            raise Exception("The option: " + textToVerify + " is present on the Web UI.")

    def getMACAddress(self, phone):
        """
        This method is used to get the MAC Address of the phone using its WUI.

        :param:
            :phone: Phone of which MAC Address is needed (PhoneComponent Object)

        :return: MAC Address of the phone (String)
        :created by: Sharma
        :creation date: 08/09/2020
        :last updated by:
        :last update date:
        """
        try:
            self.loginWebUI(phone=phone)
            self.goToSection(option='//*[@id="sidebar"]/ul[1]/li[1]/a')
            macAddress = self.driver.find_element_by_xpath('//*[@id="content"]//tr[10]/td[2]').text
            self.LogOff(deleteConfig=False)
            macAddress = macAddress.replace(':', '')
            console(macAddress)
            return macAddress
        except NoSuchElementException as e:
            self.LogOff()
            raise Exception("Not able to find the MAC Address option on the Web UI.")

    def getTextValue(self, element):
        """
            This method is used to get Text value for the webelement
        :param kwargs:
        :return:
        :created by: Milind Patil.
        :creation date: 3/02/2021
        :last update by:
        :last update date:
        """
        try:
            logger.info(element)
            textValue = self.driver.find_element(By.XPATH, element).text
            if len(textValue) == 0:
                textValue = str(self.driver.find_element(By.XPATH, element).get_attribute('value'))
            return textValue
        except:
            console("clearSendKeys EXCEPT")
            self.LogOff()


# //*[@id="details-button"]  advanced
# //*[@id="proceed-link"]    proceed link

#     # position = Select(driver.find_element(By.XPATH, position_path))
#     # position.select_by_visible_text(functionkey)


if __name__ == "__main__":
    # os.system('''start cmd /K cd C:/Program Files/Wireshark
    #           tshark -V -r captureFile.pcap > convertedFile.txt'''.replace('\n', '&'))

    # import win32com.shell.shell as shell

    # ASADMIN = 'asadmin'
    # print sys.argv[-1]
    # print sys.argv[0]
    # if sys.argv[-1] != ASADMIN:
    #     script = os.path.abspath(sys.argv[0])
    #     params = ' '.join([script] + sys.argv[1:] + [ASADMIN])
    #     print params
    #     shell.ShellExecuteEx(lpVerb='runas', lpFile=sys.executable, lpParameters=params)
    #     sys.exit(0)



    # os.chdir("C:/Program Files/Wireshark")
    # os.system('tshark -V -r captureFile.pcap > convertedFile.txt', )\
    # phone_details = {"phoneModel": "Mitel6920", "ipAddress": "10.112.123.146", "extensionNumber": "4165142503",
    #                  "phoneName": "4165142503"}
    # phone_obj = PhoneComponent(**phone_details)
    obj = WebUIComponent()
    # obj.pcap_converter(local_pcap_download_file='C:\Robo_SVN_5.1\Desktop_Automation\lib\captureFile.pcap',
    #                    outputFile='C:\Robo_SVN_5.1\Desktop_Automation\lib\covertedFile.txt')
    obj.loginWebUI(phone='10.112.123.45')
    # obj.goToSection(option='//*[@id="sidebar"]/ul[2]/li[5]/a')
    # obj.doubleClick(option='//*[@id="file0"]', fileName='directoryList.csv')
    # obj.isChecked(value='Checked', option='//*[@id="content"]//tr[24]//input')
    # print(obj.getMACAddress(phone='10.112.123.21'))
    # obj.verifyRegisteredLine(lineToVerify='1', phone='4165142526')
    # obj.registerPhone(linesToRegister='all', phoneToEnter='4165142501', phoneToOpen='4165142501')
    # obj.verifyElementIsFound('//*[@id="content"]/h')
    # print(obj.registerPhone(phone='10.112.123.144', linesToRegister='3', pbx='Asterisk'))
    # obj.verifyRegisteredLine(lineToVerify='3')
    # obj.LogOff()
    # obj.unRegisterPhone(linesToUnregister='1')
    # obj.loginWebUI(phone='10.112.123.155')
    # url = str(obj.driver.current_url)
    # print(type(url))
    # print(url.equals('10.112.123.155'))
    # obj.verifyText(option='//*[@id="header"]/div[2]//li[1]', value="6920")
    # quit()

    # phoneDetails = obj.yaml_file.get('PhoneDetails')
    # for k, v in phoneDetails.items():
    #     print(k, v)
    # SessionNotCreatedException:
    quit()
