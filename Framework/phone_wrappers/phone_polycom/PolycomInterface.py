"""
This module provides an interface to interact with the polycom phones.

Following phone models have been tested:

Phone Model SoundStation 	IP 6000 (UC Software Version		4.0.11.0583, BootROM Software Version 	5.0.1.10553)
Phone Model SoundStation 	IP 5000 (UC Software Version		4.0.11.0583, BootROM Software Version 	5.0.11.0282)
"""

__author__ = "nitin.kumar-2@mitel.com"

import base64, requests, time, re
from requests.auth import HTTPDigestAuth
from collections import OrderedDict
from xml.dom.minidom import parse, parseString
import logging
log = logging.getLogger("phones.polycom")
log.addHandler(logging.NullHandler())


class PhoneUrl:
    def __init__(self, ip):
        """
        This class contains the different urls for the phone.
        :param ip: the ip of the phone
        """
        self.urls = {"login": "http://%s/auth.htm" % ip,
                     "logs": "http://%s/Diagnostics/log" % ip,
                     "push": "http://%s/push" % ip,
                     "home": "http://%s/home.htm" % ip,
                     "device": "http://%s/polling/deviceHandler" % ip,
                     "network": "http://%s/polling/networkHandler" % ip,
                     "call": "http://%s/polling/callstateHandler" % ip
        }


class InvalidResp:
    """
    A class to represent invalid response. This is required as the phone will not intimate anything even with the wrong uri's
    This will be utilized based on the analysis of the phone logs.
    """
    status_code = 600


class PolycomInterface(object):
    """
    Class to interact with polycom phones
    """
    def __init__(self, ip, username='Polycom', password='456', push_user='Push', push_pwd="Push", extn=None, poll_user='Push', poll_pwd="Push"):
        """
        Sets the headers and urls
        :param ip: the ip of the phone
        :param username: the admin user name of the phone
        :param password: the admin password of the phone
        :param push_user: the user name for the push application
        :param push_pwd: the password for the push application
        """
        self.authorization = base64.b64encode(b":".join([('%s'%username).encode(), ('%s'%password).encode()])).decode()
        self.phone = PhoneUrl(ip)
        self.auth = HTTPDigestAuth(push_user, push_pwd)
        self.poll_auth = HTTPDigestAuth(poll_user, poll_pwd)
        self.header = {"Content-Type": "application/x-com-polycom-spipx"}
        self.admin_header = {'Cookie' : 'Authorization=Basic %s' % self.authorization,
                             'Referer': self.phone.urls['home']}
        if extn:
            self.extn = extn

    def __send_poll(self, state_to_poll):
        """
        Helper method to poll the phone for device, network and call info
        :return: current state in form of xml
        """
        r = requests.get(self.phone.urls[state_to_poll], auth=self.auth, headers=self.header)
        if r.status_code == 200:
            return r.text
        else:
            return False

    def get_node_value(self, resp, node_name):
        """
        :param resp: the response from phone - not creating instance variable so that same method can be used for all kind of polled data
        :param node_name: the name of node whose value is required
        :return:
        """
        root = parseString(resp)
        nodes = root.getElementsByTagName(node_name)
        return nodes[0].firstChild.data

    def get_call_state(self):
        """
        to poll the phone for call state
        :return: xml containing the call state
        """
        return self.__send_poll("call")

    def get_network_state(self):
        """
        to poll the phone for network state
        :return: xml containing the network state
        """
        return self.__send_poll("network")

    def get_device_state(self):
        """
        to poll the phone for device state
        :return: xml containing the device state
        """
        return self.__send_poll("device")

    def send_push_msg(self, operation_type, operation, method='Push', data=None):
        """
        To send the push message to the phone
        :param operation_type: it can have following values. "key","tel","action"
        :param operation: the operation to perform
        :param method: method to be used
        :param data: to override the data to send to the phone. Generally not required.
        :return: the response of the request
        """
        phone_log = self.get_log()

        if data is None:
            data = '<PolycomIPPhone><Data priority="Critical">%s:%s</Data></PolycomIPPhone>' % (operation_type, operation)
        if method == 'Push':
            action = getattr(requests, 'post')
        r = action(self.phone.urls['push'], auth=self.auth, headers=self.header, data=data)
        # the sleep is required to let the log update
        time.sleep(0.1)
        new_log = self.get_log()
        additional_log = new_log[len(phone_log)-1:]
        log.debug("Sent message <%s> to <%s>" % (data, r.url))
        log.debug("Log of last action from the phone <%s>" % additional_log)
        if len([x for x in additional_log if "Invalid" in x]) > 0:
            return InvalidResp()
        return r

    def __send_get_request_to_phone(self, url, payload=None, headers = None):
        """

        :param url: the phone url
        :param payload: the payload to send with the request
        :param headers: the headers which needs to be sent in addition to the defined admin headers
        :return: the response of the request
        """
        if headers:
            self.admin_header.update(headers)
        r = requests.get(url, params=payload, headers=self.admin_header)
        return r

    def get_log(self, value='app'):
        """
        To retrieve the logs from the phone.
        :param value: app or boot to get the application or boot log
        :return: log file content if log file is present
        """
        payload = OrderedDict()
        payload['value'] = value
        payload['dummyParam'] = 1524829265456
        r_log = self.__send_get_request_to_phone(self.phone.urls['logs'], payload=payload)
        if r_log.status_code == 200:
            return r_log.text.split("\n")
        elif r_log.status_code == 500:
            return "No log file to fetch"
        else:
            return False


    def clear_log(self, value='app'):
        """
        To clear the log on the phone
        :param value: app or boot
        :return: True on success
        """
        payload = OrderedDict()
        payload['value'] = value
        payload['clear'] = 1
        payload['dummyParam'] = 1524829265456
        r_log = self.__send_get_request_to_phone(self.phone.urls['logs'], payload=payload)
        if r_log.status_code == 200:
            return True
        else:
            return False

    def press_key(self,key):
        """
        To press a key on the phone
        :param key: Following keys can be used
        ['Line1', 'Line2', 'Line3', 'Softkey1',  'Softkey2', 'Softkey3', 'DoNotDistrb','Select','Conference',
        'Transfer', 'Redial','VolDown', 'Hold', 'Volp', 'Headset', 'Call', 'List', 'Dialpad0', 'Handsfree',
         'Dialpad1', 'MicMte', 'Dialpad2', 'Men', 'Dialpad3', 'Messages', 'Dialpad4', 'Applications', 'Dialpad5',
          'Directories', 'Dialpad6', 'Setup', 'Dialpad7', 'Arrowup', 'Dialpad8', 'ArrowDown', 'Dialpad9', 'ArrowLeft',
          'DialPadStar', 'ArrowRight', 'DialPadPond', 'Status', 'Backspace']
        :return: True on success

        e.g. press_hard_key("Status")
        """
        r = self.send_push_msg("Key", key)

        if r.status_code == 200:
            return True
        else:
            return False

    def dial_number(self, num_to_dial):
        """
        To dial a number on the phone
        :param num_to_dial: the num to dial
        :return: True on success
        """
        r = self.send_push_msg("tel", "\\%s" % str(num_to_dial))
        if r.status_code == 200:
            return True
        else:
            return False

    def answer_call(self, key_to_answer='Softkey1'):
        """
        To answer the call on the phone
        :param key_to_answer: the soft key which will be used to answer the phone
        :return: True on success
        """
        r = self.send_push_msg("Key", key_to_answer)
        if r.status_code == 200:
            return True
        else:
            return False

    def end_call(self, key_to_end='Softkey2'):
        """
        To end an ongoing call on the phone
        :param key_to_answer: the soft key which will be used to answer the phone
        :return: True on success
        """
        r = self.send_push_msg("Key", key_to_end)
        if r.status_code == 200:
            return True
        else:
            return False

    def get_phone_info(self):
        """
        To get the details about hardware and software of the phone.
        :return: True on success
        """
        r_about = self.__send_get_request_to_phone(self.phone.urls['home'])
        info_values = [x.strip() for x in re.findall("<td>([\w\W]+?)</td>", r_about.text) if 'span' not in x]
        info_keys = ["Phone Model", "Part Number", "MAC Address", "IP Address", "UC Software Version",
                     "BootROM Software Version"]
        return dict(zip(info_keys, info_values))

    def verify_caller(self, caller):
        """
        to validate the name of caller
        :param caller: name of caller
        :return: True for success
        """
        _state = self.get_call_state()
        _val = self.get_node_value(_state, "CallingPartyName")
        if _val == caller:
            return True
        else:
            log.debug("Verifying caller. Expected:<%s> Actual:<%s>" % (caller, _val))
            return False

    def verify_current_call_state(self, call_state="Connected"):
        """
        to validate the state of call
        :param call_state: possible values are 'Connected','CallHold','CallHeld'
        :return: True for success
        """
        _state = self.get_call_state()
        _val = self.get_node_value(_state, "CallState")
        if _val == call_state:
            return True
        else:
            log.debug("Verifying call state. Expected:<%s> Actual:<%s>" % (call_state, _val))
            return False

    def verify_ringing(self, call_state="RingBack"):
        """
        to verify phone is ringing
        :param call_state: "Ringback" for caller and "Offering" for callee
        :return: True for success
        """
        _state = self.get_call_state()
        _val = self.get_node_value(_state, "CallState")
        if _val == call_state:
            return True
        else:
            log.debug("Verifying ringing failed.")
            return False


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    phone_1 = PolycomInterface("10.198.33.228",extn=6321)
    phone_2 = PolycomInterface("10.198.32.255",extn='6323')
    # phone_1.verify_caller("Emergency Test01")
    # phone_2.verify_caller("Emergency Test01")
    # phone_1.verify_current_call_state()
    # phone_2.verify_current_call_state()
    # phone_1.verify_ringing("RingBack")
    phone_2.verify_ringing("Offering")

    # print((phone_1.get_call_state()))
    # print((phone_1.get_device_state()))
    # print((phone_1.get_network_state()))
    # phone_2.press_key("Status")
    # print(phone_1.clear_log())
    # print((phone_2.get_log()))
    # print(phone_1.press_key("wwwwww"))
    # print(phone_2.dial_number(phone_1.extn))
    # print(phone_1.dial_number(phone_2.extn))
    # time.sleep(5)
    # print(phone_2.answer_call())
    # print(phone_1.get_phone_info())
    # print(phone_2.get_phone_info())
