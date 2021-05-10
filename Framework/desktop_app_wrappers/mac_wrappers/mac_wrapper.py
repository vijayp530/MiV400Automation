__author__ = "Uttam"

import time
from atomac import AXClasses
from robot.api.logger import console

from mapMgr import mapMgr


class MacWrapper:
    """
    Wrappers for performing operations on mac desktop based apps
    """

    def __init__(self):
        self.native_elements = AXClasses.NativeUIElement()

    def __get_locator_for_tool(self, locator):
        if not locator.endswith("_mac"):
            return locator + "_mac"
        return locator

    def __clickOnElementInWindow(self, window, element):
        window.activate()
        position = element.AXPosition
        size = element.AXSize
        click_point = ((position[0] + size[0] / 2), (position[1] + size[1] / 2))
        window.clickMouseButtonLeft(click_point)

    def __read_attributes_from_map(self, locator):
        app_name = mapMgr.__getitem__(locator)["APP_NAME"].strip("'")
        control_identifiers = mapMgr.__getitem__(locator)["IDENTIFIERS"].split(",")

        search_criteria = {i.split("=")[0]: i.split("=")[1].strip('"') for i in control_identifiers}
        return app_name, search_criteria

    def __get_window(self, name, index=0):
        window_dict = {"Connect": "com.shoretel.manhattan",
                       "Presenter": "com.shoretel.MacPresenter",
                       "Chrome": "com.google.Chrome"}
        app_name = window_dict[name]
        app = self.native_elements.getAppRefByBundleId(app_name)
        w = app.windows()[index]
        return w

    def click(self, locator):
        locator = self.__get_locator_for_tool(locator)
        app_name, search_criteria = self.__read_attributes_from_map(locator)
        window = self.__get_window(app_name)

        time.sleep(2)  # wait for menu item to appear
        elements = window.findAllR(**search_criteria)
        self.__clickOnElementInWindow(window, elements[0])

    def activate_window(self, locator):
        pass

    def send_key(self, locator, key):
        pass

    def send_text(self, locator, text):
        locator = self.__get_locator_for_tool(locator)
        app_name, search_criteria = self.__read_attributes_from_map(locator)
        window = self.__get_window(app_name)

        time.sleep(2)
        elements = window.findAllR(**search_criteria)
        elements[0].sendKeys(text)


if __name__ == "__main__":
    m = MacWrapper()

    time.sleep(5)
    #m.test()
    m.send_text("", "")
