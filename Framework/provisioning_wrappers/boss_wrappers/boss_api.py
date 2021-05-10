__author__ = "nitin.kumar-2@mitel.com"

import sys, requests, os, logging, datetime, ast, time, re, json
import xml.etree.ElementTree as ET
sys.path.append(os.path.normpath(os.path.dirname(os.path.dirname(os.path.dirname((__file__))))))
from utils.decorators import func_logger
from vcfe import Vcfe
from get_details import GetDetails
from prog_buttons import ProgButtons
from urllib import unquote

log = logging.getLogger("boss_api")

class parse_xml(object):
    '''
    This class carries the responsibility to parse the params from the config xml file. All the optional params required to call a
    api are placed in the xml based config file.
    '''

    def __init__(self, filename):
        self.filename = filename
        self.tree = ET.parse(self.filename)
        self.root = self.tree.getroot()

    @func_logger
    def getparams(self, api_name):
        '''
        This function will create the list of params for the api call. The format is mentioned below.
        :param api_name: the name of the api
        :return: dict of param in the format {"val1":"abc",
                                                "val2":"def",
                                                    "val3":"ghi"}
        '''
        d = {}
        for api in self.root:
            if api.attrib['name'] == api_name:
                for p in api[0]:
                    if p.attrib.get("dt") == 'int':
                        d[p.tag] = int(p.text)
                    if p.attrib.get("dt") == 'None':
                        d[p.tag] = ""
                    else:
                        d[p.tag] = p.text
                break
        return d

    def getparams_frmt_1(self, api_name):
        '''
        This function will create the list of params for the api call. The format is mentioned below.
        :param api_name: the name of the api
        :return: dict of param in the format {"val1":"{"subval11":"a","subval12":"b"}",
                                                "val2":"{"subval21":"c","subval22":"d"}",
                                                    "val3":"{"subval31":"e","subval32":"f"}"}
        '''
        p = {}
        d = {}
        for api in self.root:
            if api.attrib["name"] == api_name:
                for b in api[0]:
                    p[b.tag] = b.text
                    if len(b):
                        for c in b:
                            # preserving the integers
                            if c.attrib.get("dt") == 'int':
                                d[c.tag] = int(c.text)
                            elif c.attrib.get("dt") == 'None':
                                d[c.tag] = ""
                            else:
                                d[c.tag] = c.text
                        p[b.tag] = str(d)
                        d = {}
                break
        return p

    def get_build_config_xml(self, req_build):
        '''
        This function will select a config file based on build number supplied
        :param req_build: The current boss build number
        :return: The name of the selected config file
        '''
        filename = None
        for build in self.root:
            l_build = build.attrib['lower_range']
            u_build = build.attrib['upper_range']
            if self.is_build_between(req_build, l_build, u_build):
                filename = build[0][0].text
                break
        return filename

    def is_build_between(self, build, l_range, u_range):
        '''
        This function will verify whether a given build is between a given build range.
        :param build: Current build
        :param l_range: Lower range
        :param u_range: Upper range
        :return: True if build is between the range
        '''
        build = [int(x) for x in build.split('.')]
        l_range = [int(x) for x in l_range.split('.')]
        u_range = [int(x) for x in u_range.split('.')]
        status = False
        if build == l_range or build == u_range:
            status = True
        else:
            for b,l,u in zip(build, l_range, u_range):
                if b >  l and b < u:
                    status = True
                    break
                elif b <  l or b > u:
                    status = False
                    break
                elif b == l or b == u:
                    status = True
        return status

    def update_boss_url(self, new_url):
        """
        Update the boss url in config file, if the url supplied by user is different from the one present in config

        :param new_url: boss url passed by user
        :return: None
        """
        from lxml import etree
        tree = etree.parse(self.filename)
        dinfo = tree.docinfo
        old_url = None
        for item in dinfo.internalDTD.iterentities():
            if item.name == "BOSSURL":
                old_url = item.content
        if old_url != new_url:
            try:
                log.info("Updating url in config file from <%s> to <%s>" % (old_url, new_url))
                fp = open(self.filename, 'r')
                content = fp.readlines()
                fp.close()
                for line in content:
                    if "--" not in line and "BOSSURL" in line:
                        x = re.sub(old_url, new_url, line)
                        content[2] = x
                        break
                fp = open(self.filename, 'w')
                fp.writelines(content)
                fp.close()
                return True
            except:
                log.error("Could not update url in config file from <%s> to <%s>.Please, change it manually." % (old_url, new_url))



class boss_api(object, Vcfe, GetDetails, ProgButtons):
    """
    Web Apis to perform actions on the BOSS portal. e.g. creating user, assigning phone, creating hunt group etc.
    """

    def __init__(self, build = None):
        '''
        To parse the config xml after selecting the config file based on given build number.
        :param build: Current build number
        '''
        self.config_path = os.path.normpath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config"))
        # calculating the correct config file based on the passed build number
        # will default to the BOSSAPIConfiguration.xml
        self.config_file = "BOSSAPIConfiguration.xml"
        if build:
            self.config_file = self.get_config_based_on_build(build)
        log.info("Config file picked for <%s> is <%s>"%(build,self.config_file))
        self.config = parse_xml(os.path.join(self.config_path, self.config_file))
        self.session_cookie = None
        self.headers = None
        # self.accountId will be set in the call to switch_account
        self.accountId = None
        self.part_id = None

    @func_logger
    def login(self, url = None, UserName = None, Password = None):
        '''
        This function will login to the boss portal with provided credentials.
        :param login_url: The boss url to login
        :param user: user name to login
        :param pwd: password for the user
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        # editing the boss url in config file
        if self.config.update_boss_url(url.split("//")[-1].split("/")[0]):
            self.config = parse_xml(os.path.join(self.config_path, self.config_file))
        params_xml = self.config.getparams("login")
        params = self.get_param_to_use(params_xml, url = url, UserName = UserName, Password = Password)
        log.info("Effective params for login are <%s>" % params)
        url = params.pop("url")
        ret = requests.post(url, data = params)
        if ret.status_code == 200 and "M5Portal" in ret.text:
        # if ret.status_code == 200 and "System Integration Test" in ret.text:
            log.info("Login to <%s> with data <%s> is successful" % (url, params))
            self.session_cookie = ret.request.headers['Cookie']
            self.headers = {"Cookie": self.session_cookie}
            result = True
            return result, ret
        else:
            log.error("Login to <%s> with data <%s> is not successful.Trying the new authentication method." % (url, params))
            if not self.login_new(url = url, UserName = UserName, Password = Password):
               return self.loginToBossCloud(url = url, UserName = UserName, Password = Password)

    @func_logger
    def login_new(self, url=None, UserName=None, Password=None):
        '''
        This function will login to the boss portal(new authentication) with provided credentials.
        :param login_url: The boss url to login
        :param user: user name to login
        :param pwd: password for the user
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        # editing the boss url in config file
        # if self.config.update_boss_url(url.split("//")[-1].split("/")[0]):
        #     self.config = parse_xml(os.path.join(self.config_path, self.config_file))
        params_xml = self.config.getparams("login")
        params = self.get_param_to_use(params_xml, url=url, UserName=UserName, Password=Password)
        log.info("Effective params for login are <%s>" % params)
        url = params.pop("url")
        self.headers = {'Content-Type': "application/json"}
        ret = requests.post(url, data=json.dumps(params), headers=self.headers)
        self.headers['Content-Type'] = "application/x-www-form-urlencoded"
        if ret.status_code == 200 and ret.json()["IsAuthenticated"]:
            # if ret.status_code == 200 and "System Integration Test" in ret.text:
            log.info("Login to <%s> with data <%s> is successful" % (url, params))
            self.session_cookie = self.get_cookies(ret.headers['Set-Cookie'])
            self.headers = {"Cookie": self.session_cookie}
            result = True
            return result, ret
        else:
            log.error("Login to <%s> with data <%s> is not successful.Exiting" % (url, params))
            return False

    @func_logger
    def loginToBossCloud(self, url=None, UserName=None, Password=None):
        try:
            # base URL :
            if '//' in url:
                url = url.split("//")[1]
                if '/' in url:
                    url = url.split('/')[0]
            baseURL = 'https://' + url
            lnkValidate = baseURL + r"/UserAccount/ValidateUserName?ReturnUrl=/"

            resp = requests.post(lnkValidate, json = {"userName": UserName})  # Authenticate user
            if resp.status_code != 200:
                print("Failed to validate user name")
                return False
            #  Fetch State and Client ID for authentication
            self.state = ''
            self.clientID = ''
            AuthPortalRedirectUrl = unquote(resp.json()['AuthPortalRedirectUrl'])
            for st in AuthPortalRedirectUrl.split('&'):
                if 'state' in st:
                    self.state = st.split('=')[1]
                if 'client_id' in st:
                    self.clientID = st.split('=')[1]
            if not self.clientID:
                print('Failed to fetch client ID')
            print(AuthPortalRedirectUrl)
            self.headers = {"Cookie" : 'ASP.NET_SessionId=' + resp.cookies['ASP.NET_SessionId']}
            self.reqCookies = {'ASP.NET_SessionId':resp.cookies['ASP.NET_SessionId']}
            urlAuthorize = r'https://authentication.dev.api.mitel.io/2017-09-01/authorize'
            reqData = {'client_id': self.clientID,
                        'response_type': 'code',
                        'username': UserName,
                        'password': Password,
                        'redirect_uri': url + '/UserAccount/LogOn'}
            # reqHeaders = {'origin': ' https://auth.dev.mitel.io',
            #               'referer': AuthPortalRedirectUrl,'path': '/2017-09-01/saml2/status?username='+ UserName}
            JustRes = requests.post(urlAuthorize, data=reqData, headers=self.headers)
            # check success
            if JustRes.status_code != 201:
                print('Authorization failed')
                return False
            code = JustRes.json()['code']
            intoSite = baseURL + '/UserAccount/LogOn?'
            reqPara = {'code': code, 'state': self.state}
            reqHead = {'Upgrade-Insecure-Requests': '1','referer': AuthPortalRedirectUrl}
            self.headers.update({'Upgrade-Insecure-Requests' : '1','referer': AuthPortalRedirectUrl})
            rsAccountDetails = requests.get(intoSite, params=reqPara, headers=reqHead, cookies=self.reqCookies)
            if rsAccountDetails.status_code == 200 and 'Account Details' in rsAccountDetails.content:
                self.headers['Cookie'] = self.headers['Cookie'] + ';.ASPXAUTH=' + rsAccountDetails.request._cookies['.ASPXAUTH']
                self.reqCookies['.ASPXAUTH'] = rsAccountDetails.request._cookies['.ASPXAUTH']
                for ac in rsAccountDetails.url.split('?')[1].split('&'):
                    if 'accountid' in str(ac).lower():
                        self.accountId = ac.split('=')[1]
                        print(self.accountId)
                        break
                # Retriving below ID's seems to be different from premise boss implimentation, so trying to get it here itself!
                self.personID = self.get_from_content(rsAccountDetails.content, 'personId')
                # Get partition id from GET /Account/Details?accountId=16370&locationId=-1
                params1 = {'accountId': self.accountId, 'locationId': '-1'}
                resPartitionId = requests.get(baseURL + r'/Account/Details' , params=params1, headers=self.headers)
                self.part_id = self.get_from_content(resPartitionId.content, 'partitionId')
                if not self.clientID or not self.personID or not self.part_id:
                    raise Exception('login failed or failed to fetch account id')
                log.info("Logged in successfully")
                return True
            else:
                raise Exception("Login failed. url=<%s> user=<%s> password=<%s>"%(url, UserName, Password))
        except Exception as e:
            log.error("Log in failed.Exiting... Exception : %s" % (str(e)))
            print(sys.exc_info()[0])
            os._exit(1)
            #return False

    def get_from_content(self, content, match):
        if content.find(match):
            stIndex = content.find(match) + len(match)
            if content[stIndex] == '=' :
                stIndex+=1
                counter =1
                while content[stIndex:stIndex+counter].isdigit():
                    counter+=1
                print(match + ":" + content[stIndex:stIndex+(counter-1)])
                return content[stIndex:stIndex+(counter-1)]
        return False

    def get_cookies(self, cookie):
        cookie_to_set = ""
        cookies = cookie.split(';')
        for c in cookies:
            if "ASP.NET" in c:
                cookie_to_set += c
                cookie_to_set += ";"
            elif ".ASPXAUTH" in c:
                cookie_to_set += c.split(",")[1]
                cookie_to_set += ";"
        return cookie_to_set



    @func_logger
    def switch_account(self, act_name=None):
        '''
        This function will switch to the account mentioned.
        :param act_name: The boss url to login
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        params = self.config.getparams("switch_account")
        act_id = self.get_account_detail(act_name = act_name)
        log.info("Switching to account <%s> with act id <%s>" % (act_name, act_id))
        url = params.pop("url")
        params["accountId"] = act_id
        ret = requests.get(url, data = params, headers = self.headers)
        if ret.status_code == 200 and act_name in ret.text:
            log.info("Successfully switched account to <%s>" % act_name)
            self.accountId = act_id
            result = True
        else:
            log.error("Could not switch account to <%s>" % act_name)
        return result, ret

    @func_logger
    def create_tenant(self, **params):
        '''
        This function will create a new tenant with the given details.
        :param act_name: The required params to create a new tenant. Please, refer to BOSSAPIConfiguration.xml for a complete list
        of params which can be passed to this function.Frequently used params are: CompanyName
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        params_xml = self.config.getparams("create_tenant")
        params = self.get_param_to_use(params_xml, **params)
        log.info("Creating a tenant with args <%s>"%params)
        url = params.pop("url")
        for opt in ["FirstName","LastName","PhoneNumber"]:
            params[opt] = ""
        data_to_send = {"accountId":1, "values":str(params)}
        ret = requests.post(url, data = data_to_send, headers = self.headers)
        if ret.status_code == 200 and params["CompanyName"] in ret.text:
            log.info("Successfully created account with name <%s>.\nMessage from server : <%s>" % (params["CompanyName"],ret.text))
            result = True
        else:
            log.error("Could not create account with name <%s>.\nMessage from server : <%s>" % (params["CompanyName"],ret.text))
        return result, ret

    @func_logger
    def add_user(self, **params):
        '''
        This function will add a new user with the given details to a given tenant. If profile order should also be created then
        PhoneType should be passed with some valid value.

        :param params: A dictionary of parameters. Refer BOSSAPIConfiguration.xml for more info on available params

        requestedSource = [Case 1 Email 2 Phone 3]
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        params_xml = self.config.getparams("add_user")
        params = self.get_param_to_use(params_xml, **params)
        # getting loc_id and part_id from the provided loc_name and partition name
        params["accountId"] = self.accountId
        params["Person_FirstName"] = params["Person_FirstName"]
        params["Person_LastName"] = params["Person_LastName"]
        params["Person_Username"] = params["Person_BusinessEmail"]
        params["partitionId"] = self.get_partition_detail(self.accountId, params["part_name"])
        params["Person_LocationId"] = self.get_location_id(self.accountId, params["loc_name"])
        params["Phone_LocationId"] = params["Person_LocationId"]
        params["User_LocationId"] = params["Person_LocationId"]
        params["RequestedBy"] = self.get_dm_detail(self.accountId, params["SU_Email"])
        params["PersonProfileExtension"] = params_xml["Person_Profile_Extension"]
        params["ActivationDate"] = datetime.date.today().strftime("%m/%d/%Y")
        params["ProfileOptions"] = '[{"ProductId":474,"Name":"Connect CLOUD Instant Messaging"},{"ProductId":434,"Name":"Connect CLOUD Teamwork"}]'
        params["UserGroup"] = "4"
        url = params.pop("url")
        log.info("Adding a user with args <%s>" % params)
        ret = requests.post(url, data=params, headers=self.headers)
        result = True
        # if ret.status_code == 200 and len(ret.text) == 2:
        #     log.info("Successfully added user username <%s>.\nMessage from server : <%s>" % (
        #     params["Person_BusinessEmail"], ret.text))
        #     result = True
        # else:
        #     log.error("Could not add user with username <%s>.\nMessage from server : <%s>" % (
        #     params["Person_BusinessEmail"], ret.text))
        return result, ret

    @func_logger
    def update_person_details(self, id, value,**params):
        '''
        This function will edit  a exsiting user with the given details to a given tenant.
        :param SU_Email: The email of the super user or the one which is capable of adding other users
        other params are obvious

        requestedSource = [Case 1 Email 2 Phone 3]
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        params_xml = self.config.getparams("update_person_details")
        params = self.get_param_to_use(params_xml, **params)
        
        if self.accountId is None:  # switch account has not been called
            act_id = self.get_account_detail(act_name=params['account_name'])
        else:
            act_id = self.accountId
        params["accountId"] = act_id
        if self.part_id:
            params['partitionId'] = self.part_id
        params["personId"] = self.get_person_detail(self.accountId, "", "", extension=params.get('extensionToBeProgrammed'))

        # params["personId"] = "999835"
        # params["id"] = id
        # params["value"] = value
        data = {}
        data["id"] = id
        data["value"] = value
        url = params.pop("url")
        params_to_pass = {}
        params_to_pass["accountId"] = params["accountId"]
        params_to_pass["personId"] = params["personId"]
        params_to_pass["locationId"] = params["locationId"]
        # url=r"https://portal.sit.shoretel.com/Person/UpdatePersonDetails"
        log.info("Editing a user with args <%s>" % params)
        # ret = requests.post(url, data=params, headers=self.headers)
        # self.headers['Content-Type']="application/x-www-form-urlencoded; charset=UTF-8"
        # self.headers['X-Requested-With'] = "XMLHttpRequest"
        # self.headers['Accept'] = "application/json"
        # self.headers['Content-Length'] = "21"
        ret = requests.post(url, params=params_to_pass, data=data, headers=self.headers)
        if ret.status_code == 200 and value in ret.text:
            log.info("Successfully Edited user username <%s>.\nMessage from server : <%s>" % (
            params["extensionToBeProgrammed"], ret.text))
            result = True
        else:
            log.error("Could not edit user with username <%s>.\nMessage from server : <%s>" % (
            params["extensionToBeProgrammed"], ret.text))
        return result, ret


    def add_tn_to_user(self, **params):
        '''
        This function will assign a tn and extension to an already created user.
        Note: Provide a keyword param "prod_name" during function call if you want to change the product

        :param params: A dictionary of parameters. Refer BOSSAPIConfiguration.xml for more info on available params
        :return: A tuple of a boolean status flag and the return object from the requested url

        The following call will assign a tn and extension to a user with username = sh12@bbqsqqassh.com
        Usage: obj.add_tn_to_user(part_name="HQ1",Person_FirstName="abc3",Person_LastName="xyz",Person_BusinessEmail="sh12@bbqsqqassh.com",loc_name="loc1",SU_Email="shi@sh.com",Person_Profile_Extension="1025",Profile_TnId="+16462016017")
        '''
        result = False
        # the api is same as add user so reading the same params
        params_xml = self.config.getparams("add_tn_to_user")
        params = self.get_param_to_use(params_xml, **params)
        # getting loc_id and part_id from the provided loc_name and partition name
        params["accountId"] = self.accountId
        params["Person_Username"] = params["Person_BusinessEmail"]
        params["partitionId"] = self.get_partition_detail(self.accountId, params["part_name"])
        params["Person_LocationId"] = self.get_location_id(self.accountId, params["loc_name"])
        params["Phone_LocationId"] = params["Person_LocationId"]
        params["RequestedBy"] = self.get_dm_detail(self.accountId, params["SU_Email"])
        params["ActivationDate"] = datetime.date.today().strftime("%m/%d/%Y")
        params["UserGroup"] = "4"
        params["personId"] = self.get_person_detail(self.accountId, params["part_name"], params["Person_Username"])
        # the product details
        prods = {"ConnectCLOUD Essentials": "351", "Connect CLOUD Standard": "352", "Connect CLOUD Advanced": "356",
         "Connect CLOUD Telephony": "354", "Connect CLOUD Voicemail Only": "399", "Programming": "-1",
         "Test Profile": "-2"}
        if params.has_key("prod_name"):
            prod_id = prods["prod_name"]
            prod_name = params["prod_name"]
            params["ProfileOptions"] = '[{"ProductId":%s,"Name":"%s"}]'%(prod_id, prod_name)
        else:
            params["ProfileOptions"] = '[{"ProductId":474,"Name":"Connect CLOUD Instant Messaging"},{"ProductId":434,"Name":"Connect CLOUD Teamwork"}]'

        url = params.pop("url")
        log.info("Assigning tn/extension to user with args <%s>" % params)
        ret = requests.post(url, data=params, headers=self.headers)
        if ret.status_code == 200:
            log.info("Successfully assigned tn to user.\nMessage from server : <%s>" % (
            ret.text))
            result = True
        else:
            log.error("Could not assigned tn to user.\nMessage from server : <%s>" % (
            ret.text))
        return result, ret

    def change_password(self, **params):
        '''
        This function will change the password for a given user.
        :param part_name: The name of the partition required to get the perposn id
        :param Person_BusinessEmail: The email of the user required to get the perposn id
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        params_xml = self.config.getparams("change_password")
        params = self.get_param_to_use(params_xml, **params)
        params["accountId"] = self.accountId
        params["personID"] = self.get_person_detail(self.accountId, params["part_name"], params["Person_BusinessEmail"])
        if params.has_key("NewPersonPassword"):
            params["ConfirmPersonPassword"] = params["NewPersonPassword"]
        url = params.pop("url")
        log.info("Modifying the password with args <%s>" % params)
        ret = requests.post(url, data=params, headers=self.headers)
        if ret.status_code == 200:
            log.info("Successfully changed the password for the user<%s>.\nMessage from server : <%s>" % (
            params["Person_BusinessEmail"], ret.text))
            result = True
        else:
            log.error("Could not change the password for the user <%s>.\nMessage from server : <%s>" % (
            params["Person_BusinessEmail"], ret.text))
        return result, ret

    def assign_role(self, **params):
        '''
        This function will change the password for a given user.
        :param part_name: The name of the partition required to get the perposn id
        :param Person_BusinessEmail: The email of the user required to get the perposn id
        :param role_name: The role name to assign to the user
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        params = self.config.getparams_frmt_1("assign_role")
        params["accountId"] = self.accountId
        params["personID"] = self.get_person_detail(self.accountId, params["part_name"], params["Person_BusinessEmail"])
        roles = {"Decision Maker":"1","Phone Manager":"2","Billing":"3","Emergency":"4","Partner":"7","Technical":"8"}
        for role in roles.keys():
            if role == params["role_name"]:
                rd = ast.literal_eval(params["rolesData"])
                rd["Id"] = roles[role]
                rd["Name"] = role
        # converting the rolesData to a list
        temp = []
        temp.append(rd)
        params["rolesData"] = str(temp)
        url = params.pop("url")
        log.info("Assigning role to the user with args <%s>" % params)
        ret = requests.post(url, data=params, headers=self.headers)
        if ret.status_code == 200 and ret.json()["success"]:
            log.info("Assigned role <%s> to user.\nMessage from server : <%s>" % (
                params["role_name"], ret.text))
            result = True
        else:
            log.error("Could not assign role <%s>.\nMessage from server : <%s>" % (
                params["role_name"], ret.text))
        return result, ret

    def unassign_role(self, **params):
        '''
        This function will change the password for a given user.
        :param part_name: The name of the partition required to get the perposn id
        :param Person_BusinessEmail: The email of the user required to get the perposn id
        :param role_name: The role name to assign to the user
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        params = self.config.getparams_frmt_1("assign_role")
        params["accountId"] = self.accountId
        params["personID"] = self.get_person_detail(self.accountId, params["part_name"], params["Person_BusinessEmail"])
        # roles = {"Decision Maker":"1","Phone Manager":"2","Billing":"3","Emergency":"4","Partner":"7","Technical":"8"}
        # for role in roles.keys():
        #     if role == role_name:
        #         rd = ast.literal_eval(params["rolesData"])
        #         rd["Id"] = roles[role]
        #         rd["Name"] = role
        # # converting the rolesData to a list
        # temp = []
        # temp.append(rd)
        # params["rolesData"] = str(temp)
        url = params.pop("url")
        log.info("Deleting all the assigned roles with args <%s>" % params)
        ret = requests.post(url, data=params, headers=self.headers)
        if ret.status_code == 200 and ret.json()["success"]:
            log.info("Deleted all the roles assigned to the user.\nMessage from server : <%s>" % (
                 ret.text))
            result = True
        else:
            log.error("Could not delete assigned roles to the user.\nMessage from server : <%s>" % (
                 ret.text))
        return result, ret

    def close_user(self, **params):
        '''
        This function will close the user.
        :param part_name: The name of the partition required to get the perposn id
        :param Person_BusinessEmail: The email of the user required to get the perposn id
        :param requestedby: The
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        params_xml = self.config.getparams("close_user")
        params = self.get_param_to_use(params_xml, **params)
        params["accountId"] = self.accountId
        params["partitionId"] = self.get_partition_detail(self.accountId, params["part_name"])
        params["personId"] = self.get_person_detail(self.accountId, params["part_name"], params["Person_BusinessEmail"])
        # params["requestedById"] = self.get_person_detail(self.accountId, part_name, Person_BusinessEmail)
        params["requestedById"] = params["personId"]
        params["billCeaseDate"] = (datetime.date.today()+datetime.timedelta(days=36)).strftime("%m/%d/%Y")
        url = params.pop("url")
        log.info("closing the user with args <%s>" % params)
        ret = requests.post(url, data=params, headers=self.headers)
        if ret.status_code == 200 and ret.json()["success"]:
            log.info("Successfully closed the user.\nMessage from server : <%s>" % (
                 ret.text))
            result = True
        else:
            log.error("Could not close the user.\nMessage from server : <%s>" % (
                 ret.text))
        return result, ret

    @func_logger
    def add_tn(self, **params):
        '''
        This function will add a telephone string to an account.
        :param act_name: The required params to add a tn string. Please, refer to BOSSAPIConfiguration.xml for a complete list
        of params which can be passed to this function.Frequently used params are: tnstring,tenant,requestedBy
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        params_xml = self.config.getparams("add_tn")
        params = self.get_param_to_use(params_xml, **params)
        log.info("Adding telephone numbers with args <%s>" % params)
        params["accountId"] = self.accountId
        params["TnAccountId"] = params["accountId"]
        params["RequestedBy"] = self.get_dm_detail(self.accountId, params["username"])
        url = params.pop("url")
        for opt in ["CaseNumber","ExtensionConflicts"]:
            params[opt] = ""

        ret = requests.post(url, data = params, headers = self.headers)
        if ret.status_code == 200 and str(params["accountId"]) in ret.text:
            log.info("Successfully added tn to the account with name <%s>.\nMessage from server : <%s>" % (
            params["act_name"], ret.text))
            result = True
        else:
            log.error("Could not add tn to account with name <%s>.\nMessage from server : <%s>" % (
            params["act_name"], ret.text))
        return result, ret

    def reassign_tn(self, **params):
        '''
        This function will reassign a tn or extension to a user
        :param act_name: The required params to add a tn string. Please, refer to BOSSAPIConfiguration.xml for a complete list
        of params which can be passed to this function.Frequently used params are: tnstring,tenant,requestedBy
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        params_xml = self.config.getparams("reassign_tn")
        params = self.get_param_to_use(params_xml, **params)
        params["accountId"] = self.accountId
        params["partitionId"] = self.get_partition_detail(self.accountId, params["part_name"])
        params["profileId"] = self.get_profile_detail(self.accountId,params["part_name"],params["username"])
        url = params.pop("url")
        log.info("Reassigning tn to user with args <%s>" % params)
        ret = requests.post(url, data = params, headers = self.headers)
        if ret.status_code == 200 and ret.json()["message"] == "Number was re-assigned":
            log.info("Successfully reassigned tn/extension to the user.\nMessage from server : <%s>" % (
            ret.text))
            result = True
        else:
            log.error("Could not reassign tn/extension to the user.\nMessage from server : <%s>" % (
            ret.text))
        return result, ret

    def add_edit_phone(self, **params):
        '''
        This function will add a given phone to an account.
        :param loc_name: location name in which the phone needs to be added
        :param mac_address: mac address of the phone to be added  e.g.  11:11:11:11:11:11
        :param params: Please, refer to BOSSAPIConfiguration.xml for a complete list
        of params which can be passed to this function.
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        params_xml = self.config.getparams("add_edit_phone")
        params = self.get_param_to_use(params_xml, **params)
        url = params.pop("url")
        params["accountId"] = self.accountId
        params["partitionId"] = self.part_id
        params["Phone_LocationId"] = self.get_location_id(self.accountId, params["loc_name"])
        params["Phone_MacAddress"] = params["mac_address"]
        log.info("Adding a new phone with args <%s>" % params)
        ret = requests.post(url, data=params, headers=self.headers)
        if ret.status_code == 200 and ret.json()["message"] == u'Note: Adding this phone does not constitute purchase or shipment of a phone from Shoretel. If you want to do so, please use the Add Services screen.':
            log.info("Successfully added phone.\nMessage from server : <%s>" % (
                ret.text))
            result = True
        elif ret.status_code == 200 and ret.json()["message"] == u'Note: Editing this phone does not constitute purchase or shipment of a phone from Shoretel. If you want to do so, please use the Add Services screen.':
            log.info("Successfully edited phone.\nMessage from server : <%s>" % (
                ret.text))
            result = True
        else:
            log.error("Could not add phone.\nMessage from server : <%s>" % (
                ret.text))
        return result, ret

    def remove_phone_entry(self, **params):
        '''
        This function will remove an added telephone.
        :param mac_address: mac address of the phone to be added  e.g.  11:11:11:11:11:11
        :param params: Please, refer to BOSSAPIConfiguration.xml for a complete list
        of params which can be passed to this function.
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        params_xml = self.config.getparams("remove_phone_entry")
        params = self.get_param_to_use(params_xml, **params)
        url = params.pop("url")
        params["accountId"] = self.accountId
        params["macAddress"] = params["mac_address"]
        log.info("Removing phone with args <%s>" % params)
        ret = requests.post(url, data=params, headers=self.headers)
        if ret.status_code == 200 and ret.json()["message"] == u'Phone With Mac Address %s has been successfully deleted.'%mac_address:
            log.info("Successfully removed phone.\nMessage from server : <%s>" % (
                ret.text))
            result = True
        else:
            log.error("Could not remove phone.\nMessage from server : <%s>" % (
                ret.text))
        return result, ret

    def check_extension_availability(self, **params):
        '''
        This function will check if an extension is available or not
        :param part_name: The partition name
        :param extension: The extension number to check
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        params_xml = self.config.getparams("check_extension_availability")
        params = self.get_param_to_use(params_xml, **params)
        params["accountId"] = self.accountId
        if not self.part_id:
            params["partitionId"] = self.get_partition_detail(self.accountId, params["part_name"])
        else:
            params["partitionId"] = self.part_id
        params["extension"] = params["extension"]
        url = params.pop("url")
        log.info("Reassigning tn to user with args <%s>" % params)
        ret = requests.post(url, params = params, headers = self.headers)
        if ret.status_code == 200 and str(ret.json()) == str(params["extension"]):
            log.info("Extension <%s> is available.\nMessage from server : <%s>" % (
                params["extension"], ret.text))
            result = True
        elif ret.status_code == 200 and str(ret.json()) != str(params["extension"]):
            log.info("Extension <%s> already in use.Suggested extension is <%s>.\nMessage from server : <%s>" % (
                params["extension"], ret.json(),ret.text))
            result = True
        else:
            log.error("Could not reassign tn/extension to the user.\nMessage from server : <%s>" % (
            ret.text))
        return result, ret

    def check_usergroup_availability(self, **params):
        '''
        This function will check if an extension is available or not
        :param part_name: The partition name
        :param ug_name: The name of the user group created
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        is_available = False
        params_xml = self.config.getparams("check_usergroup_availability")
        params = self.get_param_to_use(params_xml, **params)
        params["accountId"] = self.accountId
        params["partitionId"] = self.get_partition_detail(self.accountId, params["part_name"])
        params["userGroupName"] = params["ug_name"]
        url = params.pop("url")
        log.info("Checking availability of user group with args <%s>" % params)
        ret = requests.post(url, data = params, headers = self.headers)
        if ret.status_code == 200 and ret.json().has_key("result"):
            log.info("User group name is available.\nMessage from server : <%s>" % (
                ret.text))
            is_available = True
        else:
            log.error("User group name is not available.\nMessage from server : <%s>" % (
            ret.text))

        return is_available

    def check_username_availability(self, **params):
        '''
        This function will check if a user name is available or not
        :param user_name: The user name to be checked
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        is_available = False
        params_xml = self.config.getparams("check_username_availability")
        params = self.get_param_to_use(params_xml, **params)
        params["accountId"] = self.accountId
        params["username"] = params["user_name"]
        url = params.pop("url")
        log.info("Checking availability of user name with args <%s>" % params)
        ret = requests.post(url, data = params, headers = self.headers)
        if ret.status_code == 200 and ret.text == 'true':
            log.info("User name is available.\nMessage from server : <%s>" % (
                ret.text))
            is_available = True
        else:
            log.error("User name is not available.\nMessage from server : <%s>" % (
            ret.text))

        return is_available

    def check_mac_address_availability(self, **params):
        '''
        This function will check if a macAddress is available or not
        :param macAddress: The macAddress to be checked
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        is_available = False
        params_xml = self.config.getparams("check_mac_address_availability")
        params = self.get_param_to_use(params_xml, **params)
        params["macAddress"] = params["macAddress"]
        url = params.pop("url")
        log.info("Checking availability of macAddress with args <%s>" % params)
        ret = requests.post(url, data = params, headers = self.headers)
        if ret.status_code == 200 and ret.text == 'true':
            log.info("macAddress is available.\nMessage from server : <%s>" % (
                ret.text))
            is_available = True
        else:
            log.error("macAddress is not available.\nMessage from server : <%s>" % (
            ret.text))

        return is_available

    @func_logger
    def update_tn(self, **params):
        '''
        This function will update a tn status.
        :param tnstring: the tn string to update. don't use the + sign
        :param params: The required params to update a tn string. Please, refer to BOSSAPIConfiguration.xml for a complete list
        of params which can be passed to this function.Frequently used params are: state,type
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        tn_ends = '.840.1'
        type = {"Real":"1"}
        state = {"Available":"4"}
        # converting string to corresponding ints and overriding them in param
        params["Type"] = type[params["type"]] if params.get("type") else 1
        params["State"] = state[params["state"]] if params.get("state") else 4
        params["PortOutDate"] = datetime.date.today().strftime("%m/%d/%Y")
        params_xml = self.config.getparams("update_tn")
        # assigning not required param to ""
        for opt in ["TnCountryId", "TnAccountId", "ExtensionConflicts"]:
            params_xml[opt] = ""
        params = self.get_param_to_use(params_xml, **params)
        # mandatory param
        if "-" in params["tnstring"]:
            tn_range = params["tnstring"].split("-")
            tn_range[1] = tn_range[0][:-4] + tn_range[1] + tn_ends
            params["TnsString"] = tn_range[0]+tn_ends+'|'+tn_range[1]+tn_ends
        else:
            params["TnsString"] = params["tnstring"] + tn_ends
        params["accountId"] = self.accountId
        url = params.pop("url")

        log.info("Updating telephone numbers with args <%s>" % params)
        ret = requests.post(url, data=params, headers=self.headers)
        if ret.status_code == 200 and str(params["accountId"]) in ret.text:
            log.info("Successfully updated tn <%s>.\nMessage from server : <%s>" % (
                params["TnsString"], ret.text))
            result = True
        else:
            log.error("Could not update tn <%s>.\nMessage from server : <%s>" % (
                params["TnsString"], ret.text))
        return result, ret

    def add_contract(self, **params):
        '''
        This method will add a new contract.
        :param company_name: the name of the company to be used while adding the contract
        :param params: The required params to add a new contract. Please, refer to BOSSAPIConfiguration.xml for a complete list
        of params which can be passed to this function.Frequently used params are: CompanyName
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        params = self.config.getparams_frmt_1("add_contract")
        url = params.pop("url")
        # updating the values provided by the user
        temp_val = ast.literal_eval(params["accountValues"])
        temp_val["CompanyName"] = params["company_name"]
        params["accountValues"] = str(temp_val)
        # modifying format of some params to suit the api demand
        d =  ast.literal_eval(params["locationsValues"])
        t= d["ValidationResult"]
        p = ast.literal_eval(t)
        d["ValidationResult"] = p
        params["locationsValues"] = d
        # modifying the details of the contract pdf file
        contract = ast.literal_eval(params["contractValues"])
        if os.path.isfile(params["file_path"]):
            contract["ContractFileName"] = os.path.basename(params["file_path"])
        else:
            raise Exception("File <%s> does not exist"%params["file_path"])
        contract["ContractFilePath"] = str(self.upload_pdf(params["file_path"]))
        params["contractValues"] = str(contract)
        # converting productValues and locationValues to lists
        temp = []
        temp.append(params["locationsValues"])
        params["locationsValues"] = str(temp)
        temp = []
        temp.append(ast.literal_eval(params["productsValues"]))
        params["productsValues"] = str(temp)
        # removing quotes from the text
        params["accountValues"] = params["accountValues"].replace('\'null\'','null')
        log.info("Adding contract with args <%s>" % params)
        ret = requests.post(url, data=params, headers=self.headers)
        if ret.status_code == 200 and "New Contract successfully added " in ret.text:
            log.info("Successfully added new contract with id <%s>.\nMessage from server : <%s>" % (
                ast.literal_eval(ret.text)["newAccountId"], ret.text))
            result = True
        else:
            log.error("Could not add new contract.\nMessage from server : <%s>" % (
                ret.text))
        return result, ret

    def update_billing_location(self,account_name, billing_locationName):
        '''

        :param account_name:
        :param billing_locationName:
        :return:
        '''
        result = False
        params = self.config.getparams_frmt_1("update_billing_location")
        url = params.pop("url")
        params["accountId"] = self.accountId
        params["contractId"] = self.get_contract_detail(self.accountId)
        params["billingLocationId"] = self.get_location_id(self.accountId, billing_locationName)
        log.info("Updating the billing location for account <%s>" % account_name)
        ret = requests.post(url, data = params, headers = self.headers)
        if ret.status_code == 200 and "Contract billing location successfully updated." in ret.text:
            log.info("Successfully updated billing location <%s> for account <%s>.\nMessage from server : <%s>" % (
                billing_locationName, account_name, ret.text))
            result = True
        else:
            log.error("Could not update billing location <%s> for account <%s>.\nMessage from server : <%s>" % (
                billing_locationName, account_name, ret.text))
        return result, ret

    def add_instance_to_contract(self, **params):
        '''
        This function will add an instance to the contract
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        params_xml = self.config.getparams("add_instance_to_contract")
        url = params_xml.pop("url")
        params_xml["AccountId"] = self.accountId
        params_xml["ClusterId"] = self.get_cluster_detail(params_xml["Cluster"].split()[0])
        params["newValues"] = str(params_xml)
        log.info("Adding instance to the contract with args <%s>" % params)
        ret = requests.post(url, data = params, headers = self.headers)
        if ret.status_code == 200 and ret.json()["Id"] != None:
            log.info("Successfully added instance to the contract.\nMessage from server : <%s>" % (
                ret.text))
            result = True
        else:
            log.error("Could not add an instance to the contract.\nMessage from server : <%s>" % (
                ret.text))
        return result, ret

    def add_location_as_site(self, **params):
        '''
        This function will add a given location as a site.
        :param loc_name: location name to be added as site
        :param part_name: partition name
        :param params: The required params to add a location as site. Please, refer to BOSSAPIConfiguration.xml for a complete list
        of params which can be passed to this function.
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        params_xml = self.config.getparams("assign_location_as_site")
        params = self.get_param_to_use(params_xml, **params)
        url = params.pop("url")
        loc_id = self.get_location_id(self.accountId, params["loc_name"])
        params["accountId"] = self.accountId
        params["partitionId"] = self.get_partition_detail(self.accountId, params["part_name"])
        params["siteData"] = '[{"LocationId":"%s", "AreaCode":"auto"}]'%loc_id
        log.info("Adding location as site with args <%s>" % params)
        ret = requests.post(url, data=params, headers=self.headers)
        if ret.status_code == 200:
            log.info("Successfully added location <%s> as site.\nMessage from server : <%s>" % (
                params["loc_name"], ret.text))
            result = True
        else:
            log.error("Could not add location <%s> as site.\nMessage from server : <%s>" % (
                params["loc_name"], ret.text))
        return result, ret

    def add_location(self, **params):
        '''
        This function will add a given location as a site.
        :param loc_name: location name to be added
        :param part_name: partition name
        :param params: The required params to add a location as site. Please, refer to BOSSAPIConfiguration.xml for a complete list
        of params which can be passed to this function.
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        params_xml = self.config.getparams("add_location")
        params = self.get_param_to_use(params_xml, **params)
        url = params.pop("url")
        params["accountId"] = self.accountId
        params["partitionId"] = self.get_partition_detail(self.accountId, params["part_name"])
        params["Location_Subtenant"] = params["LocationDetails_LocationNameFormatted"] = params["loc_name"]
        params["Location_InvoiceGroupId"] = self.get_suitable_invoice_groups(self.accountId,params["invoice_group"])
        log.info("Adding a new location with args <%s>" % params)
        ret = requests.post(url, data=params, headers=self.headers)
        if ret.status_code == 200 and ret.json().has_key("retValue"):
            log.info("Successfully added location <%s>.\nMessage from server : <%s>" % (
                params["loc_name"], ret.text))
            result = True
        else:
            log.error("Could not add location <%s>.\nMessage from server : <%s>" % (
                params["loc_name"], ret.text))
        return result, ret

    def update_location(self, **params):
        '''
        This function will update the address of a location
        :param loc_name: location name to be added
        :param part_name: partition name
        :param params: The required params to add a location as site. Please, refer to BOSSAPIConfiguration.xml for a complete list
        of params which can be passed to this function.
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        params_xml = self.config.getparams("update_location")
        params = self.get_param_to_use(params_xml, **params)
        url = params.pop("url")
        params["accountId"] = self.accountId
        params["locationId"] = self.get_location_id(self.accountId, params["loc_name"])
        params["partitionId"] = self.get_partition_detail(self.accountId, params["part_name"])
        params["Location_Subtenant"] = params["LocationDetails_LocationNameFormatted"] = params["loc_name"]
        log.info("Updating a location with args <%s>" % params)
        ret = requests.post(url, data=params, headers=self.headers)
        if ret.status_code == 200 and ret.json().has_key("retValue"):
            log.info("Successfully updated location <%s>.\nMessage from server : <%s>" % (
                params["loc_name"], ret.text))
            result = True
        else:
            log.error("Could not update location <%s>.\nMessage from server : <%s>" % (
                params["loc_name"], ret.text))
        return result, ret

    def close_location(self, **params):
        '''
        This function will close a location. The function will first close the associated order
        :param loc_name: location name to be added
        :param SU_Email: super user or DM
        :param params: The required params to close a location. Please, refer to BOSSAPIConfiguration.xml for a complete list
        of params which can be passed to this function.
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        # closing the order before proceeding to close the location
        order = self.get_order_detail(self.accountId, params["loc_name"])
        self.update_order_details(order)
        # now closing the location
        params_xml = self.config.getparams("close_location")
        params = self.get_param_to_use(params_xml, **params)
        url = params.pop("url")
        params["accountId"] = self.accountId
        params["closeLocationId"] = params["locationId"] = self.get_location_id(self.accountId, params["loc_name"])
        params["billCeaseDate"] = datetime.date.today().strftime("%m/%d/%Y")
        params["requestedById"] = self.get_dm_detail(self.accountId, params["SU_Email"])
        log.info("Closing a location with args <%s>" % params)
        ret = requests.post(url, data=params, headers=self.headers)
        if ret.status_code == 200 and ret.json().has_key("message"):
            log.info("Successfully closed location <%s>.\nMessage from server : <%s>" % (
                params["loc_name"], ret.text))
            result = True
        elif ret.json().has_key("error"):
            log.error("Could not close the location <%s>.\nMessage from server : <%s>" % (
                params["loc_name"], ret.text))
        return result, ret

    def update_order_details(self, **params):
        '''
        This function will close an order
        :param order_id: the id of the order
        :param params: Please, refer to BOSSAPIConfiguration.xml for a complete list
        of params which can be passed to this function.
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        params_xml = self.config.getparams("update_order_details")
        params = self.get_param_to_use(params_xml, **params)
        url = params.pop("url")
        params["accountId"] = self.accountId
        params["orderId"] = params["order_id"]
        log.info("Closing the order with args <%s>" % params)
        ret = requests.post(url, data=params, headers=self.headers)
        if ret.status_code == 200 and ret.json().has_key("message"):
            log.info("Successfully closed the order.\nMessage from server : <%s>" % (
                ret.text))
            result = True
        elif len(ret.text) == 2 or ret.json().has_key("error"):
            log.error("Could not close the order.\nMessage from server : <%s>" % (
                ret.text))
        return result, ret

    def validate_canclose_location(self, **params):
        '''
        This function will validate if a location can be closed or not
        :param loc_name: location name to be added
        :param params: Please, refer to BOSSAPIConfiguration.xml for a complete list
        of params which can be passed to this function.
        :return: A boolean status flag
        '''
        can_close = False
        params_xml = self.config.getparams("validate_canclose_location")
        params = self.get_param_to_use(params_xml, **params)
        url = params.pop("url")
        params["accountId"] = self.accountId
        params["locationId"] = self.get_location_id(self.accountId, params["loc_name"])
        params["billCeaseDate"] = datetime.date.today().strftime("%m/%d/%Y")
        log.info("Validating if a location can be closed with args <%s>" % params)
        ret = requests.post(url, data=params, headers=self.headers)
        if ret.status_code == 200 and ret.json().has_key("message"):
            log.info("Location <%s> can be closed.\nMessage from server : <%s>" % (
                params["loc_name"], ret.text))
            can_close = True
        else:
            log.error("Location <%s> can not be closed.\nMessage from server : <%s>" % (
                params["loc_name"], ret.text))
        return can_close

    def validate_location(self, **params):
        '''
        This function will validate a given location.
        :param params: The account name
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        isValid = False
        params_xml = self.config.getparams("validate_location")
        params = self.get_param_to_use(params_xml, **params)
        url = params.pop("url")
        log.info("Validating location with args <%s>" % params)
        ret = requests.post(url, data = params, headers = self.headers)
        if ret.status_code == 200 and len(ret.json()['Errors']) == 0:
            log.info("The given location is valid.Message from server : <%s>"% (ret.text))
            isValid = True
        else:
            log.error("The given location is not valid.Message from server : <%s>"% (ret.text))

        return isValid,ret

    def validate_location_name(self,loc_name, **params):
        '''
        This function will validate a given location.
        :param loc_name: The location name to be validated
        :return: A boolean status flag
        '''
        IsValid = False
        params_xml = self.config.getparams("validate_location_name")
        params = self.get_param_to_use(params_xml, **params)
        params["accountId"] = self.accountId
        params["locationName"] = loc_name
        url = params.pop("url")
        log.info("Validating location name with args <%s>" % params)
        ret = requests.post(url, data = params, headers = self.headers)
        if ret.status_code == 200 and ret.json()['isValid']:
            log.info("The given location name is valid.Message from server : <%s>"% (ret.text))
            IsValid = True
        else:
            log.error("The given location name is not valid.Message from server : <%s>"% (ret.text))
        return IsValid

    def create_partition(self, **params):
        '''
        This function will create a partition.
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        params_xml = self.config.getparams("create_partition")
        params = self.get_param_to_use(params_xml, **params)
        params["accountId"] = self.accountId
        if params.has_key("cluster_name"):
            params["ClusterId"] = self.get_cluster_detail(params["cluster_name"])
        params["siteData"] = '[{"LocationId":%s,"AreaCode":"auto"}]'%(self.get_location_id(self.accountId,params["location_name"]))
        url = params.pop("url")
        log.info("Creating partition with args <%s>" % params)
        ret = requests.post(url, data = params, headers = self.headers)
        if ret.status_code == 200 and ret.json()['retValue'] == 132:
            log.info("The requested partition has been created.Message from server : <%s>"% (ret.text))
            result = True
        else:
            log.error("The requested partition could not be created.Message from server : <%s>"% (ret.text))

        return result, ret

    def add_profile(self, **params):
        '''
        This function will add a profile.
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        params_xml = self.config.getparams("add_profile")
        params = self.get_param_to_use(params_xml, **params)
        params["accountId"] = self.accountId
        params["partitionId"] = self.part_id
        params["RequestedByAdd"] = self.get_dm_detail(self.accountId, params["dm_name"])
        params["AddLocationToAssign"] = self.get_location_id(self.accountId, params["location_name"])
        params["DateLiveAdd"] = datetime.date.today().strftime("%m/%d/%Y")
        url = params.pop("url")
        log.info("Adding profile with args <%s>" % params)
        ret = requests.post(url, data = params, headers = self.headers)

        # todo identify the ret.json when it passes without processing in background
        if ret.status_code == 200 and ret.json()['retValue'] == 132:
            log.info("The requested profile has been added.Message from server : <%s>"% (ret.text))
            result = True
        elif "Order has been created, and processing takes longer than expected. It will be processed in the background" in ret.text:
            log.info("The requested profile has been added.Message from server : <%s>" % (ret.text))
            result = True
        else:
            log.error("The requested profile could not be added.Message from server : <%s>"% (ret.text))
        return result, ret

    def validate_assign_profile(self, user_name, **params):
        '''
        This function will validate a profile
        primary Partition -> assign number -> the username entered will be validated
        :return: A boolean result flag
        '''
        isValid = False
        params_xml = self.config.getparams("validate_assign_profile")
        params = self.get_param_to_use(params_xml, **params)
        params["accountId"] = self.accountId
        params["username"] = user_name
        url = params.pop("url")
        log.info("Validating the profile with args <%s>" % params)
        ret = requests.post(url, data = params, headers = self.headers)
        if ret.status_code == 200 and ret.json()["validationResult"]:
            log.info("The requested profile has been validated.Message from server : <%s>"% (ret.text))
            isValid = True
        else:
            log.error("The requested profile could not be validated.Message from server : <%s>"% (ret.text))
        return isValid

    def assign_number(self, **params):
        '''
        This function will assign a number to a user
        primary Partition -> assign number
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        params_xml = self.config.getparams("assign_number")
        params = self.get_param_to_use(params_xml, **params)
        params["accountId"] = self.accountId
        params["partitionId"] = self.part_id
        params["tn"] = params["tn"]
        params["Email"] = params["user_name"]
        params["LocationToAssign"] = self.get_location_id(self.accountId, params["loc_name"])
        params["DateLive"] = datetime.date.today().strftime("%m/%d/%Y")
        params["RequestedBy"] = self.get_dm_detail(self.accountId, params["dm_name"])
        params["extension"] = params["extension"]
        url = params.pop("url")
        log.info("Assigning the number with args <%s>" % params)
        ret = requests.post(url, data = params, headers = self.headers)
        # todo need to verify the succes case. At present all orders are going in pipeline to process.
        if ret.status_code == 200 and ret.json().has_key("message"):
            log.info("The number has been assigned successfully.Message from server : <%s>"% (ret.text))
            result = True
        else:
            log.error("The number could not be assigned.Message from server : <%s>"% (ret.text))
        return result, ret

    def unassign_number(self, **params):
        '''
        This function will unassign a number to a user
        primary Partition -> assign number
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        params_xml = self.config.getparams("unassign_number")
        params = self.get_param_to_use(params_xml, **params)
        params["accountId"] = self.accountId
        params["partitionId"] = self.part_id
        params["ProfileIds"] = params["profileIds"] = self.get_profile_detail(self.accountId,params["part_name"],params["user_name"])
        params["RequestedBy"] = self.get_dm_detail(self.accountId, params["dm_name"])
        url = params.pop("url")
        log.info("Unassigning the number with args <%s>" % params)
        ret = requests.post(url, data = params, headers = self.headers)
        if ret.status_code == 200 and ret.json()["success"]:
            log.info("The number has been unassigned successfully.Message from server : <%s>"% (ret.text))
            result = True
        else:
            log.error("The number could not be unassigned.Message from server : <%s>"% (ret.text))
        return result, ret

    def update_cosmo_partition_dialplan(self, **params):
        '''
        This function will update a dial plan
        primary Partition -> dial plan
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        params_xml = self.config.getparams("update_cosmo_partition_dialplan")
        params = self.get_param_to_use(params_xml, **params)
        # params["accountId"] = int(self.accountId)
        # params["partitionId"] = int(self.part_id)
        # params["locationId"] = -1
        # todo for some unknown reason at this point of time, the api works only if url is in below format
        url = params.pop("url") + "?accountId=%d&locationId=%d&partitionId=%d"%(self.accountId, -1, int(self.part_id))
        # url = params.pop("url")
        log.info("Updating dial plan with args <%s>" % params)
        ret = requests.post(url, data = params, headers = self.headers)
        if ret.status_code == 200 and ret.json()["success"]:
            log.info("The dial plan has been updated.Message from server : <%s>"% (ret.text))
            result = True
        else:
            log.error("Could not update the dial plan.Message from server : <%s>"% (ret.text))
        return result, ret


    def create_usergroup(self, **params):
        '''
        This function will create a user group

        ProfileTypeId = {"Managed":"2","Courtesy":"5","TelephoneOnly":"7"}
        : param ug_name: The name of user name to be created
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        params_xml = self.config.getparams("create_usergroup")
        params = self.get_param_to_use(params_xml, **params)
        params["accountId"] = self.accountId

        if params.get("part_name"): #MSN
            params["partitionId"] = self.get_partition_detail(self.accountId, params["part_name"])
            # params["groupId"]=self.get_usergroup_detail(self.accountId, params["part_name"],params["ug_name"])
        else:
            params["partitionId"] = self.part_id
            # params["groupId"]=self.get_usergroup_detail(self.accountId,params["ug_name"])
        params["Name"] = params["ug_name"]
        url = params.pop("url")
        log.info("Creating user group with args <%s>" % params)
        ret = requests.post(url, data=params, headers=self.headers)
        if ret.status_code == 200 and len(ret.text) == 2:
            log.info("User group created successfully.\nMessage from server : <%s>" % (
                ret.text))
            result = True
        else:
            log.error("Could not create User group.\nMessage from server : <%s>" % (
                ret.text))

        return result, ret

    def update_usergroup(self, **params):
        '''
        This function will update a user group
        : param ug_name: The name of user name to be updated
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        # With this option user can change the MOH settings for the group. NOTE: Can only change between MOH files which user uploaded. # MSN
        if params.get('moh_name'):
            isFound= False
            params_xml1 = self.config.getparams("get_all_moh_names")
            params1 = self.get_param_to_use(params_xml1, **params)
            params1["accountId"] = self.accountId
            params1["partitionId"]= self.part_id
            url = params1.pop("url")
            all_moh_names= requests.get(url, params = params1, headers = self.headers)
            for mohs in all_moh_names.json()['data']:
                if str(mohs['Name']).lower() == str(params.get('moh_name')).lower():
                   params['HoldMusicId']= mohs['id']
                   isFound=True
                   break
            if not isFound:
                print("MOH name not found in the system")
        result = False
        params_xml = self.config.getparams("update_usergroup")
        params = self.get_param_to_use(params_xml, **params)
        params["accountId"] = self.accountId
        params["Name"] = params["ug_name"]
        if params.get("part_name"): #MSN
            params["partitionId"] = self.get_partition_detail(self.accountId, params["part_name"])
            params["groupId"]=self.get_usergroup_detail(self.accountId, params["part_name"],params["ug_name"])
        else:
            params["partitionId"] = self.part_id
            params["groupId"]=self.get_usergroup_detail(self.accountId,params["ug_name"])
        url = params.pop("url")
        log.info("Updating user group with args <%s>" % params)
        ret = requests.post(url, data=params, headers=self.headers)
        if ret.status_code == 200 and len(ret.text) == 2:
            log.info("User group updated successfully.\nMessage from server : <%s>" % (
                ret.text))
            result = True
        else:
            log.error("Could not update User group.\nMessage from server : <%s>" % (
                ret.text))

        return result, ret

    def delete_usergroup(self, **params):
        '''
        This function will delete a user group
        : param ug_name: The name of user name to be created
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        params_xml = self.config.getparams("delete_usergroup")
        params = self.get_param_to_use(params_xml, **params)
        params["accountId"] = self.accountId

        # params["groupIds"] = self.get_usergroup_detail(self.accountId, params["part_name"],params["ug_name"])
        if params.get("part_name"): #MSN
            # params["partitionId"] = self.get_partition_detail(self.accountId, params["part_name"])
            params["groupIds"]=self.get_usergroup_detail(self.accountId, params["part_name"],params["ug_name"])
        else:
            # params["partitionId"] = self.part_id
            params["groupIds"]=self.get_usergroup_detail(self.accountId,params["ug_name"])


        url = params.pop("url")
        log.info("Deleting user group with args <%s>" % params)
        ret = requests.post(url, data=params, headers=self.headers)
        if ret.status_code == 200 and (ret.text) == '"success"':
            log.info("User group deleted successfully.\nMessage from server : <%s>" % (
                ret.text))
            result = True
        else:
            log.error("Could not delete User group.\nMessage from server : <%s>" % (
                ret.text))

        return result, ret

    def update_contract_status(self, **params):
        '''
        Make sure to add following to the contract before trying to confirm the status
        add location - update_billing_location
        add instance - add_instance_to_contract
        add partition- create_partition

        These functions are not called from this function to give more flexibility and control.

        This function will update the status of a contract.
        :param params: The account name
        :return: True if location is valid
        '''
        result = False
        params_xml = self.config.getparams("update_contract_status")
        params = self.get_param_to_use(params_xml, **params)
        params["accountId"] = self.accountId
        params["contractId"] = self.get_contract_detail(self.accountId)
        url = params.pop("url")
        log.info("Updating the contract status with args <%s>" % params)
        ret = requests.post(url, data = params, headers = self.headers)
        if ret.status_code == 200:
            while not self.get_async_web_job(ret.json()["Id"]) == 100:
                time.sleep(1)
            order_id = self.get_contract_line_item_data(self.accountId,params["contractId"])
            if order_id:
                log.info("The contract has been confirmed.Order id : <%s>"% (order_id))
                result = True
            else:
                log.error("The contract could not been confirmed.Order id : <%s>" % (order_id))
        else:
            log.error("The contract could not been confirmed.Message from server : <%s>"% (ret.text))

        return result, ret

    def get_async_web_job(self, id):
        '''
        This function will return the status of a async web job
        :param id: The id of the job
        :return: % value of the job completed
        '''
        params = self.config.getparams("get_async_web_job")
        url = params.pop("url")
        log.info("Updating the contract status with args <%s>" % params)
        ret = requests.post(url, data = params, headers = self.headers)
        if ret.status_code == 200:
            log.info("The contract has been confirmed.Message from server : <%s>"% (ret.text))
        else:
            log.error("The contract could not been confirmed.Message from server : <%s>"% (ret.text))
        return int(ret.json()["PercentComplete"])

    def get_contract_line_item_data(self, account_id, contract_id):
        '''
        This function will return the status of the contract
        :param account_id: The id of the account
        :param contract_id: The id of the contract in the account
        :return: the order id
        '''
        order_id = 0
        params = self.config.getparams("get_contract_line_item_data")
        params["accountId"] = account_id
        params["contractId"] = contract_id
        url = params.pop("url")
        log.info("Getting the order id for contract updated with args <%s>" % params)
        ret = requests.get(url, data = params, headers = self.headers)
        if ret.status_code == 200:
            log.info("The contract has been confirmed.Message from server : <%s>"% (ret.text))
        else:
            log.error("The contract could not been confirmed.Message from server : <%s>"% (ret.text))

        # parsing the returned content to get the id
        for loc, details in ret.json().iteritems():
            if loc == "data":
                for d in details:
                    order_id = d["OrderId"]
                    break
        return order_id

    def upload_pdf(self, filepath):
        '''
        This function will upload the pdf contract
        :param params: The param
        :return: The location of the uploaded pdf contract, which should be used while adding a new contract or None if fails
        '''
        uploaded_path = None
        params = self.config.getparams("upload_pdf")
        url = params.pop("url")
        files = {'file': open(filepath, 'rb')}
        log.info("Uploading the pdf contract file <%s>" % params)
        ret = requests.post(url, data=params, files=files, headers=self.headers)
        uploaded_path = ret.json()['filePath']
        if ret.status_code == 200 and ret.json()['message'] == "OK":
            log.info("Successfully uploaded pdf to <%s>" % (uploaded_path))
        else:
            log.error("could not upload the pdf contract file.Message from server: <%s>" % (ret.text))

        return str(uploaded_path)

    def update_cosmo_conference(self, dm_user, **params):
        '''
        This function will activate the collaboration add on
        phone system -> add on --> collaboration
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        params_xml = self.config.getparams("update_cosmo_conference")
        params = self.get_param_to_use(params_xml, **params)
        params["accountId"] = int(self.accountId)
        params["partitionId"] = int(self.part_id)
        params["EmailList"] = dm_user
        url = params.pop("url")
        log.info("Activating collaboration add on with args <%s>" % params)
        ret = requests.post(url, data = params, headers = self.headers)
        if ret.status_code == 200 and ret.json().has_key("message"):
            log.info("The collaboration has been activated.Message from server : <%s>"% (ret.text))
            result = True
        else:
            log.error("Could not activate the collaboration ad on.Message from server : <%s>"% (ret.text))
        return result, ret

    def create_cosmo_conference_handler(self, user_fullname, **params):
        '''
        This function will get the available users for creating a cosmo conference
        phone system -> add on --> collaboration --> manage
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        profile_id = None
        params_xml = self.config.getparams("create_cosmo_conference_handler")
        params = self.get_param_to_use(params_xml, **params)
        params["accountId"] = int(self.accountId)
        params["partitionId"] = int(self.part_id)
        url = params.pop("url")
        log.info("Getting the users available for creating collaboration with args <%s>" % params)
        ret = requests.get(url, data = params, headers = self.headers)
        if ret.status_code == 200 and "ProfileId" in ret.text:
            log.info("The users have been retrieved for creating collaboration.Message from server : <%s>"% (ret.text))
        else:
            log.error("Could not retrieve users for creating collaboration.Message from server : <%s>"% (ret.text))
        # parsing the returned content to get the act id
        for node in ret.json()["data"]:
            if node["FullName"] == user_fullname:
                profile_id = node["ProfileId"]
                break
        return profile_id

    def get_cosmo_conference_detail_handler(self, act_id, profile_id):
        '''
        This function will get the service id based on profile id

        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        service_id = None
        params = self.config.getparams("get_cosmo_conference_detail_handler")
        params["accountId"] = int(self.accountId)
        url = params.pop("url")
        log.info("Getting the service ids with args <%s>" % params)
        ret = requests.get(url, data = params, headers = self.headers)
        if ret.status_code == 200 and "ProfileId" in ret.text:
            log.info("The service ids have been retrieved successfully.Message from server : <%s>"% (ret.text))
        else:
            log.error("Could not retrieve the service ids.Message from server : <%s>"% (ret.text))
        # parsing the returned content to get the act id
        for node in ret.json()["data"]:
            if node["ProfileId"] == int(profile_id):
                service_id = node["ServiceId"]
                break
        return service_id

    def create_cosmo_conference(self, dm_name, user_fullname, **params):
        '''
        This function will create a cosmo conference
        phone system -> add on --> collaboration --> manage --> Add
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        params_xml = self.config.getparams("create_cosmo_conference")
        params = self.get_param_to_use(params_xml, **params)
        params["accountId"] = int(self.accountId)
        params["RequestedBy"] = self.get_dm_detail(self.accountId, dm_name)
        profile_id = self.create_cosmo_conference_handler(user_fullname)
        params["id_%s"%profile_id] = profile_id
        url = params.pop("url")
        log.info("Creating collaboration with args <%s>" % params)
        ret = requests.post(url, data = params, headers = self.headers)
        if ret.status_code == 200 and ret.json().has_key("message"):
            log.info("The conference has been created.Message from server : <%s>"% (ret.text))
            result = True
        else:
            log.error("Could not create the conference.Message from server : <%s>"% (ret.text))

        return result, ret

    def delete_cosmo_conference(self, dm_name, part_name, user_name, **params):
        '''
        This function will delete a cosmo conference
        phone system -> add on --> collaboration --> rt click on the created conference
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        params_xml = self.config.getparams("delete_cosmo_conference")
        params = self.get_param_to_use(params_xml, **params)
        params["accountId"] = int(self.accountId)
        params["serviceIds"] = self.get_cosmo_conference_detail_handler(self.accountId,
                            self.get_profile_detail(self.accountId, part_name, user_name))
        params["requestedById"] = self.get_dm_detail(self.accountId, dm_name)
        params["billCeaseDate"] = datetime.date.today().strftime("%m/%d/%Y")
        url = params.pop("url")
        log.info("Deleting collaboration with args <%s>" % params)
        ret = requests.post(url, data = params, headers = self.headers)
        if ret.status_code == 200 and ret.json().has_key("message"):
            log.info("The conference has been deleted successfully.Message from server : <%s>"% (ret.text))
            result = True
        else:
            log.error("Could not delete the conference.Message from server : <%s>"% (ret.text))

        return result, ret

    def add_account_codes(self, **params):
        '''
        This function will create a account codes
        phone system -> add on --> Account Codes --> Add
        '''
        result = False
        params_xml = self.config.getparams("add_account_codes")
        params = self.get_param_to_use(params_xml, **params)
        params["accountId"] = int(self.accountId)
        params["partitionId"] = self.get_partition_detail(self.accountId, params["part_name"])
        new_Values = '{"PartitionId":"%s","Id":"-1","BillingCode":"%s","Description":"%s"}' %(params["partitionId"] , params["ac_BillingCode"], params["ac_description"])
        params["newValues"] = (new_Values)
        url = params.pop("url")
        log.info("Creating account codes with args <%s>" % params)
        ret = requests.post(url, data = params, headers = self.headers)
        if ret.status_code == 200 and ret.json().has_key("BillingCode"):
            log.info("The account codes has been created.Message from server : <%s>"% (ret.text))
            self.account_code_id= ret.json()["Id"]
            result = True
        else:
             log.error("Could not create the Account codes.Message from server : <%s>"% (ret.text))
        return result, ret


    def delete_account_codes(self,**params):
        '''
        This function will delete a account codes
        phone system -> add on --> Account Codes --> delete
        '''
        result = False
        params_xml = self.config.getparams("delete_account_codes")
        params = self.get_param_to_use(params_xml, **params)
        new_Values = '{"PartitionId":%s,"BillingCode":"%s","Description":"%s","Id":"%s"}' %(self.get_partition_detail(self.accountId, params["part_name"]) , params["ac_BillingCode"], params["ac_description"],self.account_code_id)
        params["newValues"] = (new_Values)
        url = params.pop("url")
        log.info("Creating account codes with args <%s>" % params)
        ret = requests.post(url, data = params, headers = self.headers)
        if ret.status_code == 200 and ret.json().has_key("BillingCode"):
            log.info("The account codes has been deleted.Message from server : <%s>"% (ret.text))
            result = True
        else:
             log.error("Could not delete the Account codes.Message from server : <%s>"% (ret.text))
        return result, ret

    def add_phone(self,**params):
        '''
        This function will add a phone with given mac
        phone system -> phones --> add phone

        To add a phone anonymous, simply dont pass any value to user_email
        '''
        result = False
        params_xml = self.config.getparams("add_phone")
        params = self.get_param_to_use(params_xml, **params)
        params['accountId'] = self.accountId
        if self.part_id is None:
            if "part_name" in params.keys():
                part_id = self.get_partition_detail(self.accountId, params['part_name'])
            else:
                log.error("Partition name not provided")
        else:
            part_id = self.part_id
        params['Phone_Location_Id'] = self.get_location_id(self.accountId, params['location_name'])
        params['Phone_MacAddress'] = params['mac_address']
        if 'user_email' in params.keys():
            params['SelectedProfileId'] = self.get_profile_detail(self.accountId, params['part_name'], params['user_email'])
        params['partitionId'] = self.part_id
        url = params.pop("url")
        log.info("Adding phone with args <%s>" % params)
        ret = requests.post(url, data = params, headers = self.headers)
        if ret.status_code == 200 and ret.json().has_key("message"):
            log.info("The phohe has been added successfully.Message from server : <%s>"% (ret.text))
            result = True
        else:
             log.error("Could not add the phone.Message from server : <%s>"% (ret.text))
        return result, ret

    def modify_user_telephony_attributes(self,user_extension, **kwargs):
        """
        to modify the telephony related values for a user
        Users->users->Select user->Telephony Tab(below)-> CallStackDepth,Ring Type, Wallpaper etc.
        :param user_extension: fully qualified extension for the user
        :param kwargs: a dictionary with the values to change e.g.
        to change call depth use "call_stack_depth"
        :return: same as the return of put_user_json method
        """
        result = False
        params_xml = self.config.getparams("add_phone")
        params = self.get_param_to_use(params_xml, **params)
        params['accountId'] = self.accountId
        if self.part_id is None:
            if "part_name" in params.keys():
                part_id = self.get_partition_detail(self.accountId, params['part_name'])
            else:
                log.error("Partition name not provided")
        else:
            part_id = self.part_id

    def create_bca(self,**kwargs):
        """
        to create or modify BCA values for a user
        PhoneSystem->BCA
        :param user_extension: fully qualified extension for the user
        :param kwargs: a dictionary with the values to change
        :return:
        """
        result = False

        if not (kwargs.get('location_name') and kwargs.get('outboundCallerId')):
            print(("Location and outboundCallerId are mandatory parameters"))
            return False

        result,availableExt = self.check_extension_availability(extension='',part_name='')
        if not result:
            return False
        result,acTN,acCountryID = self.get_tn_country(str(kwargs.get('outboundCallerId')))
        if not result:
            return False
        params_xml = self.config.getparams("create_bca")
        params = self.get_param_to_use(params_xml, **kwargs)
        params['accountId'] = self.accountId
        if self.part_id is None:
            if "part_name" in params.keys():
                part_id = self.get_partition_detail(self.accountId, params['part_name'])
            else:
                log.error("Partition name not provided")
        else:
            part_id = self.part_id
        params["partitionId"] = self.part_id
        options = {}
        options["profileName"]= kwargs.get("profileName","Created By BOSS API ")
        options["location"] = str(self.get_location_id(self.accountId, kwargs.get("location_name")))
        options["outboundCallerIds"] = str(acTN).replace("(","").replace(")","").replace("-","").replace(" ","")+","+acCountryID+","+str(options["location"])+",5,1,0"
        options["extension"] = availableExt.json()
        getPhoneOption = {"dont_assign_number":"2","choose_from_all_location":"0", "choose_from_selected_location":"1"}
        options["assignPhoneNumber"] = getPhoneOption[kwargs.get("phoneNumberLocation","dont_assign_number")]
        if options["assignPhoneNumber"] != "2":
            if not kwargs.get('phone_number'):
                print("phone_number should be passed when type selected as Choose From all locations / Choose from selected location")
                return False
            result,acTN,acCountryID = self.get_tn_country(str(kwargs.get('phone_number')))
            if not result:
                return False
            options["phoneNumber"] = str(acTN).replace("(","").replace(")","").replace("-","").replace(" ","")+","+acCountryID+","+str(options["location"])+",4,1,0"
        else:
            options["phoneNumber"]="Select phone number ..."
        options["includeSystemDirectory"] = kwargs.get("includeSystemDirectory",True)
        options["includeOnPhoneDirectory"]=True
        options["CFBusy"] = kwargs.get("CFBusy","8")
        options["extension_cfbusy"] = kwargs.get("cfBusyExtension","")
        options["CFNoAnswer"] = kwargs.get("CFNoAnswer","4")
        options["extension_cfnoanswer"] = kwargs.get("cfNoAnswerExtension", "")
        confOptions = {"disable_conferencing":"0","enable_others_may_join":"2", "enable_others_may_not_join":"1"}
        options["conferencingOptions"] = confOptions[kwargs.get("conferencingOptions","disable_conferencing")]
        options["enableTone"] = kwargs.get("enableTone",False)
        options["isBCA"]=True
        options["bcaProfileId"]="-1"
        options["associatedProfileId"]="-1"
        params["values"] = json.dumps(options)
        url = params.pop("url")
        ret = requests.post(url, data = params, headers = self.headers)
        if ret.status_code == 200:
            return options["extension"]
        else:
            return False

    def delete_bca(self,**params):
        '''
        This function will delete a bca profiles
        phone system -> Bridge Call Appearance.
        '''
        result = False
        params_xml = self.config.getparams("get_bca_list")
        params = self.get_param_to_use(params_xml, **params)
        params['accountId'] = self.accountId
        params['partitionId']= self.part_id
        url = params.pop("url")
        ret = requests.get(url, params = params, headers = self.headers)
        profID = ""
        for extens in ret.json()['data']:
            if str(extens['Extension']) == str(params.get('extension')):
                profID = str(extens['ProfileId'])
                break
        if not profID:
            print("BCA Extension not found in the system")
            return False
        params_xml = self.config.getparams("delete_bca")
        params = self.get_param_to_use(params_xml, **params)
        params['accountId'] = self.accountId
        params['partitionId']= self.part_id
        params['bcaProfileId'] = profID
        url = params.pop("url")
        ret = requests.post(url, params = params, headers = self.headers)
        if ret.status_code == 200:
            log.info("The BCA profile has been deleted.Message from server : <%s>"% (ret.text))
            result = True
        else:
             log.error("Could not delete BCA profile.Message from server : <%s>"% (ret.text))
        return result, ret

    def edit_bca(self, **kwargs):
        '''
            This function will edit an already created BCA
            phone system -> BCA --> edit
            Examples for argument given as comment next to each item.
        '''
        result = False
        params_xml = self.config.getparams("edit_BCA")
        params = self.get_param_to_use(params_xml, **kwargs)
        params['accountId'] = self.accountId
        if self.part_id in [None, '1']:
            if "part_name" in params.keys():
                params['partitionId'] = self.get_partition_detail(self.accountId, params['part_name'])
            else:
                log.error("Partition name not provided")
        else:
            params['partitionId'] = self.part_id
        # getting BCA details
        bca_id = self.get_bca_profile_id(kwargs["bca_extension"], params['accountId'], params['locationId'], params['partitionId'])

        url_bca_details = params.pop("url_bca_details")
        params["isBca"] = False
        params["isCopy"] = False
        params["isPB"] = False
        params["profileId"] = bca_id

        ret = requests.get(url_bca_details, params=params, headers=self.headers)

        log.info("Editing the BCA with args <%s>" % params)
        options = {}
        confOptions = {"disable_conferencing": "0", "enable_others_may_join": "2", "enable_others_may_not_join": "1"}
        options["conferencingOptions"] = confOptions[kwargs.get("conferencingOption", "disable_conferencing")]
        options["editing"] = True
        options["bcaProfileId"] = bca_id
        options["isbca"] = False
        options["extension"] = kwargs["bca_extension"]
        options["profileName"] = kwargs.get("profileName", re.findall(r'<input id="profileName" [\d\D]+? value="([\d\D]+?)" />', ret.text)[0])
        options["assignPhoneNumber"] = "2"
        options["phoneNumber"] = "Select phone number ..."
        caller_ids = re.findall(r'currentOutboundCallerIdValue = "([\d,]+)";', ret.text)[0]
        location = caller_ids.split(',')[2]
        outboundCallerIds = "%s,%s,%s,%s"%(caller_ids, 5, 1, 0) # looks like the last 3 item will not change so leaving them as is for now
        options["outboundCallerIds"] = kwargs.get(outboundCallerIds, re.findall(r'currentOutboundCallerIdValue = "([\d,]+)";', ret.text)[0])#"4088007152,840,14,5,1,0"
        options["location"] = location
        options["includeSystemDirectory"] = True
        options["includeOnPhoneDirectory"] = True
        options["CFBusy"] = kwargs.get("CFBusy", re.findall(r'<option selected="selected" value="(\d+)">\d+ calls', ret.text)[0])#"8"
        options["extension_cfbusy"] = kwargs.get("extension_cfnoanswer", re.findall(r'<input id="extension_cfnoanswer" [\d\D]+? value="([\d\D]+?)" />', ret.text)[0])#"4101 : Voice Mail"
        options["CFNoAnswer"] = kwargs.get("CFNoAnswer", re.findall(r'<option selected="selected" value="(\d)">\d+ rings', ret.text)[0])#"3"
        options["extension_cfnoanswer"] = kwargs.get("extension_cfnoanswer", re.findall(r'<input id="extension_cfnoanswer" [\d\D]+? value="([\d\D]+?)" />', ret.text)[0])#"4101 : Voice Mail"#"4101 : Voice Mail"
        options["enableTone"] = False
        options["associatedProfileId"] = kwargs.get("associatedProfileId", re.findall(r'<option selected="selected" value="(\d\d\d\d\d\d+)">', ret.text)[0])#"9619"
        options["test_value"] = 1

        url = params.pop("url")
        params["values"] = json.dumps(options)
        ret = requests.post(url, data=params, headers=self.headers)
        if ret.status_code == 200 and ret.json().has_key("message"):
            log.info("The BCA has been edited successfully.Message from server : <%s>" % (ret.text))
            result = True
        else:
            log.error("Could not edit the BCA.Message from server : <%s>" % (ret.text))
        return result, ret


    def configure_moh(self,**params):
        '''
        This function will set MOH in phone system -> on hold music
        params : moh_name
        '''

        ur = r'https://portal.sit.shoretel.com/PartitionHoldMusic/Index?accountId=16370&locationId=-1&profileId=-1&personId=999693&partitionId=13398'
        ret = requests.get(ur, headers = self.headers)

        result = False
        params_xml = self.config.getparams("get_moh_options")
        params = self.get_param_to_use(params_xml, **params)
        params['accountId'] = self.accountId
        params['partitionId']= self.part_id
        params['personId']= self.personID
        url = params.pop("url")
        moh_options = requests.get(url,params=params ,headers = self.headers)
        select_options = re.split("\"data\":{",str(moh_options.content))[1].split("},")[0] # reads ajax selection options from html content
        select_options =  json.loads("{" + select_options.replace('\'','\"') +"}") # Converts to dic
        data={}
        data['id'] = 'musicId'
        if params.get('moh_name'):
            for key,values in select_options.items():
                if str(params.get('moh_name')).lower() == str(values).lower():
                    data['value'] = str(key)
                    break
        else:
            print("parameter moh_name is mandatory")
            return False
        if not data.get('value'):
            print("moh name not found in system")
            return False
        #json.loads("{"+(re.split("\"data\":{",str(ret.content))[1].split("},")[0]).replace('\'','\"')+"}")
        params_xml = self.config.getparams("configure_moh")
        params = self.get_param_to_use(params_xml, **params)
        params['accountId'] = self.accountId
        params['partitionId']= self.part_id
        url = params.pop("url")
        ret = requests.post(url, params = params,data=data, headers = self.headers)
        if ret.status_code == 200:
            log.info("MOH settings has been updated.Message from server : <%s>"% (ret.text))
            result = True
        else:
             log.error("Could not update MOH settings.Message from server : <%s>"% (ret.text))
        return result, ret


    def edit_user(self,**params):
        '''
        This function will edit  a existing user with the given details.
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''

        if not params.get('extensionToBeProgrammed'):
            print("Parameter 'extensionToBeProgrammed' is mandatory ")
            return False
        result = False
        data = {}
        # Identification and Privacy
        if params.get("OutboundCallerID"):
            data['id'] = "externalCallerId"
            data['value'] =params.get("OutboundCallerID")
            params_xml = self.config.getparams("update_user_phone_settings")
        elif "isInDirectory" in params.keys():
            data['id'] = "isInDirectory"
            data['value'] =params.get("isInDirectory")
            params_xml = self.config.getparams("update_user_phone_settings")
        elif "isBlockCallerId" in params.keys():
            data['id'] = "isBlockCallerId"
            data['value'] =params.get("isBlockCallerId")
            if params.get("isBlockCallerId"):
                data['value'] ="yes"
            else:
                data['value'] ="no"
            params_xml = self.config.getparams("update_user_phone_settings")
        elif "makeExtensionPrivate" in params.keys():
            data['id'] = "makeExtensionPrivate"
            if params.get("makeExtensionPrivate"):
                data['value'] ="yes"
            else:
                data['value'] ="no"
            params_xml = self.config.getparams("update_user_phone_settings")
        elif "TimeFormat" in params.keys(): # 0/1
            data['id'] = "timeFormat"
            data['value'] =params.get("TimeFormat")
            params_xml = self.config.getparams("update_user_phone_settings")
        # Features
        elif "HasCallWaitingBeep" in params.keys():
            data['id'] = "HasCallWaitingBeep"
            if params.get("HasCallWaitingBeep"):
                data['value'] ="true"
            else:
                data['value'] ="false"
            params_xml = self.config.getparams("update_user_phone_features")

        elif "VideoEnabled" in params.keys():
            data['id'] = "VideoEnabled"
            data['value'] =str(params.get("VideoEnabled")).lower()
            params_xml = self.config.getparams("update_user_phone_features")

        elif "UserGroup" in params.keys():
            data['id'] = "UserGroup"
            data['value'] =self.get_usergroup_detail(self.accountId,params["UserGroup"])
            params_xml = self.config.getparams("update_user_phone_features")

        elif "OperatorAccess" in params.keys():
            data['id'] = "OperatorAccess"
            data['value'] =str(params.get("OperatorAccess")).lower()
            # if str(params["OperatorAccess"]).lower() == "enabled":
            #     data['value'] = 'true'
            # else:
            #     data['value'] = 'false'
            params_xml = self.config.getparams("update_user_phone_features")

        elif "RingdownEnabled" in params.keys():
            data['id'] = "RingdownEnabled"
            data['value'] =str(params.get("RingdownEnabled")).lower()
            params_xml = self.config.getparams("update_user_phone_features")

        elif "RingdownDelay" in params.keys():
            data['id'] = "RingdownDelay"
            data['value'] =str(params.get("RingdownDelay")).lower()
            params_xml = self.config.getparams("update_user_phone_features")

        elif "SCA" in params.keys():
            data['id'] = "SCAEnabled"
            if params.get("SCA"):
                data['value'] ="true"
                res, availableExt = self.check_extension_availability(extension='',part_name='')
                if not res:
                    print("Failed to get next available extension")
                    return False
                data['extension'] = availableExt.json()
            else:
                data['value'] = "false"
                if not params.get("sca_extension", None):
                    print("WARN : Mandatory argument <sca_extension> missing")
                    print("Trying to fetch internally")
                    url_get_sca_extn = self.config.getparams("get_programmed_sca_extension")["url"]
                    params_xml = self.config.getparams("update_user_phone_features")
                    paramsToSend = self.get_param_to_use(params_xml, **params)
                    paramsToSend["accountId"] = self.accountId
                    paramsToSend['part_name'] = self.part_id
                    paramsToSend["profileId"] = self.get_profile_detail(self.accountId, paramsToSend['part_name'], "",extension=params.get('extensionToBeProgrammed'))
                    r = requests.get(url_get_sca_extn, params=paramsToSend,data=data, headers=self.headers)
                    extn = re.search(r'id="SCAExtensionLabel">(\d+)</label>', r.text).group(1)
                    data['extension'] = extn
                    print("SCA Extension fetched is <%s> for user <%s>"%(extn, params["extensionToBeProgrammed"]))
                else:
                    data['extension'] = params["sca_extension"]
            params_xml = self.config.getparams("update_user_phone_features")

        # log.info("Editing a user with args <%s>" % params)
        paramsToSend = self.get_param_to_use(params_xml, **params)
        url = paramsToSend.pop("url")
        paramsToSend["accountId"] = self.accountId
        paramsToSend['part_name'] = self.part_id
        paramsToSend["profileId"] = self.get_profile_detail(self.accountId, paramsToSend['part_name'],"",extension=params.get('extensionToBeProgrammed'))

        ret = requests.post(url, params=paramsToSend,data=data, headers=self.headers)
        if ret.status_code == 200 and str(data['value']) in str(ret.text)[:20]:
            log.info("Successfully programmed extension number <%s>.\nMessage from server : <%s>" % (
            params.get('extensionToBeProgrammed'), ret.text))
            result = [True, data.get("extension",None)] if data.get("extension", None) else True
        else:
            log.error("Failed to programme extension number  <%s>.\nMessage from server : <%s>" % (
            params.get('extensionToBeProgrammed'), ret.text))
        return result, ret

    def edit_user_call_routing(self,**params):

        if not params.get('extensionToBeProgrammed'):
            print("Parameter 'extensionToBeProgrammed' is mandatory ")
            return False
        result = False
        data = {}
        data["DnFollowDestination"]={}
        data["DnFollowDestination"]["id"]=""
        params_xml = self.config.getparams("update_user_phone_call_routing")
        params = self.get_param_to_use(params_xml, **params)
        self.headers['Content-Type'] = "application/json"
        url = params.pop("url")
        params["accountId"] = self.accountId
        params["part_name"]= self.part_id
        params["profileId"] = self.get_profile_detail(self.accountId, params['part_name'],"",extension=params.get('extensionToBeProgrammed'))
        all_phones = self.get_all_users(self.accountId)
        for phs in all_phones['data']:
            if str(phs['TnId']).split('-')[1] == str(params.get('extensionToBeProgrammed')):
                data["DnFollowDestination"]["id"]= phs['CurrentExtension']
        if not data["DnFollowDestination"]["id"]:
            print("Failed to find the extension in the system")
            return False
        # Parameters
        data["DnFollowDestination"]["RingAllPhoneTypeID1"] = params.get('SimultaneousRing1',0)
        data["DnFollowDestination"]["RingAllPhoneTypeID2"] = params.get('SimultaneousRing2',0)
        data["DnFollowDestination"]["FindMePhoneTypeID1"] = params.get('FindMePhone1',0)
        data["DnFollowDestination"]["FindMePhoneTypeID2"] = params.get('FindMePhone2',0)        #
        data["DnFollowDestination"]["SendCallerID"] = params.get('SendIncomingCallerID',False)
        data["DnFollowDestination"]["IsRecCallerName"] = params.get('PromtCallerToRecordThierName',False)
        data["DnFollowDestination"]["PSTNAnyphonePhoneTypeID"] = None
        data["DnFollowDestination"]["RecIfCallIDPresent"] =   False     #
        data["DnFollowDestination"]["UseAutoFindMe"] = params.get('RingMyFindMeNumbers',False)
        data["MobilityPhoneNumber"] =""
        numOfPhones = 0

        if params.get('PhonesNumbers'):
            data["UserPhones"]={}
            for phones in params.get('PhonesNumbers'):
                numOfPhones +=1
                data["UserPhones"][str(numOfPhones)]= {}
                if phones.get('destroy'):
                    dummy={}
                    _id = ""
                    dummy["DnFollowDestination"]={}
                    dummy["DnFollowDestination"]["id"] = data["DnFollowDestination"]["id"]
                    dummyResp = requests.post(url, data=json.dumps(dummy),params=params, headers=self.headers).json()
                    for uPhones in dummyResp['UserPhones']:
                        _id = uPhones
                        if str(dummyResp['UserPhones'][uPhones]['Label']).lower() == str(phones.get('Label')).lower():
                            data["UserPhones"][str(numOfPhones)]["UserPhoneTypeID"]=dummyResp['UserPhones'][uPhones]['UserPhoneTypeID']
                    if not data["UserPhones"][str(numOfPhones)].get("UserPhoneTypeID"):
                        print("Phone Label not found in the system ")
                        return False
                    data["UserPhones"][str(numOfPhones)]["Label"]= ""
                    data["UserPhones"][str(numOfPhones)]["Number"]= ""
                    data["UserPhones"][str(numOfPhones)]["_destroy"]=True
                    data["UserPhones"][str(numOfPhones)]["id"]= str(data["DnFollowDestination"]['id'] + "," + _id)
                else:
                    data["UserPhones"][str(numOfPhones)]["Label"]= phones.get('Label')
                    data["UserPhones"][str(numOfPhones)]["Number"]= phones.get('Number')
                    data["UserPhones"][str(numOfPhones)]["NoAnswerRings"]= phones.get('NoAnswerRings')
                    data["UserPhones"][str(numOfPhones)]["UserPhoneTypeID"] =numOfPhones+1

        ret = requests.post(url, data=json.dumps(data),params=params, headers=self.headers)
        # changing the content type back to default for further calls
        self.headers['Content-Type'] = "application/x-www-form-urlencoded"
        if ret.status_code == 200:# and str(data['value']) in str(ret.text)[:20]:
            log.info("Successfully programmed extension number <%s>.\nMessage from server : <%s>" % (
            params.get('extensionToBeProgrammed'), ret.text))
            result = True
        else:
            log.error("Failed to programme extension number  <%s>.\nMessage from server : <%s>" % (
            params.get('extensionToBeProgrammed'), ret.text))
            result = False
        return result, ret

if __name__ == "__main__":
    # almost all the methods have been modified to accept all the params as keyword args
    # so to call those functions as shown below, the params must be passed as keyword args
    logging.basicConfig(level=logging.DEBUG)
    import sys
    sys.path.append(r"C:\Users\nkumar\Downloads\Framework_UC")
    obj = boss_api()
    # obj.loginToBossCloud()
    # obj = boss_api("17.9.10.454")
    print(obj.login(url = "http://portal.sit.shoretel.com/",UserName="derek@mitel-test.com",Password="Mitel@1234"))
    obj.edit_bca(bca_extension='1026', conferencingOption="disable_conferencing")
    # obj.login(url = "http://10.196.7.182/UserAccount/LogOn",UserName="ptstaff@shoretel.com",Password="Shoreadmin2#")
    # print(obj.create_pickup_group(location_name="Austin",pkg_name="TODelete4",pkg_extensionlist="oo"))
    # obj.delete_pickup_group("", Extension="1029") # extension number / name can be used for deleting pickup group.
    # ENTA-3794
    # print(obj.edit_user_call_routing(extensionToBeProgrammed="1005", PhonesNumbers=[{"Label":"H2AI","Number": "1003","NoAnswerRings":3},{"Label":"H2AI2","Number": "1004","NoAnswerRings":3}]))
    # print(obj.edit_user_call_routing(extensionToBeProgrammed="1005",SimultaneousRing1=2,SimultaneousRing2=3 )  #0 is for 'Select Number', 2 for First option)
    # print(obj.edit_user_call_routing(extensionToBeProgrammed="1005",FindMePhone1=2,FindMePhone2=3 )  #0 is for 'Select Number', 2 for First option)
    # print(obj.edit_user_call_routing(extensionToBeProgrammed="1005", SendIncomingCallerID=False, PromtCallerToRecordThierName=False,RingMyFindMeNumbers=False))
    # print(obj.edit_user_call_routing(extensionToBeProgrammed="1005", PhonesNumbers=[{"destroy":True, "Label":"H2AI"}]))

    # Below configurations are done one by one since these all are ajax calls and please do not pass all args together.
    # print(obj.edit_user(extensionToBeProgrammed="1008",SCA=False))
    # print(obj.edit_user(extensionToBeProgrammed="7152", SCA=False, sca_extension="1009"))
    # print(obj.edit_user(extensionToBeProgrammed="1005",OutboundCallerID="15124991005"))
    # print(obj.edit_user(extensionToBeProgrammed="1005",isInDirectory=False) # Revisit)
    # print(obj.edit_user(extensionToBeProgrammed="1005",isBlockCallerId=False) # Revisit)
    # print(obj.edit_user(extensionToBeProgrammed="1005",makeExtensionPrivate=False))
    # print(obj.edit_user(extensionToBeProgrammed="1005",TimeFormat=1))
    # print(obj.edit_user(extensionToBeProgrammed="1005",HasCallWaitingBeep=True))
    # print(obj.edit_user(extensionToBeProgrammed="1005",VideoEnabled=False))
    # print(obj.edit_user(extensionToBeProgrammed="1005",UserGroup="TEST"))
    # print(obj.edit_user(extensionToBeProgrammed="1005",OperatorAccess=False))
    # print(obj.edit_user(extensionToBeProgrammed="1005",RingdownEnabled=True))
    # print(obj.edit_user(extensionToBeProgrammed="1005",RingdownDelay=10))


    # obj.update_usergroup(ug_name='TEST',ClassofService=1)
    # obj.configure_moh(moh_name="kkk")
    # obj.delete_extension_list(el_to_delete='DELETE1')
    # obj.delete_hunt_group(hg_to_delete="",extension="1023")
    # print(obj.create_pickup_group(location_name="Austin",pkg_name="TEST2334332",pkg_extensionlist="oo"))
    # obj.delete_bca(extension='1029')

    # obj.configure_prog_button(extensionToBeProgrammed="1002", button_box=0,soft_key=5,function="Send Digits Over Call",label="Extn2222",dtmf_digits="99999")

    #ENTA-3290

    # obj.configure_prog_button(extensionToBeProgrammed="1003",extension='1001', button_box=0,soft_key=4,function="Monitor Extension",label="Extn2222",ring_delay="2",show_caller_id="only_when_ringing",no_connected="unused",with_connected="transfer_whisper")
    # obj.configure_prog_button(user_email="auto1001@mitel-test.com",button_box=0,soft_key=4,function="Monitor Extension",label="Extn22",extension="1001",ring_delay="2",show_caller_id="only_when_ringing",no_connected="unused",with_connected="transfer_whisper")
    
    #ENTA 5019
    # obj.configure_prog_button(account_name='MT_PTA_ACC1', part_name='PTA', user_email="auto18.uc18@mitel.com",
    #                           button_box=0, soft_key=2, function="Hotline", label="MyBridge",extension="7153", call_action="Intercom")

    # obj.configure_prog_button(account_name='Derek-PIT-Automation1', part_name='PIT', user_email="auto1007@mitel-test.com",
    #                           button_box=0, soft_key=2, function="Hotline", label="NNMyBridge", extension="1008",
    #                           call_action="Intercom")

    # obj.configure_prog_button(extensionToBeProgrammed='1007',
    #                           button_box=0, soft_key=2, function="Hotline", label="NNMyBridge", extension="1008",
    #                           call_action="intercom")

    # obj.configure_prog_button(extensionToBeProgrammed='1007',
    #                           button_box=0, soft_key=2, function="TRANSFER TO WHISPER", label="ZZZZMyBridge", extension="1008",
    #                           )

    # obj.configure_prog_button(extensionToBeProgrammed='1007', button_box=0, soft_key=5, function="UNUSED")
    # obj.configure_prog_button(extensionToBeProgrammed='1007', button_box=0, soft_key=5, function="Change Availability", label="hellonitin", availability="do Not DisTurb")
    # print obj.configure_prog_button(extensionToBeProgrammed='1007',button_box=0, soft_key=2, function="Silent Coach",
    #                     label="Silenttt",extension="")
    #obj.update_person_details("homePhone", "7259234",extensionToBeProgrammed='1007')


    # for _ in range(25):
    # obj.configure_prog_button(extensionToBeProgrammed="1008", extension='1007', button_box=0, soft_key=1,
    #                               function="Monitor Extension", label="Extn222265", ring_delay="none",
    #                               show_caller_id="always", no_connected="unused",
    #                               with_connected="transfer_Whisper")

    # obj.clear_prog_button(account_name='Derek-PIT-Automation1', part_name='PIT', user_email="auto1008@mitel-test.com", button_box=0,
    #                           soft_key=1)
    #     print("SUCCESS*")
    # obj.clear_prog_button(extensionToBeProgrammed='1003',
    #                       button_box=0,
    #                           soft_key=4)

    # print(obj.create_hunt_group(hg_name="Try4",hg_backup_extn="1001",HuntGroupMember=['1001','1002'], IncludeInSystemDialByNameDirectory=False,HuntPatternID=4 , RingsPerMember=2,NoAnswerRings=4, CallMemberWhenForwarding=True,SkipMemberIfAlreadyOnCall=True) # //HuntPatternID: 1 for Top-down / 4for Simultaneous //)
    # print(obj.edit_hunt_group(hg_to_edit="Changed", hg_name="Changed2", hg_extension='1024', hg_backup_extn="1001",NoAnswerRings=3))
    # obj.edit_hunt_group(hg_to_edit="EDITED2",hg_name="EDITED3", hg_extension='1115', hg_backup_extn="1001",HuntGroupMember=[],IncludeInSystemDialByNameDirectory=False,HuntPatternID=1 , RingsPerMember=2,NoAnswerRings=5, CallMemberWhenForwarding=False,SkipMemberIfAlreadyOnCall=False) # //HuntPatternID: 1 for Top-down / 4for Simultaneous //)
    # obj.create_extension_list(el_name="el1334354", el_extns=['1001','1002'])

    # print(obj.create_paging_group(location_name="Austin", pg_name="Corrected", pg_extn_list="oo",)
    #                         PriorityPage=False,PriorityPageAudioPath=2,NoAnswerRings=4,PagingDelay=5, IncludeInDialByName=False)

    # print(obj.delete_paging_group(pg_to_delete="", location_name='Austin',extension="1020") # PG can be deleted either with Name or extension, if extension is provided, name parameter is not mandatory)
    # print(obj.delete_paging_group(pg_to_delete="pg_to_delete", location_name='Austin'))

    # print(obj.create_bca(profileName ="NEW BCA", location_name="Austin",phoneNumberLocation="dont_assign_number",outboundCallerId='1027'))
    # print(obj.create_bca(profileName ="NEW BCA", location_name="Austin",phoneNumberLocation="choose_from_all_location",CFNoAnswer=2,CFBusy=2,outboundCallerId='1027',cfNoAnswerExtension='1004',cfBusyExtension='1003',phone_number='1025'))
    # print(obj.create_bca(profileName ="NEW BCA", location_name="Austin",phoneNumberLocation="chose_from_all_location",conferencingOptions='enable_others_may_join',outboundCallerId='1002',phone_number='1026'))
    # pass

    # obj.login(url = "http://10.196.7.182/UserAccount/LogOn",UserName="staff@shoretel.com",Password="Abc123!!")
    # obj.login(url = "http://10.32.6.67/UserAccount/LogOn",UserName="staff@shoretel.com",Password="Abc123!!")
    # new login
    # obj.login(url="http://10.198.105.68/UserAccount/LogOn", UserName="sandeep.rai@contractor.mitel.com", Password="$horetel#1")
    # obj.login(url="http://10.196.7.182/UserAccount/LogOn", UserName="staff@shoretel.com", Password="Abc123!!")
    # obj.login(url="http://portal.sit.shoretel.com/", UserName="derek@mitel-test.com", Password="Mitel@123")



    # obj.login(url="http://10.198.107.70/UserAccount/LogOn", UserName="staff@shoretel.com", Password="Abc123!!")
    # obj.login(url = "http://10.32.6.67/UserAccount/LogOn",UserName="staff@shoretel.com",Password="Abc123!!")
    # print(obj.get_account_detail(act_name="Derek-PIT-Automation1"))
    # obj.create_tenant(CompanyName="Barbara-TeamworkForWeb")
    # obj.switch_account(act_name="Test_Automation_Acc")
    # obj.switch_account(act_name="CONT_RKAPALE_2019MAR15_HQ1")
    # obj.switch_account(act_name="Not Scale")
    # obj.accountId = 11509
    # obj.get_partition_detail(obj.accountId, "HQ1")
    # obj.get_dm_detail("bosswebapi_4","qw@sh.com")
    # obj.add_tn(TnsString="+16462000507",act_name="bosswebapi_4",username="qw@sh.com")
    # obj.update_tn(tnstring="6462000457",Type="Real",State="Available")
    # print(obj.get_location_id("11509","location1"))
    # print(obj.get_location_id("11509","location1"))
    # print(obj.get_location_emergency_number("11509","location1"))
    # obj.get_partition_detail("11549","MTA")
    # obj.add_location_as_site("location1","MMA")
    # new user without profile
    # obj.add_user(part_name="MMA", Person_FirstName="nn1", Person_LastName="kk", Person_BusinessEmail="sh12sh1234@aaqsqqassh.com", loc_name="location1", SU_Email="srav@mi.in")
    # new user with profile
    # obj.add_user(part_name="HQ1",Person_FirstName="nn",Person_LastName="kk",Person_BusinessEmail="sh12@ddqsqqassh.com",loc_name="loc1",SU_Email="shi@sh.com",PhoneType="355",Person_Profile_Extension="1232")
    # obj.add_contract(company_name="bosswebapi_9",file_path="C:\\Users\\nkumar\\Downloads\\SampleContract_1.pdf")
    # obj.get_contract_detail('11618')
    # obj.update_billing_location("bosswebapi_7","location")
    # obj.add_instance_to_contract()
    # obj.validate_location(Address1="Nitin")
    # obj.upload_pdf("C:\\Users\\nkumar\\Downloads\\SampleContract.pdf")
    # obj.get_cluster_detail("MTA")
    # obj.create_partition("location")
    # obj.update_contract_status()
    # obj.get_person_detail("12187","HQ1","sh12@sh.com")
    # obj.change_password("MTA","qw22@sh.com")
    # obj.assign_role("MTA","qw22@sh.com", "Technical")
    # obj.unassign_role("MTA", "qw22@sh.com", "Technical")
    # obj.close_user("MTA", "qw222@sh.com", "Technical")
    # p = obj.get_profile_detail(obj.accountId,"HQ1","sh4@sh.com")
    # obj.get_usergroup_detail("11549","MTA","System VM Only Group")
    # obj.reassign_tn("MTA", "ff@sh.com",reassignExtension="1003")
    # obj.check_extension_availability("MTA","1013")
    # obj.add_tn_to_user(part_name="HQ1",Person_FirstName="abc3",Person_LastName="xyz",Person_BusinessEmail="sh12@bbqsqqassh.com",loc_name="loc1",SU_Email="shi@sh.com",Person_Profile_Extension="1025",Profile_TnId="+16462016017")
    # obj.check_usergroup_availability(part_name="MMA",ug_name="test1")
    # to create a user group with different profile id
    # obj.create_usergroup(part_name="HQ1",ug_name="ug4",ProfileTypeId=5)
    # obj.update_usergroup(part_name="HQ1", ug_name="ug4", ProfileTypeId=5,AllowOverheadPaging=True)
    # to create a user group with default profile id
    # obj.create_usergroup("HQ1","ug4")
    # obj.delete_usergroup("HQ1","ug3")
    # obj.check_username_availability("sh33@sh.com")
    # obj.validate_location_name("loc1")
    # obj.add_location("loc1","HQ1")
    # obj.get_suitable_invoice_groups("12033","bosswebapi_1")
    # obj.update_location("loc11","HQ1",Address_Address2="nitin")
    # obj.validate_canclose_location("loc")
    # obj.close_location("loc5","sh@sh.com")
    # obj.get_order_detail(obj.accountId,"loc11")
    # obj.update_order_details("11217")
    # obj.check_mac_address_availability("11:11:11:11:11:11:11:11")
    # obj.add_edit_phone("loc5","11:11:11:11:11:11")
    # obj.remove_phone_entry("11:11:11:11:11:12")
    # obj.add_profile("loc6", "sh@sh.com")
    # obj.validate_assign_profile("aabbb@sh.com")
    # obj.assign_number("+16462000507","1114","haha12@sh.com","loc22","sh@sh.com")
    # obj.unassign_number("aabb@sh.com","HQ1","sh@sh.com")
    # obj.update_cosmo_partition_dialplan()
    # obj.update_cosmo_conference("sh@sh.com")
    # obj.create_cosmo_conference_handler("abc xyz")
    # obj.create_cosmo_conference("sh@sh.com","abc xyz")
    # obj.get_cosmo_conference_detail_handler(obj.accountId,p)
    # obj.delete_cosmo_conference("sh@sh.com","HQ1","sh4@sh.com")
    # print(obj.verify_person_detail(obj.accountId, "HQ1", "sh4@sh.com", "1001"))
    # print(obj.verify_person_detail(obj.accountId, "HQ1", "sh4@sh.com", tn="16462000501"))
    # print(obj.verify_person_detail(obj.accountId, "HQ1", "sh4@sh.com", "1001","16462000501"))
    # print(obj.verify_person_detail(obj.accountId, "HQ1", "sh4@sh.com", "1002","16462000501"))
    # print(obj.verify_person_detail(obj.accountId, "HQ1", "sh4@sh.com", "1001", "16462000502"))
    # print(obj.verify_person_detail(obj.accountId, "HQ1", "sh4@sh.com", "1002"))
    # obj.get_cosmo_component("12187", 528)
    # obj.create_auto_attendant(account_name='bosswebapi_1', part_name='BAU', location_name='loc1', aa_name="aa1", aa_extension='1201')
    # obj.get_vcfe_detail('12187', 528, 'nitin')
    # obj.edit_auto_attendant("nitin2", account_name='bosswebapi_2', part_name='BAU', location_name='loc1', aa_name="nitin")
    # obj.delete_auto_attendant("aa1", account_name='bosswebapi_1', part_name='BAU', location_name='loc1')
    # obj.create_hunt_group(account_name='bosswebapi_1', part_name='BAU', location_name='loc1', hg_name="hg1", hg_extension='1114',hg_backup_extn="1001")
    # obj.edit_hunt_group(hg_to_edit="nitin3",account_name='bosswebapi_1', part_name='BAU', location_name='loc1', hg_name="nitin33", hg_extension='1115', hg_backup_extn="1001")
    # obj.delete_hunt_group(hg_to_delete="hg1", account_name='bosswebapi_1', part_name='BAU', location_name='loc1')
    # obj.create_extension_list(account_name='bosswebapi_1', part_name='BAU', location_name='loc1', el_name="el1", el_extns=['1001','1002'])
    # obj.edit_extension_list(el_to_edit="el221", account_name='bosswebapi_1', part_name='BAU', location_name='loc1', el_name="el2",el_extns=['1001'])
    # obj.delete_extension_list(el_to_delete="el1", account_name='bosswebapi_1', part_name='BAU', location_name='loc1')
    # obj.create_paging_group(account_name='bosswebapi_1', part_name='BAU', location_name='loc1', pg_name="pg2", pg_extn_list='el1', pg_extension='1004')
    # obj.edit_paging_group(pg_to_edit="pg22", account_name='bosswebapi_1', part_name='BAU', location_name='loc1', pg_name="pg222", pg_extn_list='el1', pg_extension='1004')
    # obj.delete_paging_group(pg_to_delete="pg222", account_name='bosswebapi_1', part_name='BAU', location_name='loc1')
    # prog a button for monitor extension
    # obj.configure_prog_button(account_name='Walmart Ecommerece', part_name='PTA',user_email="wcr6@mitel.com",button_box=0,soft_key=3,function="Monitor Extension",label="Extension",extension="7944",
    #                           ring_delay="2",show_caller_id="only_when_ringing",no_connected="unused",with_connected="transfer_whisper")
    # programming BCA : SCA is enabled on extn 7654 -> Got BCA extn 1006
    # obj.configure_prog_button(account_name='Derek-PIT-Automation1', part_name='PIT',user_email="auto1007@mitel-test.com",button_box=0,soft_key=3,function="BRIDGE CALL APPEARANCE",label="MyBridge",extension="1022",ring_delay="2",show_caller_id="only_when_ringing",
    #                           no_connected="intercom",with_connected="unused",CallStackPosition=1,allow_auto_answer=1,bca_not_connected_call_acton=2)
    # obj.configure_prog_button(extensionToBeProgrammed='1007', button_box=0, soft_key=3,
    #                           function="BRIDGE CALL APPEARANCE", label="MyBridge", extension="1022", ring_delay="2",
    #                           show_caller_id="only_when_ringing",
    #                           no_connected="intercom", with_connected="unused", CallStackPosition=1,
    #                           allow_auto_answer=1, bca_not_connected_call_acton=2)
    # obj.configure_prog_button(account_name='Automation New', part_name='BAU',user_email="auser1@shoretel.com",button_box=0,soft_key=2,function="Silent Monitor",label="moni",extension="4002")
    # obj.configure_prog_button(account_name='Not Scale', part_name='SC1',user_email="scaleuser4098@mitel.com",button_box=0,soft_key=1,function="Silent Monitor",label="nitin",extension="4108")
    # obj.configure_prog_button(account_name='Derek-PIT-Automation1', part_name='User 1000',user_email="auto1000@mitel-test.com",button_box=0,soft_key=1,function="Silent Monitor",label="nitin",extension="1003")

    # obj.clear_prog_button(account_name='MT_PTA_ACC1', part_name='PTA',user_email="n6926user6@mitel.com",button_box=0,soft_key=3)
    # with a user
    # obj.add_phone(account_name='Test_Automation_Acc', part_name='MMA',user_email="tuser1@mitel.com",mac_address="13:12:12:12:45:45",location_name="location1")
    # without a user i.e. anonymous
    # obj.add_phone(account_name='Test_Automation_Acc', part_name='MMA',mac_address="13:12:12:12:45:45",location_name="location1")


    #  Pending things to do! 13-12-2019
    #     1. Check the native methods for getting patition id and comment out the old one!
    #     2. Talk to nitin and discuss about change happend in all the requests with params in data
