import os
import sys
import zipfile
import glob
import re
import shutil
from selenium import webdriver
if re.match(r'^2.7.', sys.version):
    import _winreg as winreg
else:
    import winreg


def install_client_silently(version):
    """
    Author: UKumar
    install_client() - Installs connect client
    """
    #command = r'start /wait \\10.17.1.56\Builds\213.20.2241.0\install-win\ShoreTelConnect.exe /s /sms /v"/qn INSTALLDIR=C:\NodeWebKit'
    command = r'start /wait C:\ClientInstaller\ShoreTelConnect.exe /s /sms /v"/qn INSTALLDIR=C:\NodeWebKit'
    if version.lower() == "lower":
        command = r'start /wait C:\ClientInstaller\LowerVersionInstaller\ShoreTelConnect.exe /s /sms /v"/qn INSTALLDIR=C:\NodeWebKit'
    os.system(command)

def uninstall_client():
    """
    Author: UKumar
    uninstall_client() - Uninstalls connect client
    """
    command = r'wmic product where name="ShoreTel Connect" call uninstall /nointeractive'
    os.system(command)
    
def verify_client_plugins():
    """
    Author: UKumar
    verify_client_plugins() - To verify that all the plugins required for Connect Client are installed
    """
    try:
        client_add_ins_to_verify = ['ShoreTelConnectCASConnHostAddIn', 'ShoreTelConnectContactUploadAddIn',
                                    'ShoreTelConnectSTVMAddIn', 'ShoreTelConnectUCBAddIn']
        
        connection = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        akeys = winreg.OpenKey(connection, r'SOFTWARE\Microsoft\Office\Outlook\Addins')
        installed_add_ins = []
        for i in range(10):
            try:
                x = winreg.EnumKey(akeys, i)
                y = winreg.OpenKey(akeys, x)
                val = winreg.QueryValueEx(y, "FriendlyName")
                installed_add_ins.append(val[0])
            except EnvironmentError:
                break
        winreg.CloseKey(akeys)
        
        for add_in in client_add_ins_to_verify:
            if add_in in installed_add_ins:
                #log.mjLog.LogReporter("ManhattanComponent", "info", "verify_client_plugins - %s plugin installed" %add_in)
                print("verify_client_plugins - %s plugin installed" %add_in)
            else:
                raise AssertionError("%s plugin not installed" %add_in)
    except:
        raise
        
def delete_registry_entry():
    """
    Author: UKumar
    delete_registry_entry() - Delets ShoreTel key from the registry
    """
    try:
        connection = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
        print(connection)
        akeys = winreg.OpenKey(connection, r'SOFTWARE\ShoreTel')
        print(akeys)
        winreg.DeleteKeyEx(akeys, 'Client')
        ikeys = winreg.OpenKey(connection, r'SOFTWARE')
        winreg.DeleteKeyEx(ikeys, 'ShoreTel')
        winreg.CloseKey(akeys)
    except Exception as e:
        raise e

def unzip_recording(file_path):
    """
    Author: UKumar
    unzip_recording() - extracts recording file from zip file
    """
    try:
        with zipfile.ZipFile(file_path, "r") as z:
            z.extractall(os.path.dirname(file_path))
        
        for file in glob.glob(os.path.join(os.path.dirname(file_path), '*.zip')):
            os.remove(file)
    except FileNotFoundError as e:
        raise e
    
def launch():
    browser = webdriver.Chrome("C:\\NodeWebKit\\chromedriver.exe")

def delete_shoretel_folder():
    """
    Author: Indresh
    delete_shoretel_folder() - Deletes ShoreTel folder from "\\AppData\\Local\\ShoreTel"
    """
    try:
        path = os.getenv('LOCALAPPDATA') + "\ShoreTel"
        shutil.rmtree(path)
    except:
        return False 

def close_program(**params):
    '''
    Author: Indresh
    Closes the desired program
    params["program"] will contain the program name which needs to be closed
    '''
    try:
        killCommand = "taskkill.exe /f /im " + params["program"] + ".exe"
        os.system(killCommand)
    except:
        raise

    
if __name__ == "__main__":
    param_name = sys.argv[1]
    if param_name == "install":
        install_client(sys.argv[2])
    elif param_name == "uninstall":
        uninstall_client()
    elif param_name == "verify_client_plugins":
        verify_client_plugins()
    elif param_name == "delete_registry_entry":
        delete_registry_entry()
    elif param_name == "launch":
        launch()
    else:
        pass


