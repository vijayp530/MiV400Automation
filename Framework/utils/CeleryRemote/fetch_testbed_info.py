__author__ = 'UKumar'

import sys
import requests
import urllib, base64
import re
import json


#LIST_SWITCH_URL = 'http://10.198.166.27:5478/director/switches/list'
#LIST_PPHONES_URL = 'http://10.198.166.27:5478/director/ip_phones/list'
#LIST_USERS_URL = 'http://10.198.107.18:5478/director/users/list'
#LIST_TENANTS_URL = 'http://10.198.107.18:5478/director/tenants/list'
#LIST_SWITCHES_URL = 'http://10.198.107.18:5478/director/switches/list' #dm/status_switches/switch_calls_list'


class FetchTestbedInfo():

    def __init__(self, hqIp, username, password):
        self.hqIp = hqIp
        self.client = requests.session()
        self.create_connection(hqIp, username, password)

    def create_connection(self, hqIp, username, password):
        """Create connection to HQ
        """
        # Retrieve the CSRF token first
        LOGIN_URL = 'http://'+hqIp+':5478/director/login'
        self.client.get(LOGIN_URL)  # sets cookie
        #print(client.cookies.items())
        d2_cookie = self.client.cookies['_director2_session']
        ##print(d2_cookie)
        csrftoken = re.match('(.+)--',d2_cookie).group(1)
        ##print(csrftoken)
        csrftoken = urllib.unquote(d2_cookie)
        ##print(csrftoken)
        csrftoken = base64.b64decode(csrftoken)
        # csrftoken = r'{I"session_id:EFI"%8cb0cc7d1645b236e217e3e35826b9dd; TI"abc; F{:	hostI"localhost; FI"_csrf_token; FI"1lC0TGuAk9D6C0f68Fy9T8UsQ0RaQg9uXiTRnPra+iLE=; F'
        ##print(csrftoken)
        csrftoken = re.match('.*_csrf_token.*1(.*=).*', csrftoken).group(1)
        ##print(csrftoken)

        # 'admin@mt.com', 'changeme'
        self.client.post(LOGIN_URL,data={"user_session[login_name]": username, "user_session[login_password]": password, "authenticity_token": csrftoken})
        # r = client.get(LIST_SWITCH_URL)

    def fetch_testbed_info_manhattn(self, tbInfoDict):
        """Fetch vUCB name from HQ for Manhattan
        """
        #self.create_connection(tbInfoDict["SITE1_SERVER_ADDR"], tbInfoDict["SITE1_USERNAME"], tbInfoDict["SITE1_PASSWORD"])
        LIST_SWITCH_URL = 'http://'+tbInfoDict["SITE1_SERVER_ADDR"]+':5478/director/switches/list'

        result = self.client.get(LIST_SWITCH_URL)
        d = json.loads(result.text)
        i = 1
        for device in d['rows']:
            if isinstance(device['cell'][0], list):
                tbInfoDict['SITE'+str(i)+'_SERVER_VUCB'] = str(device['cell'][0][1])
        return tbInfoDict

    def fetch_testbed_info_mobility(self, tbInfoDict):
        """Fetch vUCB name from HQ for Mobility
        """
        LIST_SWITCH_URL = 'http://'+tbInfoDict["SITE1_SERVER_ADDR"]+':5478/director/switches/list'

        result = self.client.get(LIST_SWITCH_URL)
        d = json.loads(result.text)
        #print(d)
        for device in d['rows']:
            if isinstance(device['cell'][0], list):
                tbInfoDict['BCO_VSWITCH_UCB_NAME'] = str(device['cell'][0][1])
        return tbInfoDict

    def fetch_phones_manhattn_st(self, phoneIP):
        #self.create_connection(tbInfoDict["SITE1_SERVER_ADDR"], tbInfoDict["SITE1_USERNAME"], tbInfoDict["SITE1_PASSWORD"])
        LIST_PHONES_URL = 'http://'+self.hqIp+':5478/director/ip_phones/list'

        result = self.client.get(LIST_PHONES_URL)
        d = json.loads(result.text)
        #print(d)
        phoneList = []
        for ip in phoneIP:
            for device in d['rows']:
                if ip in device['cell']:
                    phoneList.append(str(device['cell'][0]))

        print(phoneList)
            #if isinstance(device['cell'][0], list):
            #    tbInfoDict['SITE'+str(i)+'_SERVER_VUCB'] = str(device['cell'][0][1])
        return phoneList

    def fetch_tenant_specific_user(self):
        tenantID=25
        #self.create_connection(tbInfoDict["SITE1_SERVER_ADDR"], tbInfoDict["SITE1_USERNAME"], tbInfoDict["SITE1_PASSWORD"])
        #LIST_USERS_URL = 'http://'+tbInfoDict["SITE1_SERVER_ADDR"]+':5478/director/users/list'
        LIST_USERS_URL_NEW = r'http://10.198.107.18:5478/director/users/list?filters=%7B%22groupOp%22%3A%22OR%22%2C%22rules%22%3A%5B%7B%22field%22%3A%22TenantID%22%2C%22op%22%3A%22eq%22%2C%22data%22%3A%22'+str(tenantID)+r'%22%7D%5D%7D'
        print(LIST_USERS_URL_NEW)
        result = self.client.get(LIST_USERS_URL_NEW)
        d = json.loads(result.text)
        print(d)
        i = 1
        for device in d['rows']:
            print(device['cell'])
            print(device['id'])
        #return tbInfoDict

    def get_specific_tenants(self, ip, username, password, tenantNames):
        info = self.fetch_tenants_info(ip, username, password)
        specificTenants = []
        tenantNamesList = tenantNames.split(",")
        for tname in tenantNamesList:
            for tinfo in info:
                if tname.lstrip(" '").rstrip("'") == tinfo[0]:
                    specificTenants.append(tinfo)
                    break
        print("ok",specificTenants)
        return specificTenants

    def fetch_phones_mt(self, ip):
        #self.create_connection(tbInfoDict["SITE1_SERVER_ADDR"], tbInfoDict["SITE1_USERNAME"], tbInfoDict["SITE1_PASSWORD"])
        #LIST_PHONES_URL = 'http://'+ip+':5478/director/ip_phones/list'
        tenantID = 25

        LIST_PHONES_URL = r'http://'+ip+':5478/director/ip_phones/list?filters=%7B%22groupOp%22%3A%22OR%22%2C%22rules%22%3A%5B%7B%22field%22%3A%22TenantID%22%2C%22op%22%3A%22eq%22%2C%22data%22%3A%22'+str(tenantID)+r'%22%7D%5D%7D'

        result = self.client.get(LIST_PHONES_URL)
        d = json.loads(result.text)
        #print(d)
        for device in d['rows']:
            print(device['cell'])
        # phoneList = []
        # for ip in phoneIP:
        #     for device in d['rows']:
        #         if ip in device['cell']:
        #             phoneList.append(str(device['cell'][0]))
        #
        # print(phoneList)
        #     #if isinstance(device['cell'][0], list):
        #     #    tbInfoDict['SITE'+str(i)+'_SERVER_VUCB'] = str(device['cell'][0][1])
        # return phoneList

    def get_did(self, ip):
        LIST_USER_URL = "http://10.198.107.18:5478/director/users/953.json"
        result = self.client.get(LIST_USER_URL)
        d = json.loads(result.text)
        print(d['user']['dn_attributes']['DID'])

    def get_irn(self, ip):
        #LIST_USER_URL = "http://10.198.107.18:5478/director/route_points/list"
        tenantID = 70
        LIST_USER_URL = r'http://'+ip+':5478/director/route_points/list?filters=%7B%22groupOp%22%3A%22OR%22%2C%22rules%22%3A%5B%7B%22field%22%3A%22TenantID%22%2C%22op%22%3A%22eq%22%2C%22data%22%3A%22'+str(tenantID)+r'%22%7D%5D%7D'
        result = self.client.get(LIST_USER_URL)
        d = json.loads(result.text)
        for device in d['rows']:
            print(device['cell'])

    def get_system(self):
        #LIST_USER_URL = "http://10.198.107.18:5478/director/director_system_extensions/list"
        LIST_USER_URL = "http://10.198.107.18:5478/director/system_extensions.json"
        print(LIST_USER_URL)

        result = self.client.get(LIST_USER_URL)

        d = json.loads(result.text)

        print("baa: ", str(d['system_extensions']['backup_aa_dn']['DN']))
        print("aa: ",str(d['system_extensions']['aa_dn']['DN']))
        print("vm: ", str(d['system_extensions']['vm_broadcast_dn']['DN']))
        print("vmlogin: ", str(d['system_extensions']['vm_login_dn']['DN']))
        print("acs: ", str(d['system_extensions']['account_code_dn']['DN']))
        print("ucb: ", str(d['system_extensions']['make_me_conference_dn']['DN']))

    def fetch_switches(self, ip):
        LIST_SWITCH_URL = 'http://'+ip+':5478/director/switches/list'

        result = self.client.get(LIST_SWITCH_URL)
        d = json.loads(result.text)
        #print(d)
        for device in d['rows']:
            print(device['cell'])




if __name__ == "__main__":
    fo = FetchTestbedInfo("10.198.107.18", "admin@mt.com", "changeme")
    #fo.get_did("10.198.107.18")
    fo.fetch_switches("10.198.107.18")
    #fo.fetch_tenant_specific_user()
    #fo.fetch_phones_mt("10.198.107.18")
    #fo.fetch_testbed_ifo_manhattn_st({"SITE1_SERVER_ADDR":"10.198.107.18", "SITE1_USERNAME":"admin@mt.com", "SITE1_PASSWORD":"changeme"})
    #fo.fetch_users({"SITE1_SERVER_ADDR":"10.198.107.18", "MT_DEFAULT_TENANT_ID":"24"})

    #fo.fetch_phones_manhattn_st({"SITE1_SERVER_ADDR":"10.198.166.44", "SITE1_USERNAME":"admin", "SITE1_PASSWORD":"changeme"})

    ##r = client.get(LIST_PPHONES_URL)
    ##print(r.text)

    ##d = json.loads(r.text)
    # print(d['rows'][0]['cell']10.)
    ##for device in d['rows']:
    ##    print([ device['cell'][i] for i in [0, 4] ])
