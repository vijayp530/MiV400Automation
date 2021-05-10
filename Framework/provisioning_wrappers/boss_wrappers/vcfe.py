__author__ = "nitin.kumar-2@mitel.com"

import sys, requests, os, logging, ast, json
sys.path.append(os.path.normpath(os.path.dirname(os.path.dirname(os.path.dirname((__file__))))))
from utils.decorators import func_logger

log = logging.getLogger("boss_api.vcfe")


class Vcfe():
    """
    Apis for the vcfe related operations.
    """

    @func_logger
    def create_auto_attendant(self, **params):
        '''
        This function will create an auto attendant
        phone system -> visual call flow editor -> Add -> Auto attendant
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        params_xml = self.config.getparams("create_auto_attendant")
        params = self.get_param_to_use(params_xml, **params)
        if self.accountId is None:  # switch account has not been called
            act_id = self.get_account_detail(act_name=params['account_name'])
        else:
            act_id = self.accountId
        params["accountId"] = act_id
        if self.part_id is None:
            part_id = self.get_partition_detail(act_id, params['part_name'])
        else:
            part_id = self.part_id
        params["partitionId"] = part_id
        params["data"] = str(self.get_cosmo_component(act_id, part_id, params['componentType'])['data'])
        params["profileLocationId"] = self.get_location_id(act_id, params['location_name'])
        # replacing the default name and extension if provided by the user
        # the ast module could not convert data to its dictionary representation therefore using the json module
        if params.get('aa_name') is not None:
            temp = json.loads(params['data'])
            temp['menu']['dn_attributes']['Description'] = params['aa_name']
            if params.get('aa_extension') is not None:
                temp['menu']['dn_attributes']['DN_formatted'] = params['aa_extension']
            # converting the dict back to string
            params['data'] = json.dumps(temp)
        params['data'] = params['data'].replace("'",'"')
        url = params.pop("url")
        log.info("Creating auto attendant with args <%s>" % params)
        ret = requests.post(url, data=params, headers=self.headers)
        if ret.status_code == 200 and len(ret.text) == 2:
            log.info("The auto attendant has been created successfully.Message from server : <%s>" % ret.text)
            result = True
        else:
            log.error("Could not create auto attendant.Message from server : <%s>" % ret.text)

        return result, ret

    @func_logger
    def edit_auto_attendant(self, comp_name, **params):
        '''
        This function will edit an auto attendant
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        params_xml = self.config.getparams("edit_auto_attendant")
        params = self.get_param_to_use(params_xml, **params)
        if self.accountId is None:  # switch account has not been called
            act_id = self.get_account_detail(act_name=params['account_name'])
        else:
            act_id = self.accountId
        params["accountId"] = act_id
        if self.part_id is None:
            part_id = self.get_partition_detail(act_id, params['part_name'])
        else:
            part_id = self.part_id
        params["partitionId"] = part_id
        # getting the component id
        id = self.get_vcfe_detail(act_id, part_id, comp_name)
        params['id'] = id
        params["data"] = str(self.get_cosmo_component(act_id, part_id, componentType=params['componentType'],id=id)['data'])
        params["profileLocationId"] = self.get_location_id(act_id, params['location_name'])
        # replacing the default name and extension if provided by the user
        # the ast module could not convert data to its dictionary representation therefore using the json module
        if params.get('aa_name') is not None:
            temp = json.loads(params['data'])
            temp['menu']['dn_attributes']['Description'] = params['aa_name']
            if params.get('aa_extension') is not None:
                temp['menu']['dn_attributes']['DN_formatted'] = params['aa_extension']
            # converting the dict back to string
            params['data'] = json.dumps(temp)
        params['data'] = params['data'].replace("'", '"')
        url = params.pop("url")
        log.info("Editing auto attendant with args <%s>" % params)
        ret = requests.post(url, data=params, headers=self.headers)
        if ret.status_code == 200 and len(ret.text) == 2:
            log.info("The auto attendant has been edited successfully.Message from server : <%s>" % ret.text)
            result = True
        else:
            log.error("Could not edit auto attendant.Message from server : <%s>" % ret.text)

        return result, ret

    @func_logger
    def delete_auto_attendant(self, comp_name, **params):
        '''
        This function will delete an auto attendant
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        params_xml = self.config.getparams("delete_auto_attendant")
        params = self.get_param_to_use(params_xml, **params)
        if self.accountId is None:  # switch account has not been called
            act_id = self.get_account_detail(act_name=params['account_name'])
        else:
            act_id = self.accountId
        params["accountId"] = act_id
        if self.part_id is None:
            part_id = self.get_partition_detail(act_id, params['part_name'])
        else:
            part_id = self.part_id
        params["partitionId"] = part_id
        # getting the component id
        id = self.get_vcfe_detail(act_id, part_id, comp_name)
        params['id'] = id
        # params["data"] = str(self.get_cosmo_component(act_id, part_id, componentType=params['componentType'], id=id)['data'])
        params["profileLocationId"] = self.get_location_id(act_id, params['location_name'])
        url = params.pop("url")
        log.info("Deleting auto attendant with args <%s>" % params)
        ret = requests.post(url, data=params, headers=self.headers)
        if ret.status_code == 200 and ret.json()["message"] == "Component successfully deleted.":
            log.info("The auto attendant has been deleted successfully.Message from server : <%s>" % ret.text)
            result = True
        else:
            log.error("Could not delete auto attendant.Message from server : <%s>" % ret.text)

        return result, ret

    @func_logger
    def create_hunt_group(self, **params):
        '''
        This function will create an hunt group
        phone system -> visual call flow editor -> Add -> Hunt Group
        :return: A tuple of a boolean status flag and the return object from the requested url

        Note: The back up extension must be assigned to a user.
        '''
        result = False
        params_xml = self.config.getparams("create_hunt_group")
        params = self.get_param_to_use(params_xml, **params)
        if self.accountId is None:  # switch account has not been called
            act_id = self.get_account_detail(act_name=params['account_name'])
        else:
            act_id = self.accountId
        params["accountId"] = act_id
        if self.part_id is None:
            part_id = self.get_partition_detail(act_id, params['part_name'])
        else:
            part_id = self.part_id
        params["partitionId"] = part_id

        resJson = self.get_cosmo_component(act_id, part_id, params['componentType'])
        params["data"] = resJson['data']
        availbleHGnumbers = json.loads(resJson['commondata'])['rows']
        # replacing the default name and extension if provided by the user
        # the ast module could not convert data to its dictionary representation therefore using the json module
        if params.get('hg_name') is not None:
            temp = json.loads(params['data'])
            temp['hunt_group']['dn_attributes']['Description'] = params['hg_name']
            if params.get('hg_extension') is not None:
                temp['hunt_group']['dn_attributes']['DN_formatted'] = params['hg_extension']
            # adding the back up extension
            temp['hunt_group']['BackupDN_formatted'] = params['hg_backup_extn']
            # setting the SiteID -- this step is questionable but seems mandatory to create hunt group
            temp['hunt_group']['SiteID'] = temp['collections']['sites'][0]['SiteID']

            # Shankara Narayanan
            temp['hunt_group']['dn_attributes']['include_in_dial_by_name']=params.get('IncludeInSystemDialByNameDirectory',temp['hunt_group']['dn_attributes']['include_in_dial_by_name'])
            temp['hunt_group']['HuntPatternID']=params.get('HuntPatternID',temp['hunt_group']['HuntPatternID']) # 1/4
            temp['hunt_group']['RingsPerMember']=params.get('RingsPerMember',temp['hunt_group']['RingsPerMember']) # 1/4
            temp['hunt_group']['NoAnswerRings']=params.get('NoAnswerRings',temp['hunt_group']['NoAnswerRings'])
            temp['hunt_group']['IsOneHuntCallPerMember']=params.get('SkipMemberIfAlreadyOnCall',temp['hunt_group']['IsOneHuntCallPerMember'])
            temp['hunt_group']['IsDefeatCallHandling']=params.get('CallMemberWhenForwarding',temp['hunt_group']['IsDefeatCallHandling'])
            group_members = []
            if params.get("HuntGroupMember") != None :
                for HGMembers in params.get("HuntGroupMember"): # go through add hg numbers
                    isFound = False
                    for avHGs in availbleHGnumbers:
                        if str(HGMembers) == str(avHGs["cell"][0]).split('-')[1]:
                            group_members.append(avHGs["cell"][0])
                            isFound = True
                            break
                    if not isFound:
                        log.error("Extension " + str(HGMembers) + " not found in system ")
                        return False
            # converting the dict back to string
            temp['hunt_group']['dn_ids']=group_members
            params['data'] = json.dumps(temp)
        params['data'] = params['data'].replace("'",'"')
        url = params.pop("url")
        log.info("Creating hunt group with args <%s>" % params)
        ret = requests.post(url, data=params, headers=self.headers)
        if ret.status_code == 200 and len(ret.text) == 2:
            log.info("The hunt group %s has been created successfully.Message from server : <%s>" %(str(temp['hunt_group']['dn_attributes']['DN_formatted']),ret.text))
            print("hunt group "+ str(temp['hunt_group']['dn_attributes']['DN_formatted'])+" has been created ")
            result = True
        else:
            log.error("Could not create hunt group.Message from server : <%s>" % ret.text)

        return result, ret,str(temp['hunt_group']['dn_attributes']['DN_formatted'])

    @func_logger
    def edit_hunt_group(self, hg_to_edit, **params):
        '''
        This function will edit a hunt group
        phone system -> visual call flow editor -> Select hunt group -> Edit
        :return: A tuple of a boolean status flag and the return object from the requested url

        '''
        result = False
        params_xml = self.config.getparams("edit_hunt_group")
        params = self.get_param_to_use(params_xml, **params)
        if self.accountId is None:  # switch account has not been called
            act_id = self.get_account_detail(act_name=params['account_name'])
        else:
            act_id = self.accountId
        params["accountId"] = act_id
        if self.part_id is None:
            part_id = self.get_partition_detail(act_id, params['part_name'])
        else:
            part_id = self.part_id
        params["partitionId"] = part_id

        resJson = self.get_cosmo_component(act_id, part_id, params['componentType'])
        params["data"] = resJson['data']
        availbleHGnumbers = json.loads(resJson['commondata'])['rows']

        # params["data"] = str(self.get_cosmo_component(act_id, part_id, params['componentType'])['data'])
        # getting the component id
        id = self.get_vcfe_detail(act_id, part_id, hg_to_edit)
        params['id'] = id
        params["data"] = self.get_cosmo_component(act_id, part_id, componentType=params['componentType'], id=id)['data']
        # params["profileLocationId"] = self.get_location_id(act_id, params['location_name'])
        # replacing the default name and extension if provided by the user
        # the ast module could not convert data to its dictionary representation therefore using the json module
        if params.get('hg_name') is not None:
            temp = json.loads(params['data'])
            temp['hunt_group']['dn_attributes']['Description'] = params['hg_name']
            if params.get('hg_extension') is not None:
                temp['hunt_group']['dn_attributes']['DN_formatted'] = params['hg_extension']
            # adding the back up extension
            temp['hunt_group']['BackupDN_formatted'] = params['hg_backup_extn']
            # setting the SiteID -- this step is questionable but seems mandatory to create hunt group
            temp['hunt_group']['SiteID'] = temp['collections']['sites'][0]['SiteID']

            # Shankara Narayanan
            temp['hunt_group']['dn_attributes']['include_in_dial_by_name']=params.get('IncludeInSystemDialByNameDirectory',temp['hunt_group']['dn_attributes']['include_in_dial_by_name'])
            temp['hunt_group']['HuntPatternID']=params.get('HuntPatternID',temp['hunt_group']['HuntPatternID']) # 1/4
            temp['hunt_group']['RingsPerMember']=params.get('RingsPerMember',temp['hunt_group']['RingsPerMember']) # 1/4
            temp['hunt_group']['NoAnswerRings']=params.get('NoAnswerRings',temp['hunt_group']['NoAnswerRings'])
            temp['hunt_group']['IsOneHuntCallPerMember']=params.get('SkipMemberIfAlreadyOnCall',temp['hunt_group']['IsOneHuntCallPerMember'])
            temp['hunt_group']['IsDefeatCallHandling']=params.get('CallMemberWhenForwarding',temp['hunt_group']['IsDefeatCallHandling'])
            group_members = []
            if params.get("HuntGroupMember") != None :
                for HGMembers in params.get("HuntGroupMember"): # go through add hg numbers
                    isFound = False
                    for avHGs in availbleHGnumbers:
                        if str(HGMembers) == str(avHGs["cell"][0]).split('-')[1]:
                            group_members.append(avHGs["cell"][0])
                            isFound = True
                            break
                    if not isFound:
                        log.error("Extension " + str(HGMembers) + " not found in system ")
                        return False
            temp['hunt_group']['dn_ids']=group_members
            # converting the dict back to string
            params['data'] = json.dumps(temp)
        params['data'] = params['data'].replace("'",'"')
        url = params.pop("url")
        log.info("Editing hunt group with args <%s>" % params)
        ret = requests.post(url, data=params, headers=self.headers)
        if ret.status_code == 200 and len(ret.text) == 2:
            log.info("The hunt group has been edited successfully.Message from server : <%s>" % ret.text)
            result = True
        else:
            log.error("Could not edit hunt group.Message from server : <%s>" % ret.text)

        return result, ret

    @func_logger
    def delete_hunt_group(self, hg_to_delete, **params):
        '''
        This function will delete a hunt group
        phone system -> visual call flow editor -> Select hunt group -> Delete
        :return: A tuple of a boolean status flag and the return object from the requested url

        '''
        result = False
        params_xml = self.config.getparams("delete_hunt_group")
        params = self.get_param_to_use(params_xml, **params)
        if self.accountId is None:  # switch account has not been called
            act_id = self.get_account_detail(act_name=params['account_name'])
        else:
            act_id = self.accountId
        params["accountId"] = act_id
        if self.part_id is None:
            part_id = self.get_partition_detail(act_id, params['part_name'])
        else:
            part_id = self.part_id

        params["partitionId"] = part_id

        # getting the component id
        # id = self.get_vcfe_detail(act_id, part_id, hg_to_delete)
        if params.get('extension'): # Added to delete with extension number! ##MSN
            id = self.get_vcfe_details(act_id, part_id, params.get('extension'))
        else:
            id = self.get_vcfe_detail(act_id, part_id, hg_to_delete)
        params['id'] = id

        # params["data"] = str(self.get_cosmo_component(act_id, part_id, componentType=params['componentType'], id=id)['data'])
        if params.get('location_name'):
            params["profileLocationId"] = self.get_location_id(act_id, params['location_name'])

        url = params.pop("url")
        log.info("Deleting hunt group with args <%s>" % params)
        ret = requests.post(url, data=params, headers=self.headers)
        if ret.status_code == 200 and ret.json()["message"] == "Component successfully deleted.":
            log.info("The hunt group has been deleted successfully.Message from server : <%s>" % ret.text)
            result = True
        else:
            log.error("Could not delete hunt group.Message from server : <%s>" % ret.text)

        return result, ret

    @func_logger
    def create_extension_list(self, **params):
        '''
        This function will create an extension list
        phone system -> visual call flow editor -> Add -> Extension List
        :return: A tuple of a boolean status flag and the return object from the requested url

        '''
        result = False
        params_xml = self.config.getparams("create_extension_list")
        params = self.get_param_to_use(params_xml, **params)
        if self.accountId is None:  # switch account has not been called
            act_id = self.get_account_detail(act_name=params['account_name'])
        else:
            act_id = self.accountId
        params["accountId"] = act_id
        if self.part_id is None:
            part_id = self.get_partition_detail(act_id, params['part_name'])
        else:
            part_id = self.part_id
        params["partitionId"] = part_id
        el_data = str(self.get_cosmo_component(act_id, part_id, params['componentType']))
        # the ast module could not convert data to its dictionary representation therefore using the json module
        if params.get('el_name') is not None:
            temp = ast.literal_eval(el_data)
            commondata = json.loads(temp['commondata'])
            data = json.loads(temp['data'])
            data['extension_list']['Name'] = params['el_name']
            # creating the list of extensions to be supplied in the request
            my_extn_list = []
            my_extn = {}
            dn_ids = []
            for extn in params['el_extns']:
                for row in commondata['rows']:
                    if extn == row['id'].split('-')[-1]:
                        my_extn["id"] = row['cell'][0]
                        my_extn["Description"] = row['cell'][1]
                        my_extn["DN"] = extn
                        dn_ids.append(row['cell'][0])
                        my_extn_list.append(my_extn)
                        break
                my_extn = {}

            data['extension_list']['selected_extension_list'] = my_extn_list
            data['extension_list']['dn_ids'] = dn_ids
            # converting the dict back to string
            params['data'] = json.dumps(data)
        params['data'] = params['data'].replace("'",'"')
        url = params.pop("url")
        log.info("Creating extension list with args <%s>" % params)
        ret = requests.post(url, data=params, headers=self.headers)
        if ret.status_code == 200 and len(ret.text) == 2:
            log.info("The extension list has been created successfully.Message from server : <%s>" % ret.text)
            result = True
        else:
            log.error("Could not create extension list.Message from server : <%s>" % ret.text)

        return result, ret

    @func_logger
    def edit_extension_list(self, el_to_edit, **params):
        '''
        This function will edit an extension list
        phone system -> visual call flow editor -> Select extension list -> Edit
        :return: A tuple of a boolean status flag and the return object from the requested url

        '''
        result = False
        params_xml = self.config.getparams("edit_extension_list")
        params = self.get_param_to_use(params_xml, **params)
        if self.accountId is None:  # switch account has not been called
            act_id = self.get_account_detail(act_name=params['account_name'])
        else:
            act_id = self.accountId
        params["accountId"] = act_id
        if self.part_id is None:
            part_id = self.get_partition_detail(act_id, params['part_name'])
        else:
            part_id = self.part_id
        params["partitionId"] = part_id
        # getting the component id
        id = self.get_vcfe_detail(act_id, part_id, el_to_edit)
        params['id'] = id
        el_data = str(self.get_cosmo_component(act_id, part_id, params['componentType'], id=id))
        # the ast module could not convert data to its dictionary representation therefore using the json module
        if params.get('el_name') is not None:
            temp = ast.literal_eval(el_data)
            commondata = json.loads(temp['commondata'])
            data = json.loads(temp['data'])
            data['extension_list']['Name'] = params['el_name']
            # creating the list of extensions to be supplied in the request
            my_extn_list = []
            my_extn = {}
            dn_ids = []
            for extn in params['el_extns']:
                for row in commondata['rows']:
                    if extn == row['id'].split('-')[-1]:
                        my_extn["id"] = row['cell'][0]
                        my_extn["Description"] = row['cell'][1]
                        my_extn["DN"] = extn
                        dn_ids.append(row['cell'][0])
                        my_extn_list.append(my_extn)
                        break
                my_extn = {}

            data['extension_list']['selected_extension_list'] = my_extn_list
            data['extension_list']['dn_ids'] = dn_ids
            # converting the dict back to string
            params['data'] = json.dumps(data)
        params['data'] = params['data'].replace("'", '"')

        url = params.pop("url")
        log.info("Editing extension list with args <%s>" % params)
        ret = requests.post(url, data=params, headers=self.headers)
        if ret.status_code == 200 and len(ret.text) == 2:
            log.info("The extension list has been edited successfully.Message from server : <%s>" % ret.text)
            result = True
        else:
            log.error("Could not edit extension list.Message from server : <%s>" % ret.text)

        return result, ret

    @func_logger
    def delete_extension_list(self, el_to_delete, **params):
        '''
        This function will delete an extension list
        phone system -> visual call flow editor -> Select extension list -> Delete
        :return: A tuple of a boolean status flag and the return object from the requested url

        '''
        result = False
        params_xml = self.config.getparams("delete_extension_list")
        params = self.get_param_to_use(params_xml, **params)
        if self.accountId is None:  # switch account has not been called
            act_id = self.get_account_detail(act_name=params['account_name'])
        else:
            act_id = self.accountId
        params["accountId"] = act_id
        if self.part_id is None:
            part_id = self.get_partition_detail(act_id, params['part_name'])
        else:
            part_id = self.part_id
        params["partitionId"] = part_id
        # getting the component id
        id = self.get_vcfe_detail(act_id, part_id, el_to_delete)
        params['id'] = id
        if params.get('location_name'):
            params["profileLocationId"] = self.get_location_id(act_id, params['location_name'])
        url = params.pop("url")
        log.info("Deleting extension list with args <%s>" % params)
        ret = requests.post(url, data=params, headers=self.headers)
        if ret.status_code == 200 and ret.json()["message"] == "Component successfully deleted.":
            log.info("The extension list has been deleted successfully.Message from server : <%s>" % ret.text)
            result = True
        else:
            log.error("Could not delete extension list.Message from server : <%s>" % ret.text)

        return result, ret

    @func_logger
    def create_paging_group(self, **params):
        '''
        This function will create a paging group
        phone system -> visual call flow editor -> Add -> Paging Group
        :return: A tuple of a boolean status flag and the return object from the requested url

        Note: There must already be an existing extension list.
        '''
        result = False
        params_xml = self.config.getparams("create_paging_group")
        params = self.get_param_to_use(params_xml, **params)
        if self.accountId is None:  # switch account has not been called
            act_id = self.get_account_detail(act_name=params['account_name'])
        else:
            act_id = self.accountId
        params["accountId"] = act_id
        if self.part_id is None:
            part_id = self.get_partition_detail(act_id, params['part_name'])
        else:
            part_id = self.part_id
        params["partitionId"] = part_id
        params["profileLocationId"] = self.get_location_id(act_id, params['location_name'])
        pg_data = str(self.get_cosmo_component(act_id, part_id, params['componentType']))
        # the ast module could not convert data to its dictionary representation therefore using the json module
        if params.get('pg_name') is not None:
            temp = ast.literal_eval(pg_data)
            data = json.loads(temp['data'])
            data['paging_group']['dn_attributes']['Description'] = params['pg_name']
            #Shankara Narayanan. M
            result1,availableExt = self.check_extension_availability(extension='',part_name='')
            if not result1:
                return False
            data['paging_group']['dn_attributes']['DN_formatted'] = availableExt.json()
            data['paging_group']['dn_attributes']['include_in_dial_by_name'] =  params.get('IncludeInDialByName',data['paging_group']['dn_attributes']['include_in_dial_by_name'])
            data['paging_group']['PriorityPage'] = params.get('PriorityPage',data['paging_group']['PriorityPage'])
            data['paging_group']['PriorityPageAudioPath'] = params.get('PriorityPageAudioPath',data['paging_group']['PriorityPageAudioPath'])
            data['paging_group']['RingsPerMember'] = params.get('NoAnswerRings',data['paging_group']['NoAnswerRings'])
            data['paging_group']['PagingDelay'] = params.get('PagingDelay',data['paging_group']['PagingDelay'])
            collections = data['collections']
            #TODO The below step is not clear but is mandatory
            data['paging_group']['VMServerID'] = None
            # finding the id of extension list to use
            extn_list = None
            for e_list in collections['no_mbox_user_extension_list']:
                if params['pg_extn_list'] == e_list['description']:
                    extn_list = e_list['id']
            data['paging_group']['ExtensionListID'] = extn_list
            # converting the dict back to string
            params['data'] = json.dumps(data)
        params['data'] = params['data'].replace("'",'"')
        url = params.pop("url")
        log.info("Creating paging group with args <%s>" % params)
        ret = requests.post(url, data=params, headers=self.headers)
        created_extension = ""
        if ret.status_code == 200 and len(ret.text) == 2:
            log.info("The paging group has been created successfully.Message from server : <%s>" % ret.text)
            created_extension = availableExt.json()
            result = True
        else:
            log.error("Could not create paging group.Message from server : <%s>" % ret.text)
        return result, ret, created_extension

    @func_logger
    def edit_paging_group(self, pg_to_edit, **params):
        '''
        This function will edit a paging group
        phone system -> visual call flow editor -> Select paging group -> Edit
        :return: A tuple of a boolean status flag and the return object from the requested url

        '''
        result = False
        params_xml = self.config.getparams("edit_paging_group")
        params = self.get_param_to_use(params_xml, **params)
        if self.accountId is None:  # switch account has not been called
            act_id = self.get_account_detail(act_name=params['account_name'])
        else:
            act_id = self.accountId
        params["accountId"] = act_id
        if self.part_id is None:
            part_id = self.get_partition_detail(act_id, params['part_name'])
        else:
            part_id = self.part_id
        params["partitionId"] = part_id
        params["profileLocationId"] = self.get_location_id(act_id, params['location_name'])
        # getting the component id
        id = self.get_vcfe_detail(act_id, part_id, pg_to_edit)
        params['id'] = id
        pg_data = str(self.get_cosmo_component(act_id, part_id, params['componentType'], id=id))
        # the ast module could not convert data to its dictionary representation therefore using the json module
        if params.get('pg_name') is not None:
            temp = ast.literal_eval(pg_data)
            data = json.loads(temp['data'])
            data['paging_group']['dn_attributes']['Description'] = params['pg_name']
            data['paging_group']['dn_attributes']['DN_formatted'] = params['pg_extension']
            collections = data['collections']
            # finding the id of extension list to use
            extn_list = None
            for e_list in collections['no_mbox_user_extension_list']:
                if params['pg_extn_list'] == e_list['description']:
                    extn_list = e_list['id']
            data['paging_group']['ExtensionListID'] = extn_list
            # converting the dict back to string
            params['data'] = json.dumps(data)
        params['data'] = params['data'].replace("'", '"')
        url = params.pop("url")
        log.info("Creating paging group with args <%s>" % params)
        ret = requests.post(url, data=params, headers=self.headers)
        if ret.status_code == 200 and len(ret.text) == 2:
            log.info("The paging group has been edited successfully.Message from server : <%s>" % ret.text)
            result = True
        else:
            log.error("Could not edit paging group.Message from server : <%s>" % ret.text)

        return result, ret

    @func_logger
    def delete_paging_group(self, pg_to_delete, **params):
        '''
        This function will delete a paging group
        phone system -> visual call flow editor -> Select paging group -> Delete
        :return: A tuple of a boolean status flag and the return object from the requested url

        '''
        result = False
        params_xml = self.config.getparams("delete_paging_group")
        params = self.get_param_to_use(params_xml, **params)
        if self.accountId is None:  # switch account has not been called
            act_id = self.get_account_detail(act_name=params['account_name'])
        else:
            act_id = self.accountId
        params["accountId"] = act_id
        if self.part_id is None:
            part_id = self.get_partition_detail(act_id, params['part_name'])
        else:
            part_id = self.part_id
        params["partitionId"] = part_id
        # getting the component id
        if params.get('extension'): # Added to delete with extension number! ##MSN
            id = self.get_vcfe_details(act_id, part_id, params.get('extension'))
        else:
            id = self.get_vcfe_detail(act_id, part_id, pg_to_delete)
        params['id'] = id
        params["profileLocationId"] = self.get_location_id(act_id, params['location_name'])
        url = params.pop("url")
        log.info("Deleting paging group with args <%s>" % params)
        ret = requests.post(url, data=params, headers=self.headers)
        if ret.status_code == 200 and ret.json()["message"] == "Component successfully deleted.":
            log.info("The paging group has been deleted successfully.Message from server : <%s>" % ret.text)
            result = True
        else:
            log.error("Could not delete paging group.Message from server : <%s>" % ret.text)
        return result, ret


    @func_logger
    def create_pickup_group(self, **params):
        '''
        This function will create a pickup group
        phone system -> visual call flow editor -> Add -> Pickup Group
        :return: A tuple of a boolean status flag and the return object from the requested url

        Note: There must already be an existing extension list.
        '''

        result = False
        params_xml = self.config.getparams("create_pickup_group")
        params = self.get_param_to_use(params_xml, **params)
        if self.accountId is None:  # switch account has not been called
            act_id = self.get_account_detail(act_name=params['account_name'])
        else:
            act_id = self.accountId
        params["accountId"] = act_id
        if self.part_id is None:
            part_id = self.get_partition_detail(act_id, params['part_name'])
        else:
            part_id = self.part_id
        params["partitionId"] = part_id
        params["profileLocationId"] = self.get_location_id(act_id, params['location_name'])
        pkg_data = str(self.get_cosmo_component(act_id, part_id, params['componentType']))
        # the ast module could not convert data to its dictionary representation therefore using the json module
        if params.get('pkg_name') is not None:
            temp = ast.literal_eval(pkg_data)
            data = json.loads(temp['data'])
            data['pickup_group']['dn_attributes']['Description'] = params['pkg_name']
            result1,availableExt = self.check_extension_availability(extension='',part_name='')
            if not result1:
                return False
            data['pickup_group']['dn_attributes']['DN_formatted'] = availableExt.json()
            collections = data['collections']
            # finding the id of extension list to use
            extn_list = None
            for e_list in collections['no_mbox_user_extension_list']:
                if params['pkg_extensionlist'] == e_list['description']:
                    extn_list = e_list['id']
            data['pickup_group']['ExtensionListID'] = extn_list
            # converting the dict back to string
            params['data'] = json.dumps(data)
        params['data'] = params['data'].replace("'",'"')
        url = params.pop("url")
        log.info("Creating pickup group with args <%s>" % params)
        ret = requests.post(url, data=params, headers=self.headers)
        if ret.status_code == 200 and len(ret.text) == 2:
            log.info("The pickup group has been created successfully.Message from server : <%s>" % ret.text)
            result = True
        else:
            log.error("Could not create pickup group.Message from server : <%s>" % ret.text)

        return result, ret, availableExt.json()

    @func_logger
    def delete_pickup_group(self, pkg_to_delete, **params):
        '''
        This function will delete a pickup group
        phone system -> visual call flow editor -> Select pickup group -> Delete
        :return: A tuple of a boolean status flag and the return object from the requested url

        '''
        result = False
        params_xml = self.config.getparams("delete_pickup_group")
        params = self.get_param_to_use(params_xml, **params)
        if self.accountId is None:  # switch account has not been called
            act_id = self.get_account_detail(act_name=params['account_name'])
        else:
            act_id = self.accountId
        params["accountId"] = act_id
        if self.part_id is None:
            part_id = self.get_partition_detail(act_id, params['part_name'])
        else:
            part_id = self.part_id
        params["partitionId"] = part_id
        # getting the component id
        id = self.get_vcfe_detail(act_id, part_id, pkg_to_delete, Extension=params.get("Extension",""))
        params['id'] = id
        # params["profileLocationId"] = self.get_location_id(act_id, params['location_name'])
        url = params.pop("url")
        log.info("Deleting pickup group with args <%s>" % params)
        ret = requests.post(url, data=params, headers=self.headers)
        if ret.status_code == 200 and ret.json()["message"] == "Component successfully deleted.":
            log.info("The pickup group has been deleted successfully.Message from server : <%s>" % ret.text)
            result = True
        else:
            log.error("Could not delete pickup group.Message from server : <%s>" % ret.text)

        return result, ret


