import sys
import os
import time

boss_path = os.path.dirname(os.path.dirname(__file__))
framework_path = os.path.join(os.path.dirname((os.path.dirname(os.path.dirname(__file__)))),"Framework")
sys.path.append(os.path.join(framework_path,"provisioning_wrappers","boss_wrappers"))
sys.path.append(os.path.join(framework_path,"phone_wrappers"))
sys.path.append(os.path.join(framework_path,"utils"))
from robot.api.logger import console
from robot.api import logger
from boss_api import boss_api
from D2API import D2API
from PhoneComponent import PhoneComponent
from Var import *


class BossApiComponent(object):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self, **api):
        os.environ['NO_PROXY'] = 'portal.sit.shoretel.com/'
        self.boss_obj = None
        self.d2api_obj = None

        parameters = {}
        for k, v in api.items():
            k = str(k)
            v = str(v)
            parameters[k] = v

        if 'ip' in parameters:
            self.d2api_obj = D2API(**parameters)
        else:
            console("Boss Login Parameters")
            console(parameters)
            self.boss_obj = boss_api()
            self.boss_obj.login(**parameters)

    def addProgramableButton(self, **kwargs):
        """
        Below method will call the add programmable button method based on call manager

        :param:
            :self: PhoneComponent object of the phone
            :kwargs: Dictionary for getting the arguments needed:

        :return: None
        :created by: Ramkumar
        """
        if self.d2api_obj:
            self.addD2Button(**kwargs)
        else:
            self.addBossButton(**kwargs)

    def addD2Button(self, **kwargs):
        """
        Below method will add programmable button on phone

        :param:
            :self: PhoneComponent object of the phone
            :kwargs: Dictionary for adding program button needed:
                            button_box: which box you need to program
                            phoneA: user_extension
                            phoneB: target_extension
                            positionValue: softkey position
                            functionKey: function name
                            ring_delay: number of ring delay before alert on monitoring phone
                            show_caller_id: can be set as never, always, while ringing
                            no_connected: with phone in idle state operation to be performed
                            with_connected: with phone in active state operation to performed
                            ConnectedCallFunctionID: For hotline option , we need
        :return: None
        :created by: Ramkumar
        :update by: Ramkumar
        :updated on: 13/01/2019
        """

        button_box = int(kwargs.get('button_box'))
        phoneA = kwargs['phoneA']
        phoneB = kwargs['phoneB']
        phoneExtensionA = str(phoneA.phone_obj.phone_obj.phone.extensionNumber)

        softKeyPosition = int(kwargs['positionValue']) + 1
        extMode = kwargs['extNo']
        if extMode == 'noExtensionValue':
            phoneExtension = ''
            console("Programming " + str(kwargs['functionKey']) + " Button on " + phoneExtensionA + "  with no Extension")
            logger.info("Programming" + str(kwargs['functionKey']) + " Button on " + phoneExtensionA + " with no Extension")
        else:
            phoneExtension = str(phoneB.phone_obj.phone_obj.phone.extensionNumber)
            console("Programming " + str(kwargs['functionKey']) + " Button on " + phoneExtensionA + " with " + phoneExtension + " Extension")
            logger.info("Programming " + str(kwargs['functionKey']) + " Button on " + phoneExtensionA + " with " + phoneExtension + " Extension")

        functionName = str(kwargs['functionKey'])
        label = str(kwargs.get('label', functionName))
        ConnectedCallFunctionID = str(kwargs.get('ConnectedCallFunctionID'))
        availability = str(kwargs.get('availability'))

        if functionName == "Monitor Extension":
            ring_delay = kwargs.get('ring_delay')
            show_caller_id = kwargs.get('show_caller_id')
            no_connected = kwargs.get('no_connected')
            with_connected = kwargs.get('with_connected')

            programSoftKey = {'user_extension':phoneExtensionA ,'button_box': button_box, 'soft_key': softKeyPosition,
                              'function': functionName, 'label': functionName, 'target_extension': phoneExtension,
                              'RingDelayBeforeAlert': ring_delay,
                              'show_caller_id_option': show_caller_id, 'DisconnectedCallFunctionID': no_connected,
                              'ConnectedCallFunctionID': with_connected}

        elif functionName == "Hotline":
            programSoftKey = {'user_extension': phoneExtensionA, 'button_box': button_box, 'soft_key': softKeyPosition,
                              'function': functionName, 'label': label, 'target_extension': phoneExtension,
                              'ConnectedCallFunctionID':ConnectedCallFunctionID}

        elif functionName == "Change Availability":
            programSoftKey = {'user_extension': phoneExtensionA, 'button_box': button_box, 'soft_key': softKeyPosition,
                              'function': functionName, 'label': functionName, 'target_extension': phoneExtension,
                              'availability': availability}

        elif functionName == "Send Digits Over Call":
            digits = str(kwargs.get('digits'))
            programSoftKey = {'user_extension': phoneExtensionA, 'button_box': button_box, 'soft_key': softKeyPosition,
                              'function': functionName, 'label': functionName, 'Digits': digits}

        else:
            programSoftKey = {'user_extension':phoneExtensionA,'button_box': button_box, 'soft_key': softKeyPosition,
                              'function': functionName, 'label': functionName, 'target_extension': phoneExtension}

        if not self.d2api_obj.configure_prog_button(**programSoftKey):
            raise Exception("Could not create " + functionName + " on extension: " + phoneExtensionA)

    def addBossButton(self, **kwargs):
        """
        Below method is used to configure a button on the passed phone object.

        :kwargs:
            :button_box: 0 for configuring on Phone or 1 for configuring on the attached PKM.
            :phoneA: Phone to configure the button on
            functionKey: The function to configure on the button
                If Monitor Extension:

                If Hotline:
                    ConnectedCallFunctionID: Action to Perform i.e., Dial Number or Intercom
            :label: Label to be displayed on the phone. If not specified, function name will be used
            :phoneB: Phone to be for the specified function.
        :param kwargs:
        :return:
        :created by: Ramkumar G.
        :created date:
        :last udpated by: Vikhyat Sharma
        :last updated date:
        """
        button_box = int(kwargs.get('button_box'))
        phoneA = kwargs['phoneA']
        phoneAExtension = str(phoneA.phone_obj.phone_obj.phone.extensionNumber)
        functionName = str(kwargs['functionKey'])
        label = kwargs.get('label', functionName)
        phoneB = kwargs['phoneB']
        softKeyPosition = int(kwargs['positionValue'])

        extMode = kwargs['extNo']
        if extMode == 'noExtensionValue':
            phoneBExtension = ''
            console("Programming " + str(kwargs['functionKey']) + " Button on " + phoneAExtension
                    + " with no Extension on MiCloud Portal")
            logger.info("Programming <b>" + str(kwargs['functionKey']) + "</b> Button on <b>" + phoneAExtension
                        + "</b> with no Extension on MiCloud Portal")
        else:
            phoneBExtension = str(phoneB.phone_obj.phone_obj.phone.extensionNumber)
            console("Programming " + str(kwargs['functionKey']) + " Button on " + phoneAExtension + " with "
                    + phoneBExtension + " Extension using MiCloud Portal")
            logger.info("Programming <b>" + str(kwargs['functionKey']) + "</b> Button on <b>" + phoneAExtension
                        + "</b> with extension" + phoneBExtension + " Extension on MiCloud Portal", html=True)

        if functionName == "Monitor Extension":
            ring_delay = str(kwargs['ring_delay'])
            show_caller_id = str(kwargs['show_caller_id'])
            no_connected = str(kwargs['no_connected'])
            with_connected = str(kwargs['with_connected'])
            programSoftKey = {
                               'extensionToBeProgrammed': phoneAExtension,
                               'button_box': button_box,
                               'soft_key': softKeyPosition,
                               'function': functionName,
                               'label': functionName, 'extension': phoneBExtension,
                               'ring_delay': ring_delay,
                               'show_caller_id': show_caller_id,
                               'no_connected': no_connected,
                               'with_connected': with_connected
                              }

        elif functionName == "Send Digits Over Call":
            digits = str(kwargs.get('digits'))
            programSoftKey = {
                               'extensionToBeProgrammed': phoneAExtension,
                               'button_box': button_box,
                               'soft_key': softKeyPosition,
                               'function': functionName,
                               'label': functionName,
                               'dtmf_digits': digits
                              }
        elif functionName == "Hotline":
            connectedCallFunctionID = str(kwargs['ConnectedCallFunctionID'])
            programSoftKey = {
                               'extensionToBeProgrammed': phoneAExtension, 'button_box': button_box,
                               'soft_key': softKeyPosition, 'function': functionName, 'label': label,
                               'target_extension': phoneBExtension,
                               'call_action': connectedCallFunctionID
                              }
        elif functionName == "Change Availability":
            availability = str(kwargs['availability'])
            programSoftKey = {
                               'extensionToBeProgrammed': phoneAExtension, 'button_box': button_box,
                               'soft_key': softKeyPosition, 'function': functionName, 'label': label,
                               'target_extension': phoneBExtension,
                               'availability': availability
                             }

        else:
            programSoftKey = {
                              'extensionToBeProgrammed': phoneAExtension,
                              'button_box': button_box,
                              'soft_key': softKeyPosition,
                              'function': functionName,
                              'label': functionName,
                              'extension': phoneBExtension
                              }
        time.sleep(1)
        status=self.boss_obj.configure_prog_button(**programSoftKey)[0]

        logger.info("Response Status : "+str(status))
        console("Response Status : "+str(status))

        rerunStatus=False
        if status == False:
            time.sleep(5)
            rerunStatus = self.boss_obj.configure_prog_button(**programSoftKey)[0]
            logger.info("Rerequest Response Status : "+rerunStatus)
            console("Rerequest Response Status : "+rerunStatus)
        else:
            if status == True:
                logger.info("Configured <b>" + functionName + "</b> Button on extension: "
                            + phoneAExtension, html=True)
                console("Configured " + functionName + " Button on extension: "
                        + phoneAExtension)
            elif rerunStatus==True:
                logger.info("Configured <b>" + functionName + "</b> Button on extension: "
                            + phoneAExtension, html=True)
                console("Configured " + functionName + " Button on extension: "
                        + phoneAExtension)
            else:
                raise Exception("Could not Configured " + functionName + " Button on extension: "
                                + phoneAExtension)

        # if self.boss_obj.configure_prog_button(**programSoftKey)[0]:
        #     logger.info("Configured <b>" + functionName + "</b> Button on extension: "
        #                 + phoneAExtension, html=True)
        #     console("Configured " + functionName + " Button on extension: "
        #             + phoneAExtension)
        # else:
        #     raise Exception("Could not Configured " + functionName + " Button on extension: "
        #                     + phoneAExtension)

    def removeProgramableButton(self, **kwargs):
        '''
        Below method will call the remove programmable button method based on call manager

        :param:
            :self: PhoneComponent object of the phone
            :kwargs: Dictionary for getting the arguments needed:

        :return: None
        :created by: Ramkumar
        '''
        if self.d2api_obj:
            return self.removeD2Button(**kwargs)
        else:
            return self.removeBossButton(**kwargs)

    def removeD2Button(self, **kwargs):
        '''
        Ram
        '''
        button_box = int(kwargs.get('button_box'))
        phoneA = kwargs['phoneA']
        phoneExtension= str(phoneA.phone_obj.phone_obj.phone.extensionNumber)
        softKeyPosition = int(kwargs['positionValue']) + 1
        removeSoftKey = {'user_extension':phoneExtension, 'button_box':button_box, 'soft_key':softKeyPosition}

        console("Removing programmed Button on " + phoneExtension)
        logger.info("Removing programmed Button on " + phoneExtension)
        return self.d2api_obj.Unconfigure_prog_button(**removeSoftKey)

    def removeBossButton(self, **kwargs):
        """
        This method will remove the softkey configured on phone using boss portal
        :param:
                :self: PhoneComponent object of the phone
                :kwargs: Dictionary for getting the arguments needed:

        :return: None
        :created by: Milind Patil
        :creation date: 21/01/2021
        :last update by:
        :last update date:
        """
        phone = kwargs['phoneA']
        phoneExtension = str(phone.phone_obj.phone_obj.phone.extensionNumber)
        button_box = int(kwargs.get('button_box',0))
        softKeyPosition = int(kwargs['positionValue'])
        removeSoftKey = {'extensionToBeProgrammed': phoneExtension,
                         'button_box': button_box,
                         'soft_key': softKeyPosition}

        console("Removing programmed Button on Extension : " + phoneExtension + " at Softkey Position : " + str(
            softKeyPosition))
        logger.info("Removing programmed Button on Extension : " + phoneExtension + " at Softkey Position : " + str(
            softKeyPosition))
        return self.boss_obj.clear_prog_button(**removeSoftKey)

    def createHuntGroup(self, **kwargs):
        """
        This method will call the create huntgroup method based on call manager
        :param:
            :self: PhoneComponent object of the phone
            :kwargs: Dictionary for getting the arguments needed:

        :return: None
        :created by: Ramkumar
        """
        if self.d2api_obj:
            return self.createD2HuntGroup(**kwargs)
        else:
            return self.createBossHuntGroup(**kwargs)


    def createD2HuntGroup(self, **kwargs):
        """
        This method will creates huntgroup on MiVoice Connect Call Manager.

        :param:
            :self: PhoneComponent object of the phone
            :kwargs: Dictionary for getting the arguments needed:

        :return: None
        :created by: Ramkumar. G
        :creation date:
        :last update by:
        :last update date:
        """
        Extension = kwargs["BackupExtension"]
        BackupExtension = int(Extension.phone_obj.phone_obj.phone.extensionNumber)
        Members = kwargs["GroupMembers"]

        GroupMembers=[]
        for data in Members[:]:
            GroupMembers.append(data.phone_obj.phone_obj.phone.extensionNumber)

        GroupName = str(kwargs["GroupName"])
        IncludeInSystemDialByName = bool(kwargs.get('IncludeInSystem', True))

        ExtensionPrivate = kwargs.get("MakeExtnPrivate", False)
        MakeExtensionPrivate = bool(True) if ExtensionPrivate == u'True' else bool(False)

        HuntPatternID = int(kwargs.get('HuntPattern', 1))
        RingsPerMember = int(kwargs.get('RingsPerMember', 3))
        NoAnswerRings = int(kwargs.get('NoAnswerRings', 4))
        CallForwarding=bool(kwargs.get('CallMemberWhenForwarding', True))
        CallMemberWhenForwarding = bool(True) if CallForwarding == u'True' else bool(False)

        SkipMember=kwargs.get('SkipMemberOnCall', True)
        SkipMemberIfAlreadyOnCall = bool(True) if SkipMember == u'True' else bool(False)

        CallStackFull1 = kwargs.get('CallStackFull', '')
        if CallStackFull1 =='':
            CallStackFull = str(CallStackFull1)
        else:
            CallStackFull = int(CallStackFull1.phone_obj.phone_obj.phone.extensionNumber)

        NoAnswer1 = kwargs.get('NoAnswer', '')
        if NoAnswer1 == '':
            NoAnswer = str(NoAnswer1)
        else:
            NoAnswer = int(NoAnswer1.phone_obj.phone_obj.phone.extensionNumber)

        console("Creating Hunt group " + GroupName + " for member/s " + str(GroupMembers))
        logger.info("Creating Hunt group " + GroupName + " for member/s " + str(GroupMembers))

        addHuntGroup = {'BackupExtension':BackupExtension,'HuntGroupMember':GroupMembers,'HuntGroupName':GroupName,
                        'IncludeInSystemDialByName':IncludeInSystemDialByName,'MakeExtensionPrivate':MakeExtensionPrivate,
                        'HuntPatternID':HuntPatternID,'RingsPerMember':RingsPerMember,'CallMemberWhenForwarding':CallMemberWhenForwarding,
                        'SkipMemberIfAlreadyOnCall':SkipMemberIfAlreadyOnCall,'CallStackFull':CallStackFull,
                        'NoAnswer':NoAnswer,'NoAnswerRings':NoAnswerRings}

        huntGroupNumber = self.d2api_obj.create_modify_hunt_group(**addHuntGroup)
        time.sleep(60)    #adding wait cos hunt group will take time to activate
        return huntGroupNumber

    def createBossHuntGroup(self, **kwargs):
        """
        This method is used to create Hunt Group on the MiCloud portal using the parameters passed.
        :param:
            :kwargs: Dictionary:
                     :GroupName: Hunt Group Name
                     :BackupExtension: Phone object to be used as backup
                     :GroupMembers: Members of the hunt group
                     :IncludeInSystem: Include in system directory i.e., True or False
                     :HuntPattern: Hunt Pattern to choose i.e., 1 for Top/Down and 4 for Simultaneous
                     :RingsPerMember: Number of rings on each member i.e., 1 or 2 or 3 etc
                     :NoAnswerRings: Cycles before disconnecting the call i.e., 1 or 2 or 3 etc
                     :CallMemberWhenForwarding: To call mwmber when forwarding i.e., True or False
                     :SkipMemberOnCall: To skip member if already on call i.e., True or False

        :return: Hunt Group Extension
        :created by: Vikhyat Sharma
        :creation date: 13/02/2020
        :last update by:
        :last update date:
        """
        huntGroupName = str(kwargs['GroupName'])
        backupExtension = str(kwargs['BackupExtension'].phone_obj.phone_obj.phone.extensionNumber)

        groupMembers = list()
        for member in kwargs['GroupMembers']:
            groupMembers.append(str(member.phone_obj.phone_obj.phone.extensionNumber))

        includeInSystem = bool(kwargs['IncludeInSystem'])
        huntPatternID = int(kwargs['HuntPattern'])    # 1 for Top down ; 4 for Simultaneous
        ringsPerMember = int(kwargs['RingsPerMember'])
        noAnswerRings = int(kwargs['NoAnswerRings'])
        callMemberWhenForwarding = bool(kwargs['CallMemberWhenForwarding'])
        skipMemberIfOnCall = bool(kwargs['SkipMemberOnCall'])

        logger.info("Creating Hunt group <b>" + huntGroupName + "</b> for member/s <b>" + str(groupMembers) + "</b>",
                    html=True)
        console("Creating Hunt group: " + huntGroupName + " for member/s " + str(groupMembers))

        addHuntGroup = {
                        'hg_backup_extn': backupExtension,
                        'HuntGroupMember': groupMembers,
                        'hg_name': huntGroupName,
                        'IncludeInSystemDialByNameDirectory': includeInSystem,
                        'HuntPatternID': huntPatternID,
                        'RingsPerMember': ringsPerMember,
                        'NoAnswerRings': noAnswerRings,
                        'CallMemberWhenForwarding': callMemberWhenForwarding,
                        'SkipMemberIfAlreadyOnCall': skipMemberIfOnCall
                        }

        result = self.boss_obj.create_hunt_group(**addHuntGroup)
        if result[0]:
            logger.info("Hunt Group created with extension: <b>" + result[-1] + "</b>"
                        , html=True)
            console("Hunt Group created with extension: " + result[-1])
            return result[-1]
        else:
            raise Exception("Hunt Group could not be created !!")

    def deleteHuntGroup(self, **kwargs):
        if self.d2api_obj:
            return self.removeD2HuntGroup(**kwargs)
        else:
            self.removeBossHuntGroup(**kwargs)

    def removeD2HuntGroup(self,**kwargs):
        """
        Ram
        :param kwargs:
        :return:
        """

        extension = kwargs["number"]
        console("Removing " + str(extension) + " Hunt group extension")
        logger.info("Removing " + str(extension) + " Hunt group extension")
        return self.d2api_obj.delete_hunt_group(extension)

    def removeBossHuntGroup(self, **kwargs):
        """
        The method deletes the hunt group from the MiCloud portal.
        :param:
                :kwargs: Dictionary
                         :number: Hunt Group extension to delete
        :return: None
        :created by: Vikhyat Sharma
        :creation date: 20/02/2020
        :last update by:
        :last update date:
        """
        huntGroupNum = str(kwargs.get("number"))

        result = self.boss_obj.delete_hunt_group(hg_to_delete='', extension=huntGroupNum)

        if result[0]:
            logger.info("Hunt Group with extension <b>" + huntGroupNum + "</b> has been deleted successfully."
                        , html=True)
            console("Hunt Group with extension " + huntGroupNum + " has been deleted successfully.")
        else:
            raise Exception("Hunt Group with extension " + huntGroupNum + " could not be deleted !!")

    def createPagingGroups(self, **kwargs):
        if self.d2api_obj:
            return self.createD2PagingGroups(**kwargs)
        else:
            return self.createBossPagingGroups(**kwargs)


    def createD2PagingGroups(self, **kwargs):
        """

        :param kwargs:
        :return:
        """

        PagingGroupName = str(kwargs["PagingGroupName"])
        PageListName = str(kwargs['PageListName'])
        Members = kwargs["GroupMembers"]
        GroupMembers = []
        for data in Members[:]:
            GroupMembers.append(data.phone_obj.phone_obj.phone.extensionNumber)
        PagingDelay = str(kwargs.get('PagingDelay','1'))
        PriorityPage = str(kwargs.get('PriorityPage','False'))
        RingsPerMember = str(kwargs.get('RingsPerMember',3))
        ExtensionPrivate = kwargs.get('MakeExtensionPrivate', False)
        MakeExtensionPrivate = bool(True) if ExtensionPrivate == u'True' else bool(False)

        PriorityPageAudioPath = int(kwargs.get('PriorityPageAudioPath',1))

        page_list = {'name': PagingGroupName, 'extension_numbers': GroupMembers}

        console("Creating "+ PagingGroupName + " Paging group for " + str(GroupMembers) +" group members" )
        logger.info("Creating "+ PagingGroupName + " Paging group for " + str(GroupMembers) +" group members" )

        pagingGroup = {'PagingGroupName': PagingGroupName, 'PageListName': PageListName, 'PagingDelay': PagingDelay,
                       'PriorityPage': PriorityPage, 'RingsPerMember': RingsPerMember,
                       'MakeExtensionPrivate': MakeExtensionPrivate,
                       'PriorityPageAudioPath': PriorityPageAudioPath}

        self.d2api_obj.create_page_list(**page_list)
        return self.d2api_obj.create_paging_group(**pagingGroup)

    def createBossPagingGroups(self, **kwargs):
        """
        Below method creates a Paging group on the MiCloud Connect Director.
        :param:
                :kwargs: Dictionary
                         :PagingGroupName: Name of the paging group
                         :PageListName: Extension List Name to use for paging group
                         :Location: Value for Location Parameter
                         :GroupMembers: Members for the extension list
                         :MakeExtensionPrivate: Make paging extension available in directory i.e., True or False
                         :PagingDelay: Delay in Paging
                         :PriorityPage: Prioritize Paging Group i.e., True or False
                         :RingsPerMember: Number of rings before forwarding to the next member
                         :PriorityPageAudioPath: Value for the Group Page deliverable
                                                 i.e., 1 for speakerphone and 2 for Active audio path

        :return: Paging Group Extension
        :created by: Vikhyat Sharma
        :creation date: 19/02/2020
        :last update by:
        :last update date:
        """

        groupName = str(kwargs.get('PagingGroupName'))
        extensionListName = str(kwargs.get('PageListName'))
        location = str(kwargs.get('Location', miCloudLocation))
        groupMembers = list()
        for member in kwargs['GroupMembers']:
            groupMembers.append(str(member.phone_obj.phone_obj.phone.extensionNumber))

        includeInDirectory = bool(kwargs.get('MakeExtensionPrivate', False))
        pagingDelay = int(kwargs.get('PagingDelay', 4))
        priorityPage = bool(kwargs.get('PriorityPage', False))
        ringsPerMember = int(kwargs.get('RingsPerMember', 4))
        priorityPageAudioPath = int(kwargs.get('PriorityPageAudioPath', 2))

        pagingList = {'el_name': extensionListName, 'el_extns': groupMembers}
        self.boss_obj.create_extension_list(**pagingList)

        pagingGroup = {
                        'location_name': location,
                        'pg_name': groupName,
                        'pg_extn_list': extensionListName,
                        'PriorityPage': priorityPage,
                        'PriorityPageAudioPath': priorityPageAudioPath,
                        'NoAnswerRings': ringsPerMember,
                        'PagingDelay': pagingDelay,
                        'IncludeInDialByName': includeInDirectory
                       }

        result = self.boss_obj.create_paging_group(**pagingGroup)

        if result[0]:
            return str(result[-1])
        else:
            raise Exception("Paging Group could not be created !!")

    def deletePagingGroups(self, **kwargs):
        if self.d2api_obj:
            return self.deleteD2PagingGroups(**kwargs)
        else:
            return self.deleteBossPagingGroups(**kwargs)

    def deleteD2PagingGroups(self, **kwargs):
        """
        Ram
        """
        extension = str(kwargs["number"])
        extensionList = str(kwargs['pagingListName'])
        console("Deleting " + extension + " paging group extension")
        logger.info("Deleting " + extension + " paging group extension")
        self.d2api_obj.delete_paging_group(extension)
        return self.d2api_obj.delete_page_list(extensionList)

    def deleteBossPagingGroups(self, **kwargs):
        """
        The method deletes the paging group and the extension list associated with it.

        :param:
                :kwargs: Dictionary
                         :number: Paging Group Number to delete
                         :location: Location Parameter
                         :pagingListName: Extension List to delete
        :return: None
        :created by: Vikhyat Sharma
        :creation date: 19/02/2020
        :last update by: Milind Patil
        :last update date: 21/01/2021
        """

        pagingGroupExtension = str(kwargs.get("number"))
        location = str(kwargs.get("location", miCloudLocation))
        listName = str(kwargs.get("pagingListName"))

        deletePagingGroup = {
                             'pg_to_delete': '',
                             'location_name': location,
                             'extension': pagingGroupExtension
                            }

        groupResult = self.boss_obj.delete_paging_group(**deletePagingGroup)

        if groupResult[0]:
            logger.info("Paging Group with extension <b>" + pagingGroupExtension
                        + "</b> has been deleted successfully.", html=True)
            console("Paging Group with extension " + pagingGroupExtension + " has been deleted successfully.")
        else:
            raise Exception("Paging Group with extension " + pagingGroupExtension + " could not be deleted !!")

        listResult = self.boss_obj.delete_extension_list(el_to_delete=listName)

        if listResult[0]:
            logger.info("Extension list :<b>" + listName
                        + "</b> has been deleted successfully.", html=True)
            console("Extension list :<b>" + listName + " has been deleted successfully.")
        else:
            raise Exception("Extension list :" + listName + " could not be deleted !!")

    def removeCallAppearance(self, **kwargs):
        if self.d2api_obj:
            return self.D2removeCallAppearance(**kwargs)
        else:
            return self.BossremoveCallAppearance(**kwargs)


    def D2removeCallAppearance(self, **kwargs):
        '''
        Anuj Giri
        '''

        value = int(kwargs["value"])
        extn = kwargs["user_extension"]
        user_extension = extn.phone_obj.phone_obj.phone.extensionNumber

        if (extn.phone_obj.phone_obj.phone_type == "Mitel6920"):
            console("Remove call apearance button on " + str(user_extension))
            logger.info("Remove call apearance button on " + str(user_extension))
            for leaveCall in range(6 - value):
                value += 1
                programSoftKey = {'user_extension': user_extension, 'button_box': 0,
                                  'soft_key': value,
                                  'function': "Unused", 'label': "", 'target_extension': ""}
                self.d2api_obj.configure_prog_button(**programSoftKey)

        elif (extn.phone_obj.phone_obj.phone_type == "Mitel6930"):
            console("Remove call appearance button on " + str(user_extension))
            logger.info("Remove call appearance button on " + str(user_extension))
            for leaveCall in range(12 - value):
                value += 1
                programSoftKey = {'user_extension': user_extension, 'button_box': 0,
                                  'soft_key': value,
                                  'function': "Unused", 'label': "", 'target_extension': ""}
                self.d2api_obj.configure_prog_button(**programSoftKey)

    def BossremoveCallAppearance(self, **kwargs):
        pass

    def addCallAppearance(self, **kwargs):
        if self.d2api_obj:
            self.D2addCallAppearance(**kwargs)
        else:
            self.BossaddCallAppearance(**kwargs)

    def D2addCallAppearance(self, **kwargs):
        """
        This method removes the programmed keys on the MiVoice Connect phones.

        :params:
            :user_extension (PhoneComponent Object): Phone to remove Programmed keys

        :return: None
        :created by:
        :creation date:
        :last update by: Vikhyat Sharma
        :last update date: 17/12/2020
        """
        phoneObj = kwargs["user_extension"]
        userExtension = phoneObj.phone_obj.phone_obj.phone.extensionNumber

        logger.info("Clearing Programmed soft-keys on extension: <b>{}</b>".format(userExtension), html=True)
        console("Clearing Programmed soft-keys on extension: {}".format(userExtension))

        for value in range(1, 7):
            programSoftKey = {'user_extension': userExtension, 'button_box': 0,
                              'soft_key': value,
                              'function': "Call Appearance", 'label': "", 'target_extension': ""}
            self.d2api_obj.configure_prog_button(**programSoftKey)

    def BossaddCallAppearance(self, **kwargs):
        """
        The method removes all the programmed buttons on the MiCloud phone.
        :param:
                :kwargs: Dictionary
                         :user_extension: Phone to add call appearances on
        :return: None
        :created by: Vikhyat Sharma
        :creation date: 20/02/2020
        :last update by: Milind Patil
        :last update date: 17/12/2020
        """
        phone = kwargs.get("user_extension")
        userExtension = str(phone.phone_obj.phone_obj.phone.extensionNumber)
        logger.info("Clearing Programmed soft-keys on extension: <b>{}</b>".format(userExtension), html=True)
        console("Clearing Programmed soft-keys on extension: {}".format(userExtension))

        for position in range(0, 6):
            removeSoftKey = {'extensionToBeProgrammed': userExtension,
                             'button_box': 0,
                             'soft_key': position}
            self.boss_obj.clear_prog_button(**removeSoftKey)

    def cosFeature(self,**kwargs):
        """
        Ram

        """
        if self.d2api_obj:
            return self.D2configCosFeature(**kwargs)
        else:
            return self.BossconfigCosFeature(**kwargs)

    def D2configCosFeature(self,**kwargs):
        name = kwargs['Name']
        MaxCallStackDepth = kwargs.get('MaxCallStackDepth',10)
        MaxBuddiesPerUser = kwargs.get('MaxBuddiesPerUser',40)
        MaxPrivateContacts = kwargs.get('MaxPrivateContacts',30)
        MaxPartiesMakeMeConference = kwargs.get('MaxPartiesMakeMeConference',8)
        AllowCallPickupExtension = (kwargs.get('AllowCallPickup',True))
        AllowCallTransferTrunkToTrunk = kwargs.get('AllowTrunkToTrunkTransfer',True)
        AllowPaging = kwargs.get('AllowOverheadAndGroupPaging',True)
        AllowHuntBusyOut = kwargs.get('AllowHuntGroupBusy',True)
        EnableEnumHeldCalls4Unpark = kwargs.get('EnumHeldCallsForUnpark',True)
        AllowPSTNFailover= kwargs.get('AllowPSTNFailover',True)
        AllowDiffExtPrefixCalls = kwargs.get('ShowExtensions',True)
        AllowHotDesk = kwargs.get('AllowExtensionReassignment',True)
        AllowViewPresence =kwargs.get('ShowCallerIDForOtherExtension',True)
        AllowBridgeUse = kwargs.get('AllowCollaborationFeatures',True)
        AllowRecordingOwnCalls=kwargs.get('AllowRecordingOwnCalls',True)
        AllowCallNotes=kwargs.get('AllowCallNotes',True)
        ShowCallHistory=kwargs.get('ShowCallHistory',True)
        AllowInterSiteVideoCalls= kwargs.get('AllowInterSiteVideoCalls',True)
        AllowChangeOwnCHMode =kwargs.get('AllowCurrentAvailabilityStateChanges',True)
        AllowChangeOwnCHSettings= kwargs.get('AllowCurrentAvailabilityStateDetailChanges',True)
        AllowProgramOwnButtons= kwargs.get('AllowCustomizationIP',True)
        AllowUploadofPerContacts= kwargs.get('AllowUploadToServer',True)

        #Intercom
        AllowIntercomPaging = kwargs.get('AllowIntercomInitiation',True)

        AcceptIntercomPagingDN1 = kwargs.get('IntercomUserExtension')
        if AcceptIntercomPagingDN1:
            AcceptIntercomPagingDN= AcceptIntercomPagingDN1.phone_obj.phone_obj.phone.extensionNumber
        else:
            AcceptIntercomPagingDN = None

        AcceptIntercomPaging = kwargs.get('IntercomAccept',1)

        AcceptIntercomPagingDN_formatted1 = kwargs.get('IntercomTargetExtension','')
        if AcceptIntercomPagingDN_formatted1:
            AcceptIntercomPagingDN_formatted = AcceptIntercomPagingDN_formatted1.phone_obj.phone_obj.phone.extensionNumber
        else:
            AcceptIntercomPagingDN_formatted = None

        #Silent Monitor
        AllowSilentMonitor = kwargs.get('AllowSilentMonitorInitiation',True)

        AcceptSilentMonitorDN1 = kwargs.get('SilentMonitorUserExtension')
        if AcceptSilentMonitorDN1:
            AcceptSilentMonitorDN = AcceptSilentMonitorDN1.phone_obj.phone_obj.phone.extensionNumber
        else:
            AcceptSilentMonitorDN = None

        AcceptSilentMonitor = kwargs.get('SilentMonitorAccept',1)

        AcceptSilentMonitorDN_formatted1 = kwargs.get('SilentMonitorTargetExtension')
        if AcceptSilentMonitorDN_formatted1:
            AcceptSilentMonitorDN_formatted = AcceptSilentMonitorDN_formatted1.phone_obj.phone_obj.phone.extensionNumber
        else:
            AcceptSilentMonitorDN_formatted = None

        #Whisper
        AllowWhisperPaging = kwargs.get('AllowWhisperInitiation',True)

        AcceptWhisperPagingDN1 = kwargs.get('WhisperUserExtension')
        if AcceptWhisperPagingDN1:
            AcceptWhisperPagingDN = AcceptWhisperPagingDN1.phone_obj.phone_obj.phone.extensionNumber
        else:
            AcceptWhisperPagingDN = None

        AcceptWhisperPaging = kwargs.get('WhisperAccept',1)

        AcceptWhisperPagingDN_formatted1 = kwargs.get('WhisperTargetExtension')
        if AcceptWhisperPagingDN_formatted1:
            AcceptWhisperPagingDN_formatted = AcceptWhisperPagingDN_formatted1.phone_obj.phone_obj.phone.extensionNumber
        else:
            AcceptWhisperPagingDN_formatted = None

        #Barge in
        AllowBargeIn = kwargs.get('AllowBargeInInitiation',True)

        AcceptBargeInDN1 = kwargs.get('BargeInUserExtension')
        if AcceptBargeInDN1:
            AcceptBargeInDN = AcceptBargeInDN1.phone_obj.phone_obj.phone.extensionNumber
        else:
            AcceptBargeInDN = None

        AcceptBargeIn = kwargs.get('BargeInAccept',1)

        AcceptBargeInDN_formatted1 = kwargs.get('BargeInTargetExtension')
        if AcceptBargeInDN_formatted1:
            AcceptBargeInDN_formatted = AcceptBargeInDN_formatted1.phone_obj.phone_obj.phone.extensionNumber
        else:
            AcceptBargeInDN_formatted = None

        #Allow external call forwarding
        AllowCallForwardExternal = kwargs.get('AllowExternalCall',True)
        AllowPSTNAnyphone = kwargs.get('AllowExternalAssignment',True)
        AllowRingAll = kwargs.get('AllowAdditionalPhones',True)
        CFENScopeID = kwargs.get('Scope',9)
        CFENRestrictions = kwargs.get('Restrictions','')
        CFENExceptions = kwargs.get('Permissions','')

        #Allow Record others call
        AllowRecordingOthersCalls = kwargs.get('AllowRecordOtherCalls',True)
        AcceptRecordingOthersCalls = kwargs.get('AllowRecordAccept',0)

        AcceptRecordingOthersDN_formatted1 = kwargs.get('AllowRecordTargetExtension')
        if AcceptRecordingOthersDN_formatted1:
            AcceptRecordingOthersDN_formatted = AcceptRecordingOthersDN_formatted1.phone_obj.phone_obj.phone.extensionNumber
        else:
            AcceptRecordingOthersDN_formatted = None


        COS_features = {"name":name,"MaxCallStackDepth":MaxCallStackDepth,"MaxBuddiesPerUser":MaxBuddiesPerUser,
                       "MaxPrivateContacts":MaxPrivateContacts,"MaxPartiesMakeMeConference":MaxPartiesMakeMeConference,
                       "AllowCallPickupExtension":AllowCallPickupExtension,"AllowCallTransferTrunkToTrunk":AllowCallTransferTrunkToTrunk,
                       "AllowPaging":AllowPaging,"AllowHuntBusyOut":AllowHuntBusyOut,"EnableEnumHeldCalls4Unpark":EnableEnumHeldCalls4Unpark,
                       "AllowPSTNFailover":AllowPSTNFailover,"AllowDiffExtPrefixCalls":AllowDiffExtPrefixCalls,"AllowHotDesk":AllowHotDesk,
                       "AllowViewPresence":AllowViewPresence,"AllowBridgeUse":AllowBridgeUse,"AllowRecordingOwnCalls":AllowRecordingOwnCalls,
                       "AllowCallNotes":AllowCallNotes,"ShowCallHistory":ShowCallHistory,"AllowInterSiteVideoCalls":AllowInterSiteVideoCalls,
                       "AllowChangeOwnCHMode":AllowChangeOwnCHMode,"AllowChangeOwnCHSettings":AllowChangeOwnCHSettings,
                       "AllowProgramOwnButtons":AllowProgramOwnButtons,"AllowIntercomPaging":AllowIntercomPaging,
                       "AcceptIntercomPagingDN":AcceptIntercomPagingDN,"AcceptIntercomPaging":AcceptIntercomPaging,
                       "AcceptIntercomPagingDN_formatted":AcceptIntercomPagingDN_formatted,"AllowSilentMonitor":AllowSilentMonitor,
                       "AcceptSilentMonitorDN":AcceptSilentMonitorDN,"AcceptSilentMonitor":AcceptSilentMonitor,
                       "AcceptSilentMonitorDN_formatted":AcceptSilentMonitorDN_formatted,"AllowWhisperPaging":AllowWhisperPaging,
                       "AcceptWhisperPagingDN":AcceptWhisperPagingDN,"AcceptWhisperPaging":AcceptWhisperPaging,
                       "AcceptWhisperPagingDN_formatted":AcceptWhisperPagingDN_formatted,"AllowBargeIn":AllowBargeIn,
                       "AcceptBargeInDN":AcceptBargeInDN,"AcceptBargeIn":AcceptBargeIn,"AcceptBargeInDN_formatted":AcceptBargeInDN_formatted,
                       "AllowCallForwardExternal":AllowCallForwardExternal,"AllowPSTNAnyphone":AllowPSTNAnyphone,
                       "AllowRingAll":AllowRingAll,"CFENScopeID":CFENScopeID,
                       "CFENRestrictions":CFENRestrictions,"CFENExceptions":CFENExceptions,
                       "AllowRecordingOthersCalls":AllowRecordingOthersCalls,
                       "AcceptRecordingOthersCalls":AcceptRecordingOthersCalls,
                       "AcceptRecordingOthersDN_formatted":AcceptRecordingOthersDN_formatted,
                        "AllowUploadofPerContacts":AllowUploadofPerContacts}


        COSfeatures1 = {k: v for k, v in COS_features.items() if v is not None}
        COSfeatures = {}
        for k, v in COSfeatures1.items():
            if v == 'True':
                COSfeatures[k] = bool(v)
            elif v == u'False':
                COSfeatures[k] = False
            else:
                COSfeatures[k] = v
        return self.d2api_obj.change_telephony_feature_permission(**COSfeatures)

    def BossconfigCosFeature(self, **kwargs):
        logger.warn("COS Features are enabled by default. If TC is disabling something, it will not work for MiCloud")

    def configBCA(self, **kwargs):
        """
         Below method will configure Boss/dD2API BCA based on object passed
        :return: Nothing
        """
        if self.d2api_obj:
            self.D2configBCA(**kwargs)
        else:
            self.BossconfigBCA(**kwargs)

    def D2configBCA(self,**kwargs):
        """
        Ram
        :param kwargs:
        :return:
        """
        phone = kwargs['user_extension']
        user_extension = str(phone.phone_obj.phone_obj.phone.extensionNumber)
        button_box = int(kwargs['button_box'])
        soft_key = int(kwargs['soft_key'])+1
        function = str(kwargs['function'])
        label = str(kwargs['label'])
        target_extension = str(kwargs['target_extension'])
        RingDelayBeforeAlert = str(kwargs.get('RingDelayBeforeAlert'))
        CallStackPosition = int(kwargs.get('CallStackPosition',1))
        phone1 = kwargs.get('DialExtension','')
        logger.info("Creating BCA extension <b>{}</b> on Program Key: <b>{}</b> of extension: <b>{}</b>".format(
                    target_extension, soft_key, user_extension), html=True)
        console("Creating BCA extension {} on Program Key: {} of extension: {}".format(target_extension, soft_key,
                                                                                       user_extension))
        if phone1 =='':
            DialExtension = str(phone1)
        else:
            DialExtension = str(phone1.phone_obj.phone_obj.phone.extensionNumber)
        show_caller_id_option = str(kwargs.get('show_caller_id_option','always'))

        EnableAutoAnswerWhenRinging1= kwargs.get('EnableAutoAnswerWhenRinging',True)
        if EnableAutoAnswerWhenRinging1 == "True":
            EnableAutoAnswerWhenRinging = bool(EnableAutoAnswerWhenRinging1)
        else:
            EnableAutoAnswerWhenRinging = str(EnableAutoAnswerWhenRinging1)

        SecondaryType = str(kwargs.get('SecondaryType','Dial tone'))



        programSoftKey = {"user_extension": user_extension, "button_box": button_box, "soft_key": soft_key, "function": function,
                          "label": label,"SecondaryType":SecondaryType,
                          "target_extension": target_extension,"show_caller_id_option":show_caller_id_option,
                          "RingDelayBeforeAlert": RingDelayBeforeAlert, "CallStackPosition": CallStackPosition,
                          "DialExtension": DialExtension,"EnableAutoAnswerWhenRinging":EnableAutoAnswerWhenRinging}

        return self.d2api_obj.configure_prog_button(**programSoftKey)

    def BossconfigBCA(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        phone = kwargs['user_extension']
        userExtension = str(phone.phone_obj.phone_obj.phone.extensionNumber)
        buttonBox = int(kwargs['button_box'])
        softKeyPosition = int(kwargs['soft_key'])
        label = str(kwargs['label'])
        targetExtension = str(kwargs['target_extension'])
        ringDelayBeforeAlert = str(kwargs.get('RingDelayBeforeAlert', 'none'))
        callStackPosition = int(kwargs.get('CallStackPosition', 1))
        notConnectedAction = str(kwargs.get('SecondaryType'))

        if notConnectedAction != '':
            if notConnectedAction == 'Dial Tone':
                notConnectedAction = '2'
            elif notConnectedAction == 'Answer Only':
                notConnectedAction = '3'
            else:
                raise Exception("Not Supported Action Passed for Option : SECONDARY ACTION while "
                                "configuring BCA.")

        showCallerID = str(kwargs.get('show_caller_id_option', 'always'))
        allowAutoAnswer = int(bool(kwargs.get('EnableAutoAnswerWhenRinging', 'True')))

        logger.info("Creating BCA extension <b>{}</b> on Program Key: <b>{}</b> of extension: <b>{}</b>".format(
                    targetExtension, softKeyPosition, userExtension), html=True)
        console("Creating BCA extension {} on Program Key: {} of extension: {}".format(targetExtension, softKeyPosition,
                                                                                       userExtension))

        programSoftKey = {
                          "extensionToBeProgrammed": userExtension, "button_box": buttonBox, "soft_key": softKeyPosition,
                          "function": 'BRIDGE CALL APPEARANCE', "label": label, 'extension': targetExtension,
                          "ring_delay": ringDelayBeforeAlert, "show_caller_id": showCallerID,
                          "allow_auto_answer": allowAutoAnswer, "CallStackPosition": callStackPosition,
                          "bca_not_connected_call_acton": notConnectedAction, "no_connected": "intercom",
                          "with_connected": "unused"
                         }

        if self.boss_obj.configure_prog_button(**programSoftKey)[0]:
            logger.info("Successfully configured BCA Button with BCA extension <b>" + targetExtension +
                        "</b> on the extension <b>" + userExtension + "</b> on softkey <b>" + str(softKeyPosition) +
                        "</b>", html=True)
            console("Successfully configured BCA Button with BCA extension" + targetExtension +
                    "on the extension " + userExtension)
        else:
            raise Exception("Could not configure BCA Button on extension " + userExtension)

    def createBCA(self,**kwargs):
        """
        Ram
        :param kwargs:
        :return:
        """
        if self.d2api_obj:
            return self.D2CreateBCA(**kwargs)
        else:
            return self.BossCreateBCA(**kwargs)

    def D2CreateBCA(self,**kwargs):
        '''
        Ram
        '''

        name = kwargs.get("name") or str(kwargs.get("extension"))
        phone = kwargs["backupExtn"]

        BackupDN = int(phone.phone_obj.phone_obj.phone.extensionNumber)

        SwitchID = int(kwargs.get("switch",2))
        CallStack= int(kwargs.get("callStackDepth",2))
        NoAnswerRings = int(kwargs.get("forwardAfter",2))

        CFBusy1 = kwargs.get("callStackFull",'')
        if CFBusy1 =='':
            CFBusy = str(CFBusy1)
        else:
            CFBusy = int(CFBusy1)

        CFNoAnswer1 = kwargs.get("noAnswer", '')
        if CFNoAnswer1 == '':
            CFNoAnswer = str(CFNoAnswer1)
        else:
            CFNoAnswer = int(CFNoAnswer1)

        OutCallerID1 = kwargs.get("outboundCallerID", '')
        if OutCallerID1 =='':
            OutCallerID = str(OutCallerID1)
        else:
            OutCallerID = int(OutCallerID1)

        AllowBridgeConferencing = str(kwargs.get("allowBridgeConferencing", True))
        PrivacyEnabled = int(kwargs.get("defaultPrivacySettings", 0))

        value = kwargs.get('value')
        if value == "modify":
            programSoftKey = {"extension":name,"BackupDN":BackupDN,"AllowBridgeConferencing":AllowBridgeConferencing,
                              "PrivacyEnabled":PrivacyEnabled}
        else:
            programSoftKey = {"name":name, "BackupDN":BackupDN, "SwitchID":SwitchID, "CallStackDepth":CallStack,
                              "NoAnswerRings":NoAnswerRings,"CFNoAnswer":CFNoAnswer, "CFBusy":CFBusy,
                              "OutCallerID":OutCallerID, "AllowBridgeConferencing":AllowBridgeConferencing,
                              "PrivacyEnabled":PrivacyEnabled}

        return self.d2api_obj.create_modify_BCA(**programSoftKey)

    def BossCreateBCA(self, **kwargs):
        """
        The method creates a Bridge Call Appearance Extension on the MiCloud Portal.
        :param:
            :self: Boss Component object
            :kwargs: Dictionary:
                     :backupExtn: Outbound Caller Extension to use
                     :phoneLocation: Location of the phone number to use
                     :phone_number: Phone Number to use
                     :forwardAfter: Number of rings to forward after
                     :noAnswer: Extension to forward to
                     :cfBusy: Number of calls at one time
                     :callStackFull: Extension to forward the call when BCA is busy
                     :includeInDirectory: To include in directory i.e., True or False
                     :allowBridgeConferencing: Allow bridge conferencing
                     :defaultPrivacySettings: 0 for enabling others to join and 1 for not.
        :return: BCA Extension

        :created by: Vikhyat Sharma
        :creation date: 13/02/2020
        :last update date:
        :last update by:
        """
        bcaName = str(kwargs.get("name"))
        location = str(kwargs.get("location", ''))

        if "backupExtn" in kwargs:
            outboundCallerID = int(kwargs.get("backupExtn").phone_obj.phone_obj.phone.extensionNumber)
        else:
            raise Exception("Backup Extension is mandatory for MiCloud!!")

        phoneNumberLocation = str(kwargs.get("phoneLocation", "dont_assign_number"))
        phoneNumber = kwargs.get("phone_number", '')
        if not phoneNumberLocation == "dont_assign_number":
            if "phone_number" == '':
                raise Exception("Specify the phone number to choose from the location.")
            else:
                phoneNumber = str(phoneNumber.phone_obj.phone_obj.phone.extensionNumber)

        cfNoAnswer = int(kwargs.get("forwardAfter", 4))
        cfNoAnswerExtension = kwargs.get("noAnswer", '')
        if "forwardAfter" in kwargs:
            if cfNoAnswerExtension == '':
                logger.error("The extension to forward to when BCA call is not answered is not specified!!")
            else:
                cfNoAnswerExtension = str(cfNoAnswerExtension.phone_obj.phone_obj.phone.extensionNumber)

        cfBusy = int(kwargs.get("callStackDepth", 8))
        cfBusyExtension = kwargs.get("callStackFull", '')
        if "callStackDepth" in kwargs:
            if cfBusyExtension == '':
                logger.error("The extension to forward to when BCA extension is busy is not specified!!")
            else:
                cfBusyExtension = str(cfBusyExtension.phone_obj.phone_obj.phone.extensionNumber)

        includeInDirectory = kwargs.get("includeInDirectory", True)

        allowBridgeConferencing = bool(kwargs.get("allowBridgeConferencing", False))
        conferencingOptions = 'disable_conferencing'    # initially storing the default value in the conferencing options
        if allowBridgeConferencing:
            if "defaultPrivacySettings" in kwargs:
                joinOthers = str(kwargs.get("defaultPrivacySettings"))
                if joinOthers == "0":
                    conferencingOptions = "enable_others_may_join"
                else:
                    conferencingOptions = "enable_others_may_not_join"
            else:
                raise Exception("Specify whether others can join bridge conference or not!!")
        bca_details = {
                        "profileName": bcaName,
                        "location_name": location,
                        "phoneNumberLocation": phoneNumberLocation,
                        "phone_number": phoneNumber,
                        "CFNoAnswer": cfNoAnswer,
                        "cfNoAnswerExtension": cfNoAnswerExtension,
                        "CFBusy": cfBusy,
                        "cfBusyExtension": cfBusyExtension,
                        "includeSystemDirectory": includeInDirectory,
                        "outboundCallerId": outboundCallerID,
                        "conferencingOptions": conferencingOptions
                       }
        return self.boss_obj.create_bca(**bca_details)

    def deleteBCA(self,**kwargs):
        """
        Ram
        """
        if self.d2api_obj:
            return self.D2DeleteBCA(**kwargs)
        else:
            return self.BossDeleteBCA(**kwargs)

    def D2DeleteBCA(self,**kwargs):
        """
        Ram
        """
        return self.d2api_obj.delete_BCA_profile(**kwargs)

    def BossDeleteBCA(self, **kwargs):
        """
        The method deletes BCA extension from the MiCloud Portal.
        :param:
                :kwargs: Dictionary
                         :ExtensionNumber: BCA extension to delete
        :return: None
        :created by: Vikhyat Sharma
        :creation date: 19/02/2020
        :last update by:
        :last update date:
        """
        bcaExtension = str(kwargs['ExtensionNumber'])

        result = self.boss_obj.delete_bca(extension=bcaExtension)
        if result[0]:
            logger.info("BCA Extension: <b>" + bcaExtension + "</b> deleted from the Portal.", html=True)
            console("BCA Extension: " + bcaExtension + " deleted from the Portal.")
        else:
            logger.info("BCA Extension <b>" + bcaExtension + "</b> could not be deleted from the Portal.", html=True)
            console("BCA Extension: " + bcaExtension + " could not be deleted from the Portal.")

    def modifyTelephoneOptions(self,**kwargs):
        """
        Ram
        """

        if self.d2api_obj:
            return self.D2ModifyTelephoneOptions(**kwargs)
        else:
            return self.BossModifyTelephoneOptions(**kwargs)


    def D2ModifyTelephoneOptions(self,**kwargs):
        """
        Ram
        """
        return self.d2api_obj.modify_telephony_options(**kwargs)

    def BossModifyTelephoneOptions(self,**kwargs):
        raise Exception("Support not Available For changing Telephony options in MiCloud Till now.")

    def createModifySchedule(self,**kwargs):
        """
        Ram
        :param kwargs:
        :return:
        """
        if self.d2api_obj:
            return self.D2CreateModifySchedule(**kwargs)
        else:
            return self.BossCreateModifySchedule(**kwargs)


    def D2CreateModifySchedule(self,**kwargs):
        schedule = kwargs['Schedule']
        TimeZone = kwargs['TimeZone']
        ScheduleName = kwargs['ScheduleName']
        date = kwargs.get('date')
        day = kwargs.get('day')

        if schedule =="OnHours":
            Schedules_List = [{"DayOfWeek": 1, "start_time": "10:00:00", "stop_time": "17:00:00"},
            {"DayOfWeek": 2, "start_time": "10:00:00", "stop_time": "17:00:00"},
            {"DayOfWeek": 3, "start_time": "10:00:00", "stop_time": "17:00:00"},
            {"DayOfWeek": 4, "start_time": "10:00:00", "stop_time": "17:00:00"},
            {"DayOfWeek": 5, "start_time": "10:00:00", "stop_time": "17:00:00"}]

            if day == 1:
                Schedules = list(Schedules_List[0])
            if day == 2:
                Schedules = list(Schedules_List[1])
            if day == 3:
                Schedules = list(Schedules_List[2])
            if day == 4:
                Schedules = list(Schedules_List[3])
            if day == 5:
                Schedules = list(Schedules_List[4])
            if day == 0:
                Schedules = list(Schedules_List)
            if day ==None:
                Schedules = None

            values = {"Schedules":Schedules, "TimeZone":TimeZone,"ScheduleName":ScheduleName}
            return self.d2api_obj.create_modify_onhours_schedules(**values)

        elif schedule =="Holiday":
            Schedules =[{"ItemName":"holiday","schedule_date":date}]
            values = {"Schedules": Schedules, "TimeZone": TimeZone, "ScheduleName": ScheduleName}
            return self.d2api_obj.create_modify_holiday_schedule(**values)

    def BossCreateModifySchedule(self, **kwargs):
        pass

    def modifyTelephoneFeature(self,**kwargs):
        """
           This method changes the Telephony features according the Call Manager.

           :param:
                :kwargs: Key-value pair parameters for the modifications

           :return: (str) Required Parameter
           :created by: Ramkumar. G
           :creation date:
           :last update by:
           :last update date:
        """
        if self.d2api_obj:
            return self.D2ModifyTelephoneFeature(**kwargs)
        else:
            return self.BossModifyTelephoneFeature(**kwargs)

    def D2ModifyTelephoneFeature(self,**kwargs):
        """
        This method is used to modify the telephony phones of the phone.
        The parameters that can be modified can be found under: Connnect Director -> User -> Telephony

        :param:
            :kwargs: Key-Value pair to change the parameters

        :return: SCA extension (str)
        :created by: Ramkumar G.
        :creation date:
        :last update by: Vikhyat Sharma
        :last update date: 27/11/2020
        """
        phone = kwargs['phone']
        extension = phone.phone_obj.phone_obj.phone.extensionNumber
        sca_enabled1 = kwargs.get('sca_enabled', False)
        sca_enabled = bool(True) if sca_enabled1 == u'True' else bool(False)

        CallStackDepth = kwargs.get('CallStackDepth', 10)

        MakeExtensionPrivate1 = kwargs.get('MakeExtensionPrivate', False)
        MakeExtensionPrivate = bool(True) if MakeExtensionPrivate1 == u'True' else bool(False)
        MustChangeTUIPassword1 = kwargs.get('VM_pwd_change_on_next_login',False)
        MustChangeTUIPassword= bool(True) if MustChangeTUIPassword1 ==u'True' else bool(False)

        EnableDelayedRingdown1=kwargs.get("EnableDelayedRingdown",False)
        EnableDelayedRingdown = bool(True) if EnableDelayedRingdown1 == u'True' else bool(False)

        ringdownNumber = kwargs.get("RingdownNumber", '')

        if isinstance(ringdownNumber, PhoneComponent):
            ringdownNumber = ringdownNumber.phone_obj.phone_obj.phone.extensionNumber

        RingdownDelay=kwargs.get("RingdownDelay",'')

        ModifyValues = {'extension':extension,'sca_enabled':sca_enabled,"CallStackDepth":CallStackDepth,
                        "MakeExtensionPrivate":MakeExtensionPrivate,"MustChangeTUIPassword":MustChangeTUIPassword,
                        "EnableDelayedRingdown":EnableDelayedRingdown,"RingdownNumber":ringdownNumber,
                        "RingdownDelay":RingdownDelay}

        result = self.d2api_obj.create_modify_user(**ModifyValues)

        if 'sca_enabled' in kwargs:
            if result is not False:
                logger.info("Successfully enabled SCA on extension: " + extension + " with BCA number: " + result[-4:])
                return result[-4:]
            else:
                logger.warn("SCA ia already enabled for " + str(extension) + " number. Check the previous TCs.")
                logger.warn("Disabling SCA and enabling it again to get new SCA extension.")
                self.modifyTelephoneFeature(phone=phone, sca_enabled='False')
                return self.modifyTelephoneFeature(phone=phone, sca_enabled='True')

    def BossModifyTelephoneFeature(self, **kwargs):
        """
        This method is used to modify the telephony phones of the phone.
        The parameters that can be modified can be found under: MiCloud portal

        :param:
            :kwargs: Key-Value pair to change the parameters

        :return: SCA extension (str)
        :created by: Milind P.
        :creation date:
        :last update by:
        :last update date: 7/12/2020
        """
        phone = kwargs['phone']
        extension = phone.phone_obj.phone_obj.phone.extensionNumber
        sca_enabled = bool(kwargs.get('sca_enabled', False))
        sca_extension = kwargs.get('sca_extension', '')

        ModifyValues = {'extensionToBeProgrammed': extension, 'SCA': sca_enabled, 'sca_extension': sca_extension}
        result = self.boss_obj.edit_user(**ModifyValues)
        logger.info("Result of operation : " + str(result))

        if sca_enabled:
            if result is not False:
                scaExtension = list(result[0])[1]
                logger.info("Successfully enabled SCA on extension: " + extension + " with BCA number: " + scaExtension)
                return scaExtension
            else:
                raise Exception("Failed to enable SCA on extension: " + extension)

        if sca_enabled == False:
            if result is not False:
                logger.info("Successfully disabled SCA on extension: " + extension)
            else:
                raise Exception("Failed to disable SCA on extension: " + extension)

    def createUser(self,**kwargs):
        """
         This method is a caller for creating user extension number on D2api portal
               :param:
                :self: BossApiComponent object
                :d2api_obj: D2API Object
                :kwargs(dictionary):
                    consists of paramters of methods D2create_User,
                    Boss_create_User find the details of params inside the
                    methods

               :return: the create user method of boss portal or D2Api portal
               :created by :Abhishek Khanchi
               :last update Date :11/06/2019
        """
        if self.d2api_obj:
            return self.D2create_User(**kwargs)
        else:
            return self.Boss_create_User(**kwargs)

    def D2create_User(self, **kwargs):
        """
         Below method create user extension number on D2Api (MiVoice) portal
        :param:
            :self: BossApiComponent object
            :d2api_obj: D2API Object
            :kwargs(dictionary):
                :FirstName:  First Name of the user e.g., Auto
                :LastName: Last name of the user e.g., User
                :AllowTelephonyPresence: boolean value i.e., True or False
                :EmailAddress: mail string(abc@example.com)

        :return: Extension Number of the created user (str)
        :created by: Abhishek Khanchi
        :creation date: 11/06/2019
        :last update by: Sharma
        :last update Date: 29/07/2020
        """

        firstName = kwargs.get('FirstName', 'auto')
        lastName = kwargs.get('LastName', 'user')
        emailID = kwargs.get('EmailAddress', firstName + lastName + "@automation.com")
        allowTelephonyPresence = bool(kwargs.get('AllowTelephonyPresence', False))

        userDetails = {
                        'FirstName': firstName, 'LastName': lastName, "EmailAddress": emailID,
                        "AllowTelephonyPresence": allowTelephonyPresence, "PrivacyEnabled": 0
                      }

        extn = self.d2api_obj.create_modify_user(**userDetails)
        console("Successfully created a new Extension: " + extn[15:19])
        return extn[15:19]

    def Boss_create_User(self,**kwargs):
        raise Exception("NO SUPPORT FOR CREATING USERS ON MICLOUD!!")

    def deleteUser(self, **kwargs):
        """
            Below method is a caller for Deleting extension number
            from D2api portal or Boss Portal
            :param:
            :self: BossApiComponent object
            :d2api_obj: D2API Object
            :kwargs(dictionary):
                consists of paramters of methods D2deLete_extn,
                BossdeLete_extn find the details of params inside the
                methods
            :return: the delete_extension method of boss portal or D2Api portal
            :Created by :Abhishek Khanchi
            :last update Date :11/06/2019
        """

        if self.d2api_obj:
            self.D2delete_extn(**kwargs)
        else:
            self.Bossdelete_extn(**kwargs)

    def D2delete_extn(self, **kwargs):
        """
        Below method create user extension number on D2api portal or Boss Portal
        :param:
            :self: BossApiComponent object
            :d2api_obj: D2API Object
            :extension:  string (eg: 4054/1001)
            :phone: PhoneComponent object
        :return: Nothing
        :created by: Abhishek Khanchi
        :creation date: 11/06/2019
        :last update by:
        :last update date:
        """
        extensionToDelete = kwargs['extension']
        if isinstance(extensionToDelete, PhoneComponent):
            extensionToDelete = extensionToDelete.phone_obj.phone_obj.phone.extensionNumber
        console(self.d2api_obj.delete_extension(extensionToDelete))

    def Bossdelete_extn(self, **kwargs):
        raise Exception("NO SUPPORT FOR DELETING EXTENSION IN MI-CLOUD!!")

    def modifyMusicOnHold(self, **kwargs):
        """
           Ram
           :param kwargs:
           :return:
        """
        if self.d2api_obj:
            return self.D2modifyMusicOnHold(**kwargs)
        else:
            return self.BossmodifyMusicOnHold(**kwargs)

    def D2modifyMusicOnHold(self, **kwargs):
        internal_calls = str(kwargs.get('option', '0'))
        file = str(kwargs['fileName'])
        values = {'internal_call': internal_calls, 'file_to_select': str(file)}
        return self.d2api_obj.modify_moh_system_defaults(**values)

    def BossmodifyMusicOnHold(self, **kwargs):
        raise Exception("NO SUPPORT FOR MODIFYING MUSIC ON HOLD !!!")

    def create_modify_usergroups(self, **kwargs):
        """
          Ram
          :param kwargs:
          :return:
        """
        if self.d2api_obj:
             return self.D2create_modify_usergroups(**kwargs)
        else:
             return self.Bosscreate_modify_usergroups(**kwargs)

    def D2create_modify_usergroups(self,**kwargs):
        usergroup = kwargs['ExecutivesName']
        file = kwargs['fileName']   #filename: MOH_50, MOH_150. MOH_200, MOH_250
        values = {'user_group_name':usergroup,'file_to_select':file}
        return self.d2api_obj.create_modify_user_groups(**values)

    def Bosscreate_modify_usergroups(self, **kwargs):
        """

        :param:
            :kwargs:
        :return:
        """
        raise Exception("NO SUPPORT FOR MODIFYING USER GROUPS IN MI-CLOUD !!!")

    def removePKMProgrammedButton(self, **kwargs):
        if self.d2api_obj:
            return self.D2removePKMProgrammedButton(**kwargs)
        else:
            return self.bossRemovePKMProgrammedButton(**kwargs)

    def D2removePKMProgrammedButton(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        extn = kwargs["user_extension"]
        user_extension = extn.phone_obj.phone_obj.phone.extensionNumber

        console("Adding call appearance button on " + str(user_extension))
        logger.info("Adding call appearance button on " + str(user_extension))
        for value in range(1, 7):
                programSoftKey = {'user_extension': user_extension, 'button_box': 1,
                                  'soft_key': value,
                                  'function': "Unused", 'label': "", 'target_extension': ""}
                self.d2api_obj.configure_prog_button(**programSoftKey)

    def bossRemovePKMProgrammedButton(self, **kwargs):
        """

        :param:
            :kwargs:
        :return:
        """
        raise Exception("NO SUPPORT FOR REMOVING PKM PROGRAMMED BUTTON !!!")

    def createPickupGroups(self, **kwargs):
        if self.d2api_obj:
            return self.createD2PickupGroups(**kwargs)
        else:
            return self.createBossPickupGroups(**kwargs)

    def createD2PickupGroups(self,**kwargs):
        phone = kwargs['user_extension']
        PickupGroupName = str(kwargs["PickupGroupName"])
        extension_list = str(kwargs['pickupListName'])
        extension = phone.phone_obj.phone_obj.phone.extensionNumber
        switch=kwargs['switch']
        Members = kwargs["GroupMembers"]

        GroupMembers = []
        for data in Members[:]:
            GroupMembers.append(data.phone_obj.phone_obj.phone.extensionNumber)

        page_list = {'name': extension_list, 'extension_numbers': GroupMembers}
        self.d2api_obj.create_page_list(**page_list)

        pickupGroup = {'name': PickupGroupName, 'extension_list_name': extension_list,
                       'switch':switch, 'extension':extension}

        return self.d2api_obj.create_modify_pickup_group(**pickupGroup)

    def createBossPickupGroups(self,**kwargs):
        """
        The method is used to create pickup group on the MiCloud Portal.
        :param:
                :kwargs: Dictionary
                         :PickupGroupName: Name of the Pickup Group
                         :pickupListName: Pickup List Name
                         :GroupMembers: Members of the list/pickup group
        :return: Created Pickup Group Extension

        :created by: Vikhyat Sharma
        :creation date: 27/02/2020
        :last update by:
        :last update date:
        """
        location = str(kwargs.get("location", miCloudLocation))
        groupName = str(kwargs.get("PickupGroupName"))
        listName = str(kwargs.get("pickupListName"))
        groupMembers = []
        for member in kwargs.get("GroupMembers"):
            groupMembers.append(str(member.phone_obj.phone_obj.phone.extensionNumber))

        listDetails = {
                        'el_name': listName,
                        'el_extns': groupMembers
                      }
        listResult = self.boss_obj.create_extension_list(**listDetails)
        if listResult[0]:
            logger.info("Extension List: <b>" + listName + "</b> with members <b>" + str(groupMembers)
                        + "</b> created successfully.", html=True)
            console("Extension List: " + listName + " with members " + str(groupMembers) + " created successfully.")

        pickupGroupDetails = {
                               'location_name': location,
                               'pkg_name': groupName,
                               'pkg_extensionlist': listName
                             }
        groupResult = self.boss_obj.create_pickup_group(**pickupGroupDetails)
        if groupResult[0]:
            logger.info("Pickup Group created with extension: <b>" + str(groupResult[-1]) + "</b>", html=True)
            console("Pickup Group created with extension: " + str(groupResult[-1]))
            return str(groupResult[-1])
        else:
            raise Exception("Pickup group could not be created.")

    def deletePickupGroups(self, **kwargs):
        if self.d2api_obj:
            return self.deleteD2PickupGroups(**kwargs)
        else:
            pass
            # return self.deleteBossPickupGroups(**kwargs)

    def deleteD2PickupGroups(self, **kwargs):
        """
        Ram
        """
        extension = str(kwargs['number'])
        extensionList = str(kwargs['pickupListName'])
        console("Deleting " + extension + " pickup group extension")
        logger.info("Deleting " + extension + " pickup group extension")
        self.d2api_obj.delete_pickup_group(extension=extension)
        return self.d2api_obj.delete_page_list(extensionList)

    def modify_call_control_options(self, **kwargs):
        """
        Below method is written to modify the Call Control Options for D2API and Boss API.
        :param:
            :self: API Component object
            :kwargs: Dictionary for getting the arguments needed

        :return: None

        :created by: Aman Bhardwaj
        :creation date: 27/02/2020
        :last updated by:
        :last update on:
        """

        if self.d2api_obj:
            return self.D2modify_call_control_options(**kwargs)
        else:
            return self.Bossmodify_call_control_options(**kwargs)

    def D2modify_call_control_options(self, **kwargs):
        """
        Below method is written to modify the Call Control Options for D2API.
        :param:
            :self: D2API Component object
            :kwargs: Dictionary for getting the arguments needed:
            :EnableSilentCoachTone - For enabling Silent Coach Warning Tone
            :EnableSilentMonitorTone - For enabling Silent Monitor Warning Tone

        :return: None

        :created by: Aman Bhardwaj
        :creation date: 27/02/2020
        :last updated by:
        :last update on:
        """

        EnableSilentCoachWarningTones = kwargs.get("EnableSilentCoachTone", False)
        EnableSilentCoachWarningTone = bool(True) if EnableSilentCoachWarningTones == u'True' else bool(False)

        EnableRecordingWarningTones = kwargs.get("EnableSilentMonitorTone", False)

        EnableRecordingWarningTone = bool(True) if EnableRecordingWarningTones == u'True' else bool(False)

        values = {'EnableSilentCoachWarningTone': EnableSilentCoachWarningTone,
                  'EnableRecordingWarningTone': EnableRecordingWarningTone}

        return self.d2api_obj.modify_call_control_options(**values)

    def Bossmodify_call_control_options(self, **kwargs):
        """
        Below method is written to modify the Call Control Options for Boss API.
        :param:
            :self: Boss API Component object
            :kwargs: Dictionary for getting the arguments needed:
            :EnableSilentCoachTone - For enabling Silent Coach Warning Tone
            :EnableSilentMonitorTone - For enabling Silent Monitor Warning Tone

        :return: None

        :created by: Aman Bhardwaj
        :creation date: 27/02/2020
        :last updated by:
        :last update on:
        """
        pass


if __name__ == "__main__":
    fo = BossApiComponent(ip="10.112.91.49:5478", username= "desktop", password="desktop@123")
    print(fo.modifyTelephoneFeature(phone='4001', sca_enabled='True'))
