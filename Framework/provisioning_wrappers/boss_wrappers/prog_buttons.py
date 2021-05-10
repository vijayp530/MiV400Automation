__author__ = "nitin.kumar-2@mitel.com"

import sys, requests, os, logging, ast, json
from prg_btns_constants import *
sys.path.append(os.path.normpath(os.path.dirname(os.path.dirname(os.path.dirname((__file__))))))
from utils.decorators import func_logger

log = logging.getLogger("boss_api.prog_buttons")


class ProgButtons():
    """
    Apis for the programmable buttons related operations.
    """

    @func_logger
    def configure_prog_button(self, **params):
        '''
        This function will configure a programmable button on the phone
        Users -> select a user -> click on second coloum -> Programmable Buttons
        user_email : the email of the user
        button_box : the number of button box generally always is 0
        soft_key : the index of soft key in btn box list e.g. for the button 2 on the boss ui the value of soft_key should be 1 i.e. decremented by 1
        :return: A tuple of a boolean status flag and the return object from the requested url

        params for Monitor Extension
        ring_delay = [1,2,3,4,'dont_ring']
        show_caller_id = ["never","only_when_ringing","always"]
        no_connected = ["unused",""dial_number","intercom","whisper_page"]
        with_connected = ["unused",""dial_number","intercom","whisper_page","transfer_blind","transfer_consultative","transfer_intercom",park","transfer_whisper"]

        params for programming the BCA
        make sure SCA is enabled on an extension and its bca extension is passed in 'extension'
        e.g. SCA is enabled on an extension 7654 and it resulted in creation of BCA extension 1006. Now while calling configure_prog_button to program a BCA extension=1006 should be passed
        CallStackPosition : valid values are between 1 to 8
        allow_auto_answer : 0 for unchecked and 1 for checked
        bca_not_connected_call_acton : {'Dial Tone':2,'Answer Only':3} # remaining 2(dial external, dial extension) will be added in future

        '''
        result = False
        params_xml = self.config.getparams("configure_prog_button")
        params = self.get_param_to_use(params_xml, **params)
        if self.accountId is None:  # switch account has not been called
            act_id = self.get_account_detail(act_name=params['account_name'])
        else:
            act_id = self.accountId
        params["accountId"] = act_id
        if self.part_id:
            params['part_name'] = self.part_id
        if params.get('extensionToBeProgrammed'): # To go with extension instead of email
            params["profileId"] = self.get_profile_detail(act_id, params['part_name'],"",extension=params.get('extensionToBeProgrammed'))
        else:
            params["profileId"] = self.get_profile_detail(act_id, params['part_name'],params['user_email'])
        # get programmable btns data
        prg_btn_data = self.get_programmable_btns_data(act_id, params["profileId"])
        # button boxes
        btn_box = "user_prog_button_button_%s_boxes_attributes"%params['button_box']
        prg_btn_data["user"][btn_box][params['soft_key']]['selectedFunction'] = params["function"]
        prg_btn_data["user"][btn_box][params['soft_key']]['_create'] = True
        # No param required for unused function
        if params["function"].lower() == "Unused".lower():
            # prg_btn_data["user"][btn_box][params['soft_key']]['_create'] = True
            prg_btn_data["user"][btn_box][params['soft_key']]['FunctionID'] = "1"
        else:
            # Common operations
            prg_btn_data["user"][btn_box][params['soft_key']]['SoftKeyLabel'] = params["label"][0:6]
            prg_btn_data["user"][btn_box][params['soft_key']]['LongLabel'] = params["label"][0:12]

        # Change Availability
        if params["function"].lower() == "change availability".lower():
            # prg_btn_data["user"][btn_box][params['soft_key']]['_create'] = True
            prg_btn_data["user"][btn_box][params['soft_key']]['FunctionID'] = "42"
            prg_btn_data["user"][btn_box][params['soft_key']]['CHMTypeID'] = availability_options[params.get("availability").lower()]

        
        if params.get('extension') != None:
            prg_btn_data["user"][btn_box][params['soft_key']]['DialNumberDN_formatted'] = params.get("extension")
            prg_btn_data["user"][btn_box][params['soft_key']]['ConnectedCallFunctionID'] = None
            # prg_btn_data["user"][btn_box][params['soft_key']]['_create'] = True
            prg_btn_data["user"][btn_box][params['soft_key']]['FunctionID'] = function_ids[params["function"].replace(" ","_").upper()]
            prg_btn_data["user"][btn_box][params['soft_key']]['DialNumberNTID'] = "0"

        # additional params for Monitor Extension
        if params["function"].lower() in ["Monitor Extension".lower(), "BRIDGE CALL APPEARANCE".lower()]:
            prg_btn_data["user"][btn_box][params['soft_key']]['RingDelayBeforeAlert'] = ring_delay_before_alert[params["ring_delay"].lower()]
            prg_btn_data["user"][btn_box][params['soft_key']]['show_caller_id_option'] = caller_id_alert[params["show_caller_id"].lower()]
            prg_btn_data["user"][btn_box][params['soft_key']]['DisconnectedCallFunctionID'] = no_connected_action[params["no_connected"].lower()]
            prg_btn_data["user"][btn_box][params['soft_key']]['ConnectedCallFunctionID'] = with_connected_action[params["with_connected"].lower()]

        # additional params for programming a key for BCA
        if params["function"].lower() == "BRIDGE CALL APPEARANCE".lower():
            prg_btn_data["user"][btn_box][params['soft_key']]['CallStackPosition'] = params["CallStackPosition"]
            prg_btn_data["user"][btn_box][params['soft_key']]['FunctionParams4'] = params["allow_auto_answer"]
            prg_btn_data["user"][btn_box][params['soft_key']]['SecondaryType'] = params["bca_not_connected_call_acton"]
        
        #Hotline
        if params["function"].lower() == "Hotline".lower():
            prg_btn_data["user"][btn_box][params['soft_key']]['ConnectedCallFunctionID'] = hotline_call_actions[params["call_action"].lower()]
            
        ## MSN
        if params.get('dtmf_digits'):
            prg_btn_data["user"][btn_box][params['soft_key']]['DialNumberNTID'] = "4"
            prg_btn_data["user"][btn_box][params['soft_key']]['DialNumberExtern_formatted'] = params.get('dtmf_digits')
        url = params.pop("url")
        log.info("configuring a programmable button on the phone with args <%s>" % params)
        # changing the content type for this call
        self.headers['Content-Type'] = "application/json"
        ret = requests.post(url, data=json.dumps(prg_btn_data), headers=self.headers, params=params)
        # changing the content type back to default for further calls
        self.headers['Content-Type'] = "application/x-www-form-urlencoded"

        if ret.status_code == 200 and not ret.json().has_key("errors"):
            log.info("The programmable button has been created successfully.Message from server : <%s>" % ret.text)
            result = True
        else:
            log.error("Could not create programmable button.Message from server : <%s>" % ret.text)

        return result, ret

    @func_logger
    def clear_prog_button(self, **params):
        '''
        This function will clear all the onfigured  programmable buttons
        Users -> select a user -> click on second coloum -> Programmable Buttons
        user_email : the email of the user
        button_box : the number of button box generally always is 0
        soft_key : the index of soft key in btn box list e.g. for the button 2 on the boss ui the value of soft_key should be 1 i.e. decremented by 1
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        params_xml = self.config.getparams("configure_prog_button")
        params = self.get_param_to_use(params_xml, **params)
        if self.accountId is None:  # switch account has not been called
            act_id = self.get_account_detail(act_name=params['account_name'])
        else:
            act_id = self.accountId
        params["accountId"] = act_id

        if self.part_id:
            params['part_name'] = self.part_id
        if params.get('extensionToBeProgrammed'): # To go with extension instead of email
            params["profileId"] = self.get_profile_detail(act_id, params['part_name'],"",extension=params.get('extensionToBeProgrammed'))
        else:
            params["profileId"] = self.get_profile_detail(act_id, params['part_name'],params['user_email'])

        # get programmable btns data
        prg_btn_data = self.get_programmable_btns_data(act_id, params["profileId"])
        # button boxes
        btn_box = "user_prog_button_button_%s_boxes_attributes"%params['button_box']
        prg_btn_data["user"][btn_box][params['soft_key']]['FunctionID'] = 2
        prg_btn_data["user"][btn_box][params['soft_key']]['DialNumberNTID'] = -1
        prg_btn_data["user"][btn_box][params['soft_key']]['DialNumberExtern_formatted'] = ""
        prg_btn_data["user"][btn_box][params['soft_key']]['DialNumberDN_formatted'] = ""

        url = params.pop("url")
        log.info("clearing the configured programmable button on the phone with args <%s>" % params)
        self.headers['Content-Type'] = "application/json"
        ret = requests.post(url, data=json.dumps(prg_btn_data), headers=self.headers, params=params)
        # changing the content type back to default for further calls
        self.headers['Content-Type'] = "application/x-www-form-urlencoded"
        # removing extra check as trying to remove a btn which is already removed raises an exception
        if ret.status_code == 200 :
            log.info("The programmable buttons have been cleared successfully.")
            result = True
        else:
            log.error("Could not clear programmable buttons.Message from server : <%s>" % ret.text)

        return result, ret

