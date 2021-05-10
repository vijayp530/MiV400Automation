import sys
import os

#sys.path.append('..\\utils')
#sys.path.append('..\\page')
sys.path.append('..\\')
from base import LocalBrowser
from page.BOSSComponent import BossPage

class GenMap(object):

    def __init__(self, **params):
        self.browsertype = params.get('browser', 'chrome').lower()
        self._browser = LocalBrowser(self.browsertype)
        self.boss_page = BossPage(self._browser)

    def parse_page(self, url):
        ele_list = []
        self.boss_page.commonfunctionality.open_url(url)
        self.boss_page.commonfunctionality.client_login("vsam@shoretel.com" ,"Shoretel1$")
        #self.driver.get(url)
        #web_elements_id= self._browser._browser.find_elements_by_xpath("//*[@id]")
        web_elements_id = self._browser._browser.find_elements_by_xpath("*//input")
        file=open(r'.\\home.map','w')
        for ele in web_elements_id:
            text = ele.text
            print(text)
            eleTag = ele.tag_name
            absolutepath=''
            if ele.get_attribute('id') == '':
                ele1 = ele.find_element_by_xpath("..")
                while (ele1.get_attribute('id') == ''):
                    ele1 = ele1.find_element_by_xpath("..")
                    absolutepath += '/'+ele.tag_name
                parTag = ele1.tag_name
                idEle = ele1.get_attribute('id')
                printabletext = eleTag + '#xpath#' + '//' + parTag + '[id="' + idEle + '"]/'+absolutepath+'/' + eleTag + '[contains(text(),"' + text + '")]'
                print(printabletext)
            else:
                eleId=ele.get_attribute('id')
                line=eleId+'==input#id#'+eleId+'\n'
                file.write(line)

if __name__ == '__main__':
    genmap = GenMap()
    genmap.parse_page(
        'http://m5dbweb-qa.m5colo.local/Person/AddPersonWizard?accountId=11442&locationId=-1&partitionId=93&personId=-1&copyFromPersonId=-1&_=1488451255473')

    #genmap.parse_page('http://m5dbweb-qa.m5colo.local/Account/Users?accountId=1&locationId=-1&profileId=18&personId=5&partitionId=1')
