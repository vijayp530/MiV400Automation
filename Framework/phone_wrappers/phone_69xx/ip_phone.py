__author__ = "nkumar@soretel.com"

import os, clr, sys, shutil, time


class IP_Phone(object):
    """
    This class provides functionality to connect and control the Mitel 69XX phones.
    """

    def __init__(self, atap_dll_path=None):
        self.dll_name = "ATAP.dll"
        if atap_dll_path is None:
            atap_dll_path = os.path.join(os.path.dirname(__file__), self.dll_name)
        self.dll_path = atap_dll_path
        if not os.path.exists(self.dll_path):
            raise("ATAP.dll does not exist in %s" %self.dll_path)
        # Add reference to the library
        self.add_reference_to_dll(self.dll_path)

    def add_reference_to_dll(self, dll_path):
        python_installation_dir = os.path.dirname(sys.executable)
        # todo getting exception in copy from robot test case when executed from command line
        try:
            shutil.copy(dll_path, python_installation_dir)
        except:
            pass
        clr.AddReference(self.dll_name.split('.')[0])
        # importing the modules from the dll
        import PhoneHandler
        import Logger
        Logger.Logger.Initialize()

    def get_object(self, class_name, params):
        return getattr(sys.modules['PhoneHandler'], class_name)(*params)


if __name__ == "__main__":
    o = IP_Phone()
    phone1 = o.get_object('Mitel6920',["Mitel6920", False, "29", "123", "Test Extension", "10.198.34.66", "", "", "", "", "", "", "10.211.41.40"])
    phone2 = o.get_object('Mitel6920',["Mitel6920", False, "28", "123", "Test Extension", "10.198.33.98", "", "", "","", "", "", "10.211.41.40"])
    phone1.connectToPhone()
    phone2.connectToPhone()
    # phone1.pressL1key()
    # phone1.callToAnExtension(phone2)
    # phone1.verifyInPhoneDisplay(phone2.extensionNumber)
    # phone1.pressHardKey(sys.modules['PhoneHandler'].HardPhone.Keys.DialPad9, 4)
    # phone1.dialAnumber("28")
    # # phone1.pressHardKey(sys.modules['PhoneHandler'].HardPhone.Keys.OffHook, 1)
    # time.sleep(4)
    # # phone1.pressOffhook()
    # phone2.answerTheCall()
    # phone2.verifyInPhoneDisplay(phone1.extensionNumber)
    # phone1.disconnectTheCall()

    phone2.dialAnumber("29")
    # phone1.pressHardKey(sys.modules['PhoneHandler'].HardPhone.Keys.OffHook, 1)
    time.sleep(4)
    # phone1.pressOffhook()
    phone1.answerTheCall()
    phone1.verifyInPhoneDisplay(phone2.extensionNumber)
    phone2.disconnectTheCall()
