__author__ = "nkumar@soretel.com"

import sys, requests, os, logging, json
sys.path.append(os.path.normpath(os.path.dirname(os.path.dirname(os.path.dirname((__file__))))))

log = logging.getLogger("boss_api.get_details")


class GetDetails():
    """
    Apis related to general purpose operations. e.g. fetching accountId, locationId etc.
    """

    def get_param_to_use(self, xml_params, **kwargs):
        '''
        Note: The named params in the api definition must be same as expected by the boss http request.

        This function will return a list of params which should be used for the http calls. This will compare params picked from the xml file
        and override them with the param which were passed by the user during the call from the application.
        :param xml_params: A dictonary which holds the values from the xml file
        :param args: A list of the param passed to the function from the application
        :return: A dictionary with user preferences updated. User provided param will over ride the xml values.
        '''

        for param in kwargs:
            if kwargs[param] is not None:
                xml_params[param] = kwargs[param]
        return xml_params

    def get_config_based_on_build(self, build):
        '''
        To get the correct xml config file based on the build number provided
        :param build: the current build number
        :return: the file path or exception on failure
        '''
        build_xml = parse_xml(os.path.join(self.config_path,"build_info.xml"))
        build_config_file = build_xml.get_build_config_xml(build)
        if build_config_file:
            return build_config_file
        else:
            raise Exception("Incorrect build <%s> or missing range in the build_info.xml" %build)

    # Following functions are helper functions which are used to get certain details from the server

    def get_account_detail(self, url = None, act_name = None):
        '''
        This function will return all the accounts in a acount id.
        :param act_name: The account name
        :return: the account id of the specified act name
        '''
        act_id = None
        params = self.config.getparams("get_account_detail")
        url = params.pop("url")
        ret = requests.get(url, data = params, headers = self.headers)
        if ret.status_code == 200 and "Login" not in ret.text:
            log.info("Successfully retrieved all accounts info.")
        else:
            log.error("Could not retrieve all accounts info.")
        # parsing the returned content to get the act id
        for node in ret.json()["data"]:
            if node["CompanyName"] == act_name:
                act_id = node["id"]
                break
        return act_id

    def get_suitable_invoice_groups(self, act_id, invoice_group_name):
        '''
        This function will return all the invoice groups in a account
        :param act_name: The account name
        :return: the acount id of the specified act name
        '''
        invoice_group_id = None
        params = self.config.getparams("get_suitable_invoice_groups")
        url = params.pop("url")
        params["accountId"] = act_id
        ret = requests.post(url, data = params, headers = self.headers)
        if ret.status_code == 200 and invoice_group_name in ret.text:
            log.info("Successfully retrieved all invoice group info.")
        else:
            log.error("Could not retrieve all invoice group info.")
        # parsing the returned content to get the act id
        for grp in ret.json():
            if grp["Name"] == invoice_group_name:
                invoice_group_id = grp["Id"]
                break
        return invoice_group_id

    def get_dm_detail(self, act_id, username):
        '''
        This function will return the id of the DM in the specified tenant.
        :param act_name: The account name
        :param dm_name: The name of dm
        :return: the DM id in the specified act name
        '''
        dm_id = None
        params = self.config.getparams("dm_details")
        params["selectedAccountId"] = act_id
        url = params.pop("url")
        ret = requests.post(url, data = params, headers = self.headers)
        if ret.status_code == 200 and "Login" not in ret.text:
            log.info("Successfully retrieved all accounts info.")
        else:
            log.error("Could not retrieve all accounts info.")
        # parsing the returned content to get the dm id
        for node in ret.json():
            if node["Username"] == username:
                dm_id = node["id"]
                break
        return dm_id

    def get_contract_detail(self, accountId):
        '''
        This function will return the id of the contract in the specified account.
        :param accountId: The account id
        :return: the contract id in the specified act name
        '''
        contract_id = None
        params = self.config.getparams("get_contract_details")
        params["accountId"] = params["selectedAccountId"] = accountId
        url = params.pop("url")
        ret = requests.get(url, data = params, headers = self.headers)
        if ret.status_code == 200 and "AccountId" in ret.text:
            log.info("Successfully retrieved contract info.")
        else:
            log.error("Could not retrieve all contract info.")
        # parsing the returned content to get contract id
        for cont, details in ret.json().iteritems():
            if cont == "data":
                for d in details:
                    if d["AccountId"] == int(accountId):
                        contract_id = d["id"]
                        break

        return contract_id

    def get_order_detail(self, accountId, loc_name):
        '''
        This function will return the id of the order based on the provided location name.
        :param accountId: The account id
        :param loc_name: The name of the location
        :return: the order id in the specified act name
        '''
        order_id = None
        loc_id = self.get_location_id(accountId, loc_name)
        params = self.config.getparams("get_order_detail")
        params["accountId"] = accountId
        url = params.pop("url")
        ret = requests.get(url, data = params, headers = self.headers)
        if ret.status_code == 200 and ret.json().has_key("data"):
            log.info("Successfully retrieved order info.")
        else:
            log.error("Could not retrieve all order info.")
        # parsing the returned content to get id
        for cont, details in ret.json().iteritems():
            if cont == "data":
                for d in details:
                    if d["LocationId"] == int(loc_id):
                        order_id = d["Id"]
                        break

        return order_id

    def get_location_detail(self, act_id, loc_name):
        '''
        This function will return the id of the location in the specified tenant.
        :param act_id: The account id
        :param location_name: The name of location
        :return: the location id in the specified act name
        '''
        loc_id = None
        params = self.config.getparams("get_location_detail")
        params["accountId"] = act_id
        url = params.pop("url")
        ret = requests.get(url, params = params, headers = self.headers)
        if ret.status_code == 200 and "FullAddress" in ret.text:
            log.info("Successfully retrieved all location info.")
        else:
            log.error("Could not retrieve all location info.")

        # parsing the returned content to get the id
        # for loc,details in ret.json().iteritems():
        #     if loc == "data":
        #         for d in details:
        #             if d["LabelFormatted"] == loc_name:
        #                 loc_id = d["LocationId"]
        #                 break
        #
        # return loc_id
        return ret

    def get_location_id(self, act_id, loc_name):
        '''
        This function will return the id of the location in the specified tenant.
        :param act_id: The account id
        :param location_name: The name of location
        :return: the location id in the specified act name
        '''

        ret = self.get_location_detail(act_id,loc_name)
        for loc, details in ret.json().iteritems():
            if loc == "data":
                for d in details:
                    if d["LabelFormatted"] == loc_name:
                        loc_id = d["LocationId"]
                        break

        return loc_id

    # def get_country_id(self, act_id, loc_name):
    #     '''
    #     This function will return the id of the location in the specified tenant.
    #     :param act_id: The account id
    #     :param location_name: The name of location
    #     :return: the location id in the specified act name
    #     '''
    #
    #     ret = self.get_location_detail(act_id,loc_name)
    #     for loc, details in ret.json().iteritems():
    #         if loc == "data":
    #             for d in details:
    #                 if d["LabelFormatted"] == loc_name:
    #                     loc_id = d["LocationId"]
    #                     break
    #
    #     return loc_id



    def get_location_emergency_number(self, act_id, loc_name):
        '''
        This function will return the id of the location in the specified tenant.
        :param act_id: The account id
        :param location_name: The name of location
        :return: the location id in the specified act name
        '''

        ret = self.get_location_detail(act_id, loc_name)
        for loc, details in ret.json().iteritems():
            if loc == "data":
                for d in details:
                    if d["LabelFormatted"] == loc_name:
                        em_num = d["EmergencyAni"]
                        break

        return em_num

    def get_partition_detail(self, act_id, part_name):
        '''
        This function will return the id of the partition in the specified tenant.
        :param act_id: The account id
        :param part_name: The name of partition
        :return: the partition id in the specified act name
        '''

        if self.part_id:
            return self.part_id
        self.part_id = None
        params = self.config.getparams("get_partition_detail")
        params["accountId"] = act_id
        url = params.pop("url")
        ret = requests.get(url, params = params, headers = self.headers)
        if ret.status_code == 200 and "ClusterId" in ret.text:
            log.info("Successfully retrieved all partition info.")
        else:
            log.error("Could not retrieve all partition info.")
        # parsing the returned content to get the id
        for loc,details in ret.json().iteritems():
            if loc == "data":
                for d in details:
                    if d["Cluster"] == part_name:
                        self.part_id = d["Id"]
                        break

        return self.part_id

    def get_profile_detail(self, act_id, part_name,user_name,**kwargs):
        '''
        This function will return the id of the profile of a user.
        :param act_id: The account id
        :param part_name: The name of partition
        :param user_name: The user name of the user
        :return: the partiton id in the specified act name
        '''
        profile_id = None
        params = self.config.getparams("get_profile_detail")
        params["accountId"] = act_id
        if not self.part_id:
            params["partitionId"] = self.get_partition_detail(act_id,part_name)
        else:
            params["partitionId"] = self.part_id
        url = params.pop("url")
        # ret = requests.get(url, data = params, headers = self.headers)
        ret = requests.get(url, params = params, headers = self.headers) # 13-12-2019 - Shankara Narayanan
        if ret.status_code == 200:
            log.info("Successfully retrieved all profile info.")
        else:
            log.error("Could not retrieve all profile info.")
        # parsing the returned content to get the id
        for loc,details in ret.json().iteritems():
            if loc == "data":
                for d in details:
                    if kwargs.get('extension'): # get the details with extension which is unique than email! ##MSN
                        if d["Extension"] == kwargs.get('extension'):
                            profile_id = d["ProfileId"]
                            break
                    else:
                        if d["BusinessEmail"] == user_name:
                            profile_id = d["ProfileId"]
                            break

        return str(profile_id)

    def get_all_users(self,act_id ):
        '''
        This function will return the id of the profile of a user.
        :param act_id: The account id
        :param part_name: The name of partition
        :param user_name: The user name of the user
        :return: the partiton id in the specified act name
        '''
        profile_id = None
        params = self.config.getparams("get_all_phone_numbers")
        params["accountId"] = act_id
        params["partitionId"] = self.part_id
        url = params.pop("url")
        # ret = requests.get(url, data = params, headers = self.headers)
        ret = requests.get(url, params = params, headers = self.headers) # 13-12-2019 - Shankara Narayanan
        if ret.status_code == 200:
            log.info("Successfully retrieved all profile info.")
        else:
            log.error("Could not retrieve all profile info.")
        return ret.json()

    def get_usergroup_detail(self, act_id, part_name, usergroup_name):
        '''
        This function will return the id of a user group.
        :param act_id: The account id
        :param part_name: The name of partition
        :param usergroup_name: The user name of the user group
        :return: the partiton id in the specified act name
        '''
        usergroup_id = None
        params = self.config.getparams("get_usergroup_detail")
        params["accountId"] = act_id
        params["partitionId"] = self.get_partition_detail(act_id,part_name)
        url = params.pop("url")
        ret = requests.get(url, params = params, headers = self.headers)
        if ret.status_code == 200:
            log.info("Successfully retrieved all user group info.")
        else:
            log.error("Could not retrieve all user group info.")
        # parsing the returned content to get the id
        for loc,details in ret.json().iteritems():
            if loc == "data":
                for d in details:
                    if d["Name"] == usergroup_name:
                        usergroup_id = d["id"]
                        break

        return str(usergroup_id)

    def get_usergroup_detail(self, act_id, usergroup_name):
        '''
        This function will return the id of a user group.
        :param act_id: The account id
        :param part_name: The name of partition
        :param usergroup_name: The user name of the user group
        :return: the partiton id in the specified act name
        '''
        usergroup_id = None
        params = self.config.getparams("get_usergroup_detail")
        params["accountId"] = act_id
        params["partitionId"] = self.part_id
        url = params.pop("url")
        ret = requests.get(url, params = params, headers = self.headers)
        if ret.status_code == 200:
            log.info("Successfully retrieved all user group info.")
        else:
            log.error("Could not retrieve all user group info.")
        # parsing the returned content to get the id
        for loc,details in ret.json().iteritems():
            if loc == "data":
                for d in details:
                    if d["Name"] == usergroup_name:
                        usergroup_id = d["id"]
                        break

        return str(usergroup_id)

    def get_person_detail(self, act_id, part_name, BusinessEmail, **kwargs):
        '''
        This function will return the id of the person in the specified account.
        :param act_id: The account id
        :param part_name: The name of partition
        :param BusinessEmail: The email of the user whose id is required
        :return: the partiton id in the specified act name
        '''
        person_id = None
        params = self.config.getparams("get_person_detail")
        params["accountId"] = act_id
        if not self.part_id:
            params["partitionId"] = self.get_partition_detail(act_id, part_name)
        else:
            params["partitionId"] = self.part_id
        url = params.pop("url")
        # ret = requests.get(url, data=params, headers=self.headers)  # does not work with SIt but works with http
        ret = requests.get(url, params=params, headers=self.headers)
        if ret.status_code == 200 and "PersonId" in ret.text:
            log.info("Successfully retrieved all person info.")
        else:
            log.error("Could not retrieve all person info.")
        # parsing the returned content to get the id

        for loc, details in ret.json().iteritems():
            if loc == "data":
                for d in details:
                    if kwargs.get('extension'):
                        if d["Extension"] == kwargs.get('extension'):
                            person_id = d["PersonId"]
                            break
                    else:
                        if d["BusinessEmail"] == BusinessEmail:
                            person_id = d["PersonId"]
                            break

        return int(person_id)

    def verify_person_detail(self, act_id, part_name,BusinessEmail, ext=None, tn=None):
        '''
        This function will verify the details of a person.
        :param act_id: The account id
        :param part_name: The name of partition
        :param BusinessEmail: The email of the user whose id is required
        :param ext: The extension to be verified
        :param tn: The telephone number to be verified
        :return: the partiton id in the specified act name
        '''
        is_ext_correct = True
        is_tn_correct = True
        params = self.config.getparams("get_person_detail")
        params["accountId"] = act_id
        params["partitionId"] = self.get_partition_detail(act_id,part_name)
        url = params.pop("url")
        ret = requests.get(url, data = params, headers = self.headers)
        if ret.status_code == 200 and "PersonId" in ret.text:
            log.info("Successfully retrieved all person info.")
        else:
            log.error("Could not retrieve all person info.")
        # parsing the returned content to get the id
        for loc,details in ret.json().iteritems():
            if loc == "data":
                for d in details:
                    if d["BusinessEmail"] == BusinessEmail:
                        if ext is not None:
                            if d["Extension"] == ext:
                                is_ext_correct = True
                            else:
                                is_ext_correct = False
                        if tn is not None:
                            if d["Tn"] == "%s (%s) %s-%s"%(tn[0],tn[1:4],tn[4:7],tn[7:]):
                                is_tn_correct = True
                            else:
                                is_tn_correct = False

                        break

        return is_ext_correct and is_tn_correct

    def get_cluster_detail(self, cluster_name):
        '''
        This function will return the id of the cluster.
        :param act_id: The account id
        :param part_name: The name of partition
        :return: the cluster id in the specified act name
        '''
        cluster_id = None
        params = self.config.getparams("get_cluster_detail")
        url = params.pop("url")
        ret = requests.get(url, data = params, headers = self.headers)
        if ret.status_code == 200 and "ClusterStatus" in ret.text:
            log.info("Successfully retrieved all cluster info.")
        else:
            log.error("Could not retrieve cluster info.")
        # parsing the returned content to get the id
        for loc,details in ret.json().iteritems():
            if loc == "data":
                for d in details:
                    if str(d["Name"]) == cluster_name:
                        cluster_id = d["Id"]
                        break

        return str(cluster_id)

    def get_cosmo_component(self, act_id, part_id, componentType=None,id=None):
        """
        This function will return the data related to a cosmo component
        :param act_id: The account id
        :param part_id: The name of partition
        :param component_type: The name of the component
        :return: the data of the cosmo component
        """
        params = self.config.getparams("get_cosmo_component")
        params["componentType"] = componentType
        params["accountId"] = act_id
        params["partitionId"] = part_id
        if id is not None:
            params['id'] = id
        url = params.pop("url")
        ret = requests.post(url, data=params, headers=self.headers)
        if ret.status_code == 200 and "data" in ret.text:
            log.info("Successfully retrieved the data about specified cosmo component.")
        else:
            log.error("Could not retrieve the data about specified cosmo component.")
        # returning the data related to the cosmo component
        return ret.json()

    def get_vcfe_detail(self, act_id, part_id, comp_name,**kwargs):
        """
        This function will return the id of a cosmo component
        :param act_id: The account id
        :param part_id: The name of partition
        :return: the data of the cosmo component
        """
        comp_id = None
        params = self.config.getparams("get_vcfe_detail")
        params["accountId"] = act_id
        params["partitionId"] = part_id
        url = params.pop("url")
        ret = requests.get(url, params=params, headers=self.headers) # Shankara Narayanan
        if ret.status_code == 200 and "data" in ret.text:
            log.info("Successfully retrieved the data about all cosmo component.")
        else:
            log.error("Could not retrieve the data about cosmo components.")
        # parsing the returned content to get the id
        for loc, details in ret.json().iteritems():
            if loc == "data":
                for d in details:
                    if kwargs.get("Extension") and (str(d["ExtensionData"]))==str(kwargs.get("Extension")):
                        comp_id = d["ComponentId"]
                        break
                    elif str(json.loads(d["ComponentData"])[0]) == comp_name:
                        comp_id = d["ComponentId"]
                        break
        if not comp_id: # Shankara Narayanan
            logging.error("vcfe component not found in the system")
            raise Exception("vcfe component not found in the system")
        return str(comp_id)

    # Shankara Narayanan
    def get_vcfe_details(self, act_id, part_id, extension):
        """
        This function will return the id of a cosmo component
        :param act_id: The account id
        :param part_id: The name of partition
        :return: the data of the cosmo component
        """
        comp_id = None
        params = self.config.getparams("get_vcfe_detail")
        params["accountId"] = act_id
        params["partitionId"] = part_id
        url = params.pop("url")
        ret = requests.get(url, params=params, headers=self.headers)
        if ret.status_code == 200 and "data" in ret.text:
            log.info("Successfully retrieved the data about all cosmo component.")
        else:
            log.error("Could not retrieve the data about cosmo components.")
        # parsing the returned content to get the id
        for loc, details in ret.json().iteritems():
            if loc == "data":
                for d in details:
                    if str(d["ExtensionData"]) == str(extension):
                        comp_id = d["ComponentId"]
                        break
        if not comp_id: # Shankara Narayanan
            logging.error("vcfe component not found in the system")
            raise Exception("vcfe component not found in the system")
        return str(comp_id)

    def get_programmable_btns_data(self, act_id, profile_id):
        """
        This function will return the programmable buttons data for an user
        :param act_id: The account id
        :param profile_id: The profile id for a user
        :return: the data of the programmable buttons
        """

        params = self.config.getparams("configure_prog_button")
        params["accountId"] = act_id
        params["profileId"] = profile_id
        url = params.pop("url")
        # ret = requests.get(url, data=params, headers=self.headers)
        ret = requests.get(url, params=params, headers=self.headers) # 13-12-2019 Shankara Narayanan. M
        if ret.status_code == 200 and "user" in ret.json().keys():
            log.info("Successfully retrieved the data about the programmable buttons.")
        else:
            log.error("Could not retrieve the data about the programmable buttons.")

        return ret.json()

    def get_tn_country(self,phoneNumber):
        result = False
        acTN=""
        acCountryID=""
        acDetails = self.get_all_users(self.accountId)
        for acs in acDetails['data']:
            if str(acs['TnId']).split('-')[1] == str(phoneNumber):
                acTN = str(acs['TnId'][1:])
                acCountryID = str(acs['CountryId'])
                result=True
                break
        if not (acTN and acCountryID):
            log.error("Outbound caller ID not found")
        else:
            return result,acTN,acCountryID

    def get_bca_profile_id(self, bca_extn, act_id, loc_id, part_id):
        """
        This api will return the bca profile id
        :param act_id:
        :param loc_id:
        :param part_id:
        :return:
        """
        bca_id = None
        params = self.config.getparams("get_bca_id")
        params["accountId"] = act_id
        params["partitionId"] = part_id
        url = params.pop("url")
        ret = requests.get(url, params=params, headers=self.headers)
        if ret.status_code == 200 and "data" in ret.text:
            log.info("Successfully retrieved all bca ids.")
        else:
            log.error("Could not retrieve the bca id.")
        # parsing the returned content to get the id
        for loc, details in ret.json().iteritems():
            if loc == "data":
                for d in details:
                    if d["Extension"] == bca_extn:
                        bca_id = d["ProfileId"]
                        break

        return str(bca_id)