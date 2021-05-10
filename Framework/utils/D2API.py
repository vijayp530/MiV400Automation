"""
This module provides helping methods to get and set data to D2.
Author: Nitin Kumar and Shankar Narayanan M
"""


import sys, os, datetime
import requests
import urllib, base64
import re
import json
from threading import Thread
import logging
log = logging.getLogger("d2API")
import time

def decorator_get_specific_tenants(func):
    def wrapper_get_specific_tenants(self, tenantNames):
        if self.BOSS_Auto:
            tList = []
            tList1 = [[]]
            tList1.append(tenantNames.strip())
            tList.append(tList1)
            return tList
        else:
            return func(self, tenantNames)
    return wrapper_get_specific_tenants


class D2API():

    def __init__(self, ip,  username, password, boss_auto=False):
        self.BOSS_Auto = boss_auto
        self.client = requests.session()

        if ":" in ip:
            ip_split = ip.split(":")
            self.ip = ip_split[0]
            self.pno = ip_split[-1]
        else:
            self.ip = ip
            self.pno = '5478'
        self.create_connection(self.ip, self.pno, username, password)

    def create_connection(self, hqIp, pno, username, password):
        """
        """
        # Retrieving the CSRF token
        LOGIN_URL = 'http://'+hqIp+':'+pno+'/director/login'
        r = self.client.get(LOGIN_URL)  # sets cookie
        try:
            d2_cookie = self.client.cookies['_director2_session']
            csrftoken = urllib.unquote(d2_cookie)
            csrftoken = base64.b64decode(csrftoken)
            csrftoken = re.match('.*_csrf_token.*\"1(.*=).*', csrftoken).group(1)
        except:
            # for upgraded D2 -> Automation support for Rails 4 Upgrade
            csrftoken = re.search(r'meta name="csrf-token" content="([\d\D]+?)"', r.text).group(1)
        self.token = csrftoken
        self.client.post(LOGIN_URL,data={"user_session[login_name]": username, "user_session[login_password]": password, "authenticity_token": csrftoken})
        self.username = username
        self.password = password

        # t = Thread(target=self.refreshToken)
        # t.daemon = True;
        # t.start()

        trRefreshConnection = Thread(target=self.refreshConnection)
        trRefreshConnection.daemon = True
        trRefreshConnection.start()

        # r = client.get(LIST_SWITCH_URL)

    def refreshToken(self):
        # while True:
        #     refreshURL = 'http://'+self.ip+':'+self.pno+'/director/renew-ticket'
        #     resp = self.client.get(refreshURL)
        #     # print("Refreshed" + str (resp.status_code)+ resp.content)
        #     TickURL = 'http://'+self.ip+':'+self.pno+'/director/ticket?client_time_now_utc='+str(time.time()).replace('.','')
        #     resp = self.client.get(TickURL)
        #     # print("Send time" + str (resp.status_code) + resp.content)
        #     time.sleep(600)
        try:
            while True:
                refreshURL = 'http://'+self.ip+':'+self.pno+'/dm/dashboard/chart_data?interval=one-hour&charts%5B%5D=call_volume_chart&software=&pageid=1'
                resp = self.client.get(refreshURL)
                time.sleep(60)
        except:
            pass


    def refreshConnection(self):
        try:
            while True:
                # print("Connection Refreshed" + time.ctime())
                LOGIN_URL = 'http://'+self.ip+':'+self.pno+'/director/login'
                self.client.get(LOGIN_URL)
                self.client.post(LOGIN_URL,data={"user_session[login_name]": self.username, "user_session[login_password]": self.password, "authenticity_token": self.token})
                time.sleep(1200)
        except:
            pass


    def fetch_tenants_info(self):
        """
        """
        #self.create_connection(ip, username, password)
        LIST_TENANTS_URL = 'http://'+self.ip+':'+self.pno+'/director/tenants/list?_search=false&rows=600'
        result = self.client.get(LIST_TENANTS_URL)

        d = json.loads(result.text)
        tInfo = []
        for device in d['rows']:
            tmpList = [str(device['cell'][0]), str(device['cell'][1]), str(device['cell'][2])]
            tInfo.append(tmpList)
        tInfo.pop(0)
        return tInfo

    @decorator_get_specific_tenants
    def get_specific_tenants(self, tenantNames):
        info = self.fetch_tenants_info()
        specificTenants = []
        tenantNamesList = tenantNames.split(",")
        for tname in tenantNamesList:
            for tinfo in info:
                if tname.lstrip(" '").rstrip("'") == tinfo[0]:
                    specificTenants.append(tinfo)
                    break
        print("ok",specificTenants)
        return specificTenants

    def fetch_tenant_specific_sites(self, tenantNames):
        tList = self.get_specific_tenants(tenantNames)
        sites = []
        for tenant in tList:
            LIST_USERS_URL_NEW = r'http://'+self.ip+':'+self.pno+'/director/sites/list?filters=%7B%22groupOp%22%3A%22OR%22%2C%22rules%22%3A%5B%7B%22field%22%3A%22TenantID%22%2C%22op%22%3A%22eq%22%2C%22data%22%3A%22'+str(tenant[1])+r'%22%7D%5D%7D'
            print(LIST_USERS_URL_NEW)
            result = self.client.get(LIST_USERS_URL_NEW)
            d = json.loads(result.text)
            print(d)
            for userData in d['rows']:
                sites.append(str(userData['cell'][0]))
        print("sites from specific : ", sites)
        return sites

    def fetch_tenant_specific_hunt_group(self, tenantNames):
        tList = self.get_specific_tenants(tenantNames.strip('"'))
        #LIST_USERS_URL = 'http://'+ip+':'+self.pno+'/director/users/list'
        hunt_group = []
        for tenant in tList:
            LIST_USERS_URL_NEW = r'http://'+self.ip+':'+self.pno+'/director/hunt_groups/list?list=hunt_group&rows=1000&_filter_tenant_id='+str(tenant[1])+r'&_filter_system_tenant_id='+str(tenant[1])+r''
            print(LIST_USERS_URL_NEW)
            result = self.client.get(LIST_USERS_URL_NEW)
            d = json.loads(result.text)
            print(d)
            for userData in d['rows']:
                hunt_group.append((str(userData['id']),str(userData['cell'][0]), str(userData['cell'][1]).split('-')[-1]))
        print("hunt_group from specific : ", hunt_group)
        return hunt_group

    def fetch_tenant_specific_hunt_group_member(self, tenantNames, hunt_group_extension):

        hunt_groups = self.fetch_tenant_specific_hunt_group(tenantNames)
        #hunt_group_member = []
        id=0
        for hgmember in hunt_groups:
            if hunt_group_extension==hgmember[2]:
                id = hgmember[0]
                print((id))
                break
        specific_hg_url = 'http://'+self.ip+':'+self.pno+'/director/hunt_groups/'+id+'.json'
        print(specific_hg_url)
        result = self.client.get(specific_hg_url)
        d = json.loads(result.text)
        print(d)
        for key, value in d['hunt_group'].items():
            if key == "selected_hunt_group_members":
                print(value)
                print("hunt group member details : ", value)
                return value
        return False

    def fetch_tenant_specific_pickup_group(self, tenantNames):
        tList = self.get_specific_tenants(tenantNames.strip('"'))
        # LIST_USERS_URL = 'http://'+ip+':'+self.pno+'/director/users/list'
        pickup_group = []
        for tenant in tList:
            LIST_USERS_URL_NEW = r'http://'+self.ip+':'+self.pno+'/director/group_pickups/list?rows=1000&_filter_tenant_id='+str(tenant[1])+r'&_filter_system_tenant_id='+str(tenant[1])+r''
            print(LIST_USERS_URL_NEW)
            result = self.client.get(LIST_USERS_URL_NEW)
            d = json.loads(result.text)
            print(d)
            for userData in d['rows']:
                pickup_group.append((str(userData['cell'][0]), str(userData['cell'][1]).split('-')[-1]))
        print("pickup_group from specific : ", pickup_group)
        return pickup_group

    def fetch_tenant_specific_auto_attendant(self,tenantNames):
        tenantNames = tenantNames.strip('"')
        tList = self.get_specific_tenants(tenantNames)
        auto_attendant=[]
        for tenant in tList:
            LIST_USERS_URL_NEW = r'http://'+self.ip+':'+self.pno+'/director/menus/list?rows=1000&_filter_tenant_id='+str(tenant[1])+r'&_filter_system_tenant_id='+str(tenant[1])+r''
            #print(LIST_USERS_URL_NEW)
            result = self.client.get(LIST_USERS_URL_NEW)
            d = json.loads(result.text)
            #print(d)
            for userData in d['rows']:
                auto_attendant.append((str(userData['cell'][0]), str(userData['cell'][1]).split('-')[-1]))
            print("auto_attendant from specific : ", auto_attendant)
            return auto_attendant

    def fetch_tenant_specific_page_group(self,tenantNames):
        tenantNames = tenantNames.strip('"')
        tList = self.get_specific_tenants(tenantNames)
        paging_groups=[]
        for tenant in tList:
            #LIST_USERS_URL_NEW=r'http://'+self.ip+':'+self.pno+'/director/paging_groups/list?_search=true&nd=1495616642261&rows=50&page=1&sidx=&sord=asc&filters=%7B%22groupOp%22%3A%22OR%22%2C%22rules%22%3A%5B%7B%22field%22%3A%22TenantID%22%2C%22op%22%3A%22eq%22%2C%22data%22%3A%'+str(tenant[1])+r'%22%7D%5D%7D'
            LIST_USERS_URL_NEW = r'http://'+self.ip+':'+self.pno+'/director/paging_groups/list?rows=1000&_filter_tenant_id='+str(tenant[1])+r'&_filter_system_tenant_id='+str(tenant[1])+r''
            result = self.client.get(LIST_USERS_URL_NEW)
            d = json.loads(result.text)
            for userData in d['rows']:
                paging_groups.append((str(userData['cell'][0]), str(userData['cell'][1]).split('-')[-1]))
            print("auto_attendant from specific : ",paging_groups)
            return paging_groups

    def fetch_tenant_specific_custom_schedule(self, tenantNames):
        tList = self.get_specific_tenants(tenantNames.strip('"'))
        #LIST_USERS_URL = 'http://'+ip+':'+self.pno+'/director/users/list'
        custom_schedule = []
        for tenant in tList:
            LIST_USERS_URL_NEW =r'http://'+self.ip+':'+self.pno+'/director/schedules_customs/list?rows=1000&_filter_tenant_id='+str(tenant[1])+r'&_filter_system_tenant_id='+str(tenant[1])+r''
            print(LIST_USERS_URL_NEW)
            result = self.client.get(LIST_USERS_URL_NEW)
            d = json.loads(result.text)
            print(d)
            for userData in d['rows']:
                custom_schedule.append(str(userData['cell'][0]))
        print("custom_schedule from specific : ", custom_schedule)
        return custom_schedule

    def fetch_tenant_specific_holiday_schedule(self, tenantNames):
        tList = self.get_specific_tenants(tenantNames.strip('"'))
        #LIST_USERS_URL = 'http://'+ip+':'+self.pno+'/director/users/list'
        holiday_schedule = []
        for tenant in tList:
            LIST_USERS_URL_NEW =r'http://'+self.ip+':'+self.pno+'/director/schedules_holidays/list?rows=1000&_filter_tenant_id='+str(tenant[1])+r'&_filter_system_tenant_id='+str(tenant[1])+r''
            print(LIST_USERS_URL_NEW)
            result = self.client.get(LIST_USERS_URL_NEW)
            d = json.loads(result.text)
            print(d)
            for userData in d['rows']:
                holiday_schedule.append((str(userData['cell'][0]), str(userData['cell'][1]), str(userData['cell'][2])))
        print("Holiday schedule from specific : ", holiday_schedule)
        return holiday_schedule

    def fetch_tenant_specific_Extension_List(self,tenantNames):
        tenantNames = tenantNames.strip('"')
        tList = self.get_specific_tenants(tenantNames)
        extension_List=[]
        for tenant in tList:
            LIST_USERS_URL_NEW=r'http://'+self.ip+':'+self.pno+'/director/extension_lists/list?rows=1000&_filter_tenant_id='+str(tenant[1])+r'&_filter_system_tenant_id='+str(tenant[1])+r''
            result = self.client.get(LIST_USERS_URL_NEW)
            d = json.loads(result.text)
            for userData in d['rows']:
                extension_List.append(str(userData['cell'][0]))
            print("Extension List from specific : ",extension_List)
            return extension_List

    def fetch_tenant_specific_on_hours_schedule(self, tenantNames):
        tList = self.get_specific_tenants(tenantNames.strip('"'))
        # LIST_USERS_URL = 'http://'+ip+':'+self.pno+'/director/users/list'
        on_hours_schedule = []
        for tenant in tList:
            list_users_url_new = r'http://' + self.ip + ':'+self.pno+'/director/schedules_on_hours/list?rows=1000&_filter_tenant_id=' + str(
                tenant[1]) + r'&_filter_system_tenant_id=' + str(tenant[1]) + r''
            print(list_users_url_new)
            result = self.client.get(list_users_url_new)
            d = json.loads(result.text)
            print(d)
            for userData in d['rows']:
                on_hours_schedule.append(str(userData['cell'][0]))
        print("on_hours_schedule from specific : ", on_hours_schedule)
        return on_hours_schedule

    def fetch_tenant_specific_users(self, tenantNames):
        tList = self.get_specific_tenants(tenantNames.strip('"'))
        #LIST_USERS_URL = 'http://'+ip+':'+self.pno+'/director/users/list'
        user = []
        for tenant in tList:
            LIST_USERS_URL_NEW =r'http://'+self.ip+':'+self.pno+'/director/users/list?&rows=1000&_filter_tenant_id='+str(tenant[1])+r''
            print(LIST_USERS_URL_NEW)
            result = self.client.get(LIST_USERS_URL_NEW)
            print(result)
            d = json.loads(result.text)
            print(d)

            for userData in d['rows']:
                user.append((str(userData['cell'][4]), str(userData['cell'][2]).split('-')[-1]))
        print("user from specific Tenant : ", user)
        return user

    def fetch_user_DNId(self, tenantNames, user_business_email):
        tList = self.get_specific_tenants(tenantNames.strip('"'))
        d = {}
        userdnid = None
        for tenant in tList:
            # Get the users info
            LIST_USERS_URL_NEW = r'http://' + self.ip + ':' + self.pno + '/director/users/list?_filter_tenant_id=' + str(
                tenant[1]) + r''
            print LIST_USERS_URL_NEW
            result = self.client.get(LIST_USERS_URL_NEW)
            # print result
            d = json.loads(result.text)
            # print d
        # get the UserDNID
        for userData in d['rows']:
            if user_business_email == str(userData['cell'][4]):
                userdnid = str(userData["id"])
                break
        return userdnid

    def fetch_complete_user_info(self, userdnid):
        user_info = {}
        # Get the user specific info
        USER_INFO_URL = r'http://' + self.ip + ':' + self.pno + '/director/users/' + str(userdnid) + r'.json' + r''
        print USER_INFO_URL
        result = self.client.get(USER_INFO_URL)
        user_info = json.loads(result.text)
        return user_info

    def fetch_tenant_specific_user_groups(self,tenantNames):
        tenantNames = tenantNames.strip('"')
        tList = self.get_specific_tenants(tenantNames)
        ug_List=[]
        for tenant in tList:
            LIST_USERS_URL_NEW=r'http://'+self.ip+':'+self.pno+'/director/user_groups/list?&rows=1000&_filter_tenant_id='+str(tenant[1])+r''
            result = self.client.get(LIST_USERS_URL_NEW)
            d = json.loads(result.text)
            for ugData in d['rows']:
                ug_List.append(str(ugData['cell'][0]))
            print("User Group from specific Tenant: ",ug_List)
            return ug_List

    def fetch_tenant_specific_cost(self,tenantNames):
        tenantNames = tenantNames.strip('"')
        tList = self.get_specific_tenants(tenantNames)
        cost_List=[]
        for tenant in tList:
            LIST_USERS_URL_NEW=r'http://'+self.ip+':'+self.pno+'/director/costs/list?&rows=1000&_filter_tenant_id='+str(tenant[1])+r''
            result = self.client.get(LIST_USERS_URL_NEW)
            d = json.loads(result.text)
            for costData in d['rows']:
                cost_List.append(str(costData['cell'][0]))
            print("COST from specific Tenant: ",cost_List)
            return cost_List

    def fetch_tenant_specific_coscp(self,tenantNames):
        tenantNames = tenantNames.strip('"')
        tList = self.get_specific_tenants(tenantNames)
        coscp_List=[]
        for tenant in tList:
            LIST_USERS_URL_NEW=r'http://'+self.ip+':'+self.pno+'/director/coscps/list?&rows=1000&_filter_tenant_id='+str(tenant[1])+r''
            result = self.client.get(LIST_USERS_URL_NEW)
            d = json.loads(result.text)
            for coscpData in d['rows']:
                coscp_List.append(str(coscpData['cell'][0]))
            print("COSCP from specific Tenant: ",coscp_List)
            return coscp_List

    def fetch_tenant_specific_cosv(self,tenantNames):
        tenantNames = tenantNames.strip('"')
        tList = self.get_specific_tenants(tenantNames)
        cosv_List=[]
        for tenant in tList:
            LIST_USERS_URL_NEW=r'http://'+self.ip+':'+self.pno+'/director/cosvms/list?&rows=1000&_filter_tenant_id='+str(tenant[1])+r''
            result = self.client.get(LIST_USERS_URL_NEW)
            #print(result)
            d = json.loads(result.text)
            #print(d)
            for cosvData in d['rows']:
                cosv_List.append(str(cosvData['cell'][0]))
            print("COSV from specific Tenant: ",cosv_List)
            return cosv_List

    def fetch_switch_info(self):
        """
        """
        LIST_SWITCH_URL = 'http://' + self.ip + ':'+self.pno+'/dm/status_switches/switch_status_list'
        swresult = self.client.get(LIST_SWITCH_URL)
        d = json.loads(swresult.text)
        #print(d['data']['aaData'])
        sInfo = []
        for device in d['data']['aaData']:
            tmpList = [str(device[2]), str(device[3]), str(device[5]),str(device[7]),str(device[15]),str(device[16])]
            sInfo.append(tmpList)
        return sInfo

    def fetch_tenant_specific_bridged_call_appearance(self, tenantNames):
        tenantNames = tenantNames.strip('"')
        tList = self.get_specific_tenants(tenantNames)
        Bca = []
        for tenant in tList:
            LIST_USERS_URL_NEW = r'http://'+self.ip+':'+self.pno+'/director/bridged_call_appearances/list?rows=1000&_filter_tenant_id='+str(tenant[1])+r'&_filter_system_tenant_id='+str(tenant[1])+r''
            result = self.client.get(LIST_USERS_URL_NEW)
            d = json.loads(result.text)
            for userData in d['rows']:
                Bca.append(str(userData['cell'][0]))
            print("BCA from specific Tenant : ", Bca)
            return Bca

    def fetch_tenant_specific_dnis(self, tenantNames):
        tenantNames = tenantNames.strip('"')
        tList = self.get_specific_tenants(tenantNames)
        dnis = []
        for tenant in tList:
            LIST_DNIS_MAP = r'http://'+self.ip+':'+self.pno+'/director/dnis/list?rows=1000&_filter_tenant_id='+str(tenant[1])+r'&_filter_system_tenant_id='+str(tenant[1])+r''
            result = self.client.get(LIST_DNIS_MAP)
            d = json.loads(result.text)
            for userData in d['rows']:
                dnis.append(str(userData['cell'][1]))
            print("DNIS from specific Tenant : ", dnis)
            return dnis

    def fetch_tenant_specific_moh(self, tenantNames):
        tList = self.get_specific_tenants(tenantNames.strip('"'))
        #LIST_USERS_URL = 'http://'+ip+':'+self.pno+'/director/users/list'
        moh = []
        for tenant in tList:
            LIST_USERS_URL_NEW = r'http://'+self.ip+':'+self.pno+'/director/moh_resources/list?&rows=1000&_filter_tenant_id='+str(tenant[1])+r'&_filter_system_tenant_id='+str(tenant[1])+r''
            print(LIST_USERS_URL_NEW)
            result = self.client.get(LIST_USERS_URL_NEW)
            d = json.loads(result.text)
            print(d)
            for userData in d['rows']:
                moh.append(str(userData['cell'][0]))
        print("Music On Hold from specific : ", moh)
        return moh


    def fetch_tenant_specific_AccountCodes(self,tenantNames):
        tenantNames = tenantNames.strip('"')
        tList = self.get_specific_tenants(tenantNames)
        account_codes=[]
        for tenant in tList:
            LIST_USERS_URL_NEW = r'http://'+self.ip+':'+self.pno+'/director/account_codes/list?&rows=1000&_filter_tenant_id='+str(tenant[1])+r'&_filter_system_tenant_id='+str(tenant[1])+r''
            result = self.client.get(LIST_USERS_URL_NEW)
            d = json.loads(result.text)
            for userData in d['rows']:
                account_codes.append(str(userData['cell'][1]))
            print("Account Codes from specific : ",account_codes)
            return account_codes

    def fetch_im_switch_info(self):
        """
        """
        # self.create_connection(ip, username, password)

        LIST_SWITCH_URL = 'http://' + self.ip + ':'+self.pno+'/dm/status_ims/ucb_status_list'
        swresult = self.client.get(LIST_SWITCH_URL)
        d = json.loads(swresult.text)
        # print(d['data']['aaData'])
        sInfo = []
        for device in d['data']['aaData']:
            # print(device)
            tmpList = [str(device[1]), str(device[2]), str(device[3]), str(device[4])]
            sInfo.append(tmpList)
        return sInfo

    def fetch_ip_phone_info(self, phonemac):
        """
        """
        # self.create_connection(ip, username, password)

        LIST_SWITCH_URL = 'http://' + self.ip + ':'+self.pno+'/dm/status_ip_phones/ip_phones_status_list'
        swresult = self.client.get(LIST_SWITCH_URL)
        d = json.loads(swresult.text)
        #print(d)

        sInfo = []
        for device in d['data']['aaData']:
            phonemac1=re.sub('[^0-9A-F]+','',str(device[3]))
            if phonemac1 == phonemac:
                tmpList = [str(device[1]), str(device[2]), str(device[3]), str(device[4]), str(device[5]),
                           str(device[6]), str(device[7]), str(device[8]), str(device[9])]
                sInfo.append(tmpList)
        return sInfo

    def fetch_audio_web_switch_info(self):
        """
        """

        LIST_SWITCH_URL = 'http://' + self.ip + ':'+self.pno+'/dm/status_audio_web_confs/ucb_status_list'
        swresult = self.client.get(LIST_SWITCH_URL)
        d = json.loads(swresult.text)

        sInfo = []
        for device in d['data']['aaData']:
            tmpList = [str(device[1]), str(device[2]), str(device[3]), str(device[4])]
            sInfo.append(tmpList)

        return sInfo

    def fetch_calls_info(self):

        """
        """
        call_counts = {}
        LIST_SWITCH_URL = r'http://' + self.ip + ':'+self.pno+'/dm/call_quality_reports/call_quality_data'
        swresult = self.client.get(LIST_SWITCH_URL)
        d = json.loads(swresult.text)

        sInfo = []
        for device in d['data']['aaData']:
            tmpList = [str(device[1]), str(device[2]), str(device[6]), str(device[11])]
            sInfo.append(tmpList)
            call_counts[str(device[2])] = call_counts.get(str(device[2]), 0) + 1

        return sInfo, call_counts

    def fetch_call_details(self, call_id):

        """
        """
        LIST_SWITCH_URL = 'http://' + self.ip + ':'+self.pno+'/dm/call_quality_reports/stream_details?call_guid=' + call_id
        # modified signature as below
        # LIST_SWITCH_URL = "http://10.196.7.180:5478/dm/call_quality_reports/stream_details?call_guid=00300000aaf5e43a464005056b61f22&pair_id=19189&id=45"
        swresult = self.client.get(LIST_SWITCH_URL)
        d1 = json.loads(swresult.text)

        sInfo = []
        for device in d1['data']['aaData']:
            tmpList = [str(device[1]), str(device[2]), str(device[3]), str(device[4])]
            sInfo.append(tmpList)

        return sInfo

    def fetch_switch_specific_call_info(self):
        """
        """

        LIST_SWITCH_URL = r'http://' + self.ip + ':'+self.pno+'/dm/status_audio_web_confs/ucb_calls_list'
        swresult = self.client.get(LIST_SWITCH_URL)
        d = json.loads(swresult.text)
        sInfo = []
        for device in d['data']['aaData']:
            # print(device)
            tmpList = [str(device[1]), str(device[2]), str(device[3]), str(device[4]), str(device[5]), str(device[6]),
                       str(device[7]), str(device[8]), str(device[9])]
            sInfo.append(tmpList)
        return sInfo

    def fetch_ip_phone_specific_call_info(self, phonemac):
        """
        """
        # self.create_connection(ip, username, password)

        LIST_SWITCH_URL = r'http://' + self.ip + ':'+self.pno+'/dm/status_ip_phones/ip_phone_calls_list?mac_address=' + phonemac + r''
        swresult = self.client.get(LIST_SWITCH_URL)
        d = json.loads(swresult.text)
        #print(d['data']['aaData'])

        sInfo = []
        for device in d['data']['aaData']:
            # print(device)
            tmpList = [str(device[1]), str(device[2]), str(device[3]), str(device[4]), str(device[5]), str(device[6]),
                       str(device[7]), str(device[8]), str(device[9])]
            sInfo.append(tmpList)
        return sInfo


    def add_did_ranges(self,trunkgrpid, basephno, nophonenum):
        ADD_URL='http://'+self.ip+':'+self.pno+'/director/did_ranges.json'
        JSON_DATA={ "did_range":{"NumPhoneNumbers":nophonenum,"TrunkGroupID":trunkgrpid,"base_phone_number_input_formatted":basephno,"site_id":1,"num_of_digits_from_co":12}}
        #self.refreshToken()
        result = self.client.post(ADD_URL,json=JSON_DATA)
        d = json.loads(result.text)
        return d

    def get_did_ranges(self):
        GET_URL='http://'+self.ip+':'+self.pno+'/director/did_ranges/list'
        #self.refreshToken()
        result = self.client.get(GET_URL)
        d = json.loads(result.text)
        return d

    def get_did_range_data(self):
        GET_URL='http://'+self.ip+':'+self.pno+'/director/users/get_did_range_data'
        #self.refreshToken()
        result = self.client.get(GET_URL)
        d = json.loads(result.text)
        return d

    def delete_did_ranges(self,didrangeid):
        DELETE_URL='http://'+self.ip+':'+self.pno+'/director/did_ranges/'+didrangeid+'.json'
        #self.refreshToken()
        result = self.client.delete(DELETE_URL)
        d = json.loads(result.text)
        return d

    def add_trunk_groups(self,trunkgrpname, destinationdn):
        ADD_URL='http://'+self.ip+':'+self.pno+'/director/trunk_groups.json'
        JSON_DATA={"collections":{"countries":[]},"trunk_group":{"AccessCode":"T","AreaCode":"408","TenantID":1,"TrunkGroupName":trunkgrpname,"TrunkTypeID":6,"SiteID":1,"TS911":"true","num_digits_from_co":"12","destination_dn_formatted":destinationdn,"Outgoing":"true"},"new_tg":"false","$resolved":"true","new_record":"true"}
        #self.refreshToken()
        result = self.client.post(ADD_URL,json=JSON_DATA)
        d = json.loads(result.text)
        return d

    def get_trunk_groups(self):
        GET_URL='http://'+self.ip+':'+self.pno+'/director/trunk_groups/list'
        #self.refreshToken()
        result = self.client.get(GET_URL)
        d = json.loads(result.text)
        return d

    def delete_trunk_groups(self,trunkgrpid):
        DELETE_URL='http://'+self.ip+':'+self.pno+'/director/trunk_groups/'+trunkgrpid+'.json'
        #self.refreshToken()
        result = self.client.delete(DELETE_URL)
        d = json.loads(result.text)
        return d

    def fetch_site_info(self):
        """
        """
        # self.create_connection(ip, username, password)
        #self.refreshToken()
        LIST_SITE_URL = 'http://' + self.ip + ':'+self.pno+'/dm/status_sites/site_status_list'
        siteresult = self.client.get(LIST_SITE_URL)
        d = json.loads(siteresult.text)
        # print(d['data']['aaData'])
        sInfo = []
        for device in d['data']['aaData']:
            # print(device)
            tmpList = [str(device[1]), str(device[4]), str(device[12])]
            sInfo.append(tmpList)
        return sInfo

    def fetch_server_info(self):
        """
        """
        #self.refreshToken()
        # self.create_connection(ip, username, password)
        LIST_SERVER_URL = 'http://' + self.ip + ':'+self.pno+'/dm//status_servers/server_status_list'
        srresult = self.client.get(LIST_SERVER_URL)
        d = json.loads(srresult.text)
        # print(d['data']['aaData'])
        sInfo = []
        for device in d['data']['aaData']:
            # print(device)
            tmpList = [str(device[1]), str(device[2]), str(device[3]), str(device[5]), str(device[6]), str(device[7])]
            sInfo.append(tmpList)
        return sInfo

    def fetch_ipphone_info(self):
        """
        """
        # self.create_connection(ip, username, password)
        #self.refreshToken()
        LIST_IPPHONE_URL = 'http://' + self.ip + ':'+self.pno+'/dm/status_ip_phones/ip_phones_status_list'
        ipphoneresult = self.client.get(LIST_IPPHONE_URL)
        d = json.loads(ipphoneresult.text)
        print(d)
        # print(d['data']['aaData'])
        sInfo = []
        for device in d['data']['aaData']:
            # print(device)
            tmpList = [str(device[1]), str(device[5]), str(device[6]), str(device[8]), str(device[9]), str(device[11]),
                       str(device[12]), str(device[20])]
            sInfo.append(tmpList)
        return sInfo

    def fetch_voicemail_server_info(self):
        #self.refreshToken()
        VOICEMAIL_URL = 'http://' + self.ip + ':'+self.pno+'/dm/status_voice_mail_servers/vm_server_status_list'
        result = self.client.get(VOICEMAIL_URL)
        json_result = json.loads(result.text)
        vm_server_info = []
        for vm_row in json_result['data']['aaData']:
            tmpList = [str(i) for i in vm_row]
            vm_server_info.append(tmpList)
        return vm_server_info

    def fetch_trunk_group_info(self):
        #self.refreshToken()
        Trunk_Groups_URL = 'http://' + self.ip + ':'+self.pno+'/dm/status_trunk_groups/trunk_groups_status_list'
        result = self.client.get(Trunk_Groups_URL)
        json_result = json.loads(result.text)
        trunk_group_list = []
        for tg_row in json_result['data']['aaData']:
            tmpList = [str(i) for i in tg_row]
            trunk_group_list.append(tmpList)
        return trunk_group_list

    def fetch_make_me_conf_info(self):
        #self.refreshToken()
        make_me_conf_url = 'http://' + self.ip + ':'+self.pno+'/dm/status_site_confs/conf_switch_status_list'
        result = self.client.get(make_me_conf_url)
        json_result = json.loads(result.text)
        conf_switch_info = []
        for conf_row in json_result['data']['aaData']:
            tmpList = [str(i) for i in conf_row]
            conf_switch_info.append(tmpList)
        return conf_switch_info

   

    def fetch_phone_info(self, mac, AccName):
        """
        """
        tenantNames = AccName
        #self.refreshToken()
        tList = self.get_specific_tenants(tenantNames)
        dnis = []
        for tenant in tList:
            #LIST_DNIS_MAP = r'http://'+self.ip+':5478/director/dnis/list?rows=1000&_filter_tenant_id='+str(tenant[1])+r'&_filter_system_tenant_id='+str(tenant[1])+r''

            LIST_SWITCH_URL = r'http://' + self.ip + ':5478/director/ip_phones/list?_search=false&sidx=&sord=asc&_filter_tenant_id=' + str(tenant[1])+ '&_filter_system_tenant_id=' +str(tenant[1])+r''
            result = self.client.get(LIST_SWITCH_URL)
            d1 = json.loads(result.text)
            n_rows = d1["records"]
            print(n_rows)
            ph = []
            import re
            for x in range(n_rows):
                d1["rows"][x]["cell"][0]=re.sub("-", "", d1["rows"][x]["cell"][0])
                if d1["rows"][x]["cell"][0]==mac:
                    tmplist= d1["rows"][x]["id"]
                    ph.append(tmplist)
                    tmplist= d1["rows"][x]["cell"][2][1]
                    ph.append(tmplist)
                    print(ph)
        return ph


    def fetch_switch_status_D2(self, switch_name):
        URL = 'http://' +self.ip+ ':5478/dm/status_switches/switch_status_list?'
        #self.refreshToken()
        result = self.client.get(URL)
        jresult = json.loads(result.text)
        print(jresult)
        n_rows = jresult["data"]["iTotalRecords"]
        #print(n_rows)
        p = []
        for x in range(n_rows):
            if jresult["data"]["aaData"][x][2]==switch_name:
                tmplist = jresult["data"]["aaData"][x][7]
                p.append(tmplist)
                tmplist = jresult["data"]["aaData"][x][18]
                p.append(tmplist)
        for x in range(n_rows):
            if jresult["data"]["aaData"][x][3]=='vPhone' and jresult["data"]["aaData"][x][2]!=switch_name and  jresult["data"]["aaData"][x][7]=='In Service':
                tmplist = jresult["data"]["aaData"][x][2]
                p.append(tmplist)
                tmplist = jresult["data"]["aaData"][x][18]
                p.append(tmplist)
                break
        print(p)
        return p


    def change_ipphone_switch(self,phoneid,switchid):
        #self.refreshToken()
        URL ='http://' +self.ip+ ':5478/director/ip_phones/move.json?ids=' +phoneid+ '&site_id=3&switch_id=' +switchid
        JSON_DATA = {}
        result = self.client.post(URL,json=JSON_DATA)
        jresult = json.loads(result.text)
        print(jresult)
        return True


    def fetch_system_extn_info(self):
        """
        """
        # self.create_connection(ip, username, password)
        #self.refreshToken()
        LIST_SYSTEM_EXTN_URL = 'http://' + self.ip + ':'+self.pno+'/director/system_extensions.json'
        systemextnresult = self.client.get(LIST_SYSTEM_EXTN_URL)

        d = json.loads(systemextnresult.text)
        return d

    def fetch_build_info(self):
        from bs4 import BeautifulSoup
        url = 'http://' + self.ip + ':5478/dm/monitoring_service'
        #self.refreshToken()
        result = self.client.get(url)
        soup = BeautifulSoup(result.text, 'html.parser')
        var = soup.find_all("script", type="text/javascript")

        for x in var:
            if x.contents:
                var2 = x.text
                var2 = var2.encode('ascii', 'ignore')
                var3 = var2[var2.find('aaData') + 13: var2.find(',1]]')]
                var3 = var3.replace('\\"', ' ')
                res = var3.split(',')
                return res
        null = []
        return null

    def fetch_system_details(self):
        from bs4 import BeautifulSoup
        #self.refreshToken()
        url = 'http://' + self.ip + ':5478/dm/status_system'
        result = self.client.get(url)
        soup = BeautifulSoup(result.text, 'html.parser')
        var1 = soup.find_all("script", type="text/javascript")
        var2 = var1[4].text
        var2 = var2.encode('ascii', 'ignore')
        var3 = var2[var2.find('aaData') + 10: var2.find(']}')]
        var3 = var3.replace('\\"', ' ')
        l1 = (var3[:var3.find('],') + 1]).split(',')
        l2 = (var3[var3.find('],') + 1:]).split(',')
        var1 = soup.find_all("button", id="backup_db_command_button", type="button")
        var4 = var1[0].text
        var4 = (var4.encode('ascii', 'ignore')).strip()
        return l1, l2, var4
    

    def configure_prog_button(self,**kwargs):
        """
        :param args: user_extension,button_box,soft_key,function,label,target_extension,Digits,external_number,availability,audio_path,mailbox


        params for Monitor Extension
        ring_delay = [1,2,3,4,'dont_ring']
        show_caller_id = ["never","only_when_ringing","always"]
        no_connected = ["unused",""dial_number","intercom","whisper_page"]
        with_connected = ["unused",""dial_number","intercom","whisper_page","transfer_blind","transfer_consultative","transfer_intercom",park","transfer_whisper"]

        :return:
        """
        # get the user
        #self.refreshToken()
        user_id = None
        url = r'http://%s:%s/director/users_phones/list'%(self.ip,self.pno)
        r = self.client.get(url)
        for user in r.json()["rows"]:
            if kwargs.get('user_extension') == user["cell"][2]:
                user_id = user['id']
        if user_id is None:
            print("Can not get the id of user")
        # download user specific json
        url = r'http://%s:%s/director/users_phones/%s.json' % (self.ip, self.pno, str(user_id))
        user_json = self.client.get(url).json()

        # modifying the json with requested values
        function_ids = {'SHARED_CALL_APPEARANCE': '86',  'SILENT_COACH': '82',
                        'TRANSFER_WHISPER': '28',
                        'TRANSFER_INTERCOM': '18',
                        'MONITOR_EXTENSION': '3',
                        'ASSIGN_TO_LAST_EXTERNAL': '43',
                        'INTERCOM': '6',
                        'TOGGLE_HANDSFREE': '60',
                        'PARK': '22',
                        'CENTREX_FLASH': '29',
                        'RECORD_EXTENSION': '24',
                        'AGENT_LOGOUT': '45',
                        'WHISPER_PAGE_MUTE': '26',
                        'CONFERENCE_BLIND': '19',
                        'GROUP_PICKUP': '33',
                        'TRANSFER_TO_MAILBOX': '17',
                        'CALL_MOVE': '84',
                        'INVOKE_URL': '37',
                        'TO_VM': '39',
                        'INVOKE_COMMAND_LINE': '36',
                        'PARK_AND_PAGE': '23',
                        'CONFERENCE': '41',
                        'TOGGLE_LOCK_UNLOCK': '87',
                        'WRAP_UP_CODE': '75',
                        'CONTACT_CENTER': '4',
                        'PAPI': '80',
                        'WINDOWING': '2',
                        'MALICIOUS_CALL_TRACE': '83',
                        'CALL_APPEARANCE': '2',
                        'RECORD_CALL': '25',
                        'HANGUP': '34',
                        'SILENT_MONITOR': '7',
                        'RELEASE_WITH_CODE': '74',
                        'CHANGE_CHM': '42',
                        'ANSWER': '31',
                        'BRIDGE_CALL_APPEARANCE': '30',
                        'TRANSFER_CONSULTATIVE': '16',
                        'AGENT_WRAP_UP': '46',
                        'DIAL_MAILBOX': '5',
                        'PICKUP_NIGHT_BELL': '13',
                        'EXECUTE_DDE_COMMAND': '32',
                        'RUN_CONTACT_CENTER_APP': '79',
                        'SEND_DIGITS_OVER_CALL': '27',
                        'CONFERENCE_INTERCOM': '21',
                        'UNUSED': '1',
                        'UNPARK': '11',
                        'BARGE_IN': '8',
                        'FUNCTION_CATEGORY': '{}',
                        'HOLD': '35',
                        'OPEN_HISTORY_VIEWER': '47',
                        'TRANSFER_BLIND': '15',
                        'WHISPER_PAGE': '9',
                        'CONFERENCE_CONSULTATIVE': '20',
                        'ALL': '0',
                        'SUPERVISOR_HELP': '78',
                        'CHANGE_DEFAULT_AUDIO_PATH': '62',
                        'MOBILE': '88',
                        'TRANSFER': '40',
                        'DIAL_NUMBER_SPEED_DIAL': '4',
                        'TO_AA': '38',
                        'TELEPHONY': '1',
                        'PICKUP': '10',
                        'OTHER': '5',
                        'HOTLINE': '81',
                        'PICK_AND_PARK': '12',
                        'CONFIG': '3',
                        'PAGE': '14',
                        'AGENT_LOGIN': '44',

                        'CHANGE_AVAILABILITY': '42'
                        }
        with_connected_action = { "unused": 1,
                                  "dial_number": 4,
                                  "intercom": 6,
                                  "whisper_page": 9,
                                  "transfer_blind": 15,
                                  "transfer_consultative": 16,
                                  "transfer_intercom": 18,
                                  "park": 22,
                                  "transfer_whisper": 28, }
        availability_state = { "available" : 1,
                                "in_a_meeting": 2,
                               "out_of_office": 3,
                               "do_not_disturb": 6,
                               "vacation": 4,
                               "custom":5
                               }
        default_aduio_path = { "speaker" : 0,
                                "headset": 1,
                               "wireless_headset": 2,
                               "bluetooth_headset": 3
                               }
        no_connected_call_action = { "answer_only" : 3,
                                "dial_tone": 2,
                               "dial_extension": 0,
                               "dial_external": 1
                            }

        button_box = "user_prog_button_button_%s_boxes_attributes" % kwargs.get('button_box')
        soft_key = kwargs.get('soft_key')-1 # to make it as per the UI
        user_json["user"][button_box][soft_key]['selectedFunction'] = kwargs.get('function')
        user_json["user"][button_box][soft_key]['SoftKeyLabel'] = kwargs.get('label')[0:6]
        user_json["user"][button_box][soft_key]['LongLabel'] = kwargs.get('label')[0:12]
        user_json["user"][button_box][soft_key]['DialNumberDN_formatted'] = kwargs.get('target_extension',"")
        user_json["user"][button_box][soft_key]['_create'] = True
        user_json["user"][button_box][soft_key]['FunctionID'] = function_ids[kwargs.get('function').replace(" ", "_").upper()]
        user_json["user"][button_box][soft_key]['DialNumberExtern_formatted']= kwargs.get('external_number',"") # Send digits over call #Extnl number
        user_json["user"][button_box][soft_key]['SecondaryDN_formatted']=kwargs.get('mailbox',"")

        # else:
        user_json["user"][button_box][soft_key]['RingDelayBeforeAlert'] ='-1'
        if kwargs.get('external_number'):
            user_json["user"][button_box][soft_key]['ConnectedCallFunctionID'] =4
            user_json["user"][button_box][soft_key]['DialNumberNTID'] = "-1"
        if kwargs.get('mailbox'):
            user_json["user"][button_box][soft_key]['SecondaryType'] = "0"
        if kwargs.get('target_extension'):
            user_json["user"][button_box][soft_key]['DialNumberNTID'] = "0"
        if kwargs.get('ConnectedCallFunctionID'):
           user_json["user"][button_box][soft_key]['ConnectedCallFunctionID']= with_connected_action[kwargs.get('ConnectedCallFunctionID').replace(" ", "_").lower()]

        if kwargs.get('availability'):
           user_json["user"][button_box][soft_key]['CHMTypeID']= availability_state[kwargs.get('availability').replace(" ", "_").lower()]
        if kwargs.get('audio_path'):
            user_json["user"][button_box][soft_key]['FunctionParams4']=default_aduio_path[kwargs.get('audio_path').replace(" ", "_").lower()]
        if kwargs.get('EnableAutoAnswerWhenRinging'):
            # user_json["user"][button_box][soft_key]['FunctionParams4']=int(kwargs.get('EnableAutoAnswerWhenRinging'))
            user_json["user"][button_box][soft_key]['FunctionParams4']=kwargs.get('EnableAutoAnswerWhenRinging')
        if kwargs.get('Digits'):
            user_json["user"][button_box][soft_key]['DialNumberNTID'] = "4"
            user_json["user"][button_box][soft_key]['DialNumberExtern_formatted'] = kwargs.get('Digits')
        # Monitor
        user_json["user"][button_box][soft_key]['RingDelayBeforeAlert'] = kwargs.get('RingDelayBeforeAlert',user_json["user"][button_box][soft_key]['RingDelayBeforeAlert'])
        user_json["user"][button_box][soft_key]['show_caller_id_option']= kwargs.get('show_caller_id_option',user_json["user"][button_box][soft_key]['show_caller_id_option']).replace(" ", "_").lower()
        user_json["user"][button_box][soft_key]['dtmf_digits']= kwargs.get('Digits',"")

        if user_json["user"][button_box][soft_key]['selectedFunction'] == "Monitor Extension" :
            user_json["user"][button_box][soft_key]['DisconnectedCallFunctionID'] =4
        if kwargs.get('DisconnectedCallFunctionID'):
           user_json["user"][button_box][soft_key]['DisconnectedCallFunctionID']= with_connected_action[kwargs.get('DisconnectedCallFunctionID').replace(" ", "_").lower()]
        # BCA
        user_json["user"][button_box][soft_key]['CallStackPosition']= kwargs.get('CallStackPosition',user_json["user"][button_box][soft_key]['CallStackPosition'])
        if kwargs.get('SecondaryType'):
            user_json["user"][button_box][soft_key]['SecondaryType'] =no_connected_call_action[kwargs.get('SecondaryType').replace(" ", "_").lower()]
        if kwargs.get('DialExtension'):
            user_json["user"][button_box][soft_key]['SecondaryDN_formatted'] = kwargs.get('DialExtension')
        # upload the modified json
        if user_json["user"][button_box][soft_key]['selectedFunction'] =='UNUSED' or user_json["user"][button_box][soft_key]['selectedFunction'] == 'Call Appearance' :
            user_json["user"][button_box][soft_key]['SecondaryDN_formatted'] ='null'
            user_json["user"][button_box][soft_key]['SecondaryType'] ='null'
            # user_json["user"][button_box][soft_key]['DialNumberNTID'] = -1
        # user_json = json.dumps(user_json)
        # new_python_object = json.loads(user_json)
        url = r'http://%s:%s/director/users_phones/%s.json' % (self.ip, self.pno, str(user_id))
        r = self.client.put(url,json=user_json,headers={"X-CSRF-Token": self.token,"Content-Type": "application/json"})
        if r.status_code == 200:
            return True
        else:
            return False
            
    def Unconfigure_prog_button(self,**kwargs):
        """
        :param args: user_extension,button_box,soft_key
        :return:
        """
        #self.refreshToken()
        if kwargs.get('button_box') == 0:
            #kwargs.
            self.configure_prog_button(user_extension = kwargs.get('user_extension'),button_box=kwargs.get('button_box'),soft_key=kwargs.get('soft_key'), function='Call Appearance',label='',target_extension='')
        else:
            self.configure_prog_button(user_extension = kwargs.get('user_extension'),button_box=kwargs.get('button_box'),soft_key=kwargs.get('soft_key'), function='UNUSED',label ='',target_extension='')
        
    def create_hunt_group(self,**args):
        """
        :param :
        :param args: (BackupExtension,HuntGroupMember, HuntGroupName)
        :return: Hunt group extension
        """
        #self.refreshToken()
        getParams = r'http://%s:%s/director/hunt_groups/new.json'% (self.ip, self.pno)
        createHGParams = self.client.get(getParams).json() # This should give json for creating HG with all params.
        group_members = []
        if args.get("HuntGroupMember") != None :
            url = r'http://%s:%s/director/dns/list?list=hunt_group' % (self.ip, self.pno)
            user_json = self.client.get(url).json()
            for HGMembers in args.get("HuntGroupMember"):
                for users in user_json['rows']:
                    if str(HGMembers) == users["cell"][0]:
                        group_members.append(users['cell'][0])
                        break
                if str(HGMembers) not in group_members :
                    print("Extension " + str(HGMembers) + " not found in system ")
                    return False
        # Insert all the values to json
        createHGParams['hunt_group']['dn_ids']=group_members
        createHGParams['hunt_group']['BackupDN'] = args.get('BackupExtension')
        createHGParams['hunt_group']['dn_attributes']['Description'] = args.get("HuntGroupName","Created from D2 API")
        createHGParams['hunt_group']['BackupDN_formatted'] =args.get('BackupExtension')
        createHG = r'http://%s:%s/director/hunt_groups.json'% (self.ip, self.pno)
        outp = self.client.post(createHG,json=createHGParams,headers = {"X-CSRF-Token": self.token,"Content-Type": "application/json"})
        if outp.status_code == 200:
            return createHGParams['hunt_group']['dn_attributes']['DN']
        else:
            return False
            
    def create_ring_down_delay(self,**kwargs):
        """
        :param ExtensionNumber:
        :param RingDownDelay:
        :return:
        """
        #self.refreshToken()
        # get id from extension number
        urlGetAllUsers = "http://%s:%s/director/users/list" %(self.ip, self.pno)
        users = self.client.get(urlGetAllUsers).json()
        userID = None
        for rows in users['rows']:
            if rows['cell'][2] == kwargs.get('ExtensionNumber',""):
                userID = rows['id']
        if userID is None:
            print("Can not get the id of user")
            return False
        # get all user parameters from the retireved id.
        url = "http://%s:%s/director/users/%s.json" %(self.ip, self.pno, userID)
        getUserParams = self.client.get(url).json()
        getUserParams['user']['EnableDelayedRingdown'] = True
        getUserParams['user']['RingdownDelay']=kwargs.get('RingDownDelay',"")
        result = self.client.put(url, json=getUserParams,headers = {"X-CSRF-Token": self.token,"Content-Type": "application/json"})
        if result.status_code == 200:
            return True
        else:
            return False

    def delete_extension(self, extensionNumber):
        """
        To delete a user in D2 aka delete user
        :param extensionNumber:
        :return:
        """
        #self.refreshToken()
        # get id from extension number
        urlGetAllUsers = "http://%s:%s/director/users/list?rows=250" %(self.ip, self.pno)
        users = self.client.get(urlGetAllUsers).json()
        userID = None
        for rows in users['rows']:
            if rows['cell'][2] == extensionNumber:
                userID = rows['id']
        if userID is None:
            print("Cannot get the id of user")
            return False
        url = "http://%s:%s/director/users/%s.json" %(self.ip, self.pno, userID)
        getUserParams = self.client.get(url).json()
        # get all user parameters from the retireved id.
        url = "http://%s:%s/director/users/%s.json" %(self.ip, self.pno, userID)
        result = self.client.delete(url, json=getUserParams,headers = {"X-CSRF-Token": self.token,"Content-Type": "application/json"})
        if result.status_code == 200:
            return True
        else:
            return False

    def create_modify_user(self, **kwargs):
        """
        To create a new user in D2 aka extension
        :param FirstName:
        :param LastName:
        :param EmailAddress:
        :param ClientUserName:
        :return: User Extension number
        """
        # createUser = ""
        if not kwargs.get('extension'):
            print("Creating new user")
            getParams = r'http://%s:%s/director/users/new.json'% (self.ip, self.pno)
            createUser = r'http://%s:%s/director/users.json'% (self.ip, self.pno)
        else:
            print("Modifying User")
            getParams = r'http://%s:%s/director/users/list'% (self.ip, self.pno)
            userList = self.client.get(getParams).json()
            userID = None
            for rows in userList['rows']:
                if rows['cell'][2] == str(kwargs.get('extension')):
                    userID = rows['id']
                    break
            if not userID:
                print("User Extension doesn't exist, please create new")
                return False
            getParams = r'http://%s:%s/director/users/%s.json'% (self.ip, self.pno,userID)
            createUser = r'http://%s:%s/director/users/%s.json'% (self.ip, self.pno,userID)
        UserParams = self.client.get(getParams).json() # This should give json for creating user with all params.
        UserParams['user']['BridgeUserID'] = ""
        UserParams['user']['dn_attributes']['Description'] = kwargs.get('FirstName', "") +" " + kwargs.get('LastName', "")
        UserParams['user']['tab_address_attributes']['FirstName'] = kwargs.get('FirstName', UserParams['user']['tab_address_attributes']['FirstName'])
        UserParams['user']['tab_address_attributes']['LastName'] = kwargs.get('LastName', UserParams['user']['tab_address_attributes']['LastName'])
        UserParams['user']['tab_address_attributes']['EmailAddress'] = kwargs.get('EmailAddress', "")
        UserParams['user']['GuiLoginName'] = kwargs.get('ClientUserName',UserParams['user']['GuiLoginName'])
        if not UserParams['user']['GuiLoginName']:
            # ENTA 5645
            # UserParams['user']['GuiLoginName'] = kwargs.get('ClientUserName', UserParams['user']['tab_address_attributes']['LastName'] + str(time.time())[:6]+"@autotest.com")
            UserParams['user']['GuiLoginName'] = kwargs.get('ClientUserName', str(time.time())[:6] + "@autotest.com")
        UserParams['user']['dn_attributes']['Hidden'] =kwargs.get('MakeExtensionPrivate',UserParams['user']['AllowPAPI']) # YET TO CHECK
        UserParams['user']['AutoCHM']=kwargs.get('AutoCHM',UserParams['user']['AutoCHM'])
        UserParams['user']['EnableDelayedRingdown']=kwargs.get('EnableDelayedRingdown',UserParams['user']['EnableDelayedRingdown'])
        UserParams['user']['ringdown_number_formatted']=kwargs.get('RingdownNumber',UserParams['user']['ringdown_number_formatted'])
        UserParams['user']['RingdownDelay']=kwargs.get('RingdownDelay',UserParams['user']['RingdownDelay'])
        UserParams['user']['voice_mailbox_for_recorded_calls_formatted']=kwargs.get('VoiceMailboxForRecordedCalls',UserParams['user']['voice_mailbox_for_recorded_calls_formatted'])
        UserParams['user']['mailbox_server_id']=kwargs.get('MailboxServer',UserParams['user']['mailbox_server_id'])
        UserParams['user']['RingToneID']=kwargs.get('RingType',UserParams['user']['RingToneID'])
        UserParams['user']['WPID']=kwargs.get('WallPaper',UserParams['user']['WPID'])
        UserParams['user']['dn_attributes']['include_in_dial_by_name'] =kwargs.get('IncludeInSystemDialByNameDirectory',UserParams['user']['dn_attributes']['include_in_dial_by_name'])
        if kwargs.get('Notes'):
            UserParams['user']['dn_note_attributes']= {"Notes": str(kwargs.get('Notes'))}
        # DID Settings
        UserParams['user']['DIDEnabled']=kwargs.get('DIDEnabled',UserParams['user']['DIDEnabled'])
        #UserParams['user']['did_warning']=kwargs.get('did_warning',UserParams['user']['did_warning'])
        UserParams['user']['did_range_did_range_id']=kwargs.get('DIDRange',UserParams['user']['did_range_did_range_id'])
        UserParams['user']['did_range_digits']=kwargs.get('DIDNumber',UserParams['user']['did_range_digits'])
        # UserParams['user']['configured_base_phone_number']=kwargs.get('configured_base_phone_number',UserParams['user']['configured_base_phone_number'])
        # License Type
        license_types = {"Extension and Mailbox": "1", "Extension-Only": "2", "Mailbox-Only": "3"}
        UserParams['user']['LicenseTypeID'] = license_types.get(kwargs.get("LicenseType"), UserParams['user']['LicenseTypeID'])
        access_licenses = {"Phone Only": 0, "Connect Client": 5, "Workgroup Agent": 3, "Workgroup Supervisor": 2, "Operator": 1}
        UserParams['user']['ClientType'] = access_licenses.get(kwargs.get("AccessLicense"), UserParams['user']['ClientType'])



        # UserParams['user']['primary_port_selection']=kwargs.get('primary_port_selection',UserParams['user']['primary_port_selection']) not req
        UserParams['user']['ip_phone_port_id']=kwargs.get('IPPhone',UserParams['user']['ip_phone_port_id'])
        UserParams['user']['analog_port_id']=kwargs.get('analog_port_id',UserParams['user']['analog_port_id'])
        UserParams['user']['softswitch_id']=kwargs.get('softswitch_id',UserParams['user']['softswitch_id'])
        UserParams['user']['jack_number']=kwargs.get('JackNumber',UserParams['user']['jack_number'])
        # Telephony
        UserParams['user']['CurrentCallStackDepth']=kwargs.get('CallStackDepth',UserParams['user']['CurrentCallStackDepth'])
        UserParams['user']['UseHeadsetAudioPath']=kwargs.get('AutomaticOffHookPreference',UserParams['user']['UseHeadsetAudioPath'])
        UserParams['user']['HeadsetMode']=kwargs.get('EnableHandsFreeMode',UserParams['user']['HeadsetMode'])
        UserParams['user']['CallWaitingToneEnabled']=kwargs.get('EnableCallWaitingTone',UserParams['user']['CallWaitingToneEnabled'])
        UserParams['user']['DefaultTrunkAccessCode']=kwargs.get('TrunkAccessCode',UserParams['user']['DefaultTrunkAccessCode'])
        UserParams['user']['IDectPowerMode']=kwargs.get('DectPowerMode',UserParams['user']['IDectPowerMode'])
        UserParams['user']['IDectQuality']=kwargs.get('DectQuality',UserParams['user']['IDectQuality'])
        UserParams['user']['FaxSupport']=kwargs.get('FaxSupport',UserParams['user']['FaxSupport'])
        UserParams['user']['AllowVideoCalls_bool']=kwargs.get('EnableVideoCalls',UserParams['user']['AllowVideoCalls_bool'])
        UserParams['user']['AllowVideoCalls']=kwargs.get('VideoCallMode',UserParams['user']['AllowVideoCalls'])
        UserParams['user']['AllowTelephonyPresence']=kwargs.get('EnableTelephonyPresence',UserParams['user']['AllowTelephonyPresence'])
        UserParams['user']['AllowSoftPhone']=kwargs.get('EnableSoftPhone',UserParams['user']['AllowSoftPhone'])
        UserParams['user']['AllowPAPI']=kwargs.get('EnablePAPI',UserParams['user']['AllowPAPI'])
        UserParams['user']['EnableRemotePhoneAuthentication']=kwargs.get('EnableRemotePhoneAuthentication',UserParams['user']['EnableRemotePhoneAuthentication'])
        UserParams['user']['enable_mobile_dn']=kwargs.get('EnableEnhancedMobility',UserParams['user']['enable_mobile_dn'])
        auxNumber = ''
        if UserParams['user']['enable_mobile_dn'] is True :
            getAXNum = r'http://%s:%s/director/users/next_auxiliary_dn'% (self.ip, self.pno)
            AvailableAXNum = self.client.get(getAXNum).json()
            auxNumber= AvailableAXNum['next_dn']
            UserParams['user']['mobile_dn_formatted']=auxNumber
        else:
            UserParams['user']['mobile_dn_formatted']=""
        UserParams['user']['MobilityPhoneNumber_formatted'] = kwargs.get('MobilePhoneNumber',UserParams['user']['MobilityPhoneNumber_formatted'])
        # Voice Mail
        if kwargs.get("LicenseType") and not "Mailbox" in kwargs.get("LicenseType"): # mailbox as License type will make the mailbox_attribute as None
            UserParams['user']['mailbox_attributes']['accept_broadcasts'] = kwargs.get('AcceptBroadcastMessages',UserParams['user']['mailbox_attributes']['accept_broadcasts'] )
            UserParams['user']['mailbox_attributes']['PlayEnvelope'] = kwargs.get('PlayEnvelope',UserParams['user']['mailbox_attributes']['PlayEnvelope'] )
            UserParams['user']['mailbox_attributes']['EmailNotifyWhenFull'] = kwargs.get('SendEmailWarningWhenFull',UserParams['user']['mailbox_attributes']['EmailNotifyWhenFull'] )
            UserParams['user']['mailbox_attributes']['IsDeletedWhenForward'] = kwargs.get('DeleteMessageAfterForwarding',UserParams['user']['mailbox_attributes']['IsDeletedWhenForward'] )
            UserParams['user']['mailbox_attributes']['auto_def_dest'] = kwargs.get('AutomaticMessageForwardingDestination',UserParams['user']['mailbox_attributes']['auto_def_dest'] )
            UserParams['user']['mailbox_attributes']['mailbox_destination_DN_formatted'] = kwargs.get('Mailbox',UserParams['user']['mailbox_attributes']['mailbox_destination_DN_formatted'] )
            UserParams['user']['mailbox_attributes']['AMIS_destination_DN'] = kwargs.get('AMISDestinationDN',UserParams['user']['mailbox_attributes']['AMIS_destination_DN'] )
            UserParams['user']['mailbox_attributes']['SendEmailForVMTypeID'] = kwargs.get('DeliveryType',UserParams['user']['mailbox_attributes']['SendEmailForVMTypeID'] )
            UserParams['user']['mailbox_attributes']['MarkAsHeard'] = kwargs.get('MarkAsHeard',UserParams['user']['mailbox_attributes']['MarkAsHeard'] )

        # DNIS
        if kwargs.get('DNIS'):
            for trunks in kwargs.get('DNIS'):
                if trunks.get('TrunkDigits') and trunks.get('TrunkDescription') and trunks.get('TrunkMOHID'):
                    groupID = self.get_did_range_data()['did_ranges'][0]['trunk_group_id']
                    UserParams['user']['did_digit_map_attributes'] += [{"TrunkGroupID": groupID,"DIDDigitMapID":2,"Digits":trunks.get('TrunkDigits'), "Description":trunks.get('TrunkDescription'), "MOHResourceID": trunks.get('TrunkMOHID'),"DNIS":True }] #'DNIS':True
                elif trunks.get('TrunkDigits'):
                    availableCount = 0
                    for availables in UserParams['user']['did_digit_map_attributes']:
                        if str(availables["Digits"]) == str(trunks.get('TrunkDigits')):
                            UserParams['user']['did_digit_map_attributes'][availableCount]["_destroy"]= 1
                        availableCount +=1
        #others

        UserParams['user']['MCMAllowed']= kwargs.get('MCMAllowed',UserParams['user']['MCMAllowed'])
        UserParams['user']['sca_enabled']=kwargs.get('sca_enabled',UserParams['user']['sca_enabled'])
        getBCADN = r'http://%s:%s/director/users/next_auxiliary_dn?dn=%s'% (self.ip, self.pno,auxNumber)
        bcadn = self.client.get(getBCADN).json()
        UserParams['user']['fake_bBcaDN_formatted']=bcadn['next_dn']
        # Membership
        UserParams['user']['selected_work_groups']=kwargs.get('SelectedWorkGroups',UserParams['user']['selected_work_groups'])
        if kwargs.get('DistributionList'):
            UserParams['user']['distribution_list_ids']=kwargs.get('DistributionList')
        if kwargs.get('Delegation'):
            UserParams['user']['chm_delegation_policy_user_ids']=kwargs.get('Delegation')


        # if
        if kwargs.get('UserGroupName'):
            isFound = False
            getAllUGs = r'http://%s:%s/director/user_groups/list?rows=500'% (self.ip, self.pno)
            ug = self.client.get(getAllUGs).json()['rows']
            for userG in ug:
                if str(userG['cell'][0]).lower()==str(kwargs.get('UserGroupName')).lower():
                    UserParams['user']['UserGroupID'] = userG['id']
                    isFound = True
                    break
            if not isFound:
                print("User group not found in the system")
                return False

        # Routing  - Phones.

        if kwargs.get('RountingPhones'):
            UserPhoneTypeID = 1
            for rOptions in kwargs.get('RountingPhones'):
                UserParams['user']['user_phones_attributes'][UserPhoneTypeID-1]['UserDN'] = UserParams['user']['UserDN']
                UserParams['user']['user_phones_attributes'][UserPhoneTypeID-1]['UserPhoneTypeID'] =UserPhoneTypeID
                UserParams['user']['user_phones_attributes'][UserPhoneTypeID-1]['Label'] =rOptions.get('Label',"LABEL1")
                UserParams['user']['user_phones_attributes'][UserPhoneTypeID-1]['NoAnswerRings'] =rOptions.get('NumberOfRings',UserParams['user']['user_phones_attributes'][UserPhoneTypeID-1]['NoAnswerRings'])
                UserParams['user']['user_phones_attributes'][UserPhoneTypeID-1]['ActivationTypeID'] =rOptions.get('Activation')
                # UserParams['user']['user_phones_attributes'][UserPhoneTypeID-1]['id'] =str(UserParams['user']['UserDN']) + ',' + str(UserPhoneTypeID)
                # UserParams['user']['user_phones_attributes'][UserPhoneTypeID-1]['is_mobile_dn'] = False
                UserParams['user']['user_phones_attributes'][UserPhoneTypeID-1]['Number_formatted'] =rOptions.get('PhoneNumber')
                UserPhoneTypeID +=1
        # if kwargs.get('RingMeOptions'):
        # UserParams['user']['dn_follow_destination_attributes']['FindMePhoneTypeID1'] =1
        # UserParams['user']['dn_follow_destination_attributes']['FindMePhoneTypeID2'] =1

        # Routing -RingMe
        UserParams['user']['dn_follow_destination_attributes']['SendCallerID'] =kwargs.get('SendIncomingCallerID',UserParams['user']['dn_follow_destination_attributes']['SendCallerID'] ) # Send incoming caller ID
        UserParams['user']['dn_follow_destination_attributes']['UseAutoFindMe'] =kwargs.get('EnableFindMeForIncomingCalls',UserParams['user']['dn_follow_destination_attributes']['UseAutoFindMe'] )
        UserParams['user']['dn_follow_destination_attributes']['IsRecCallerName'] =kwargs.get('EnableRecordCallerName',UserParams['user']['dn_follow_destination_attributes']['IsRecCallerName'] )
        UserParams['user']['dn_follow_destination_attributes']['RecIfCallIDPresent'] =kwargs.get('RecordNameEvenCallerIDIsPresent',UserParams['user']['dn_follow_destination_attributes']['RecIfCallIDPresent'])
        UserParams['user']['dn_follow_destination_attributes']['RingAllRingDelay'] =kwargs.get('RingAdditionalRingDelay',UserParams['user']['dn_follow_destination_attributes']['RingAllRingDelay'])
        UserParams['user']['dn_follow_destination_attributes']['RingAllPhoneTypeID1'] =kwargs.get('SimultaneouslyRing',UserParams['user']['dn_follow_destination_attributes']['RingAllPhoneTypeID1'])
        UserParams['user']['dn_follow_destination_attributes']['RingAllPhoneTypeID2'] = kwargs.get('AlsoRing',UserParams['user']['dn_follow_destination_attributes']['RingAllPhoneTypeID2'])
        UserParams['user']['dn_follow_destination_attributes']['FindMePhoneTypeID1'] = kwargs.get('FindMeFirstPhone',UserParams['user']['dn_follow_destination_attributes']['FindMePhoneTypeID1'])
        UserParams['user']['dn_follow_destination_attributes']['FindMePhoneTypeID2']  =kwargs.get('FindMeSecondPhone',UserParams['user']['dn_follow_destination_attributes']['FindMePhoneTypeID2'])

        UserParams['user']['call_handling_modes_attributes'][0]['EnableFindMeFollowMe'] = kwargs.get('FindMeAvailable',UserParams['user']['call_handling_modes_attributes'][0]['EnableFindMeFollowMe'])
        UserParams['user']['call_handling_modes_attributes'][1]['EnableFindMeFollowMe'] = kwargs.get('FindMeInAMeeting',UserParams['user']['call_handling_modes_attributes'][1]['EnableFindMeFollowMe'])
        UserParams['user']['call_handling_modes_attributes'][2]['EnableFindMeFollowMe'] = kwargs.get('FindMeOutOfOffice',UserParams['user']['call_handling_modes_attributes'][2]['EnableFindMeFollowMe'])
        UserParams['user']['call_handling_modes_attributes'][4]['EnableFindMeFollowMe'] = kwargs.get('FindMeVecation',UserParams['user']['call_handling_modes_attributes'][4]['EnableFindMeFollowMe'])
        UserParams['user']['call_handling_modes_attributes'][5]['EnableFindMeFollowMe'] = kwargs.get('FindMeCustom',UserParams['user']['call_handling_modes_attributes'][5]['EnableFindMeFollowMe'])

        UserParams['user']['call_handling_modes_attributes'][0]['EnableRingAll'] = kwargs.get('RingAdditionalPhoneWhenAvailable',UserParams['user']['call_handling_modes_attributes'][0]['EnableRingAll'])
        UserParams['user']['call_handling_modes_attributes'][1]['EnableRingAll'] = kwargs.get('RingAdditionalPhoneWhenInAMeeting',UserParams['user']['call_handling_modes_attributes'][1]['EnableRingAll'])
        UserParams['user']['call_handling_modes_attributes'][2]['EnableRingAll'] = kwargs.get('RingAdditionalPhoneWhenOutOfOffice',UserParams['user']['call_handling_modes_attributes'][2]['EnableRingAll'])
        UserParams['user']['call_handling_modes_attributes'][4]['EnableRingAll'] = kwargs.get('RingAdditionalPhoneWhenVecation',UserParams['user']['call_handling_modes_attributes'][4]['EnableRingAll'])
        UserParams['user']['call_handling_modes_attributes'][5]['EnableRingAll'] = kwargs.get('RingAdditionalPhoneWhenCustom',UserParams['user']['call_handling_modes_attributes'][5]['EnableRingAll'])


        # UserParams['user']['PSTNFailoverTypeID']=kwargs.get('PSTNFailover',UserParams['user']['PSTNFailoverTypeID'])
        # UserParams['user']['PSTNFailoverNumber_formatted']=kwargs.get('PSTNFailoverNumber',UserParams['user']['PSTNFailoverNumber_formatted'])
        # UserParams['user']['BridgeID']=kwargs.get('BridgeID',UserParams['user']['BridgeID'])
        # UserParams['user']['BridgeUserID']=kwargs.get('BridgeUserID',UserParams['user']['BridgeUserID'])
        # UserParams['user']['CESID']=kwargs.get('CESID',UserParams['user']['CESID'])
        # UserParams['user']['CName']=kwargs.get('CName',UserParams['user']['CName'])
        # UserParams['user']['CNameTypeID']=kwargs.get('CNameTypeID',UserParams['user']['CNameTypeID'])
        # UserParams['user']['CallRecordingModeID']=kwargs.get('CallRecordingModeID',UserParams['user']['CallRecordingModeID'])
        # UserParams['user']['CallerIDBlocked']=kwargs.get('CallerIDBlocked',UserParams['user']['CallerIDBlocked'])
        # UserParams['user']['ContactCenterIntegration']=kwargs.get('ContactCenterIntegration',UserParams['user']['ContactCenterIntegration'])
        # UserParams['user']['CurrentCHMTypeID']=kwargs.get('CurrentCHMTypeID',UserParams['user']['CurrentCHMTypeID'])
        # UserParams['user']['DaysNotified']=kwargs.get('DaysNotified',UserParams['user']['DaysNotified'])
        # UserParams['user']['DefaultTrunkGroupID']=kwargs.get('DefaultTrunkGroupID',UserParams['user']['DefaultTrunkGroupID'])
        # UserParams['user']['FaxEnabled']=kwargs.get('FaxEnabled',UserParams['user']['FaxEnabled'])
        # UserParams['user']['GuiLoginName']=kwargs.get('GuiLoginName',UserParams['user']['GuiLoginName'])
        # UserParams['user']['IMArchiveSettings']=kwargs.get('IMArchiveSettings',UserParams['user']['IMArchiveSettings'])
        # UserParams['user']['IMPrivacySetting']=kwargs.get('IMPrivacySetting',UserParams['user']['IMPrivacySetting'])
        # UserParams['user']['IMServerID']=kwargs.get('IMServerID',UserParams['user']['IMServerID'])
        # UserParams['user']['LDAPDomainName']=kwargs.get('LDAPDomainName',UserParams['user']['LDAPDomainName'])
        # UserParams['user']['LDAPGuid']=kwargs.get('LDAPGuid',UserParams['user']['LDAPGuid'])
        UserParams['user']['MustChangeGUIPassword']=kwargs.get('MustChangeGUIPassword',UserParams['user']['MustChangeGUIPassword'])
        UserParams['user']['MustChangeTUIPassword']=kwargs.get('MustChangeTUIPassword',UserParams['user']['MustChangeTUIPassword'])
        # UserParams['user']['NTLoginName']=kwargs.get('NTLoginName',UserParams['user']['NTLoginName'])
        # UserParams['user']['RotationTime']=kwargs.get('RotationTime',UserParams['user']['RotationTime'])
        # UserParams['user']['ScribeEnabled']=kwargs.get('ScribeEnabled',UserParams['user']['ScribeEnabled'])
        # UserParams['user']['UseProgButtonsIP100']=kwargs.get('UseProgButtonsIP100',UserParams['user']['UseProgButtonsIP100'])
        # UserParams['user']['UserDN']=kwargs.get('UserDN',UserParams['user']['UserDN'])
        # UserParams['user']['UserDNID']=kwargs.get('UserDNID',UserParams['user']['UserDNID'])
        # UserParams['user']['id']=kwargs.get('id',UserParams['user']['id'])
        # UserParams['user']['current_port_display']=kwargs.get('current_port_display',UserParams['user']['current_port_display'])
        # UserParams['user']['supports_wrapup']=kwargs.get('supports_wrapup',UserParams['user']['supports_wrapup'])
        # UserParams['user']['incoming_calls_ring']=kwargs.get('incoming_calls_ring',UserParams['user']['incoming_calls_ring'])
        # UserParams['user']['enable_mobile_dn']=kwargs.get('enable_mobile_dn',UserParams['user']['enable_mobile_dn'])
        # UserParams['user']['CIDNumber_formatted']=kwargs.get('CallerID',UserParams['user']['CIDNumber_formatted'])
        # UserParams['user']['CESID_formatted']=kwargs.get('CESID_formatted',UserParams['user']['CESID_formatted'])
        # UserParams['user']['true_base_phone_number']=kwargs.get('true_base_phone_number',UserParams['user']['true_base_phone_number'])

        # result = self.client.post(createUser,json=UserParams,headers = {"X-CSRF-Token": self.token,"Content-Type": "application/json"})
        if not kwargs.get('extension'):
            result = self.client.post(createUser,json=UserParams,headers = {"X-CSRF-Token": self.token,"Content-Type": "application/json"})
        else:
            result = self.client.put(createUser,json=UserParams,headers = {"X-CSRF-Token": self.token,"Content-Type": "application/json"})

        if result.status_code == 200 and "errors" not in result.json():
            if not kwargs.get('extension'):
                if kwargs.get('sca_enabled') is True:
                    return "User Extension " +UserParams['user']['UserDN'] +" is created with BCA Number " +UserParams['user']['fake_bBcaDN_formatted']
                return "User Extension " +UserParams['user']['UserDN']+" is created."
            else:
                if kwargs.get('sca_enabled') is True:
                    return "User Extension " +UserParams['user']['UserDN'] +" is enabled with BCA Number " +UserParams['user']['fake_bBcaDN_formatted']
                return "User Extension " +UserParams['user']['UserDN']+" modified."
        else:
            print("Error occurred : " + str(result.json()["errors"]))
            return False

    def delete_hunt_group(self,ExtensionNumber):
        """
        :param ExtensionNumber:
        :return:
        """
        #self.refreshToken()
        getHuntGroup = r'http://%s:%s/director/hunt_groups/list'% (self.ip, self.pno)
        AvailableHuntGroups = self.client.get(getHuntGroup).json()
        for rows in AvailableHuntGroups['rows']:
            if ExtensionNumber == rows['cell'][1]:
                delHuntGroup = r'http://%s:%s/director/hunt_groups/%s.json'% (self.ip, self.pno,rows['id'])
                delHG = self.client.delete(delHuntGroup,headers = {"X-CSRF-Token": self.token})
                if delHG.status_code == 200:
                    return True
                else:
                    return False
        raise Exception("Extension not found")

    def create_page_list(self,**kwargs):
        '''
        :param kwargs: name and extension_numbers
        :return:
        '''
        #self.refreshToken()
        urlNewPageList = r'http://%s:%s/director/extension_lists/new.json?'% (self.ip, self.pno)
        getParametersForNewPageList = self.client.get(urlNewPageList).json()
        getParametersForNewPageList['extension_list']['Name']=kwargs.get('name')
        getParametersForNewPageList['extension_list']['dn_ids']=kwargs.get('extension_numbers')
        urlSubmitRequest = r'http://%s:%s/director/extension_lists.json'% (self.ip, self.pno)
        resSubmitRespone = self.client.post(urlSubmitRequest,json=getParametersForNewPageList,headers = {"X-CSRF-Token": self.token,"Content-Type": "application/json"})
        if resSubmitRespone.status_code == 200:
            return True
        else:
            return False

    def delete_page_list(self, ExtensionListName):
        '''
        :param ExtensionNumber:
        :return:
        '''
        #self.refreshToken()
        if not ExtensionListName:
            print("Extension List Name is mandatory")
            return False
        urlExtList = r'http://%s:%s/director/extension_lists/list?_search=false&rows=250'% (self.ip, self.pno)
        AvailableExtList = self.client.get(urlExtList).json()

        for rows in AvailableExtList['rows']:
            if rows['cell'][0] == ExtensionListName:
                urlDelete = r'http://%s:%s/director/extension_lists/%s.json'% (self.ip, self.pno,rows['id'])
                status = self.client.delete(urlDelete,headers = {"X-CSRF-Token": self.token})
                if status.status_code == 200:
                    return True
                else:
                    return False
        raise Exception("Extension number not found in the system")

    def create_paging_group(self, **args):
        '''
        :param PagingGroupName:
        :param args: (PageListName,PagingDelay, PriorityPage,RingsPerMember,MakeExtensionPrivate)
        :return:
        '''
        #self.refreshToken()
        urlNewPagingGroup = r'http://%s:%s/director/paging_groups/new.json?'% (self.ip, self.pno)
        getParamsNewPagingGroup = self.client.get(urlNewPagingGroup).json()
        if args.get('PageListName'):
            getParamsNewPagingGroup['paging_group']['ExtensionListID'] = "" # clear default value
            for lists in getParamsNewPagingGroup['collections']['no_mbox_user_extension_list']:
                if lists['description'] == args.get('PageListName'):
                    getParamsNewPagingGroup['paging_group']['ExtensionListID'] = lists['id']
                    break
            if not getParamsNewPagingGroup['paging_group']['ExtensionListID']:
                raise Exception("Mentioned pagelist("+ args.get('PageListName') +") is not found in the system")

        getParamsNewPagingGroup['paging_group']['dn_attributes']['Description'] = args.get('PagingGroupName',"")
        getParamsNewPagingGroup['paging_group']['dn_attributes']['Hidden'] = args.get('MakeExtensionPrivate',getParamsNewPagingGroup['paging_group']['dn_attributes']['Description'])
        getParamsNewPagingGroup['paging_group']['PagingDelay'] = args.get('PagingDelay',"3")
        getParamsNewPagingGroup['paging_group']['PriorityPage'] = args.get('PriorityPage',"false")
        getParamsNewPagingGroup['paging_group']['RingsPerMember'] = args.get('RingsPerMember',"2")
        getParamsNewPagingGroup['paging_group']['PriorityPageAudioPath']=args.get('PriorityPageAudioPath',getParamsNewPagingGroup['paging_group']['PriorityPageAudioPath'])

        urlSubmitPagingGroup = r'http://%s:%s/director/paging_groups.json'% (self.ip, self.pno)
        output = self.client.post(urlSubmitPagingGroup,json=getParamsNewPagingGroup,headers = {"X-CSRF-Token": self.token,"Content-Type": "application/json"})
        if output.status_code == 200:
            return getParamsNewPagingGroup['paging_group']['dn_attributes']['DN']
        else:
            return False

    def delete_paging_group(self, ExtensionNumber):
        '''
        :param ExtensionNumber:
        :return:
        '''
        #self.refreshToken()
        urlListPagingGroup = r'http://%s:%s/director/paging_groups/list?_search=false'% (self.ip, self.pno)
        AvailablePageGroups = self.client.get(urlListPagingGroup).json()

        for rows in AvailablePageGroups['rows']:
            if rows['cell'][1] == str(ExtensionNumber):
                urlDelete = r'http://%s:%s/director/paging_groups/%s.json'% (self.ip, self.pno,rows['id'])
                status = self.client.delete(urlDelete,headers = {"X-CSRF-Token": self.token})
                if status.status_code == 200:
                    return True
                else:
                    return False
        raise Exception("Extension number not found in the system")

    def change_telephony_feature_permission(self, **kwargs):
        '''
        :param kwargs:
        change_telephony_feature_permission
        :return:
        '''
        #self.refreshToken()
        if not kwargs.get('name'):
            print("name is mandatory parameter")
            return False
        urlGetAllCOS = "http://%s:%s/director/costs/list" %(self.ip, self.pno)
        COSs = self.client.get(urlGetAllCOS).json()
        cosID = None
        for rows in COSs['rows']:
            if rows['cell'][0] == kwargs.get('name'):
                cosID = rows['id']
                break
        if cosID is None:
            print("COS Name doesnt exist in system.")
            return False
        urlGetCOS = r'http://%s:%s/director/costs/%s.json'% (self.ip, self.pno, cosID)
        cosParams = self.client.get(urlGetCOS).json()

        cosParams['$resolved'] ="false"
        cosParams['new_record']= "false"
        cosParams['cost']['AcceptBargeIn']=kwargs.get('AcceptBargeIn',cosParams['cost']['AcceptBargeIn'])
        cosParams['cost']['AcceptBargeInDN']=kwargs.get('AcceptBargeInDN',cosParams['cost']['AcceptBargeInDN'])
        cosParams['cost']['AcceptIntercomPaging']=kwargs.get('AcceptIntercomPaging',cosParams['cost']['AcceptIntercomPaging'])
        cosParams['cost']['AcceptIntercomPagingDN']=kwargs.get('AcceptIntercomPagingDN',cosParams['cost']['AcceptIntercomPagingDN'])
        cosParams['cost']['AcceptRecordingOthersCalls']=kwargs.get('AcceptRecordingOthersCalls',cosParams['cost']['AcceptRecordingOthersCalls'])
        cosParams['cost']['AcceptRecordingOthersDN']=kwargs.get('AcceptRecordingOthersDN',cosParams['cost']['AcceptRecordingOthersDN'])
        cosParams['cost']['AcceptSilentMonitor']=kwargs.get('AcceptSilentMonitor',cosParams['cost']['AcceptSilentMonitor'])
        cosParams['cost']['AcceptSilentMonitorDN']=kwargs.get('AcceptSilentMonitorDN',cosParams['cost']['AcceptSilentMonitorDN'])
        cosParams['cost']['AcceptWhisperPaging']=kwargs.get('AcceptWhisperPaging',cosParams['cost']['AcceptWhisperPaging'])
        cosParams['cost']['AcceptWhisperPagingDN']=kwargs.get('AcceptWhisperPagingDN',cosParams['cost']['AcceptWhisperPagingDN'])
        cosParams['cost']['AllowBargeIn']=kwargs.get('AllowBargeIn',cosParams['cost']['AllowBargeIn'])
        cosParams['cost']['AllowBridgeUse']=kwargs.get('AllowBridgeUse',cosParams['cost']['AllowBridgeUse'])
        cosParams['cost']['AllowCallForwardExternal']=kwargs.get('AllowCallForwardExternal',cosParams['cost']['AllowCallForwardExternal'])
        cosParams['cost']['AllowCallNotes']=kwargs.get('AllowCallNotes',cosParams['cost']['AllowCallNotes'])
        cosParams['cost']['AllowCallPickupExtension']=kwargs.get('AllowCallPickupExtension',cosParams['cost']['AllowCallPickupExtension'])
        cosParams['cost']['AllowCallPickupNightBell']=kwargs.get('AllowCallPickupNightBell',cosParams['cost']['AllowCallPickupNightBell'])
        cosParams['cost']['AllowCallTransferTrunkToTrunk']=kwargs.get('AllowCallTransferTrunkToTrunk',cosParams['cost']['AllowCallTransferTrunkToTrunk'])
        cosParams['cost']['AllowChangeOwnCHMode']=kwargs.get('AllowChangeOwnCHMode',cosParams['cost']['AllowChangeOwnCHMode'])
        cosParams['cost']['AllowChangeOwnCHSettings']=kwargs.get('AllowChangeOwnCHSettings',cosParams['cost']['AllowChangeOwnCHSettings'])
        cosParams['cost']['AllowDiffExtPrefixCalls']=kwargs.get('AllowDiffExtPrefixCalls',cosParams['cost']['AllowDiffExtPrefixCalls'])
        cosParams['cost']['AllowHotDesk']=kwargs.get('AllowHotDesk',cosParams['cost']['AllowHotDesk'])
        cosParams['cost']['AllowHuntBusyOut']=kwargs.get('AllowHuntBusyOut',cosParams['cost']['AllowHuntBusyOut'])
        cosParams['cost']['AllowIM']=kwargs.get('AllowIM',cosParams['cost']['AllowIM'])
        cosParams['cost']['AllowInterSiteVideoCalls']=kwargs.get('AllowInterSiteVideoCalls',cosParams['cost']['AllowInterSiteVideoCalls'])
        cosParams['cost']['AllowIntercomPaging']=kwargs.get('AllowIntercomPaging',cosParams['cost']['AllowIntercomPaging'])
        cosParams['cost']['AllowPSTNAnyphone']=kwargs.get('AllowPSTNAnyphone',cosParams['cost']['AllowPSTNAnyphone'])
        cosParams['cost']['AllowPSTNFailover']=kwargs.get('AllowPSTNFailover',cosParams['cost']['AllowPSTNFailover'])
        cosParams['cost']['AllowPaging']=kwargs.get('AllowPaging',cosParams['cost']['AllowPaging'])
        cosParams['cost']['AllowProgramOwnButtons']=kwargs.get('AllowProgramOwnButtons',cosParams['cost']['AllowProgramOwnButtons'])
        cosParams['cost']['AllowRecordingOthersCalls']=kwargs.get('AllowRecordingOthersCalls',cosParams['cost']['AllowRecordingOthersCalls'])
        cosParams['cost']['AllowRecordingOwnCalls']=kwargs.get('AllowRecordingOwnCalls',cosParams['cost']['AllowRecordingOwnCalls'])
        cosParams['cost']['AllowRingAll']=kwargs.get('AllowRingAll',cosParams['cost']['AllowRingAll'])
        cosParams['cost']['AllowSilentMonitor']=kwargs.get('AllowSilentMonitor',cosParams['cost']['AllowSilentMonitor'])
        cosParams['cost']['AllowUploadofPerContacts']=kwargs.get('AllowUploadofPerContacts',cosParams['cost']['AllowUploadofPerContacts'])
        cosParams['cost']['AllowViewPresence']=kwargs.get('AllowViewPresence',cosParams['cost']['AllowViewPresence'])
        cosParams['cost']['AllowWhisperPaging']=kwargs.get('AllowWhisperPaging',cosParams['cost']['AllowWhisperPaging'])
        cosParams['cost']['BOSSKeyID']=kwargs.get('BOSSKeyID',cosParams['cost']['BOSSKeyID'])

        cosParams['cost']['CFENScopeID']=kwargs.get('CFENScopeID',cosParams['cost']['CFENScopeID'])
        cosParams['cost']['COSTID']=kwargs.get('COSTID',cosParams['cost']['COSTID'])
        cosParams['cost']['COSTName']=kwargs.get('COSTName',cosParams['cost']['COSTName'])
        cosParams['cost']['EnableEnumHeldCalls4Unpark']=kwargs.get('EnableEnumHeldCalls4Unpark',cosParams['cost']['EnableEnumHeldCalls4Unpark'])
        cosParams['cost']['IMPrivacySetting']=kwargs.get('IMPrivacySetting',cosParams['cost']['IMPrivacySetting'])

        cosParams['cost']['MaxBuddiesPerUser']=kwargs.get('MaxBuddiesPerUser',cosParams['cost']['MaxBuddiesPerUser'])
        cosParams['cost']['MaxCallStackDepth']=kwargs.get('MaxCallStackDepth',cosParams['cost']['MaxCallStackDepth'])
        cosParams['cost']['MaxPartiesMakeMeConference']=kwargs.get('MaxPartiesMakeMeConference',cosParams['cost']['MaxPartiesMakeMeConference'])
        cosParams['cost']['MaxPrivateContacts']=kwargs.get('MaxPrivateContacts',cosParams['cost']['MaxPrivateContacts'])
        cosParams['cost']['ShowCallHistory']=kwargs.get('ShowCallHistory',cosParams['cost']['ShowCallHistory'])
        cosParams['cost']['TenantID']=kwargs.get('TenantID',cosParams['cost']['TenantID'])
        cosParams['cost']['AcceptIntercomPagingDN_formatted']=kwargs.get('AcceptIntercomPagingDN_formatted',cosParams['cost']['AcceptIntercomPagingDN_formatted'])
        cosParams['cost']['AcceptWhisperPagingDN_formatted']=kwargs.get('AcceptWhisperPagingDN_formatted',cosParams['cost']['AcceptWhisperPagingDN_formatted'])
        cosParams['cost']['AcceptBargeInDN_formatted']=kwargs.get('AcceptBargeInDN_formatted',cosParams['cost']['AcceptBargeInDN_formatted'])
        cosParams['cost']['AcceptRecordingOthersDN_formatted']=kwargs.get('AcceptRecordingOthersDN_formatted',cosParams['cost']['AcceptRecordingOthersDN_formatted'])
        cosParams['cost']['AcceptSilentMonitorDN_formatted']=kwargs.get('AcceptSilentMonitorDN_formatted',cosParams['cost']['AcceptSilentMonitorDN_formatted'])

        cosParams['cost']['CFENExceptions']=kwargs.get('CFENExceptions',cosParams['cost']['CFENExceptions'])
        cosParams['cost']['CFENRestrictions']=kwargs.get('CFENRestrictions',cosParams['cost']['CFENRestrictions'])

        urlChangeIT = "http://%s:%s/director/costs/%s.json" %(self.ip, self.pno,cosID)
        result = self.client.put(urlChangeIT, json=cosParams,headers = {"X-CSRF-Token": self.token,"Content-Type": "application/json"})
        if result.status_code == 200:
            return True
        else:
            return False

    def create_modify_BCA(self, **kwargs):
        '''
        :param kwargs:
        create_modify_BCA
        :return:
        '''
        #self.refreshToken()

        urlGetAllBCA = "http://%s:%s/director/bridged_call_appearances/list" %(self.ip, self.pno)
        BCAs = self.client.get(urlGetAllBCA).json()
        self.bcaID = None
        if kwargs.get('name'):
            for rows in BCAs['rows']:
                if rows['cell'][0] == kwargs.get('name'):
                    print('BCA profile exist with given name')
                    return False
        for rows in BCAs['rows']:
            if rows['cell'][1] == kwargs.get('extension',''):
                self.bcaID = rows['id']
                break
        self.urlGetBCA = None
        self.urlChangeIT = None
        if self.bcaID is None: # create new
            print("Creating new BCA profile")
            self.urlGetBCA = r'http://%s:%s/director/bridged_call_appearances/new.json'% (self.ip, self.pno)
            self.urlChangeIT = r'http://%s:%s/director/bridged_call_appearances.json'% (self.ip, self.pno)
            if not kwargs.get('name'):
                print("name is mandatory parameter")
                return False
        else:
            self.urlGetBCA = r'http://%s:%s/director/bridged_call_appearances/%s.json'% (self.ip, self.pno, self.bcaID)
            self.urlChangeIT = "http://%s:%s/director/bridged_call_appearances/%s.json" %(self.ip, self.pno,self.bcaID)
            # return False

        bcaParams = self.client.get(self.urlGetBCA).json()
        bcaParams['bca']['AllowBridgeConferencing']=kwargs.get('AllowBridgeConferencing',bcaParams['bca']['AllowBridgeConferencing'])
        bcaParams['bca']['CallStackDepth']=kwargs.get('CallStackDepth',bcaParams['bca']['CallStackDepth'])
        bcaParams['bca']['NoAnswerRings']=kwargs.get('NoAnswerRings',bcaParams['bca']['NoAnswerRings'])
        bcaParams['bca']['PrivacyEnabled']=kwargs.get('PrivacyEnabled',bcaParams['bca']['PrivacyEnabled'])
        bcaParams['bca']['SiteID']=kwargs.get('SiteID',bcaParams['bca']['SiteID'])
        bcaParams['bca']['SwitchID']=kwargs.get('SwitchID',bcaParams['bca']['SwitchID'])
        bcaParams['bca']['ToneEnabled']=kwargs.get('ToneEnabled',bcaParams['bca']['ToneEnabled'])
        bcaParams['bca']['CFNoAnswer_formatted']=kwargs.get('CFNoAnswer',bcaParams['bca']['CFNoAnswer_formatted'])
        bcaParams['bca']['CFBusy_formatted']=kwargs.get('CFBusy',bcaParams['bca']['CFBusy_formatted'])
        bcaParams['bca']['OutCallerID_formatted']=kwargs.get('OutCallerID',bcaParams['bca']['OutCallerID_formatted'])
        bcaParams['bca']['BackupDN_formatted']=kwargs.get('BackupDN',bcaParams['bca']['BackupDN_formatted'])
        bcaParams['bca']['dn_attributes']['Description']=kwargs.get('name',bcaParams['bca']['dn_attributes']['Description'])
        self.ExtenNum = bcaParams['bca']['dn_attributes']['DN']
        self.result = None
        if self.bcaID is None:
            self.result = self.client.post(self.urlChangeIT, json=bcaParams,headers = {"X-CSRF-Token": self.token,"Content-Type": "application/json"})
        else:
            self.result = self.client.put(self.urlChangeIT, json=bcaParams,headers = {"X-CSRF-Token": self.token,"Content-Type": "application/json"})
        if self.result.status_code == 200:
            if self.ExtenNum is not None:
                return self.ExtenNum
            return True
        else:
            return False

    def modify_telephony_options(self, **kwargs):
        '''
        :param kwargs:
        modify_telephony_options
        :return:
        '''
        #self.refreshToken()
        urlGetTelephonyOptions = "http://%s:%s/director/ip_phone_options.json" %(self.ip, self.pno)
        telephonyOptions = self.client.get(urlGetTelephonyOptions).json()
        telephonyOptions['ip_phone_options']['DelayAfterCollectDigits'] =kwargs.get('DelayAfterCollectDigits',telephonyOptions['ip_phone_options']['DelayAfterCollectDigits'])
        telephonyOptions['ip_phone_options']['UnassignedIPPhoneUserGroupID'] =kwargs.get('UserGroupForUnassignedIP',telephonyOptions['ip_phone_options']['UnassignedIPPhoneUserGroupID'])
        telephonyOptions['ip_phone_options']['UnassignedTelephoneUserGroupID'] = kwargs.get('UserGroupForAnonymousPhones',telephonyOptions['ip_phone_options']['UnassignedTelephoneUserGroupID'])
        urlChangeIT = "http://%s:%s/director/ip_phone_options.json" %(self.ip, self.pno)
        result = self.client.put(urlChangeIT, json=telephonyOptions,headers = {"X-CSRF-Token": self.token,"Content-Type": "application/json"})
        if result.status_code == 200:
            return True
        else:
            return False

    def create_modify_hunt_group(self,**args):
        """ Method will create new HG if extension is not provided, else will modify
        :param :
        :param args: (extension, BackupExtension,HuntGroupMember, HuntGroupName, OnHourSchedule, HolidaySchedule, CallStackFull, NoAnswer, OffHoursHoliday, HuntPatternID, RingsPerMember, NoAnswerRings, SkipMemberIfAlreadyOnCall, CallMemberWhenForwarding, MakeExtensionPrivate,IncludeInSystemDialByName)
        :return: Hunt group extension
        """
        #self.refreshToken()
        if not args.get('extension'):
            print("Creating new Hunt Group")
            getParams = r'http://%s:%s/director/hunt_groups/new.json'% (self.ip, self.pno)
            createHG = r'http://%s:%s/director/hunt_groups.json'% (self.ip, self.pno)
        else:
            print("Modifying Hunt Group")
            urlGetAllHG = "http://%s:%s/director/hunt_groups/list" %(self.ip, self.pno)
            HGs = self.client.get(urlGetAllHG).json()
            self.hgID = None
            for rows in HGs['rows']:
                if rows['cell'][1] == str(args.get('extension')):
                    self.hgID = rows['id']
                    break
            if not self.hgID:
                print("HG Extension doesn't exist, please create new")
                return False
            getParams = r'http://%s:%s/director/hunt_groups/%s.json'% (self.ip, self.pno,self.hgID)
            createHG = r'http://%s:%s/director/hunt_groups/%s.json'% (self.ip, self.pno,self.hgID)

        modifyHGParams = self.client.get(getParams).json() # This should give json for creating HG with all params.
        group_members = []
        if args.get("HuntGroupMember") != None :
            url = r'http://%s:%s/director/dns/list?list=hunt_group' % (self.ip, self.pno)
            user_json = self.client.get(url).json()
            for HGMembers in args.get("HuntGroupMember"):
                for users in user_json['rows']:
                    if str(HGMembers) == users["cell"][0]:
                        group_members.append(users['cell'][0])
                        break
                if str(HGMembers) not in group_members :
                    print("Extension " + str(HGMembers) + " not found in system ")
                    return False
        # Insert all the values to json
        modifyHGParams['hunt_group']['dn_ids']=group_members
        # modifyHGParams['hunt_group']['BackupDN'] = args.get('BackupExtension')
        modifyHGParams['hunt_group']['dn_attributes']['Description'] = args.get("HuntGroupName","Created from D2 API")
        modifyHGParams['hunt_group']['BackupDN_formatted'] =args.get('BackupExtension')
        modifyHGParams['hunt_group']['CFBusy_formatted']=args.get('CallStackFull',modifyHGParams['hunt_group']['CFBusy_formatted'])
        modifyHGParams['hunt_group']['CFNoAnswer_formatted']=args.get('NoAnswer',modifyHGParams['hunt_group']['CFNoAnswer_formatted'])
        modifyHGParams['hunt_group']['CFOffHoursHoliday_formatted']=args.get('OffHoursHoliday',modifyHGParams['hunt_group']['CFOffHoursHoliday_formatted'])
        modifyHGParams['hunt_group']['HuntPatternID']=args.get('HuntPatternID',modifyHGParams['hunt_group']['HuntPatternID']) # 1/4
        modifyHGParams['hunt_group']['RingsPerMember']=args.get('RingsPerMember',modifyHGParams['hunt_group']['RingsPerMember'])
        modifyHGParams['hunt_group']['NoAnswerRings']=args.get('NoAnswerRings',modifyHGParams['hunt_group']['NoAnswerRings'])
        modifyHGParams['hunt_group']['IsOneHuntCallPerMember']=args.get('SkipMemberIfAlreadyOnCall',modifyHGParams['hunt_group']['IsOneHuntCallPerMember'])
        modifyHGParams['hunt_group']['IsDefeatCallHandling']=args.get('CallMemberWhenForwarding',modifyHGParams['hunt_group']['IsDefeatCallHandling'])
        modifyHGParams['hunt_group']['dn_attributes']['Hidden']=args.get('MakeExtensionPrivate',modifyHGParams['hunt_group']['dn_attributes']['Hidden'])
        modifyHGParams['hunt_group']['dn_attributes']['include_in_dial_by_name']=args.get('IncludeInSystemDialByName',modifyHGParams['hunt_group']['dn_attributes']['include_in_dial_by_name'])
        modifyHGParams['hunt_group']['OnHourScheduleID']=args.get('OnHourSchedule',modifyHGParams['hunt_group']['OnHourScheduleID']) # 1/2/3...
        modifyHGParams['hunt_group']['HolidayScheduleID']= args.get('HolidaySchedule',modifyHGParams['hunt_group']['HolidayScheduleID'])
        modifyHGParams['hunt_group']['current_time_type']= args.get('CurrentTimeType',modifyHGParams['hunt_group']['current_time_type'])

        if not args.get('extension'):
            outp = self.client.post(createHG,json=modifyHGParams,headers = {"X-CSRF-Token": self.token,"Content-Type": "application/json"})
            return modifyHGParams['hunt_group']['dn_attributes']['DN']
        else:
            outp = self.client.put(createHG,json=modifyHGParams,headers = {"X-CSRF-Token": self.token,"Content-Type": "application/json"})
        if outp.status_code == 200:
            return True
        else:
            return False

    def delete_BCA_profile(self, ExtensionNumber):
        '''
        :param ExtensionNumber:
        :return:
        '''
        #self.refreshToken()
        urlBCA = r'http://%s:%s/director/bridged_call_appearances/list'% (self.ip, self.pno)
        AvailableBCA = self.client.get(urlBCA).json()

        for rows in AvailableBCA['rows']:
            if rows['cell'][1] == str(ExtensionNumber):
                urlDelete = r'http://%s:%s/director/bridged_call_appearances/%s.json'% (self.ip, self.pno,rows['id'])
                status = self.client.delete(urlDelete,headers = {"X-CSRF-Token": self.token})
                if status.status_code == 200:
                    return True
                else:
                    return False
        raise Exception("Extension number not found in the system")

    def create_modify_onhours_schedules(self,**args):
        """ Method will create new onhours schedule if extension is not provided, else will modify
        :param :
        :param args:ScheduleName, TimeZone,
        :return:
        """
        urlGetAllSchedules = "http://%s:%s/director/schedules_on_hours/list" %(self.ip, self.pno)
        Schedules = self.client.get(urlGetAllSchedules).json()
        ID = None
        for rows in Schedules['rows']:
            if rows['cell'][0] == str(args.get('ScheduleName')):
                ID = rows['id']
                break
        if not ID:
            print("Schedules doesn't exist, creating new")
            getParams = r'http://%s:%s/director/schedules_on_hours/new.json'% (self.ip, self.pno)
            createSchedule = r'http://%s:%s/director/schedules_on_hours.json'% (self.ip, self.pno)
        else:
            print("Modifying Schedule")
            getParams = r'http://%s:%s/director/schedules_on_hours/%s.json'% (self.ip, self.pno,ID)
            createSchedule = r'http://%s:%s/director/schedules_on_hours/%s.json'% (self.ip, self.pno,ID)

        modifySchedules = self.client.get(getParams).json()

        modifySchedules['schedules_on_hour']['ScheduleName'] =args.get('ScheduleName', modifySchedules['schedules_on_hour']['ScheduleName'])
        # modifySchedules['schedules_on_hour']['TimeZone']= 'US Eastern Standard Time'
        modifySchedules['schedules_on_hour']['TimeZone']= args.get('TimeZone',modifySchedules['schedules_on_hour']['TimeZone'])

        # for schs in args.get('Schedules'):
        #     schs[]
        modifySchedules['schedules_on_hour']['schedule_items_attributes'] = args.get('Schedules')

        if not ID:
            outp = self.client.post(createSchedule,json=modifySchedules,headers = {"X-CSRF-Token": self.token,"Content-Type": "application/json"})
            # return modifyHGParams['hunt_group']['dn_attributes']['DN']
        else:
            outp = self.client.put(createSchedule,json=modifySchedules,headers = {"X-CSRF-Token": self.token,"Content-Type": "application/json"})
        if outp.status_code == 200:
            try:
                return outp.json()['schedules_on_hour']['ScheduleID']
            except:
                print("failed to create / modify schedules")
                return  False
        else:
            return False

    def delete_onhours_schedule(self, ScheduleName):
        '''
        :param ScheduleName:
        :return:
        '''
        urlGetAllSchedules = "http://%s:%s/director/schedules_on_hours/list" %(self.ip, self.pno)
        Schedules = self.client.get(urlGetAllSchedules).json()
        ID = None
        for rows in Schedules['rows']:
            if rows['cell'][0] == str(ScheduleName):
                ID = rows['id']
                break
        if not ID:
            raise Exception("Schedule Name not found in the system")
        else:
            urlDelete = r'http://%s:%s/director/schedules_on_hours/%s.json'% (self.ip, self.pno,ID)
            status = self.client.delete(urlDelete,headers = {"X-CSRF-Token": self.token})
            if status.status_code == 200:
                return True
            else:
                return False

    def create_modify_holiday_schedule(self, **args):
        """ Method will create new holiday schedule if name is not provided, else will modify
        :param :
        :param args:ScheduleName, TimeZone,
        :return:
        """
        urlGetAllSchedules = "http://%s:%s/director/schedules_holidays/list" %(self.ip, self.pno)
        Schedules = self.client.get(urlGetAllSchedules).json()
        ID = None
        for rows in Schedules['rows']:
            if rows['cell'][0] == str(args.get('ScheduleName')):
                ID = rows['id']
                break
        if not ID:
            print("Schedules doesn't exist, creating new")
            getParams = r'http://%s:%s/director/schedules_holidays/new.json'% (self.ip, self.pno)
            createSchedule = r'http://%s:%s/director/schedules_holidays.json'% (self.ip, self.pno)
        else:
            print("Modifying Schedule")
            getParams = r'http://%s:%s/director/schedules_holidays/%s.json'% (self.ip, self.pno,ID)
            createSchedule = r'http://%s:%s/director/schedules_holidays/%s.json'% (self.ip, self.pno,ID)

        modifySchedules = self.client.get(getParams).json()
        modifySchedules['schedules_holiday']['ScheduleName']=args.get('ScheduleName')
        modifySchedules['schedules_holiday']['TimeZone']=args.get('TimeZone')
        modifySchedules['schedules_holiday']['schedule_items_attributes'] = args.get('Schedules')
        if not ID:
            outp = self.client.post(createSchedule,json=modifySchedules,headers = {"X-CSRF-Token": self.token,"Content-Type": "application/json"})
            # return modifyHGParams['hunt_group']['dn_attributes']['DN']
        else:
            outp = self.client.put(createSchedule,json=modifySchedules,headers = {"X-CSRF-Token": self.token,"Content-Type": "application/json"})
            # return ID
        if outp.status_code == 200:
            try:
                return outp.json()['schedules_holiday']['ScheduleID']
            except:
                print("failed to create / modify schedules")
                return  False
        else:
            return False

    def delete_holiday_schedule(self, ScheduleName):
        '''
        :param ScheduleName:
        :return:
        '''
        urlGetAllSchedules = "http://%s:%s/director/schedules_holidays/list" %(self.ip, self.pno)
        Schedules = self.client.get(urlGetAllSchedules).json()
        ID = None
        for rows in Schedules['rows']:
            if rows['cell'][0] == str(ScheduleName):
                ID = rows['id']
                break
        if not ID:
            raise Exception("Schedule Name not found in the system")
        else:
            urlDelete = r'http://%s:%s/director/schedules_holidays/%s.json'% (self.ip, self.pno,ID)
            status = self.client.delete(urlDelete,headers = {"X-CSRF-Token": self.token})
            if status.status_code == 200:
                return True
            else:
                return False

    def create_modify_custom_schedule(self, **args):
        """ Method will create new custom schedule if name is not provided, else will modify
        :param :
        :param args:ScheduleName, TimeZone,
        :return:
        """
        urlGetAllSchedules = "http://%s:%s/director/schedules_customs/list" %(self.ip, self.pno)
        Schedules = self.client.get(urlGetAllSchedules).json()
        ID = None
        for rows in Schedules['rows']:
            if rows['cell'][0] == str(args.get('ScheduleName')):
                ID = rows['id']
                break
        if not ID:
            print("Schedules doesn't exist, creating new")
            getParams = r'http://%s:%s/director/schedules_customs/new.json'% (self.ip, self.pno)
            createSchedule = r'http://%s:%s/director/schedules_customs.json'% (self.ip, self.pno)
        else:
            print("Modifying Schedule")
            getParams = r'http://%s:%s/director/schedules_customs/%s.json'% (self.ip, self.pno,ID)
            createSchedule = r'http://%s:%s/director/schedules_customs/%s.json'% (self.ip, self.pno,ID)

        modifySchedules = self.client.get(getParams).json()
        modifySchedules['schedules_custom']['ScheduleName']=args.get('ScheduleName')
        modifySchedules['schedules_custom']['TimeZone']=args.get('TimeZone')
        modifySchedules['schedules_custom']['schedule_items_attributes'] = args.get('Schedules')
        if not ID:
            outp = self.client.post(createSchedule,json=modifySchedules,headers = {"X-CSRF-Token": self.token,"Content-Type": "application/json"})
            # return modifyHGParams['hunt_group']['dn_attributes']['DN']
        else:
            outp = self.client.put(createSchedule,json=modifySchedules,headers = {"X-CSRF-Token": self.token,"Content-Type": "application/json"})
        if outp.status_code == 200:
            try:
                return outp.json()['schedules_custom']['ScheduleID']
            except:
                print("failed to create / modify schedules")
                return  False
        else:
            return False

    def delete_custom_schedule(self, ScheduleName):
        '''
        :param ScheduleName:
        :return:
        '''
        urlGetAllSchedules = "http://%s:%s/director/schedules_customs/list" %(self.ip, self.pno)
        Schedules = self.client.get(urlGetAllSchedules).json()
        ID = None
        for rows in Schedules['rows']:
            if rows['cell'][0] == str(ScheduleName):
                ID = rows['id']
                break
        if not ID:
            raise Exception("Schedule Name not found in the system")
        else:
            urlDelete = r'http://%s:%s/director/schedules_customs/%s.json'% (self.ip, self.pno,ID)
            status = self.client.delete(urlDelete,headers = {"X-CSRF-Token": self.token})
            if status.status_code == 200:
                return True
            else:
                return False

    def get_user_id(self,user_extension):
        """

        :param user_extension: fully qualified extension for the user
        :return: the id of the user
        """
        user_id = None
        url = r'http://%s:%s/director/users_phones/list?rows=5000' % (self.ip, self.pno)
        r = self.client.get(url)
        for user in r.json()["rows"]:
            if user_extension == user["cell"][2]:
                user_id = user['id']
        if user_id is None:
            print("Can not get the id of user")
        return user_id

    def get_user_specific_json(self, user_id):
        """

        :param user_id: downloads the user specific json e.g. 1556.json
        :return: return the json content for the user
        """
        # url = r'http://%s:%s/director/users_phones/%s.json' % (self.ip, self.pno, str(user_id)) # returns only 5 keys
        url = r'http://%s:%s/director/users/%s.json' % (self.ip, self.pno, str(user_id))          # returns 10 keys
        user_json = self.client.get(url).json()
        return user_json

    def put_user_json(self, id, json_to_put, telephony=False):
        """

        :param id: the id of the user
        :param json_to_put: json content for the user
        :param telephony: True if the request is to change telephony will affect the constructed url to send request
        :return: True if status is 200 else False
        """
        url = r'http://%s:%s/director/users_phones/%s.json' % (self.ip, self.pno, str(id))
        if telephony:
            url = r'http://%s:%s/director/users/%s.json' % (self.ip, self.pno, str(id))
        r = self.client.put(url, json=json_to_put,
                            headers={"X-CSRF-Token": self.token, "Content-Type": "application/json"})
        if r.status_code == 200:
            return True
        else:
            return False

    def modify_user_telephony_attributes(self,user_extension, **kwargs):
        """
        to modify the telephony related values for a user
        Users->users->Select user->Telephony Tab(below)-> CallStackDepth,Ring Type, Wallpaper etc.
        :param user_extension: fully qualified extension for the user i.e. UserDN
        :param kwargs: a dictionary with the values to change e.g.
        "call_stack_depth"         : to change call depth use
        "incoming_calls_ring"      : the label of the phone i.e. external,Primary Phone etc.
        :return: same as the return of put_user_json method
        """
        id = self.get_user_id(user_extension)
        user_json = self.get_user_specific_json(id)    # user_json['collections']["pstn_phones"]
        user_json['user']['CurrentCallStackDepth'] = kwargs.get("call_stack_depth",user_json['user']['CurrentCallStackDepth'])
        if "incoming_calls_ring" in kwargs:
            for phone in user_json['collections']["pstn_phones"]:
                if phone["description"] == kwargs["incoming_calls_ring"]:
                    val_to_set = phone["id"]
                    user_json['user']['incoming_calls_ring'] = val_to_set
                    break
            else:
                print("Unable to set incoming_calls_ring. Can not find id of phone with label <%s>"%kwargs["incoming_calls_ring"])
                return False

        return self.put_user_json(id,user_json,True)


    def put_json_to_server(self, url, json_to_put):
        """
        :param url: the server url
        :param json_to_put: json content to send to server
        :return: True if status is 200 else False
        """
        url = url
        r = self.client.put(url, json=json_to_put,
                            headers={"X-CSRF-Token": self.token, "Content-Type": "application/json"})
        if r.status_code == 200:
            return r
        else:
            return False

    def get_all_codeclists(self, specific_cl_json=False):
        """returns all the available codec lists or a codec list specific json if
            specific_cl_json is not False
        """
        if not specific_cl_json:
            url = r'http://%s:%s/director/codec_lists/list' % (self.ip, self.pno)
            codec_lists = self.client.get(url).json()
            return codec_lists
        else:
            url = r'http://%s:%s/director/codec_lists/%s' % (self.ip, self.pno, specific_cl_json)
            cl_json = self.client.get(url).json()
            return cl_json


    def get_all_codecs(self):
        """returns all the available codecs"""
        url = r'http://%s:%s/director/codecs/list' % (self.ip, self.pno)
        codecs = self.client.get(url).json()
        return codecs

    def order_codecs_in_codeclist(self, codeclist, codecs_to_set, **kwargs):
        """
        Administration-> Features-> Call Control-> Codecs List
        :param codeclist: the name of codec list to modify
        :param codecs_to_set: the list of codecs in the required order(first in this list will appear at the top on D2 UI)
        :param kwargs: for future use
        :return: True if successful
        """
        codec_lists = self.get_all_codeclists()
        codecs = self.get_all_codecs()
        cl_id = None
        for cl in codec_lists['rows']:
            if codeclist == cl['cell'][0]:
                cl_id = cl['id']
                break
        if not cl_id:
            print("Requested codeclist <%s> not present in the system.Could be a spelling mistake.\nAborting..."%codeclist)
            os._exit(1)

        codecs_to_set_ids = []
        for c in codecs_to_set:
            for codec in codecs['rows']:
                if c == codec['cell'][0]:
                    id = codec['id']
                    codec_to_set = {"Description":c, "CodecID":id, "id":id}
                    codecs_to_set_ids.append(codec_to_set)
                    break
        if len(codecs_to_set) != len(codecs_to_set_ids):
            print("Some of the codecs not found. Found/Valid codecs among requested codecs are <%s>"%(codecs_to_set_ids))

        # Getting the json for the requested codec list
        cl_json = self.get_all_codeclists(specific_cl_json = cl_id)
        # inserting the list of requested codecs into the codec list json
        cl_json["codec_list"]["selected_codecs"] = codecs_to_set_ids
        cl_json["codec_list"]["LastUpdateUTCTime"] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        cl_json["codec_list"]["codec_ids"] = [x['id'] for x in codecs_to_set_ids]
        # creating the json payload
        json_to_put = {"collections": {}, "codec_list": cl_json["codec_list"], "general_messages": cl_json["general_messages"],
                       "select_general": 'true', "$resolved": 'true'}
        # putting the updated json to server
        url = r'http://%s:%s/director/codec_lists/%s.json' % (self.ip, self.pno, cl_id)
        r = self.put_json_to_server(url, json_to_put)
        if r:
            if r.json()['codec_list']["selected_codecs"][0]["Description"] == codecs_to_set[0]:
                return True
            else:
                return False
        else:
            return False

    def modify_user_telephony_attributes(self,user_extension, **kwargs):
        """
        to modify the telephony related values for a user
        Users->users->Select user->Telephony Tab(below)-> CallStackDepth,Ring Type, Wallpaper etc.
        :param user_extension: fully qualified extension for the user
        :param kwargs: a dictionary with the values to change e.g.
        to change call depth use "call_stack_depth"
        :return: same as the return of put_user_json method
        """
        id = self.get_user_id(user_extension)
        user_json = self.get_user_specific_json(id)
        user_json['user']['CurrentCallStackDepth'] = kwargs.get("call_stack_depth",user_json['user']['CurrentCallStackDepth'])
        return self.put_user_json(id,user_json,True)

    def modify_moh_system_defaults(self,**kwargs):
        """
        to modify the moh_system_defaults
        Features->MOH->System Defaults
        :return: boolean
        """
        url = r'http://%s:%s/director/moh_system_defaults.json?TenantID=1' % (self.ip, self.pno)
        if not kwargs.get('internal_call') or not kwargs.get('file_to_select') :
            print("arguments internal_call and file_to_select are mandatory")
            return False
        r = self.client.get(url)
        if r.status_code == 200:
            jsonOut= r.json()
            if str(kwargs.get('file_to_select')).lower() =='jack based':
                jsonOut['moh_options']['MOHResourceID'] = None
            else:
                for files in jsonOut['collections']['internal_calls_options']:
                    if str(files['description']).lower() == str(kwargs.get('file_to_select')).lower():
                        filelD = files['id']
                        jsonOut['moh_options']['MOHResourceID'] =filelD
                        break
            url = r'http://%s:%s/director/moh_system_defaults.json' % (self.ip, self.pno)
            # update json and put to server
            jsonOut['moh_options']['InternalMOHToneID']=kwargs.get('internal_call')

            try:
                r = self.client.put(url, json=jsonOut,headers={"X-CSRF-Token": self.token, "Content-Type": "application/json"})
            except:
                print(str(sys.exc_info()[0]))
            if r.status_code == 200:
                return True
            else:
                return False
        else:
            print('Failed to fetch MOH system defaults')
            return False

    def create_modify_user_groups(self, **args):
        """ Method will create new user group if name is not provided, else will modify
        :param :
        :param args:
        :return:
        """
        urlGetAllUserGroups = "http://%s:%s/director/user_groups/list" %(self.ip, self.pno)
        user_groups = self.client.get(urlGetAllUserGroups).json()
        ID = None
        if not args.get('user_group_name'):
            print("Argument 'user_group_name' is mandatory")
            return False
        for rows in user_groups['rows']:
            if rows['cell'][0] == str(args.get('user_group_name')):
                ID = rows['id']
                break
        if not ID:
            print("User Group doesn't exist, creating new")
            getParams = r'http://%s:%s/director/user_groups/new.json?TenantID=1'% (self.ip, self.pno)
            createUG = r'http://%s:%s/director/user_groups.json'% (self.ip, self.pno)
        else:
            print("Modifying User group")
            getParams = r'http://%s:%s/director/user_groups/%s.json'% (self.ip, self.pno,ID)
            createUG = r'http://%s:%s/director/user_groups/%s.json'% (self.ip, self.pno,ID)

        modifyUG = self.client.get(getParams).json()

        modifyUG['user_group']['UserGroupName'] = args.get('user_group_name')
        modifyUG['user_group']['ShowAccountCodes'] = args.get('show_account_codes',modifyUG['user_group']['ShowAccountCodes'])
        modifyUG['user_group']['AccountCodeTypeID'] = args.get('account_code_type',modifyUG['user_group']['AccountCodeTypeID'])
        modifyUG['user_group']['SendCIDAsCESID'] = args.get('send_caller_id',modifyUG['user_group']['SendCIDAsCESID'])
        modifyUG['user_group']['SendDIDAsCESID'] = args.get('send_DID',modifyUG['user_group']['SendDIDAsCESID'])
        modifyUG['user_group']['COSCPID'] = args.get('cos_call_permissions',modifyUG['user_group']['COSCPID'])
        modifyUG['user_group']['COSTID'] = args.get('cos_telephony_id',modifyUG['user_group']['COSTID'])
        modifyUG['user_group']['COSVMID'] = args.get('cos_voice_mail',modifyUG['user_group']['COSVMID'])
        modifyUG['user_group']['selected_trunk_groups'] = [{}]
        if args.get('file_to_select'):
            if str(args.get('file_to_select')).lower() =='system defaults':
                modifyUG['user_group']['MOHResourceID'] = None
            else:
                for files in modifyUG['collections']['moh_options']:
                        if str(files['description']).lower() == str(args.get('file_to_select')).lower():
                            modifyUG['user_group']['MOHResourceID'] = files['id']
                            break
        if not ID:
            outp = self.client.post(createUG,json=modifyUG,headers = {"X-CSRF-Token": self.token,"Content-Type": "application/json"})
            # return modifyHGParams['hunt_group']['dn_attributes']['DN']
        else:
            outp = self.client.put(createUG,json=modifyUG,headers = {"X-CSRF-Token": self.token,"Content-Type": "application/json"})
        if outp.status_code == 200:
            try:
                return outp.json()['user_group']['UserGroupID']
            except:
                print("failed to create / modify user groups")
                return  False
        else:
            return False

    def create_modify_pickup_group(self, **kwargs):
        '''
        :param kwargs:
        create_modify_pickup_group
        :return:
        '''
        urlGetAllPickupGroups = "http://%s:%s/director/group_pickups/list?rows=100" %(self.ip, self.pno)
        PGs = self.client.get(urlGetAllPickupGroups).json()
        pgID = None
        if kwargs.get('extension'):
            for rows in PGs['rows']:
                if rows['cell'][1] == kwargs.get('extension'):
                    print('Pickup profile exist, modifying')
                    pgID = rows['id']
                    break
        urlGetPG = None
        urlChangeIT = None

        if pgID is None: # create new
            print("Creating new Pick Group profile")
            urlGetPG = r'http://%s:%s/director/group_pickups/new.json'% (self.ip, self.pno)
            urlChangeIT = r'http://%s:%s/director/group_pickups.json'% (self.ip, self.pno)
            if not kwargs.get('name'):
                print("name is mandatory parameter")
                return False
        else:
            urlGetPG = r'http://%s:%s/director/group_pickups/%s.json'% (self.ip, self.pno, pgID)
            urlChangeIT = "http://%s:%s/director/group_pickups/%s.json" %(self.ip, self.pno,pgID)

        pgParams = self.client.get(urlGetPG).json()
        pgParams['pickup_group']['dn_attributes']['Description'] = kwargs.get('name',pgParams['pickup_group']['dn_attributes']['Description'])
        extensionListID = None
        if kwargs.get('extension_list_name'):
            urlExtList = r'http://%s:%s/director/extension_lists/list?_search=false&rows=250'% (self.ip, self.pno)
            AvailableExtList = self.client.get(urlExtList).json()
            for rows in AvailableExtList['rows']:
                if rows['cell'][0] == kwargs.get('extension_list_name'):
                    extensionListID = rows['id']
            if not extensionListID:
                print("Extension List is missing in the system")
                return False
            pgParams['pickup_group']['ExtensionListID'] = extensionListID
        pgParams['pickup_group']['SwitchID'] = kwargs.get('switch',pgParams['pickup_group']['SwitchID'] )

        if not pgID:
            outp = self.client.post(urlChangeIT,json=pgParams,headers = {"X-CSRF-Token": self.token,"Content-Type": "application/json"})
            # return modifyHGParams['hunt_group']['dn_attributes']['DN']
        else:
            outp = self.client.put(urlChangeIT,json=pgParams,headers = {"X-CSRF-Token": self.token,"Content-Type": "application/json"})
        if outp.status_code == 200:
            try:
                return outp.json()['pickup_group']['GROUP_DN']
            except:
                print("failed to create / modify user groups")
                return  False
        else:
            return False

    def delete_pickup_group(self, **kwargs):
        '''
        :param kwargs:
        create_modify_pickup_group
        :return:
        '''
        if not kwargs.get('extension'):
            print("extension is mandatory parameter")
            return  False
        urlGetAllPickupGroups = "http://%s:%s/director/group_pickups/list?rows=100" %(self.ip, self.pno)
        PGs = self.client.get(urlGetAllPickupGroups).json()
        pgID = None
        if kwargs.get('extension'):
            for rows in PGs['rows']:
                if rows['cell'][1] == str(kwargs.get('extension')):
                    pgID = rows['id']
                    break
        if not pgID:
            print("Extension doesn't exist")
            return False
        urlDelete = r'http://%s:%s/director/group_pickups/%s.json'% (self.ip, self.pno,pgID)
        status = self.client.delete(urlDelete,headers = {"X-CSRF-Token": self.token})
        if status.status_code == 200:
            return True
        else:
            return False

    def create_modify_work_group(self, **kwargs):
        '''
        :param kwargs:
        Create work group
        :return:
        '''

        if not kwargs.get('Extension'):
            print("Creating new WorkGroup")
            urlNewWG = "http://%s:%s/director/work_groups/new.json?TenantID=1" %(self.ip, self.pno)
            if not kwargs.get('BackupExtension'):
                print("BackupExtension is mandatory parameter")
                return  False
        else:
            print("Modifying WorkGroup")
            getAllWGs = "http://%s:%s/director/work_groups/list?&rows=500" %(self.ip, self.pno)
            allWGs = self.client.get(getAllWGs).json()
            id=''
            for wg in allWGs['rows']:
                if str(wg['cell'][1]) == str(kwargs.get('Extension')):
                    id = wg['id']
                    break
            if not id:
                print("User doesnt exist in the system")
                return False
            urlNewWG = "http://%s:%s/director/work_groups/%s.json" %(self.ip, self.pno,id)

        # urlNewWG = "http://%s:%s/director/work_groups/new.json?TenantID=1" %(self.ip, self.pno)
        newWG = self.client.get(urlNewWG).json()

        # GENERAL TAB
        newWG['work_group']['tab_address_attributes']['FirstName'] = kwargs.get('WorkGroupName',"Created By D2 API")
        newWG['work_group']['BackupDN_formatted'] =kwargs.get('BackupExtension',newWG['work_group']['BackupDN_formatted'])
        newWG['work_group']['dn_attributes']['include_in_dial_by_name']=kwargs.get('IncludeInDialByName',newWG['work_group']['dn_attributes']['include_in_dial_by_name'])
        newWG['work_group']['dn_attributes']['Hidden'] = kwargs.get('MakeExtensionPrivate',newWG['work_group']['dn_attributes']['Hidden'])
        newWG['work_group']['dn_attributes']['LanguageID'] = kwargs.get('LanguageID',newWG['work_group']['dn_attributes']['LanguageID'])
        newWG['work_group']['DIDEnabled']=kwargs.get('DIDEnabled',newWG['work_group']['DIDEnabled'])
        newWG['work_group']['did_range_did_range_id']=kwargs.get('DIDRange',newWG['work_group']['did_range_did_range_id'])
        newWG['work_group']['did_range_digits']=kwargs.get('DIDNumber',newWG['work_group']['did_range_digits'])
        newWG['work_group']['HasMailBox']=kwargs.get('EnableMailBox',newWG['work_group']['HasMailBox'])
        newWG['work_group']['AutoAgentLogout']=kwargs.get('EnableAutoAgentLogout',newWG['work_group']['AutoAgentLogout'])
        newWG['work_group']['WrapUpTimeSec']=kwargs.get('WrapUpTimeSec',newWG['work_group']['WrapUpTimeSec'])
        if kwargs.get('Members'):
            tempMembers = []
            for mems in kwargs.get('Members'):
                tempMembers.append({"id":mems,"AgentState": "0"})
            newWG['work_group']['work_group_agents_with_name'] = tempMembers

        # Voice Mail
        newWG['work_group']['work_group_mailbox_attributes']['accept_broadcasts'] = kwargs.get('AcceptBroadcastMessages',newWG['work_group']['work_group_mailbox_attributes']['accept_broadcasts'] )
        newWG['work_group']['work_group_mailbox_attributes']['EmailNotifyWhenFull'] = kwargs.get('SendEmailWarningWhenFull',newWG['work_group']['work_group_mailbox_attributes']['EmailNotifyWhenFull'] )
        newWG['work_group']['work_group_mailbox_attributes']['IsDeletedWhenForward'] = kwargs.get('DeleteMessageAfterForwarding',newWG['work_group']['work_group_mailbox_attributes']['IsDeletedWhenForward'] )
        newWG['work_group']['work_group_mailbox_attributes']['auto_def_dest'] = kwargs.get('AutomaticMessageForwardingDestination',newWG['work_group']['work_group_mailbox_attributes']['auto_def_dest'] )
        newWG['work_group']['work_group_mailbox_attributes']['mailbox_destination_DN_formatted'] = kwargs.get('Mailbox',newWG['work_group']['work_group_mailbox_attributes']['mailbox_destination_DN_formatted'] )
        newWG['work_group']['work_group_mailbox_attributes']['AMIS_destination_DN'] = kwargs.get('AMISDestinationDN',newWG['work_group']['work_group_mailbox_attributes']['AMIS_destination_DN'] )
        newWG['work_group']['work_group_mailbox_attributes']['SendEmailForVMTypeID'] = kwargs.get('DeliveryType',newWG['work_group']['work_group_mailbox_attributes']['SendEmailForVMTypeID'] )
        newWG['work_group']['work_group_mailbox_attributes']['MarkAsHeard'] = kwargs.get('MarkAsHeard',newWG['work_group']['work_group_mailbox_attributes']['MarkAsHeard'] )
        newWG['work_group']['tab_address_attributes']['EmailAddress'] = kwargs.get('EmailAddress',newWG['work_group']['tab_address_attributes']['EmailAddress'])
        # DNIS
        if kwargs.get('DNIS'):
            for trunks in kwargs.get('DNIS'):
                if trunks.get('TrunkDigits') and trunks.get('TrunkDescription') and trunks.get('TrunkMOHID'):
                    groupID = self.get_did_range_data()['did_ranges'][0]['trunk_group_id']
                    newWG['work_group']['did_digit_map_attributes'] += [{"TrunkGroupID": groupID,"DIDDigitMapID":2,"Digits":trunks.get('TrunkDigits'), "Description":trunks.get('TrunkDescription'), "MOHResourceID": trunks.get('TrunkMOHID'),"DNIS":True }] #'DNIS':True
                elif trunks.get('TrunkDigits'):
                    availableCount = 0
                    for availables in newWG['work_group']['did_digit_map_attributes']:
                        if str(availables["Digits"]) == str(trunks.get('TrunkDigits')):
                            newWG['work_group']['did_digit_map_attributes'][availableCount]["_destroy"]= 1
                        availableCount +=1

        if kwargs.get('UserGroupName'):
            isFound = False
            getAllUGs = r'http://%s:%s/director/user_groups/list?rows=500'% (self.ip, self.pno)
            ug = self.client.get(getAllUGs).json()['rows']
            for userG in ug:
                if str(userG['cell'][0]).lower()==str(kwargs.get('UserGroupName')).lower():
                    newWG['work_group']['UserGroupID'] = userG['id']
                    isFound = True
                    break
            if not isFound:
                print("User group not found in the system")
                return False
        if not kwargs.get('Extension'):
            postWG = "http://%s:%s/director/work_groups.json" %(self.ip, self.pno)
            Out = self.client.post(postWG,json=newWG,headers = {"X-CSRF-Token": self.token,"Content-Type": "application/json"})
        else:
            postWG = "http://%s:%s/director/work_groups/%s.json" %(self.ip, self.pno,id)
            Out = self.client.put(postWG,json=newWG,headers = {"X-CSRF-Token": self.token,"Content-Type": "application/json"})

        if Out.status_code == 200:
            if not kwargs.get('Extension'):
                return "Workgroup " +newWG['work_group']['dn_attributes']['DN']+" is created."
            else:
                return True
        else:
            return False


    def delete_work_group(self, **kwargs):
        '''
        :param kwargs: Extension
        Delete work group
        :return:
        '''

        if not kwargs.get('Extension'):
            print("Extension is mandatory parameter for deleting Workgroup")
            return False
        getAllWGs = "http://%s:%s/director/work_groups/list?&rows=500" %(self.ip, self.pno)
        allWGs = self.client.get(getAllWGs).json()
        id=''
        for wg in allWGs['rows']:
            if str(wg['cell'][1]) == str(kwargs.get('Extension')):
                id = wg['id']
                break
        if not id:
            print("User doesnt exist in the system")
            return False
        urlDelWG = "http://%s:%s/director/work_groups/%s.json" %(self.ip, self.pno, id)
        status = self.client.delete(urlDelWG,headers = {"X-CSRF-Token": self.token})
        if status.status_code == 200:
            return True
        else:
            return False

    def modify_call_control_options(self,**kwargs):
        getAllOptions = "http://%s:%s/director/call_control_options.json?TenantID=1" %(self.ip, self.pno)
        allOPs = self.client.get(getAllOptions).json()
        allOPs['call_control_options']['EnableWhisperCoachWarningTone'] =kwargs.get('EnableSilentCoachWarningTone',allOPs['call_control_options']['EnableWhisperCoachWarningTone'])
        allOPs['call_control_options']['EnableRecordingWarningTone'] =kwargs.get('EnableRecordingWarningTone',allOPs['call_control_options']['EnableRecordingWarningTone'])
        # Just enabled all the options but not tested.
        allOPs['call_control_options']['CallControlQualityOfService'] =kwargs.get('CallControlQualityOfService',allOPs['call_control_options']['CallControlQualityOfService'])
        allOPs['call_control_options']['ClusterMode'] =kwargs.get('ClusterMode',allOPs['call_control_options']['ClusterMode'])
        allOPs['call_control_options']['CompressRTPHeaders'] =kwargs.get('CompressRTPHeaders',allOPs['call_control_options']['CompressRTPHeaders'])
        allOPs['call_control_options']['DTMFPayloadType'] =kwargs.get('DTMFPayloadType',allOPs['call_control_options']['DTMFPayloadType'])
        allOPs['call_control_options']['DelayBeforeSendingDTMFToFaxServer'] =kwargs.get('DelayBeforeSendingDTMFToFaxServer',allOPs['call_control_options']['DelayBeforeSendingDTMFToFaxServer'])
        allOPs['call_control_options']['EnableSIPSessionTimer'] =kwargs.get('EnableSIPSessionTimer',allOPs['call_control_options']['EnableSIPSessionTimer'])
        allOPs['call_control_options']['JitterBuffer'] =kwargs.get('JitterBuffer',allOPs['call_control_options']['JitterBuffer'])
        allOPs['call_control_options']['MediaEncryption'] =kwargs.get('MediaEncryption',allOPs['call_control_options']['MediaEncryption'])
        allOPs['call_control_options']['QualityOfService'] =kwargs.get('QualityOfService',allOPs['call_control_options']['QualityOfService'])
        allOPs['call_control_options']['RemoteIPPhoneCodecListID'] =kwargs.get('RemoteIPPhoneCodecListID',allOPs['call_control_options']['RemoteIPPhoneCodecListID'])
        allOPs['call_control_options']['SIPDefRegExpiry'] =kwargs.get('SIPDefRegExpiry',allOPs['call_control_options']['SIPDefRegExpiry'])
        allOPs['call_control_options']['SIPRealm'] =kwargs.get('SIPRealm',allOPs['call_control_options']['SIPRealm'])
        allOPs['call_control_options']['SIPRefresher'] =kwargs.get('SIPRefresher',allOPs['call_control_options']['SIPRefresher'])
        allOPs['call_control_options']['SIPSessionInterval'] =kwargs.get('SIPSessionInterval',allOPs['call_control_options']['SIPSessionInterval'])
        allOPs['call_control_options']['T2TGEMinutes'] =kwargs.get('T2TGEMinutes',allOPs['call_control_options']['T2TGEMinutes'])
        allOPs['call_control_options']['T2TGenEvent'] =kwargs.get('T2TGenEvent',allOPs['call_control_options']['T2TGenEvent'])
        allOPs['call_control_options']['T2THUMinutes'] =kwargs.get('T2THUMinutes',allOPs['call_control_options']['T2THUMinutes'])
        allOPs['call_control_options']['T2THangUp'] =kwargs.get('T2THangUp',allOPs['call_control_options']['T2THangUp'])
        allOPs['call_control_options']['T2TSHUMinutes'] =kwargs.get('T2TSHUMinutes',allOPs['call_control_options']['T2TSHUMinutes'])
        allOPs['call_control_options']['T2TSilentHangUp'] =kwargs.get('T2TSilentHangUp',allOPs['call_control_options']['T2TSilentHangUp'])
        allOPs['call_control_options']['UsePort5004'] =kwargs.get('UsePort5004',allOPs['call_control_options']['UsePort5004'])
        allOPs['call_control_options']['VideoQualityOfService'] =kwargs.get('VideoQualityOfService',allOPs['call_control_options']['VideoQualityOfService'])
        allOPs['call_control_options']['QualityOfServiceInt'] =kwargs.get('QualityOfServiceInt',allOPs['call_control_options']['QualityOfServiceInt'])
        allOPs['call_control_options']['AllowBCACallerID'] =kwargs.get('AllowBCACallerID',allOPs['call_control_options']['AllowBCACallerID'])
        allOPs['call_control_options']['BCACallOnHoldBlink'] =kwargs.get('BCACallOnHoldBlink',allOPs['call_control_options']['BCACallOnHoldBlink'])
        allOPs['call_control_options']['BCAReminderRings'] =kwargs.get('BCAReminderRings',allOPs['call_control_options']['BCAReminderRings'])
        allOPs['call_control_options']['ConferenceTimeout'] =kwargs.get('ConferenceTimeout',allOPs['call_control_options']['ConferenceTimeout'])

        allOPs['call_control_options']['OverheadPagingTimeout'] =kwargs.get('OverheadPagingTimeout',allOPs['call_control_options']['OverheadPagingTimeout'])
        allOPs['call_control_options']['ParkTimeout'] =kwargs.get('ParkTimeout',allOPs['call_control_options']['ParkTimeout'])
        allOPs['call_control_options']['PlayLogonFindMeBranding'] =kwargs.get('PlayLogonFindMeBranding',allOPs['call_control_options']['PlayLogonFindMeBranding'])
        allOPs['call_control_options']['PlayShorelineFwdCallMsg'] =kwargs.get('PlayShorelineFwdCallMsg',allOPs['call_control_options']['PlayShorelineFwdCallMsg'])
        allOPs['call_control_options']['RecordingBeep'] =kwargs.get('RecordingBeep',allOPs['call_control_options']['RecordingBeep'])
        allOPs['call_control_options']['ParkTimeoutBoolean'] =kwargs.get('ParkTimeoutBoolean',allOPs['call_control_options']['ParkTimeoutBoolean'])
        allOPs['call_control_options']['ConferenceTimeoutBoolean'] =kwargs.get('ConferenceTimeoutBoolean',allOPs['call_control_options']['ConferenceTimeoutBoolean'])
        allOPs['call_control_options']['OverheadPagingTimeoutBoolean'] =kwargs.get('OverheadPagingTimeoutBoolean',allOPs['call_control_options']['OverheadPagingTimeoutBoolean'])
        allOPs['call_control_options']['BCAReminderRingsBoolean'] =kwargs.get('BCAReminderRingsBoolean',allOPs['call_control_options']['BCAReminderRingsBoolean'])

        postOP = "http://%s:%s/director/call_control_options.json?id=1" %(self.ip, self.pno)
        Out = self.client.put(postOP,json=allOPs,headers = {"X-CSRF-Token": self.token,"Content-Type": "application/json"})

        if Out.status_code == 200:
            return True
        else:
            return False

    def add_to_system_directory(self,**kwargs):
        getAllOptions = "http://%s:%s/director/system_directories/new.json?TenantID=1" %(self.ip, self.pno)
        allOPs = self.client.get(getAllOptions).json()

        allOPs['system_directory']['FirstName'] =kwargs.get('FirstName',allOPs['system_directory']['FirstName'])
        allOPs['system_directory']['LastName'] =kwargs.get('LastName',allOPs['system_directory']['LastName'])
        allOPs['system_directory']['HomePhone_formatted'] =kwargs.get('HomePhone',allOPs['system_directory']['HomePhone_formatted'])
        allOPs['system_directory']['WorkPhone_formatted'] =kwargs.get('WorkPhone',allOPs['system_directory']['WorkPhone_formatted'])
        allOPs['system_directory']['FaxPhone_formatted'] =kwargs.get('FaxPhone',allOPs['system_directory']['FaxPhone_formatted'])
        allOPs['system_directory']['CellPhone_formatted'] =kwargs.get('CellPhone',allOPs['system_directory']['CellPhone_formatted'])
        allOPs['system_directory']['PagerPhone_formatted'] =kwargs.get('PagerPhone',allOPs['system_directory']['PagerPhone_formatted'])
        allOPs['system_directory']['CompanyName'] =kwargs.get('CompanyName',allOPs['system_directory']['CompanyName'])
        allOPs['system_directory']['DepartmentName'] =kwargs.get('DepartmentName',allOPs['system_directory']['DepartmentName'])
        allOPs['system_directory']['EmailAddress'] =kwargs.get('EmailAddress',allOPs['system_directory']['EmailAddress'])

        postOP = "http://%s:%s/director/system_directories.json" %(self.ip, self.pno)
        Out = self.client.post(postOP,json=allOPs,headers = {"X-CSRF-Token": self.token,"Content-Type": "application/json"})
        if Out.status_code == 200:
            return True
        else:
            return False
            
    def create_work_group(self, **kwargs):
        """
        :param kwargs: (back_up_extension,work_group_members, wgname)
        :return: The id of newly created Work group if success else False
        """
        #self.refreshToken()
        getParams = r'http://%s:%s/director/work_groups/new.json?TenantID=1'% (self.ip, self.pno)
        createWGParams = self.client.get(getParams).json() # This should give json for creating WG with all params.

        createWGParams = self._modify_wg_json(createWGParams, **kwargs)
        # making the create request
        createWG = r'http://%s:%s/director/work_groups.json'% (self.ip, self.pno)
        outp = self.client.post(createWG, json=createWGParams, headers={"X-CSRF-Token": self.token, "Content-Type": "application/json"})
        if outp.status_code == 200:
            return outp.json()['work_group']['id']
        else:
            return False

    def _modify_wg_json(self, wg_json, **kwargs):
        if kwargs.get("work_group_members") != None:
            group_members = []
            users_url = r'http://%s:%s//director/users/list?list=work_group_users' % (self.ip, self.pno)
            users_json = self.client.get(users_url).json()
            for wg_member in kwargs.get("work_group_members"):
                user_to_add = {}
                for user in users_json['rows']:
                    if str(wg_member['id']) == user["cell"][0]:
                        user_to_add["AgentState"] = wg_member.get("state", 0)
                        user_to_add["id"] = user['cell'][0]
                        group_members.append(user_to_add)
                        break
                else:
                    print("Extension " + str(wg_member) + " not found in system ")
                    return False
            wg_json['work_group']['work_group_agents_with_name'] = group_members
        # Insert all the values to json
        # createWGParams['work_group']['dn_ids'] = group_members
        wg_json['work_group']['BackupDN_formatted'] = kwargs.get('back_up_extension', wg_json['work_group']['BackupDN_formatted'])
        wg_json['work_group']['tab_address_attributes']['FirstName'] = kwargs.get('wgname', wg_json['work_group']['tab_address_attributes']['FirstName'])
        wg_json['work_group']['WrapUpTimeSec'] = kwargs.get('wrap_up_time', wg_json['work_group']['WrapUpTimeSec'])
        if kwargs.get('did_range_description'):
            wg_json['work_group']['DIDEnabled'] = "true"
            did_range_id = None
            did_range_url = "http://%s:%s/director/work_groups/get_did_range_data" % (self.ip, self.pno)   #?id=330&TenantID=1
            did_ranges = self.client.get(did_range_url).json()
            for did_range in did_ranges["collections"]:
                if did_range["Description"] == kwargs["did_range_description"]:
                    did_range_id = did_range["ID"]

            wg_json['work_group']['did_range_did_range_id'] = did_range_id
            wg_json['work_group']['did_range_digits'] = kwargs.get('did_number', "8066666683")
        if kwargs.get("mailbox_server"):
            if kwargs["mailbox_server"] != "Disable":
                mailbox_server_url = "http://%s:%s/director/work_groups/common_data?TenantID=1" % (self.ip, self.pno)
                mailboxes = self.client.get(mailbox_server_url).json()
                for mailbox in mailboxes["vmservers_with_mailboxes"]:
                    if mailbox["Name"] == kwargs["mailbox_server"]:
                        mailbox_id = mailbox["VMServerID"]
                        break
                wg_json["work_group"]["work_group_mailbox_attributes"] = {"VMServerID": mailbox_id}
                wg_json["work_group"]["HasMailBox"] = "true"
            else:
                wg_json["work_group"]["HasMailBox"] = "false"
        if kwargs.get("routing_onh_dp"):
            routing_onh_dp_values = {"Top Down": 1, "Round Robin": 2, "Longest Idle": 3, "Simultaneous": 4}
            wg_json['work_group']['work_group_chms_attributes'][0]["HuntPatternID"] = routing_onh_dp_values[kwargs["routing_onh_dp"]]
        if kwargs.get("routing_onh_cf_no_answer"):
            if kwargs["routing_onh_cf_no_answer"] == "Queue":
                wg_json['work_group']['work_group_chms_attributes'][0]["CFNoAnswerOption"] = 2
                wg_json['work_group']['work_group_chms_attributes'][0]["CFNoAnswer_formatted"] = "null"
            else:
                wg_json['work_group']['work_group_chms_attributes'][0]["CFNoAnswerOption"] = 1
                wg_json['work_group']['work_group_chms_attributes'][0]["CFNoAnswer_formatted"] = kwargs["routing_onh_cf_no_answer"]

        return wg_json

    def delete_a_work_group(self, work_group_name):
        """
        :param work_group_name: the name of work group to delete
        :return: True if deleted else False
        """
        #self.refreshToken()
        all_work_groups_url = r'http://%s:%s/director/work_groups/list' % (self.ip, self.pno)
        all_work_groups = self.client.get(all_work_groups_url).json()
        for rows in all_work_groups['rows']:
            if work_group_name == rows['cell'][0]:
                delete_work_group_url = r'http://%s:%s/director/work_groups/%s.json'% (self.ip, self.pno, rows['id'])
                del_wg = self.client.delete(delete_work_group_url, headers={"X-CSRF-Token": self.token})
                if del_wg.status_code == 200:
                    return True
                else:
                    return False
        raise Exception("Work Group Id not found.")

    def edit_work_group(self, work_group_name, **kwargs):
        """
        :param work_group_name: the name of work group to delete
        :return: The id of work group edited if success else False
        """
        #self.refreshToken()
        wg_id = None
        all_work_groups_url = r'http://%s:%s/director/work_groups/list' % (self.ip, self.pno)
        all_work_groups = self.client.get(all_work_groups_url).json()
        for rows in all_work_groups['rows']:
            if work_group_name == rows['cell'][0]:
                wg_id = rows['id']
                if wg_id:
                    break
        else:
            raise Exception("Work Group <%s> not found." % (work_group_name))
        # get the wg params
        wg_params_url = r'http://%s:%s/director/work_groups/%s.json' % (self.ip, self.pno, wg_id)
        edit_wg_params = self.client.get(wg_params_url).json()
        # Editing the work group json
        edit_wg_params = self._modify_wg_json(edit_wg_params, **kwargs)
        # Making the edit request
        outp = self.client.put(wg_params_url, json=edit_wg_params,
                                headers={"X-CSRF-Token": self.token, "Content-Type": "application/json"})
        if outp.status_code == 200:
            return outp.json()['work_group']['id']
        else:
            return False

if __name__ == "__main__":
    import time
    # fo = D2API("10.211.41.103:5478", "admin", "Mitel@123")
    d2 = D2API("10.211.44.230:5478", "admin", "Shoreadmin1")
    # print(d2.create_work_group(wgname="temp4", back_up_extension=31160, work_group_members=[{'id':'31-161', 'state':1}, {'id':'31-162'}]))
    # print(d2.delete_work_group(work_group_name="temp1"))
    # print(d2.edit_work_group(work_group_name="temp4", work_group_members=[{'id':'31-161', 'state':1}, {'id':'31-162'}]))
    # print(d2.edit_work_group(work_group_name="temp4", wrap_up_time=15, did_range_description="+918066666681 (2 of 5 available) TrunkGroup_WDVS_Auto"))
    # print(d2.edit_work_group(work_group_name="temp4", routing_onh_dp="Simultaneous", routing_onh_cf_no_answer="Queue"))
    # print(d2.edit_work_group(work_group_name="temp4", routing_onh_cf_no_answer="101 : Voice Mail", mailbox_server="Headquarters"))
    # print(d2.edit_work_group(work_group_name="temp4", mailbox_server="Disable"))
    

    # print(fo.add_to_system_directory(FirstName="FirstName",LastName="LastName",HomePhone="2345678",WorkPhone="2345678",CellPhone="2345678",FaxPhone="2345678",PagerPhone="2345678",CompanyName="Mitel",DepartmentName="Mitel123",EmailAddress="asas@fsfs.com"))
    # print(fo.modify_call_control_options(EnableSilentCoachWarningTone=False,EnableRecordingWarningTone=True))

    # print(fo.delete_work_group(Extension=154))
    # d2.create_modify_user(extension='31-255', LicenseType="Extension and Mailbox")  # Extension and Mailbox   Mailbox-Only  Extension-Only
    d2.create_modify_user(extension='31-255', EnableVideoCalls=False)  #
    # d2.create_modify_user(extension='31-255', EnableVideoCalls=True, VideoCallMode="2")  # VideoCallMode = 1(Standard) or 2(High)
    # d2.create_modify_user(extension='31-255', AccessLicense="Phone Only")  # Phone Only     Connect Client   Workgroup Agent   Workgroup Supervisor    Operator
    # fo.create_modify_user(extension='31-255',FindMeAvailable = False, FindMeInAMeeting=False,FindMeOutOfOffice=False,FindMeVecation=False,FindMeCustom=False)
    # fo.create_modify_user(extension='198',RingAdditionalPhoneWhenAvailable = False, RingAdditionalPhoneWhenInAMeeting=False,RingAdditionalPhoneWhenOutOfOffice=False,RingAdditionalPhoneWhenVecation=False,RingAdditionalPhoneWhenCustom=False)

    # "" - for <None> , for all other values count from 1 for all drop down values.
    # fo.create_modify_user(extension='198',RingAdditionalRingDelay=2,SimultaneouslyRing=2,AlsoRing="",FindMeFirstPhone=2,FindMeSecondPhone=2)
    # fo.create_modify_user(extension='198',SendIncomingCallerID=True, EnableFindMeForIncomingCalls=True,EnableRecordCallerName=True,RecordNameEvenCallerIDIsPresent=True)#
    # fo.create_modify_user(extension='893', RountingPhones=[{"Label": "NEW", "NumberOfRings":"5","PhoneNumber":"115","Activation":"2"},{"Label": "NEW2", "NumberOfRings":"8","PhoneNumber":"196","Activation":"2"}]) # Activation = 2 / 1
    # fo.create_modify_user(extension='198', RountingPhones=[{"Label": "NEW", "NumberOfRings":"3","PhoneNumber":"115","Activation":"2"}]) # Activation = 2 / 1
    # fo.create_modify_user(extension='198', RountingPhones=[{"Label": "", "NumberOfRings":"3","PhoneNumber":"","Activation":"1"}]) # To Remove

    # print(fo.create_modify_work_group(BackupExtension=120,IncludeInDialByName=False,MakeExtensionPrivate=False,DIDEnabled=False,UserGroupName="okok",EnableMailBox=False,)
    #                      WrapUpTimeSec=1,EnableAutoAgentLogout=False,Members=[120,135])
    #DNIS
    # print(fo.create_modify_work_group(Extension=190,WorkGroupName="SSSS",DNIS = [{"TrunkDigits":"65501","TrunkDescription":"Trial","TrunkMOHID" : 1}]) # DNIS can be added only to an existing work group.)
    #VOICE MAIL
    # print(fo.create_modify_work_group(Extension=190, EmailAddress="Voice@mail,com",WorkGroupName="TT",)
    #                             AcceptBroadcastMessages=False, AutomaticMessageForwardingDestination=0, DeliveryType=2,MarkAsHeard=True,SendEmailWarningWhenFull=True,DeleteMessageAfterForwarding=False)
    # print(fo.create_modify_work_group(Extension=190, AutomaticMessageForwardingDestination=1,Mailbox="195"))

    # fo.create_modify_pickup_group(extension=201,name= 'Modified2',extension_list_name='oo',switch=4) # switch 2/4
    # fo.delete_pickup_group(extension=153)

    # ENTA-3997
    # print(fo.create_modify_user_groups(user_group_name='Executives3',file_to_select='system defaults',send_caller_id=False,)
    #                                    send_DID=False,show_account_codes=False,cos_call_permissions=3,cos_telephony_id=1,cos_voice_mail=3,account_code_type=1) #file_to_select = ' system defaults' for defaults
    # print(fo.modify_moh_system_defaults(internal_call='0',file_to_select='Mitel') # 0/1, file_to_select = 'jack based' for default)
    # ENTA-3561
    # TimeZone : For "(UTC+02:00)Cairo, Egypt Standard Time " you may just pass the value after the comma ie "Egypt Standard Time"
    # print(fo.create_modify_custom_schedule(ScheduleName='RRRR', TimeZone="Egypt Standard Time", Schedules =[{"ItemName":'Custom',"schedule_date": "09/12","start_time":"09:00","stop_time":"17:00"}]))
    # fo.delete_custom_schedule('NEWdFA')

    # fo.delete_holiday_schedule("TEST")
    # fo.delete_onhours_schedule("NEWFA")
    # print(fo.create_modify_onhours_schedules(ScheduleName='NEsasaWFA', TimeZone="Egypt Standard Time", Schedules =[{"DayOfWeek":3,"start_time": "10:00:00","stop_time":"17:00:00"}]))
    # print(fo.create_modify_holiday_schedule(ScheduleName='TESTxz',TimeZone="Egypt Standard Time", Schedules=[{"ItemName":"holiday",'schedule_date':'9/11'}]))
    # print(fo.create_modify_hunt_group(extension =191,BackupExtension=121,HolidaySchedule=33,OffHoursHoliday=161,OnHourSchedule = 1,NoAnswer=161,))

    # ENTA-3475
    # print(fo.create_modify_BCA(name = "BCA_2",BackupDN = 162,SwitchID =4, CallStackDepth=10,NoAnswerRings=10,CFNoAnswer=121,CFBusy=121,OutCallerID ="123456789123",AllowBridgeConferencing= 'false',PrivacyEnabled=1) # SwitchID = 2/4, PrivacyEnabled = 0 /1)
    # fo.delete_BCA_profile(ExtensionNumber=144)
    # print(fo.create_modify_BCA(extension ="112",name ='BCA_5', AllowBridgeConferencing =True))
    # print(fo.create_modify_BCA(extension ="161", AllowBridgeConferencing =True))
    # ENTA-3433
    # print(fo.create_paging_group(PagingGroupName="dsdFDFDFD", PageListName = "oo", PagingDelay='4',PriorityPage='true',RingsPerMember='10',MakeExtensionPrivate=False,PriorityPageAudioPath=2))
    # fo.delete_page_list(ExtensionListName='Delete')

    # ENTA-3439
    # fo.create_modify_hunt_group(extension =200, BackupExtension=121,HuntGroupMember=[110],HuntGroupName = "HG Name", OnHourSchedule = 2,HolidaySchedule=4,CallStackFull=121,NoAnswer=161, OffHoursHoliday=161
    #                      , RingsPerMember=4, NoAnswerRings=6,SkipMemberIfAlreadyOnCall=True,CallMemberWhenForwarding=False, MakeExtensionPrivate=True,IncludeInSystemDialByName=True )
    # fo.create_modify_hunt_group(extension =134,BackupExtension=121,HuntGroupMember=[],HuntPatternID=4,HuntGroupName="New HG") # HuntPatternID = 1/4
    # print(fo.create_modify_hunt_group(BackupExtension=4012,HuntGroupMember=[],HuntPatternID=4,HuntGroupName="New HG1", NoAnswer=None,CallStackFull=None))
    # print(fo.create_modify_hunt_group(extension =136,BackupExtension=121,HuntGroupMember=[],HuntPatternID=4,HuntGroupName="New HG1", NoAnswer=None,CallStackFull=None))
    # print(fo.create_modify_hunt_group(extension =191,BackupExtension=121,HolidaySchedule=33,OffHoursHoliday=161,OnHourSchedule = 1,NoAnswer=161,))




    # ENTA -3434
    # fo.modify_telephony_options(DelayAfterCollectDigits =3000)
    # fo.Unconfigure_prog_button(user_extension ="120",button_box= 0,soft_key =4)
    # print("DONE")
    # fo.Unconfigure_prog_button(user_extension ="162",button_box= 0,soft_key =5)
    # print(fo.create_modify_BCA(name = "BCA_1",BackupDN = 162,SwitchID =4, CallStackDepth=10,NoAnswerRings=10,CFNoAnswer=121,CFBusy=121,OutCallerID ="123456789123",AllowBridgeConferencing= 'false',PrivacyEnabled=1) # SwitchID = 2/4, PrivacyEnabled = 0 /1)
    # fo.configure_prog_button(user_extension ="4012",button_box =0,soft_key =5,function="Bridge Call Appearance",label ="BCA",target_extension = 4013,RingDelayBeforeAlert='1',CallStackPosition =1,show_caller_id_option = 'Never',EnableAutoAnswerWhenRinging =True,SecondaryType ='Dial extension',DialExtension='4014')
    # fo.configure_prog_button(user_extension ="162",button_box =0,soft_key =6,function="Bridge Call Appearance",label ="BCA2",target_extension = 197,RingDelayBeforeAlert='2',CallStackPosition =2,show_caller_id_option = 'Only when ringing',EnableAutoAnswerWhenRinging ='false',SecondaryType ='Answer only')
    # fo.configure_prog_button(user_extension ="162",button_box =0,soft_key =7,function="Bridge Call Appearance",label ="BCA3",target_extension = 197,RingDelayBeforeAlert='3',CallStackPosition =3,show_caller_id_option = 'Always',EnableAutoAnswerWhenRinging =True,SecondaryType ='Dial tone')

    # ENTA -3377
    # AllowViewPresence =Show caller ID name and number for other extension
    # AllowBridgeUse = Allow collaboration features
    # AllowHotDesk = Allow extension reassignment
    # AllowCallForwardExternal=Allow external call forwarding and find me destinations
    # AllowChangeOwnCHMode =Allow current availability state changes
    # AllowChangeOwnCHSettings =Allow current availability state detail changes

    # fo.change_telephony_feature_permission(name ='Fully Featured', MaxBuddiesPerUser = '43',MaxPrivateContacts ='30',MaxCallStackDepth='5', AllowCallPickupExtension =True,AllowCallTransferTrunkToTrunk =True,AllowPaging=True,AllowHuntBusyOut=False,MaxPartiesMakeMeConference =8)
    # fo.change_telephony_feature_permission(name ='Fully Featured',AcceptWhisperPagingDN_formatted ="162", AcceptWhisperPaging =2,AllowWhisperPaging= True)
    # fo.change_telephony_feature_permission(name ='Fully Featured',AcceptIntercomPagingDN ="162", AcceptIntercomPaging =2,AllowIntercomPaging= True)
    # fo.change_telephony_feature_permission(name ='Fully Featured',AcceptBargeInDN_formatted ="162", AcceptBargeIn =2,AllowBargeIn= True)
    # fo.change_telephony_feature_permission(name ='Fully Featured',AcceptRecordingOthersDN_formatted ="162", AcceptRecordingOthersCalls =2,AllowRecordingOthersCalls= True)
    # fo.change_telephony_feature_permission(name ='Fully Featured',AcceptSilentMonitorDN_formatted ="162", AcceptSilentMonitor =2,AllowSilentMonitor= True)
    # fo.change_telephony_feature_permission(name ='Fully Featured',AllowChangeOwnCHSettings=False,AllowChangeOwnCHMode =False)
    # fo.change_telephony_feature_permission(name ='Partially Featured',CFENExceptions='311',CFENRestrictions ='123456789',CFENScopeID=9, AllowCallForwardExternal=True,AllowProgramOwnButtons=False) # Scope =All call & Allow customization of IP phone buttons and client monitor window

    # ENTA-3339

    # General
    # print(fo.create_modify_user(FirstName ="First", LastName="Last", EmailAddress="email@email,com", DIDEnabled=True, DIDNumber='20753', DIDRange=1,UserGroupName='managers'))
    # print(fo.create_modify_user(FirstName ="First", LastName="Last", EmailAddress="email@email,com",PSTNFailoverNumber="9+1(408)234-5678",PSTNFailover=2,CallerID="+1(408)234-5678"))
    # print(fo.create_modify_user(FirstName ="Shankara", LastName="Narayanan", EmailAddress="Assfdfrtert@ddAd,com",IncludeInSystemDialByNameDirectory=True,MakeExtensionPrivate=True))
    # print(fo.create_modify_user(FirstName ="Ffirst", LastName="Lfast", EmailAddress="emafil@emaifl,com",UserGroup=2))

    # Telephony Tab:
    # CallStackDepth,RingType,WallPaper,AutomaticOffHookPreference,EnableHandsFreeMode,EnableCallWaitingTone,TrunkAccessCode,VoiceMailboxForRecordedCalls,DectPowerMode,DectQuality
    # EnableVideoCalls,VideoCallMode, EnableTelephonyPresence,sca_enabled,EnableSoftPhone,EnableRemotePhoneAuthentication,EnablePAPI,EnableEnhancedMobility,MobilePhoneNumber,RingdownNumber & RingdownDelay

    # print(fo.create_modify_user(FirstName ="Fifdffdrst", LastName="Laffddfdst", EmailAddress="efdmail@emafdifdl,com",CallStackDepth=2, RingType=1,WallPaper=1,AutomaticOffHookPreference=2,EnableHandsFreeMode=False,EnableCallWaitingTone=True,)
    #                             VoiceMailboxForRecordedCalls=100,DectPowerMode=1,DectQuality=1,EnableVideoCalls=True,VideoCallMode=1,
    #                             EnableTelephonyPresence=True,EnableSoftPhone=True,EnableRemotePhoneAuthentication=True,EnableEnhancedMobility=True,
    #                             MobilePhoneNumber='1(408)234-5678',
    #                             EnableDelayedRingdown=True,RingdownNumber=121,RingdownDelay=2)
    # print(fo.create_modify_user(extension=201,sca_enabled=True,EnableEnhancedMobility=True))
    # print(fo.create_modify_user(FirstName ="Fifdffdrst", LastName="Laffddfdst", EmailAddress="efdmail@emafdifdl,com",sca_enabled=True,EnableEnhancedMobility=True))

    # print(fo.create_modify_user(FirstName ="Shankara", LastName="Narayanan", EmailAddress="A@ddA,com",)
    #                      AllowPAPI=True,AllowSoftPhone=True,AllowTelephonyPresence=True,
    #                      AutoCHM=True,EnableDelayedRingdown=True,EnableRemotePhoneAuthentication=True,
    #                      RingdownNumber =121,RingdownDelay=2,
    #                      FaxSupport =3,VoiceMailboxForRecordedCalls=121,MailboxServer=2,AllowVideoCalls=True,
    #                      RingType=5,WallPaper=3,sca_enabled=True )
    # Voice Mail
    # AcceptBroadcastMessages, PlayEnvelope, SendEmailWarningWhenFull, DeleteMessageAfterForwarding, MarkAsHeard ,AutomaticMessageForwardingDestination, Mailbox, AMISDestinationDN, DeliveryType
    # print(fo.create_modify_user(FirstName ="Voice", LastName="Mail", EmailAddress="Voice@mail,com",)
    #                             AcceptBroadcastMessages=True,PlayEnvelope=True,MarkAsHeard=True,SendEmailWarningWhenFull=True,
    #                             AutomaticMessageForwardingDestination=1,Mailbox=121,
    #                             DeleteMessageAfterForwarding=True)
    # print(fo.create_modify_user(FirstName ="Voice1", LastName="Mail1", EmailAddress="Voic1e@ma1il,com",)
    #                             DeliveryType=2,MarkAsHeard=True)
    # Membership
    # print(fo.create_modify_user(FirstName ="Voice1", LastName="Mail1", EmailAddress="Voic1e@ma1il,com",)
    #                             SelectedWorkGroups=["165"],DistributionList=["602"],Delegation=["115"])

    # DNIS
    # print(fo.create_modify_user(extension=893,DNIS = [{"TrunkDigits":"65501","TrunkDescription":"Trial","TrunkMOHID" : 1}]) # To ADD DNIS)
    # print(fo.create_modify_user(extension=893,DNIS = [{"TrunkDigits":"65501"}]) # To REMOVE Trunk from DNIS)

    # print(fo.create_modify_user(FirstName ="Firsfbt1", LastName="Lfagbst1", EmailAddress="efmailj@embail,com",UserGroup=3,AccessLicense=3,IPPhone=7))
    # print(fo.create_modify_user(FirstName ="Firfccsffbt1", LastName="Lfffagccvbfst1",EmailAddress="evfmfacccfilfj@embfail.com", Notes = 'Super'))
    # Nw LIST : License type, Access Lic, User group, Site

    # print(fo.create_modify_user(extension="196",sca_enabled=True))

    # fo.delete_extension("201")
    #  print(fo.create_hunt_group(BackupExtension=121,HuntGroupMember=[161,16122], HuntGroupName='TESTGt') # BackupExtension is mandatory)
    # fo.delete_hunt_group("123")
    # fo.create_page_list(name ="Created Page List From D2 API",extension_numbers =['160', '162'])
    # print(fo.create_paging_group(PagingGroupName="FDFDFD", PageListName = "oo", PagingDelay='4',PriorityPage='true',RingsPerMember='10'))
    # fo.delete_paging_group("189")
    # print((time.ctime()))
    # fo.configure_prog_button(user_extension ="120",button_box =0,soft_key =1,function="Agent Login",label ="Some")
    # time.sleep(4400)
    # print((time.ctime()))
    # fo.Unconfigure_prog_button(user_extension ="120",button_box= 0,soft_key =1)
    # time.sleep(1800)
    # print((time.ctime()))
    # fo.configure_prog_button(user_extension ="120",button_box =0,soft_key =2,function="Agent Wrap Up",label ="Some")
    # time.sleep(1800)
    # print((time.ctime()))
    # fo.Unconfigure_prog_button(user_extension ="120",button_box= 0,soft_key =2)
    # time.sleep(1800)
    # print((time.ctime()))
    # fo.configure_prog_button(user_extension ="120",button_box =0,soft_key =3,function="Agent Logout",label ="Some")
    # time.sleep(1800)
    # print((time.ctime()))
    # fo.Unconfigure_prog_button(user_extension ="120",button_box= 0,soft_key =3)
    # time.sleep(1800)
    # print((time.ctime()))
    # fo.configure_prog_button(user_extension ="120",button_box =0,soft_key =4,function="Agent Logout",label ="Some")
    # time.sleep(1800)
    # print((time.ctime()))
    # fo.configure_prog_button(user_extension ="120",button_box =0,soft_key =4,function="Call Move",label ="Some")
    # time.sleep(1800)
    # print((time.ctime()))
    # fo.configure_prog_button(user_extension ="120",button_box =0,soft_key =5,function="Centrex Flash",label ="Some")
    # time.sleep(1800)
    # print((time.ctime()))
    # fo.configure_prog_button(user_extension ="120",button_box =0,soft_key =6,function="Page",label ="Some")
    # time.sleep(1800)
    # print((time.ctime()))
    # fo.configure_prog_button(user_extension ="120",button_box =0,soft_key =7,function="Pickup night bell",label ="Some")
    # time.sleep(1800)
    # print((time.ctime()))
    # fo.configure_prog_button(user_extension ="120",button_box =0,soft_key =8,function="Whisper page mute",label ="Some")
    # fo.configure_prog_button(user_extension ="120",button_box =0,soft_key =9,function="Park",label ="Some",target_extension ='161')
    # fo.configure_prog_button(user_extension ="120",button_box =0,soft_key =10,function="Park and page",label ="Some",target_extension ='161')
    # fo.configure_prog_button(user_extension ="120",button_box =0,soft_key =11,function="Pickup",label ="Some",target_extension ='161')
    # fo.configure_prog_button(user_extension ="120",button_box =0,soft_key =12,function="UNPARK",label ="Some",target_extension ='161')

    # fo.configure_prog_button(user_extension ="120",button_box =0,soft_key =1,function="Barge In",label ="Some1",target_extension ='161')
    # fo.configure_prog_button(user_extension ="120",button_box =0,soft_key =2,function="Change Availability",label ="Some2",availability="available")
    # fo.configure_prog_button(user_extension ="120",button_box =0,soft_key =3,function="Whisper Page",label ="Some3",target_extension ='161')
    # fo.configure_prog_button(user_extension ="120",button_box =0,soft_key =4,function="change default audio path",label ="Some4",audio_path ='speaker')
    # fo.configure_prog_button(user_extension ="154",button_box =0,soft_key =5,function="SEND DIGITS OVER CALL",label ="Some5",Digits="160#")
    # fo.configure_prog_button(user_extension ="120",button_box =0,soft_key =6,function="Silent Coach",label ="Some6",target_extension ='161')
    # fo.configure_prog_button(user_extension ="120",button_box =0,soft_key =7,function="TOGGLE LOCK UNLOCK",label ="Some7")
    # fo.configure_prog_button(user_extension ="120",button_box =0,soft_key =8,function="transfer blind",label ="Some8",target_extension ='161')    #
    # fo.configure_prog_button(user_extension ="120",button_box =0,soft_key =9,function="transfer Consultative",label ="Some9",target_extension ='161')
    # fo.configure_prog_button(user_extension ="120",button_box =0,soft_key =10,function="transfer intercom",label ="Some10",target_extension ='161')
    # fo.configure_prog_button(user_extension ="120",button_box =0,soft_key =11,function="transfer to mailbox",label ="Some11",target_extension ='161')
    # fo.configure_prog_button(user_extension ="120",button_box =0,soft_key =12,function="transfer whisper",label ="Some12",target_extension ='161')
    # fo.configure_prog_button(user_extension ="120",button_box =0,soft_key =1,function="Record Extension",label ="Some",target_extension = 121,mailbox = 121)
    # fo.configure_prog_button(user_extension ="120",button_box =0,soft_key =2,function="Dial Mailbox",label ="Some", target_extension ='161')
    # fo.configure_prog_button(user_extension ="120",button_box =0,soft_key =3,function="Dial Number speed dial",label ="Some", target_extension ='161')
    # fo.configure_prog_button(user_extension ="120",button_box =0,soft_key =4,function="Group Pickup",label ="Some", target_extension ='170')
    # fo.configure_prog_button(user_extension ="120",button_box =0,soft_key =5,function="Hotline",label ="Some", target_extension ='162',ConnectedCallFunctionID='Dial Number') # 4 =
    # fo.configure_prog_button(user_extension ="120",button_box =0,soft_key =7,function="Intercom",label ="Some", target_extension ='161')
    # fo.configure_prog_button(user_extension ="120",button_box =0,soft_key =7,function="Malicious Call Trace",label ="Some", target_extension ='162')
    # fo.configure_prog_button(user_extension ="120",button_box =0,soft_key =8,function="Monitor Extension",RingDelayBeforeAlert = -1,label ="SomeMonitor", target_extension = 160,show_caller_id_option = "never", DisconnectedCallFunctionID='Whisper page')  # -1 for DONT RING
    # fo.configure_prog_button(user_extension ="120",button_box =0,soft_key =9,function="Conference Blind",label ="Some", external_number='161')
    # fo.configure_prog_button(user_extension ="120",button_box =0,soft_key =10,function="Conference Consultative",label ="Some", external_number='161')
    # fo.configure_prog_button(user_extension ="120",button_box =0,soft_key =11,function="Conference Intercom",label ="Some", external_number='161')

    
    # fo.Unconfigure_prog_button(user_extension ="120",button_box= 0,soft_key =1)
    # fo.Unconfigure_prog_button(user_extension ="162",button_box= 0,soft_key =2)
    # fo.Unconfigure_prog_button(user_extension ="162",button_box= 0,soft_key =3)
    # fo.Unconfigure_prog_button(user_extension ="162",button_box= 0,soft_key =4)
    # fo.Unconfigure_prog_button(user_extension ="162",button_box= 0,soft_key =5)
    # fo.Unconfigure_prog_button(user_extension ="162",button_box= 0,soft_key =6)
    # fo.Unconfigure_prog_button(user_extension ="162",button_box= 0,soft_key =7)
    # fo.Unconfigure_prog_button(user_extension ="162",button_box= 0,soft_key =8)
    # fo.Unconfigure_prog_button(user_extension ="162",button_box= 0,soft_key =9)
    # fo.Unconfigure_prog_button(user_extension ="162",button_box= 0,soft_key =10)
    # fo.Unconfigure_prog_button(user_extension ="162",button_box= 0,soft_key =11)
    # fo.Unconfigure_prog_button(user_extension ="162",button_box= 0,soft_key =12)
    # # #

    # i = 0
    # while i<12:
        # fo.Unconfigure_prog_button(user_extension ="162",button_box= 0,soft_key =i)
        # i+=1
    # i = 0
    # while i<12:
        # fo.Unconfigure_prog_button(user_extension ="195",button_box= 0,soft_key =i)
        # i+=1
    # i = 0
    # while i<12:
        # fo.Unconfigure_prog_button(user_extension ="121",button_box= 0,soft_key =i)
        # i+=1







