__author__ = "Uttam"

import autoit
from robot.api.logger import console

from mapMgr import mapMgr


class AutoitWrapper:
    """
    Wrappers for performing operations on windows desktop based apps
    """
    def __init__(self):
        pass

    def __get_locator_for_tool(self, locator):
        if not locator.endswith("_win"):
            return locator + "_win"
        return locator

    def activate_window(self, locator):
        """
        Activates a window identified by locator
        :param locator: user defined name from map files
        Ex: activate_window("locator_name")
        """
        locator = self.__get_locator_for_tool(locator)
        window_identifier = mapMgr.__getitem__(locator)["IDENTIFIERS"].strip("'").split(",")[0]
        autoit.win_activate(window_identifier)

    def click(self, locator):
        """
        Clicks on an element identified by locator
        :param locator: user defined name from map files
        Ex: click("locator_name")
        """
        locator = self.__get_locator_for_tool(locator)
        window_identifier, control_identifier = mapMgr.__getitem__(locator)["IDENTIFIERS"].strip("'").split(",")
        autoit.control_click(window_identifier, control_identifier.strip('"'))

    def send_key(self, locator, key):
        """
        Press any key on an element identified by locator
        :param locator: user defined name from map files
        :param key: key which you want to press
        Ex: send_key("locator_name", "ENTER")
        """
        locator = self.__get_locator_for_tool(locator)
        window_identifier, control_identifier = mapMgr.__getitem__(locator)["IDENTIFIERS"].strip("'").split(",")
        key = "{%s}" % key
        autoit.control_send(window_identifier, control_identifier.strip('"'), key)

    def send_text(self, locator, text):
        """
        Enters text in an input element identified by locator
        :param locator: user defined name from map files
        :param text: text which you want to enter
        Ex: send_text("locator_name", "hello")
        """
        locator = self.__get_locator_for_tool(locator)
        window_identifier, control_identifier = mapMgr.__getitem__(locator)["IDENTIFIERS"].strip("'").split(",")
        autoit.control_send(window_identifier, control_identifier.strip('"'), text)


if __name__ == "__main__":
    a = AutoitWrapper()
    import time; time.sleep(2)
    a.activate_window("Mitel Connect")
