import time
import platform
from robot.api.logger import console


class DesktopAppWrapper:

    def __init__(self):
        pass

    def get_desktop_tool(self, platform_name=None, tool_name=None):

        if tool_name:
            pass
            # "for other tools used in future, ex: winium."
            # not yet implemented
        else:
            if not platform_name:
                platform_name = platform.system().lower()
            if platform_name == "windows":
                from windows_wrappers.autoit_wrapper import AutoitWrapper
                return AutoitWrapper()
            elif platform_name == "darwin":  # for MAC
                from mac_wrappers.mac_wrapper import MacWrapper
                return MacWrapper()
            else:
                pass
                # "functionality is not implemented (for other platforms, ex: Linux)"


if __name__ == "__main__":
    obj = DesktopAppWrapper()
    print(DesktopAppWrapper().get_desktop_tool())
