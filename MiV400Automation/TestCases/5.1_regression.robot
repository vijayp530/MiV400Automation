*** Settings ***
Resource   ../RobotKeywords/Setup_And_Teardown.robot
Library    ../lib/MyListner.py
Test Timeout  25 minutes
Suite Setup  Phones Initialization
Test Setup  Check Phone Connection
#Test Setup   Boss Portal Login
Test Teardown      Disconnect Terminal
Suite Teardown       Check Phone Connection

*** Test Cases ***

########################  crash file test cases ##############################

762201: ConfigCrashFile_Retriev_10-D-3-1Configured_Action URI_Off Hook
    [Tags]    Owner:Anuj    Reviewer:    configcrash    762201
    &{Details}=    Create Dictionary    DownloadProtocol=FTP    FTP_Server=10.112.123.107    FTP_Username=desktop    FTP_Path=systeminfo    FTP_Password=desktop
    &{parameters}=    Create Dictionary       upload system info manual option=1     `upload system info on crash=1    upload system info server=${serverDetails}
    Given I want to configure ConfigurationServer parameters using ${Details} for ${phone1}
    &{fileName}=    Create Dictionary    fileName=["server.cfg","aastra.cfg"]
    Then Create ${startUp} file using ${parameters}
    Then Create ${systeminfo} folder on FTP server
    Then Send ${startUp} file in ${systeminfo} folder on FTP server
    Then reboot ${phone1}
    Then on the WUI of ${phone1} click on the ${uploadButton}
    Then check ${fileSent} text in the webUI on ${phone1}
    Then Using ${phone1} verify configuration ${fileName} files in sysinfo folder on FTP server
    And disconnect the call from ${phone1}

762203: ConfigCrashFile_Retriev_17
    [Tags]    Owner:Anuj    Reviewer:    configcrash    762203
    &{Details} =  Create Dictionary    DownloadProtocol=FTP    FTP_Server=10.112.123.107    FTP_Username=desktop    FTP_Password=desktop    FTP_Path=systeminfo
    &{parameters} =  Create Dictionary       upload system info manual option= 1     upload system info server=${serverDetails}
    Given I want to configure ConfigurationServer parameters using ${Details} for ${phone1}
    &{fileName}=    Create Dictionary    fileName=["server.cfg","aastra.cfg"]
    Then Create ${startUp} file using ${parameters}
    Then Create ${systeminfo} folder on FTP server
    Then Send ${startUp} file in ${systeminfo} folder on FTP server
    Then reboot ${phone1}
    Then on the WUI of ${phone1} click on the ${uploadButton}
    Then check ${fileSent} text in the webUI on ${phone1}
    Then Using ${phone1} verify configuration ${fileName} files in sysinfo folder on FTP server
    And disconnect the call from ${phone1}

762204: ConfigCrashFile_Retriev_19
    [Tags]    Owner:Anuj    Reviewer:    configcrash    762204
    &{Details} =  Create Dictionary    DownloadProtocol=FTP    FTP_Server=10.112.123.107    FTP_Username=desktop    FTP_Password=desktop     FTP_Path=systeminfo
    &{parameters} =  Create Dictionary       upload system info manual option= 1     upload system info server=${serverDetails}
    Given I want to configure ConfigurationServer parameters using ${Details} for ${phone1}
    &{fileName}=    Create Dictionary    fileName=["server.cfg","aastra.cfg"]
    Then Create ${startUp} file using ${parameters}
    Then Create ${systeminfo} folder on FTP server
    Then Send ${startUp} file in ${systeminfo} folder on FTP server
    Then reboot ${phone1}
    Then on the WUI of ${phone1} click on the ${uploadButton}
    Then check ${fileSent} text in the webUI on ${phone1}
    Then Using ${phone1} verify configuration ${fileName} files in systeminfo folder on FTP server
    Then press hardkey as ${menu} on ${phone1}
    Then on ${phone1} press ${softKey} ${bottomKey1} for 1 times
    Then on ${phone1} verify display message ${sysInfo}
    Then press hardkey as ${menu} on ${phone1}
    Then check ${upload_Xpath} text in the webUI on ${phone1}

762205: ConfigCrashFile_Retriev_20
    [Tags]    Owner:Anuj    Reviewer:    configcrash    762205
    &{Details} =  Create Dictionary    DownloadProtocol=HTTP    Http_Serv=10.112.123.89    Http_Path=systeminfo
    &{parameters} =  Create Dictionary       upload system info manual option= 1     upload system info server=${httpserverDetails}
    Given I want to configure ConfigurationServer parameters using ${Details} for ${phone1}
    &{fileName}=    Create Dictionary    fileName=["server.cfg","aastra.cfg"]
    Then Create ${startUp} file using ${parameters}
    Then Create ${systeminfo} folder on HTTP server
    Then Send ${startUp} file in ${systeminfo} folder on HTTP server
    Then reboot ${phone1}
    Then on the WUI of ${phone1} click on the ${uploadButton}
    Then check ${fileSent} text in the webUI on ${phone}
    Then Using ${phone1} verify configuration ${fileName} files in sysinfo folder on FTP server
    Then press hardkey as ${menu} on ${phone1}
    Then on ${phone1} press ${softKey} ${bottomKey1} for 1 times
    Then on ${phone1} verify display message ${sysInfo}
    Then press hardkey as ${menu} on ${phone1}
    Then check ${upload_Xpath} text in the webUI on ${phone1}

762206: ConfigCrashFile_Retriev_22
    [Tags]    Owner:Anuj    Reviewer:    configcrash    762206
    &{Details} =  Create Dictionary    DownloadProtocol=FTP    FTP_Server=10.112.123.107    FTP_Username=desktop    FTP_Password=desktop    FTP_Path=systeminfo
    &{parameters} =  Create Dictionary       upload system info manual option= 1     upload system info server=${serverDetails}
    Given I want to configure ConfigurationServer parameters using ${Details} for ${phone1}
    &{fileName}=    Create Dictionary    fileName=["server.cfg","aastra.cfg"]
    Then Create ${startUp} file using ${parameters}
    Then Create ${systeminfo} folder on FTP server
    Then Send ${startUp} file in ${systeminfo} folder on FTP server
    Then reboot ${phone1}
    Then on the WUI of ${phone1} click on the ${uploadButton}
    Then check ${fileSent} text in the webUI on ${phone}
    Then Using ${phone1} verify configuration ${fileName} files in sysinfo folder on FTP server
    Then press hardkey as ${menu} on ${phone1}
    Then on ${phone1} press ${softKey} ${bottomKey1} for 1 times
    Then on ${phone1} verify display message ${sysInfo}
    Then press hardkey as ${menu} on ${phone1}
    Then check ${upload_Xpath} text in the webUI on ${phone1}

    &{Details} =  Create Dictionary    DownloadProtocol=HTTP    Http_Serv=10.112.123.89    Http_Path=systeminfo
    &{parameters} =  Create Dictionary       upload system info manual option= 1     upload system info server=${httpserverDetails}
    Given I want to configure ConfigurationServer parameters using ${Details} for ${phone1}
    &{fileName}=    Create Dictionary    fileName=["server.cfg","aastra.cfg"]
    Then Create ${startUp} file using ${parameters}
    Then Create ${systeminfo} folder on HTTP server
    Then Send ${startUp} file in ${systeminfo} folder on HTTP server
    Then reboot ${phone1}
    Then on the WUI of ${phone1} click on the ${uploadButton}
    Then check ${fileSent} text in the webUI on ${phone1}
    Then Using ${phone1} verify configuration ${fileName} files in sysinfo folder on FTP server
    Then press hardkey as ${menu} on ${phone1}
    Then on ${phone1} press ${softKey} ${bottomKey1} for 1 times
    Then on ${phone1} verify display message ${sysInfo}
    Then press hardkey as ${menu} on ${phone1}
    Then check ${upload_Xpath} text in the webUI on ${phone1}

841086: Failed download - server unavaible (no response) reattempt
    [Tags]    Owner:Anuj    Reviewer:    configcrash    841086   little change are required
    &{Details} =  Create Dictionary    DownloadProtocol=FTP    FTP_Server=10.112.123.106    FTP_Username=desktop    FTP_Password=desktop    FTP_Path=systeminfo
    &{parameters} =  Create Dictionary       upload system info manual option= 1     config files mandatory download= "startup.cfg"    config files number of reattempt= -1    config files max delay= 60    config files skip key enabled= 1    upload system info server=${serverDetails}
    Given I want to configure ConfigurationServer parameters using ${Details} for ${phone1}
    Then Create ${startUp} file using ${parameters}
    Then Create ${systeminfo} folder on FTP server
    Then Send ${startUp} file in ${systeminfo} folder on FTP server
    Then reboot ${phone1}

841087: Failed download - file not avaible reattempt
    [Tags]    Owner:Anuj    Reviewer:    configcrash    841087   little change are required
    &{Details} =  Create Dictionary    DownloadProtocol=FTP    FTP_Server=10.112.123.107    FTP_Username=desktop    FTP_Password=desktop    FTP_Path=systeminfo
    &{parameters} =  Create Dictionary       upload system info manual option= 1     config files mandatory download= "startup.cfg"    config files number of reattempt= -1    config files max delay= 60    config files skip key enabled= 1    upload system info server=${serverDetails}
    Given I want to configure ConfigurationServer parameters using ${Details} for ${phone1}
    Then Create ${startUp} file using ${parameters}
    Then Create ${systeminfo} folder on FTP server
    Then Send ${startUp} file in ${systeminfo} folder on FTP server
    Then reboot ${phone1}
    Then on the WUI of ${phone1} click on the ${uploadButton}
    &{fileName}=    Create Dictionary    fileName=["startup.cfg"]
    Then Using ${phone1} delete configuration ${fileName} files from ${folderName} folder on ${server} server

841090: download protocol ftp reattempt
    [Tags]    Owner:Anuj    Reviewer:    configcrash    841090   little change are required
    &{Details} =  Create Dictionary    DownloadProtocol=FTP    FTP_Server=10.112.123.107    FTP_Username=desktop    FTP_Password=desktop    FTP_Path=systeminfo
    &{parameters} =  Create Dictionary       upload system info manual option= 1     config files mandatory download= "startup.cfg"    config files number of reattempt= -1    config files max delay= 60    config files skip key enabled= 1    upload system info server=${serverDetails}
    Given I want to configure ConfigurationServer parameters using ${Details} for ${phone1}
    Then Create ${startUp} file using ${parameters}
    Then Create ${systeminfo} folder on FTP server
    Then Send ${startUp} file in ${systeminfo} folder on FTP server
    Then reboot ${phone1}
    Then on the WUI of ${phone1} click on the ${uploadButton}
    &{fileName}=    Create Dictionary    fileName=["startup.cfg"]
    Then Using ${phone1} delete configuration ${fileName} files from ${folderName} folder on ${server} server


841091: download protocol http reattempt
    [Tags]    Owner:Anuj    Reviewer:    configcrash    841091   little change are required
    [&{Details} =  Create Dictionary    DownloadProtocol=HTTP    FTP_Server=10.112.123.89    FTP_Username=root    FTP_Password=Jafe@20_20    FTP_Path=systeminfo
    &{parameters} =  Create Dictionary       upload system info manual option= 1     config files mandatory download= "startup.cfg"    config files number of reattempt= -1    config files max delay= 60    config files skip key enabled= 1    upload system info server=${httpserverDetails}
    Given I want to configure ConfigurationServer parameters using ${Details} for ${phone1}
    Then Create ${startUp} file using ${parameters}
    Then Create ${systeminfo} folder on HTTP server
    Then Send ${startUp} file in ${systeminfo} folder on HTTP server
    Then reboot ${phone1}
    Then on the WUI of ${phone1} click on the ${uploadButton}
    &{fileName}=    Create Dictionary    fileName=["startup.cfg"]
    Then Using ${phone1} delete configuration ${fileName} files from ${folderName} folder on ${server} server

841129: change conf files mandatory parameter will auto restart - config files number of reattempt
    [Tags]    Owner:Anuj    Reviewer:    configcrash    841129   little change are required
    &{Details} =  Create Dictionary    DownloadProtocol=FTP    FTP_Server=10.112.123.107    FTP_Username=desktop    FTP_Password=desktop    FTP_Path=systeminfo
    &{parameters} =  Create Dictionary       upload system info manual option= 1     config files mandatory download= "startup.cfg"    config files number of reattempt= -1    config files max delay= 60    config files skip key enabled= 1    upload system info server=${serverDetails}
    Given I want to configure ConfigurationServer parameters using ${Details} for ${phone1}
    Then Create ${startUp} file using ${parameters}
    Then Create ${systeminfo} folder on FTP server
    Then Send ${startUp} file in ${systeminfo} folder on FTP server
    Then reboot ${phone1}

    &{parameters} =  Create Dictionary       upload system info manual option= 1     config files mandatory download= "startup.cfg"    config files number of reattempt= -1    config files max delay= 60    config files skip key enabled= 1    upload system info server=${serverDetails}
    Then Create ${startUp} file using ${parameters}
    Then Create ${systeminfo} folder on FTP server
    Then Send ${startUp} file in ${systeminfo} folder on FTP server
    Then reboot ${phone1}
    Then on the WUI of ${phone1} click on the ${uploadButton}

841089: download protocol tftp reattempt
    [Tags]    Owner:Anuj    Reviewer:    configcrash    841089   little change are required
    &{Details} =  Create Dictionary    DownloadProtocol=TFTP    Primary_Server=10.112.91.70
    &{parameters} =  Create Dictionary      upload_system_info_server=1    paramone=upload system info manual option: 1    paramtwo=config files mandatory download: "startup.cfg"     paramthree=config files number of reattempt: -1    paramfour=config files max delay: 60    paramfive=config files skip key enabled: 1
    Given I want to configure ConfigurationServer parameters using ${Details} for ${phone1}
    Given I want to copy startup.cfg on ${phone1} using tftp with ${parameters}


762363:DTMF23: Verify Global dtmf method can be dynamically set to BOTH using WUI
    [Tags]    Owner:Anuj    Reviewer:    762363
    &{Details} =  Create Dictionary      line=line1    dtmfMethod=0
    Given on ${phone1} register the line with ${Details} for MiV400 pbx
    &{Details} =  Create Dictionary      line=line5    dtmfMethod=0
    Given on ${phone1} register the line with ${Details} for MiV400 pbx
    &{Details} =  Create Dictionary      line=line2    dtmfMethod=1
    Given on ${phone1} register the line with ${Details} for MiV400 pbx
    &{Details} =  Create Dictionary      line=line6    dtmfMethod=1
    Given on ${phone1} register the line with ${Details} for MiV400 pbx
    &{Details} =  Create Dictionary      line=line3    dtmfMethod=2
    Given on ${phone1} register the line with ${Details} for MiV400 pbx
    &{Details} =  Create Dictionary      line=line7    dtmfMethod=2
    Given on ${phone1} register the line with ${Details} for MiV400 pbx
    &{Details} =  Create Dictionary      dtmfMethod=2
    Then I want to configure GlobalSettings parameters using ${Details} for ${phone1}
    using ${phonewui} log into ${phone1} url
    Then Using ${PhoneWUI} Start the capture on all port on ${phone1} URL
    Then i want to make a two party call between ${phone1} and ${phone2} using ${line1}
    Then answer the call on ${phone2} using ${line1}
    Then press hardkey as ${dialNumber2} on ${phone1}
    Then disconnect the call from ${phone2}
    Then Using ${PhoneWUI} stop the capture from ${phone1} URL
    Then Using ${PhoneWUI} download the capture from ${phone1} URL
    Then Verify the captureFile contains RFC 2833 inside ${Protocols['RTP']} packets

    Then using ${phonewui} log into ${phone1} url
    Then Using ${PhoneWUI} Start the capture on all port on ${phone1} URL
    Then i want to make a two party call between ${phone1} and ${phone2} using ${line2}
    Then answer the call on ${phone2} using ${line1}
    Then press hardkey as ${dialNumber2} on ${phone1}
    Then disconnect the call from ${phone2}
    Then Using ${PhoneWUI} stop the capture from ${phone1} URL
    Then Using ${PhoneWUI} download the capture from ${phone1} URL
    Then verify the captureFile contains INFO sip inside ${Protocols['RTP']} all packets

    Then using ${phonewui} log into ${phone1} url
    Then Using ${PhoneWUI} Start the capture on all port on ${phone1} URL
    Then i want to make a two party call between ${phone1} and ${phone2} using ${line3}
    Then answer the call on ${phone2} using ${line1}
    Then press hardkey as ${dialNumber2} on ${phone1}
    Then disconnect the call from ${phone2}
    Then Using ${PhoneWUI} stop the capture from ${phone1} URL
    Then Using ${PhoneWUI} download the capture from ${phone1} URL
    Then verify the captureFile contains INFO sip inside ${Protocols['RTP']} all packets
    Then Verify the captureFile contains RFC 2833 inside ${Protocols['RTP']} packets

762364: DTMF24: Verify per line dtmf method can be dynamically set using WUI
    [Tags]    Owner:Anuj    Reviewer:    762364
    &{Details} =  Create Dictionary      line=line1    dtmfMethod=0
    Given on ${phone1} register the line with ${Details} for MiV400 pbx
    &{Details} =  Create Dictionary      line=line5    dtmfMethod=0
    Given on ${phone1} register the line with ${Details} for MiV400 pbx
    &{Details} =  Create Dictionary      line=line2    dtmfMethod=1
    Given on ${phone1} register the line with ${Details} for MiV400 pbx
    &{Details} =  Create Dictionary      line=line6    dtmfMethod=1
    Given on ${phone1} register the line with ${Details} for MiV400 pbx
    &{Details} =  Create Dictionary      line=line3    dtmfMethod=2
    Given on ${phone1} register the line with ${Details} for MiV400 pbx
    &{Details} =  Create Dictionary      line=line7    dtmfMethod=2
    Given on ${phone1} register the line with ${Details} for MiV400 pbx

    &{Details} =  Create Dictionary      line=line1    dtmfMethod=1
    Given on ${phone1} register the line with ${Details} for MiV400 pbx
    &{Details} =  Create Dictionary      line=line5    dtmfMethod=1
    Given on ${phone1} register the line with ${Details} for MiV400 pbx
    &{Details} =  Create Dictionary      line=line2    dtmfMethod=2
    Given on ${phone1} register the line with ${Details} for MiV400 pbx
    &{Details} =  Create Dictionary      line=line6    dtmfMethod=2
    Given on ${phone1} register the line with ${Details} for MiV400 pbx
    &{Details} =  Create Dictionary      line=line3    dtmfMethod=0
    Given on ${phone1} register the line with ${Details} for MiV400 pbx
    &{Details} =  Create Dictionary      line=line7    dtmfMethod=0
    Given on ${phone1} register the line with ${Details} for MiV400 pbx

    using ${phonewui} log into ${phone1} url
    Then Using ${PhoneWUI} Start the capture on all port on ${phone1} URL
    Then i want to make a two party call between ${phone1} and ${phone2} using ${line1}
    Then answer the call on ${phone2} using ${line1}
    Then press hardkey as ${dialNumber2} on ${phone1}
    Then disconnect the call from ${phone2}
    Then Using ${PhoneWUI} stop the capture from ${phone1} URL
    Then Using ${PhoneWUI} download the capture from ${phone1} URL
    Then Verify the captureFile contains INFO sip inside ${Protocols['RTP']} packets

    Then using ${phonewui} log into ${phone1} url
    Then Using ${PhoneWUI} Start the capture on all port on ${phone1} URL
    Then i want to make a two party call between ${phone1} and ${phone2} using ${line2}
    Then answer the call on ${phone2} using ${line1}
    Then press hardkey as ${dialNumber2} on ${phone1}
    Then disconnect the call from ${phone2}
    Then Using ${PhoneWUI} stop the capture from ${phone1} URL
    Then Using ${PhoneWUI} download the capture from ${phone1} URL
    Then verify the captureFile contains INFO sip inside ${Protocols['RTP']} all packets
    Then Verify the captureFile contains RFC 2833 inside ${Protocols['RTP']} packets

    Then using ${phonewui} log into ${phone1} url
    Then Using ${PhoneWUI} Start the capture on all port on ${phone1} URL
    Then i want to make a two party call between ${phone1} and ${phone2} using ${line3}
    Then answer the call on ${phone2} using ${line1}
    Then press hardkey as ${dialNumber2} on ${phone1}
    Then disconnect the call from ${phone2}
    Then Using ${PhoneWUI} stop the capture from ${phone1} URL
    Then Using ${PhoneWUI} download the capture from ${phone1} URL
    Then verify the captureFile contains RFC 2833 inside ${Protocols['RTP']} all packets


763142: WebUI restart
    [Tags]    Owner:Anuj    Reviewer:    xfer    763142
    &{configurationDetails}=    CREATE DICTIONARY    log level= 1
    Given Configure parameters on ${phone1} using ${configurationDetails}
    Then using ${phonewui} log into ${phone1} url
    Then Using ${UIPortal} Navigate to go to ${TroubleShootingMenu} page on ${phone1} URL
    Then Verify text min for ${TroubleshootLink['min']} on the ${phone1} URL
    Then reboot ${phone1}
    Then using ${phonewui} log into ${phone1} url
    Then Using ${UIPortal} Navigate to go to ${TroubleShootingMenu} page on ${phone1} URL
    Then Verify text min for ${TroubleshootLink['min']} on the ${phone1} URL
    Then Verify text min for ${TroubleshootLink['webuirestart']} on the ${phone1} URL

763143: TUI Restart
    [Tags]    Owner:Anuj    Reviewer:    xfer    763143
    &{configurationDetails}=    CREATE DICTIONARY    log level= 1
    Given Configure parameters on ${phone1} using ${configurationDetails}
    Then Using ${PhoneWUI} Start the capture on all port on ${phone1} URL
    Then press hardkey as ${menu} on ${phone1}
    Then on ${phone1} press ${hardKey} ${scrollRight} for 4 times
    Then on ${phone1} press ${softkey} ${bottomKey1} for 1 times
    Then on ${phone1} press ${hardKey} ${scrollLeft} for 1 times
    Then press hardkey as ${enter} on ${phone1}
    Then on ${phone1} wait for 180 seconds
    Then Using ${PhoneWUI} stop the capture from ${phone1} URL
    Then Using ${PhoneWUI} download the capture from ${phone1} URL
    Then verify the captureFile contains LogReboot inside ${Protocols['RTP']} all packets
    Then using ${phonewui} log into ${phone1} url
    Then Using ${UIPortal} Navigate to go to ${TroubleShootingMenu} page on ${phone1} URL
    Then Verify text min for ${TroubleshootLink['min']} on the ${phone1} URL

763144: WebUI- restore- Restart
    [Tags]    Owner:Anuj    Reviewer:    xfer    763144
    Then using ${phonewui} log into ${phone1} url
    Then Using ${Phone_wui} Navigate to go to ${ResetMenu} page on ${phone1} URL
    Then Using ${Phone_wui} Navigate to go to ${ResetLink['FactoryReset']} page on ${phone1} URL
    Then Using ${Phone_wui} Navigate to go to ${NetworkMenu} page on ${phone1} URL
    Then Using ${Phone_wui} send ${phone1} value for ${NetworkMenuLink['IpAddress']} to ${phone1} URL
    Then Using ${Phone_wui} send 0 value for ${NetworkMenuLink['Dhcp']} to ${phone1} URL
    Then Using ${Phone_wui} send ${subnetMask} value for ${NetworkMenuLink['subnetMask']} to ${phone1} URL
    Then Using ${Phone_wui} send 10.112.123.1 value for ${NetworkMenuLink['Gateway']} to ${phone1} URL
    Then Using ${Phone_wui} send 10.112.68.10 value for ${NetworkMenuLink['PrimaryDns']} to ${phone1} URL
    Then Using ${Phone_wui} send 10.98.10.194 value for ${NetworkMenuLink['SecondartDns']} to ${phone1} URL
    Then Using ${Phone_wui} send 1 value for ${NetworkMenuLink['Dhcp']} to ${phone1} URL
    Then Using ${Phone_wui} click on the ${NetworkMenuLink['SaveSettings']} on ${phone1} URL
    Then on ${phone1} wait for 240 seconds
    &{Details} =  Create Dictionary    DownloadProtocol=TFTP    Primary_Server=10.112.95.75
    Given I want to configure ConfigurationServer parameters using ${Details} for ${phone1}
    Then reboot ${phone1}
    Then using ${phonewui} log into ${phone1} url
    Then Using ${Phone_wui} Navigate to go to ${TroubleShootingMenu} page on ${phone1} URL
    Then Verify text WEBUI::Restart for ${webUiRestart} on the ${phone1} URL


763563: TC01: "Verify: When blacklist parameter value changed back to same value as server.cfg - parameters are deleted from local.cfg
    [Tags]    Owner:Anuj    Reviewer:    vdp    763563
    &{Details} =  Create Dictionary    DownloadProtocol=TFTP    Primary_Server=10.112.123.107
    &{parameters} =  Create Dictionary      upload_system_info_server=1    paramone=sip xml notify event: 1   paramtwo=user config URL: ${vdpdetails}
    Given I want to configure ConfigurationServer parameters using ${Details} for ${phone1}
    Given I want to copy startup.cfg on ${phone1} using tftp with ${parameters}
    Then reboot ${phone1}
    Then I want to program bottomkey softkey with hotdesklogin on position 1 for ${phone1}
    Then on ${phone1} press ${softkey} ${bottomKey1} for 1 times
    Then on ${phone1} enter number 4165142501
    Then on ${phone1} press ${softkey} ${bottomKey1} for 1 times
    &{configurationDetails}=    CREATE DICTIONARY    log module linemgr= 65533    log server ip= 10.112.123.107   log server port= 513
    Given Configure parameters on ${phone1} using ${configurationDetails}
    Then using ${phonewui} log into ${phone1} url
    Then Using ${Phone_wui} Navigate to go to ${TroubleShootingMenu} page on ${phone1} URL
    Then Using ${Phone_wui} click on the ${TroubleShootingMenu['local_cfg']} on ${phone1} URL
    ### need to write verification method
    Then disconnect the call from ${phone1}
    Then on ${phone1} press ${softkey} ${bottomKey1} for 1 times
    Then on ${phone1} press ${softkey} ${bottomKey1} for 1 times
    Then on ${phone} press ${softkey} ${bottomKey1} for 1 times
    Then on ${phone1} enter number 4165142501
    Then on ${phone} press ${softkey} ${bottomKey1} for 1 times
    Then using ${phonewui} log into ${phone1} url
    Then Using ${Phone_wui} Navigate to go to ${TroubleShootingMenu} page on ${phone1} URL
    Then Using ${Phone_wui} click on the ${TroubleShootingMenu['local_cfg']} on ${phone1} URL
    ### need to write verification method



    &{configurationDetails}=    CREATE DICTIONARY    log module linemgr= 65533    log server ip= 10.112.123.107   log server port= 513
    Given Configure parameters on ${phone1} using ${configurationDetails}
    Then using ${phonewui} log into ${phone1} url
    Then Using ${Phone_wui} Navigate to go to ${TroubleShootingMenu} page on ${phone1} URL
    Then Using ${Phone_wui} click on the ${TroubleShootingMenu['local_cfg']} on ${phone1} URL
    ### need to write verification method
    Then disconnect the call from ${phone1}
    Then on ${phone} press ${softkey} ${bottomKey1} for 1 times
    Then on ${phone} press ${softkey} ${bottomKey1} for 1 times

    Then on ${phone} press ${softkey} ${bottomKey1} for 1 times
    Then on ${phone1} enter number 4165142501
    Then on ${phone} press ${softkey} ${bottomKey1} for 1 times
    Then using ${phonewui} log into ${phone1} url
    Then Using ${Phone_wui} Navigate to go to ${TroubleShootingMenu} page on ${phone1} URL
    Then Using ${Phone_wui} click on the ${TroubleShootingMenu['local_cfg']} on ${phone1} URL
    ### need to write verification method
    Then reboot ${phone1}
    Then using ${phonewui} log into ${phone1} url
    Then Using ${Phone_wui} Navigate to go to ${TroubleShootingMenu} page on ${phone1} URL
    Then Using ${Phone_wui} click on the ${TroubleShootingMenu['local_cfg']} on ${phone1} URL
    ### need to write verification method


763568: TC06: "Verify: When blacklist parameter value changed back to same value as default - parameters are deleted from local.cfg
    [Tags]    Owner:Anuj    Reviewer:    vdp    763568
    &{configurationDetails}=    CREATE DICTIONARY    sip blacklist duration= 180
    Given Configure parameters on ${phone1} using ${configurationDetails}
    Then using ${phonewui} log into ${phone1} url
    Then Using ${Phone_wui} Navigate to go to ${TroubleShootingMenu} page on ${phone1} URL
    Then Using ${Phone_wui} click on the ${TroubleShootingMenu['local_cfg']} on ${phone1} URL
    ### need to write verification method
    &{configurationDetails}=    CREATE DICTIONARY    sip blacklist duration= 0
    Given Configure parameters on ${phone1} using ${configurationDetails}
    Then using ${phonewui} log into ${phone1} url
    Then Using ${Phone_wui} Navigate to go to ${TroubleShootingMenu} page on ${phone1} URL
    Then Using ${Phone_wui} click on the ${TroubleShootingMenu['local_cfg']} on ${phone1} URL
    ### need to write verification method

763569: TC07: Test for Precedence
    [Tags]    Owner:Anuj    Reviewer:    vdp    763569

    &{Details} =  Create Dictionary    DownloadProtocol=TFTP    Primary_Server=10.112.123.107
    &{parameters} =  Create Dictionary      upload_system_info_server=1    paramone=sip xml notify event: 1   paramtwo=user config URL: ${vdpdetails}
    Given I want to configure ConfigurationServer parameters using ${Details} for ${phone1}
    Given I want to copy startup.cfg on ${phone1} using tftp with ${parameters}
    Then reboot ${phone1}
    Then I want to program bottomkey softkey with hotdesklogin on position 1 for ${phone1}
    Then on ${phone1} press ${softkey} ${bottomKey1} for 1 times
    Then on ${phone1} enter number 4165142501
    Then on ${phone1} press ${softkey} ${bottomKey1} for 1 times

    &{parameters} =  Create Dictionary       download protocol= HTTP     http server= 0.112.123.89    http path= systeminfo
    Then Create ${startUp} file using ${parameters}
    Then Create ${systeminfo} folder on HTTP server
    Then Send ${startUp} file in ${systeminfo} folder on HTTP server

    &{parameters} =  Create Dictionary       download protocol= FTP     ftp server= 10.112.123.107    ftp path= systeminfo    ftp username= desktop    ftp password= desktop

    Then Create ${user_cfg} file using ${parameters}
    Then Create ${systeminfo} folder on FTP server
    Then Send ${user_cfg} file in ${systeminfo} folder on FTP server
    &{Details} =  Create Dictionary    DownloadProtocol=FTP    FTP_Server=10.112.123.107    FTP_Username=desktop    FTP_Password=desktop    FTP_Path=systeminfo
    Given I want to configure ConfigurationServer parameters using ${Details} for ${phone1}
    Then reboot ${phone1}
    Then using ${phonewui} log into ${phone1} url
    Then Using ${Phone_wui} Navigate to go to ${TroubleShootingMenu} page on ${phone1} URL
    Then Using ${Phone_wui} click on the ${TroubleShootingMenu['local_cfg']} on ${phone1} URL
    ### need to write verification method
    disconnect the call from ${phone1}
    &{configurationDetails}=    CREATE DICTIONARY    DownloadProtocol=TFTP    Primary_Server=10.112.123.107
    Given Configure parameters on ${phone1} using ${configurationDetails}
    Then using ${phonewui} log into ${phone1} url
    Then Using ${Phone_wui} Navigate to go to ${TroubleShootingMenu} page on ${phone1} URL
    Then Using ${Phone_wui} click on the ${TroubleShootingMenu['local_cfg']} on ${phone1} URL
    ### need to write verification method
    Then on ${phone1} press ${softkey} ${bottomKey1} for 1 times
    Then on ${phone1} press ${softkey} ${bottomKey1} for 1 times

    Then on ${phone1} press ${softkey} ${bottomKey1} for 1 times
    Then on ${phone1} enter number 4165142501
    Then on ${phone1} press ${softkey} ${bottomKey1} for 1 times
    Then using ${phonewui} log into ${phone1} url
    Then Using ${Phone_wui} Navigate to go to ${TroubleShootingMenu} page on ${phone1} URL
    Then Using ${Phone_wui} click on the ${TroubleShootingMenu['local_cfg']} on ${phone1} URL
    ### need to write verification method

763570: TC08: Disable/Enable LLDP via TUI, and verify the parameter is populated in local.cfg
    [Tags]    Owner:Anuj    Reviewer:     763570
    Given press hardkey as ${menu} on ${phone1}
    Then on ${phone1} press ${hardKey} ${scrollleft} for 6 times
    Then on ${phone1} press ${hardKey} ${scrolldown} for 7 times
    Then on ${phone1} press ${softkey} ${bottomkey1} for 1 times
    Then on ${phone1} press ${hardKey} ${scrollup} for 1 times
    Then on ${phone1} press ${hardKey} ${scrollleft} for 1 times
    Then press hardkey as ${enter} on ${phone1}
    Then on ${phone1} wait for 180 seconds
    Then using ${phonewui} log into ${phone1} url
    Then Using ${Phone_wui} Navigate to go to ${TroubleShootingMenu} page on ${phone1} URL
    Then Using ${Phone_wui} click on the ${TroubleShootingMenu['local_cfg']} on ${phone1} URL
    ### need to write verification method

763573: TC11: XML
    [Tags]    Owner:Anuj    Reviewer:     vdp    763573
    &{configurationDetails}=    CREATE DICTIONARY    download protocol=TFTP    tftp server=10.112.123.107    lldp= 0    log server ip=10.112.123.107    log server port=513    auto resync mode=1    auto resync mode = 17:00    action uri poll=http://10.112.123.89/weather.xml    action uri poll=45    paging group listening=224.0.0.2:10000,239.0.1.20:15000
    Given Configure parameters on ${phone1} using ${configurationDetails}
    Then using ${phonewui} log into ${phone1} url
    Then Using ${Phone_wui} Navigate to go to ${TroubleShootingMenu} page on ${phone1} URL
    Then Using ${Phone_wui} click on the ${TroubleShootingMenu['local_cfg']} on ${phone1} URL
    ### need to write verification method

763572: TC10: "Add blacklisted parameter and non blacklisted parameter in user-local.cfg.
    [Tags]    Owner:Anuj    Reviewer:     vdp    763572
    &{Details} =  Create Dictionary    DownloadProtocol=TFTP    Primary_Server=10.112.123.107
    &{parameters} =  Create Dictionary      upload_system_info_server=1    paramone=sip xml notify event: 1   paramtwo=user config URL: ${vdpdetails}    paramthree= lldp: 0    paramfour= web language: "2"
    Given I want to configure ConfigurationServer parameters using ${Details} for ${phone1}
    Given I want to copy startup.cfg on ${phone1} using tftp with ${parameters}
    Then reboot ${phone1}
    Then using ${phonewui} log into ${phone1} url
    Then Using ${Phone_wui} Navigate to go to ${TroubleShootingMenu} page on ${phone1} URL
    Then Using ${Phone_wui} click on the ${TroubleShootingMenu['local_cfg']} on ${phone1} URL
    ### need to write verification method

762404: TC001: Verify changes made to basic network settings by VDP user are not uploaded to user-local.cfg. They should be loaded in local.cfg
    [Tags]    Owner:Anuj    Reviewer:     762404
    &{Details} =  Create Dictionary    DownloadProtocol=TFTP    Primary_Server=10.112.123.107
    &{parameters} =  Create Dictionary      upload_system_info_server=1    paramone=sip xml notify event: 1   paramtwo=user config URL: ${vdpdetails}
    Given I want to configure ConfigurationServer parameters using ${Details} for ${phone1}
    Given I want to copy startup.cfg on ${phone1} using tftp with ${parameters}
    Then reboot ${phone1}
    Then I want to program bottomkey softkey with hotdesklogin on position 1 for ${phone1}
    Then on ${phone1} press ${softkey} ${bottomKey1} for 1 times
    Then on ${phone1} enter number 4165142501
    Then on ${phone1} press ${softkey} ${bottomKey1} for 1 times
    Then using ${phonewui} log into ${phone1} url
    Then Using ${Phone_wui} Navigate to go to ${NetworkMenu} page on ${phone1} URL
    Then Using ${Phone_wui} click on the ${NetworkMenuLink['Dhcp']} on ${phone1} URL
    Then Using ${Phone_wui} send 255.255.255.255 value for ${NetworkMenuLink['subnetMask']} to ${phone1} URL
    Then Using ${Phone_wui} send 10.112.123.10 value for ${NetworkMenuLink['Gateway']} to ${phone1} URL
    Then Using ${Phone_wui} send 10.112.68.68 value for ${NetworkMenuLink['PrimaryDns']} to ${phone1} URL
    Then Using ${Phone_wui} click on the ${NetworkMenuLink['SaveSettings']} on ${phone1} URL
    Then on ${phone1} press ${softkey} ${bottomKey1} for 1 times
    Then on ${phone1} press ${softkey} ${bottomKey1} for 1 times
    # check on server there parameter are not available in user_local.cfg file
    Then using ${phonewui} log into ${phone1} url
    Then Using ${Phone_wui} Navigate to go to ${TroubleShootingMenu} page on ${phone1} URL
    Then Using ${Phone_wui} click on the ${TroubleShootingMenu['local_cfg']} on ${phone1} URL
    ### need to write verification method

762405: TC002: Verify changes made to 802.1X settings by VDP user are not uploaded to user-local.cfg. They should be loaded in local.cfgTC002: Verify changes made to 802.1X settings by VDP user are not uploaded to user-local.cfg. They should be loaded in local.cfg
    [Tags]    Owner:Anuj    Reviewer:     762405
    &{Details} =  Create Dictionary    DownloadProtocol=TFTP    Primary_Server=10.112.123.107
    &{parameters} =  Create Dictionary      upload_system_info_server=1    paramone=sip xml notify event: 1   paramtwo=user config URL: ${vdpdetails}
    Given I want to configure ConfigurationServer parameters using ${Details} for ${phone1}
    Given I want to copy startup.cfg on ${phone1} using tftp with ${parameters}
    Then reboot ${phone1}
    Then I want to program bottomkey softkey with hotdesklogin on position 1 for ${phone1}
    Then on ${phone1} press ${softkey} ${bottomKey1} for 1 times
    Then on ${phone1} enter number 4165142501
    Then on ${phone1} press ${softkey} ${bottomKey1} for 1 times
    Then using ${phonewui} log into ${phone1} url
    Then Using ${Phone_wui} Navigate to go to ${TLSSupportMenu} page on ${phone1} URL
    Then Using ${Phone_wui} send http://10.112.123.89/server.crt value for ${TLSSupport['RootAndIntermidiateCrtFileName']} to ${phone1} URL
    Then Using ${Phone_wui} send http://10.112.123.89/server.crt value for ${TLSSupport['LocalCrtFileName']} to ${phone1} URL
    Then Using ${Phone_wui} send http://10.112.123.89/server.crt value for ${TLSSupport['PrivateKeyFileName']} to ${phone1} URL
    Then Using ${Phone_wui} send http://10.112.123.89/server.crt value for ${TLSSupport['TrustedCrtFileName']} to ${phone1} URL
    Then Using ${Phone_wui} click on the ${TLSSupport['SaveSettings']} on ${phone1} URL
    Then on ${phone1} press ${softkey} ${bottomKey1} for 1 times
    Then on ${phone1} press ${softkey} ${bottomKey1} for 1 times
    # check on server there parameter are not available in user_local.cfg file
    Then using ${phonewui} log into ${phone1} url
    Then Using ${Phone_wui} Navigate to go to ${TroubleShootingMenu} page on ${phone1} URL
    Then Using ${Phone_wui} click on the ${TroubleShootingMenu['local_cfg']} on ${phone1} URL
    ### need to write verification method

762406: TC005: Verify when VDP user makes changes to permitted parameters andparameters in blacklist filter table, necessary action takes place
    [Tags]    Owner:Anuj    Reviewer:     762406
    &{Details} =  Create Dictionary    DownloadProtocol=TFTP    Primary_Server=10.112.123.107
    &{parameters} =  Create Dictionary      upload_system_info_server=1    paramone=sip xml notify event: 1   paramtwo=user config URL: ${vdpdetails}
    Given I want to configure ConfigurationServer parameters using ${Details} for ${phone1}
    Given I want to copy startup.cfg on ${phone1} using tftp with ${parameters}
    Then reboot ${phone1}
    Then I want to program bottomkey softkey with hotdesklogin on position 1 for ${phone1}
    Then on ${phone1} press ${softkey} ${bottomKey1} for 1 times
    Then on ${phone1} enter number 4165142501
    Then on ${phone1} press ${softkey} ${bottomKey1} for 1 times
    Then I want to program ${speeddial} key on position 3 on ${phone1}
    Then I want to program ${blf} key on position 4 on ${phone1}
    Then using ${phonewui} log into ${phone1} url
    Then Using ${Phone_wui} Navigate to go to ${NetworkMenu} page on ${phone1} URL
    Then Using ${Phone_wui} click on the ${NetworkMenuLink['Dhcp']} on ${phone1} URL
    Then Using ${Phone_wui} click on the ${NetworkMenuLink['Dhcp']} on ${phone1} URL
    Then Using ${Phone_wui} click on the ${NetworkMenuLink['SaveSettings']} on ${phone1} URL
    Then on ${phone1} press ${softkey} ${bottomKey1} for 1 times
    Then on ${phone1} press ${softkey} ${bottomKey1} for 1 times
    # check on server dhcp parameter are not available in user_local.cfg file
    # check on server speeddial and blf parameter are not available in user_local.cfg file
    Then using ${phonewui} log into ${phone1} url
    Then Using ${Phone_wui} Navigate to go to ${TroubleShootingMenu} page on ${phone1} URL
    Then Using ${Phone_wui} click on the ${TroubleShootingMenu['local_cfg']} on ${phone1} URL
    ### need to write verification method

762407: TC007: verify parameter (blacklist and non blacklist) changes made via TUI work as expected
    [Tags]    Owner:Anuj    Reviewer:     762407
    &{Details} =  Create Dictionary    DownloadProtocol=TFTP    Primary_Server=10.112.123.107
    &{parameters} =  Create Dictionary      upload_system_info_server=1    paramone=sip xml notify event: 1   paramtwo=user config URL: ${vdpdetails}
    Given I want to configure ConfigurationServer parameters using ${Details} for ${phone1}
    Given I want to copy startup.cfg on ${phone1} using tftp with ${parameters}
    Then reboot ${phone1}
    Then I want to program bottomkey softkey with hotdesklogin on position 1 for ${phone1}
    Then on ${phone1} press ${softkey} ${bottomKey1} for 1 times
    Then on ${phone1} enter number 4165142501
    Then on ${phone1} press ${softkey} ${bottomKey1} for 1 times
    Then I want to program ${speeddial} key on position 3 on ${phone1}
    Then I want to program ${blf} key on position 4 on ${phone1}
    Then i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then using ${phonewui} log into ${phone1} url
    Then Using ${Phone_wui} Navigate to go to ${NetworkMenu} page on ${phone1} URL
    Then Using ${Phone_wui} click on the ${NetworkMenuLink['Dhcp']} on ${phone1} URL
    Then Using ${Phone_wui} click on the ${NetworkMenuLink['Dhcp']} on ${phone1} URL
    Then Using ${Phone_wui} click on the ${NetworkMenuLink['SaveSettings']} on ${phone1} URL
    Then on ${phone1} press ${softkey} ${bottomKey1} for 1 times
    Then on ${phone1} press ${softkey} ${bottomKey1} for 1 times
    # check on server dhcp parameter are not available in user_local.cfg file
    # check on server speeddial and blf parameter are not available in user_local.cfg file
    Then using ${phonewui} log into ${phone1} url
    Then Using ${Phone_wui} Navigate to go to ${TroubleShootingMenu} page on ${phone1} URL
    Then Using ${Phone_wui} click on the ${TroubleShootingMenu['local_cfg']} on ${phone1} URL
    ### need to write verification method

763585: Verify phone WebUI support selecting custom ring tone
    [Tags]    Owner:Anuj    Reviewer:     763585
    Then using ${phonewui} log into ${phone1} url
    Then Using ${Phone_wui} Navigate to go to ${PreferencesMenu} page on ${phone1} URL
    Then Using ${Phone_wui} click on the ${RingTones['GlobalRingTones']} on ${phone1} URL
    Then Verify text Velocity for ${RingTones['GlobalRingTones']} on the ${phone1} URL
    Then Using ${Phone_wui} click on the ${RingTones['Line1']} on ${phone1} URL
    Then Verify text Global for ${RingTones['Line1']} on the ${phone1} URL
    Then Go to the ${RingTones['Line1']} option and select the Velocity value
    Then Verify text Velocity for ${RingTones['Line1']} on the ${phone1} URL

762663: TC-09b: Configuration from user_local.cfg will override user.cfg
    [Tags]    Owner:Anuj    Reviewer:     763585
    &{Details} =  Create Dictionary    DownloadProtocol=FTP    FTP_Server=10.112.123.107    FTP_Username=desktop    FTP_Password=desktop    FTP_Path=vdp
    &{parameters} =  Create Dictionary       softkey1 type= speeddial     csoftkey1 value= 2513
    Given I want to configure ConfigurationServer parameters using ${Details} for ${phone1}
    Then Create ${mac_cfg} file using ${parameters}
    Then Send ${mac_cfg} file in vdp folder on FTP server
    Then on ${phone1} press ${softkey} ${bottomKey1} for 1 times
    Then on ${phone1} enter number 4165142501
    Then on ${phone1} press ${softkey} ${bottomKey1} for 1 times
    &{parameters} =  Create Dictionary       softkey3 type= speeddial     softkey3 value= 2514    sip xml notify event: 1    sip registrar ip: 10.112.123.89    sip backup registrar ip: 10.112.123.89    sip proxy ip: 10.112.123.89    sip backup proxy ip: 10.112.123.89    sip proxy port: 5060    sip registrar port: 5060    sip backup proxy port: 5060    sip backup registrar port: 5060    sip user name: 4165142501    sip password: 4165142501    sip auth name: 4165142501    sip screen name: Visitor    sip display name: Visitor-Surender    user config URL: ftp://10.112.123.107vdp/
    Then Create 4165142520.cfg file using ${parameters}
    Then Send 4165142520.cfg file in vdp folder on FTP server
    Then reboot ${phone1}
    Then using ${phonewui} log into ${phone1} url
    Then Using ${Phone_wui} Navigate to go to ${SoftkeysAndXMLMenu} page on ${phone1} URL
    Then Using ${Phone_wui} click on the ${TopKeys} on ${phone1} URL
    Then Verify text speeddial for ${Topsoftkey3type} on the ${phone1} URL
    Then Verify text 2514 for ${Topsoftkey3value} on the ${phone1} URL

762665: test-2 ENH43040 Verify with VDP logged in that user.cfg/user_local.cfg files ARE listed under Troubleshooting tab
    [Tags]    Owner:Anuj    Reviewer:     762665
    &{Details} =  Create Dictionary    DownloadProtocol=FTP    FTP_Server=10.112.123.107    FTP_Username=desktop    FTP_Password=desktop    FTP_Path=vdp
    &{parameters} =  Create Dictionary       URL= ftp://10.112.123.107/vdp
    Given I want to configure ConfigurationServer parameters using ${Details} for ${phone1}
    Then Create ${startUp} file using ${parameters}
    Then Send ${startUp} file in vdp folder on FTP server
    Then on ${phone1} press ${softkey} ${bottomKey1} for 1 times
    Then on ${phone1} enter number 4165142501
    Then on ${phone1} press ${softkey} ${bottomKey1} for 1 times
    Then i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify the caller id on ${phone1} and ${phone2} display
    Then disconnect the call from ${phone2}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then verify the caller id on ${phone1} and ${phone2} display
    Then disconnect the call from ${phone2}
    Then using ${phonewui} log into ${phone1} url
    Then Using ${Phone_wui} Navigate to go to ${TroubleShootingMenu} page on ${phone1} URL
    Then Using ${Phone_wui} click on the ${TroubleShootingMenu['local_cfg']} on ${phone1} URL
    ### need to write verification method
762666: test-5 ENH43040 Verify VDP user.cfg/user_local.cfg files after restart with hot desk high security:
    [Tags]    Owner:Anuj    Reviewer:     762666
    &{Details} =  Create Dictionary    DownloadProtocol=FTP    FTP_Server=10.112.123.107    FTP_Username=desktop    FTP_Password=desktop    FTP_Path=vdp
    &{parameters} =  Create Dictionary       sip xml notify event= 1   user config URL= ${vdpdetailsftp}    user config URL= ftp://10.112.123.107/vdp    hot desk high security= 0
    Given I want to configure ConfigurationServer parameters using ${Details} for ${phone1}
    Then Create ${startUp} file using ${parameters}
    Then Send ${startUp} file in vdp folder on FTP server
    Then using ${phonewui} log into ${phone1} url
    Then Using ${Phone_wui} Navigate to go to ${LoginLogoutMenu} page on ${phone1} URL
    Then Using ${Phone_wui} send ${vdpuser} value for ${LoginLogout['Userid']} to ${phone1} URL
    Then Using ${Phone_wui} send ${vdppassword} value for ${LoginLogout['Password']} to ${phone1} URL
    Then Using ${Phone_wui} click on the ${LoginLogout['Submit']} on ${phone1} URL
    Then i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify the caller id on ${phone1} and ${phone2} display
    Then disconnect the call from ${phone2}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then verify the caller id on ${phone1} and ${phone2} display
    Then disconnect the call from ${phone2}
    Then reboot ${phone1}
    Then using ${phonewui} log into ${phone1} url
    Then Using ${Phone_wui} Navigate to go to ${TroubleShootingMenu} page on ${phone1} URL
    Then Using ${Phone_wui} click on the ${TroubleShootingMenu['local_cfg']} on ${phone1} URL
    ### need to write verification method
    Then i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify the caller id on ${phone1} and ${phone2} display
    Then disconnect the call from ${phone2}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then verify the caller id on ${phone1} and ${phone2} display
    Then disconnect the call from ${phone2}

762667: test-3 ENH43062 Verify VDP can login remotely via webui
    [Tags]    Owner:Anuj    Reviewer:     762667
    &{Details} =  Create Dictionary    DownloadProtocol=HTTP    Http_Serv=10.112.123.89    Http_Path=vdp
    &{parameters} =  Create Dictionary       user config URL= ${vdpdetails}    https user certificates= tftp://10.112.123.107/cacert.pem
    Given I want to configure ConfigurationServer parameters using ${Details} for ${phone1}
    Then Create ${startUp} file using ${parameters}
    Then Send ${startUp} file in vdp folder on TFTP server
    Then using ${phonewui} log into ${phone1} url
    Then Using ${Phone_wui} Navigate to go to ${LoginLogoutMenu} page on ${phone1} URL
    Then Using ${Phone_wui} send ${vdpuser} value for ${LoginLogout['Userid']} to ${phone1} URL
    Then Using ${Phone_wui} send ${vdppassword} value for ${LoginLogout['Password']} to ${phone1} URL
    Then Using ${Phone_wui} click on the ${LoginLogout['Submit']} on ${phone1} URL
    Then i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify the caller id on ${phone1} and ${phone2} display
    Then disconnect the call from ${phone2}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then verify the caller id on ${phone1} and ${phone2} display
    Then disconnect the call from ${phone2}

762670: test-25 ENH43062 Verify VDP login maintained after restart with high security disabled
    [Tags]    Owner:Anuj    Reviewer:     762670
    &{Details} =  Create Dictionary    DownloadProtocol=HTTP    Http_Serv=10.112.123.89    Http_Path=vdp
    &{parameters} =  Create Dictionary       user config URL= ${vdpdetails}    https user certificates= tftp://10.112.123.107/cacert.pem    hot desk high security= 0
    Given I want to configure ConfigurationServer parameters using ${Details} for ${phone1}
    Then Create ${startUp} file using ${parameters}
    Then Send ${startUp} file in vdp folder on TFTP server
    Then using ${phonewui} log into ${phone1} url
    Then Using ${Phone_wui} Navigate to go to ${LoginLogoutMenu} page on ${phone1} URL
    Then Using ${Phone_wui} send ${vdpuser} value for ${LoginLogout['Userid']} to ${phone1} URL
    Then Using ${Phone_wui} send ${vdppassword} value for ${LoginLogout['Password']} to ${phone1} URL
    Then Using ${Phone_wui} click on the ${LoginLogout['Submit']} on ${phone1} URL
    Then i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify the caller id on ${phone1} and ${phone2} display
    Then disconnect the call from ${phone2}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then verify the caller id on ${phone1} and ${phone2} display
    Then disconnect the call from ${phone2}
    Then reboot ${phone1}
    Then i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify the caller id on ${phone1} and ${phone2} display
    Then disconnect the call from ${phone2}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then verify the caller id on ${phone1} and ${phone2} display
    Then disconnect the call from ${phone2}

762668: test-4 ENH43062 Verify VDP can logout remotely via webui
    [Tags]    Owner:Anuj    Reviewer:     762668
    &{Details} =  Create Dictionary    DownloadProtocol=HTTP    Http_Serv=10.112.123.89    Http_Path=vdp
    &{parameters} =  Create Dictionary       user config URL= ${vdpdetails}    https user certificates= tftp://10.112.123.107/cacert.pem
    Given I want to configure ConfigurationServer parameters using ${Details} for ${phone1}
    Then Create ${startUp} file using ${parameters}
    Then Send ${startUp} file in vdp folder on TFTP server
    Then using ${phonewui} log into ${phone1} url
    Then Using ${Phone_wui} Navigate to go to ${LoginLogoutMenu} page on ${phone1} URL
    Then Using ${Phone_wui} send ${vdpuser} value for ${LoginLogout['Userid']} to ${phone1} URL
    Then Using ${Phone_wui} send ${vdppassword} value for ${LoginLogout['Password']} to ${phone1} URL
    Then Using ${Phone_wui} click on the ${LoginLogout['Submit']} on ${phone1} URL
    Then i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify the caller id on ${phone1} and ${phone2} display
    Then disconnect the call from ${phone2}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then verify the caller id on ${phone1} and ${phone2} display
    Then disconnect the call from ${phone2}
    Then using ${phonewui} log into ${phone1} url
    Then Using ${Phone_wui} Navigate to go to ${LoginLogoutMenu} page on ${phone1} URL
    Then Using ${Phone_wui} click on the ${LoginLogout['Submit']} on ${phone1} URL
    Then i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify the caller id on ${phone1} and ${phone2} display
    Then disconnect the call from ${phone2}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then verify the caller id on ${phone1} and ${phone2} display
    Then disconnect the call from ${phone2}

762669: test-7 ENH43062 Verify VDP can logout remotely via webui with high security disabled
    [Tags]    Owner:Anuj    Reviewer:     762669
    &{Details} =  Create Dictionary    DownloadProtocol=HTTP    Http_Serv=10.112.123.89    Http_Path=vdp
    &{parameters} =  Create Dictionary       user config URL= ${vdpdetails}    https user certificates= tftp://10.112.123.107/cacert.pem    hot desk high security= 0
    Given I want to configure ConfigurationServer parameters using ${Details} for ${phone1}
    Then Create ${startUp} file using ${parameters}
    Then Send ${startUp} file in vdp folder on TFTP server
    Then using ${phonewui} log into ${phone1} url
    Then Using ${Phone_wui} Navigate to go to ${LoginLogoutMenu} page on ${phone1} URL
    Then Using ${Phone_wui} send ${vdpuser} value for ${LoginLogout['Userid']} to ${phone1} URL
    Then Using ${Phone_wui} send ${vdppassword} value for ${LoginLogout['Password']} to ${phone1} URL
    Then Using ${Phone_wui} click on the ${LoginLogout['Submit']} on ${phone1} URL
    Then i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify the caller id on ${phone1} and ${phone2} display
    Then disconnect the call from ${phone2}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then verify the caller id on ${phone1} and ${phone2} display
    Then disconnect the call from ${phone2}
    Then Using ${Phone_wui} Navigate to go to ${LoginLogoutMenu} page on ${phone1} URL
    Then Using ${Phone_wui} send ${vdpuser} value for ${LoginLogout['Userid']} to ${phone1} URL
    Then Using ${Phone_wui} click on the ${LoginLogout['Submit']} on ${phone1} URL
    Then i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify the caller id on ${phone1} and ${phone2} display
    Then disconnect the call from ${phone2}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then verify the caller id on ${phone1} and ${phone2} display
    Then disconnect the call from ${phone2}

763687: BLF in Hold State (Local Hold)
    [Tags]    Owner:Anuj    Reviewer:    blf    notApplicableFor6910    763687
    Given On ${phone1} program ${blf} key on position 3 with ${phone2} value
    Then On ${phone1} program ${blf} key on position 4 with ${phone3} value
    Then On ${phone1} verify display message blf
    Then i want to make a two party call between ${phone2} and ${phone3} using ${loudspeaker}
    Then answer the call on ${phone3} using ${loudspeaker}
    Then verify audio path between ${phone2} and ${phone3}
    Then press hardkey as ${holdState} on ${phone2}
    # blf key is yellow at 3rd position on dut
    # blf key is solid red at 4th position on dut
    Then press hardkey as ${holdState} on ${phone2}
    # blf key is solid red at 3rd position on dut
    And disconnect the call from ${phone2}

763688: Check BLF Status in Idle mode
    [Tags]    Owner:Anuj    Reviewer:    blf    notApplicableFor6910    763688
    Given On ${phone1} program ${blf} key on position 3 with ${phone2} value
    Then On ${phone1} verify display message blf
    # blf key is green square at 3rd position on dut
    And disconnect the call from ${phone1}

763690: BLF/XFER in Hold state(Remote Hold)
    [Tags]    Owner:Anuj    Reviewer:    blf    notApplicableFor6910    763687
    Given On ${phone1} program ${blf} key on position 3 with ${phone2} value
    Then On ${phone1} program ${blf} key on position 4 with ${phone3} value
    Then On ${phone1} verify display message blf
    Then i want to make a two party call between ${phone2} and ${phone3} using ${loudspeaker}
    Then answer the call on ${phone3} using ${loudspeaker}
    Then verify audio path between ${phone2} and ${phone3}
    Then press hardkey as ${holdState} on ${phone2}
    # blf key is yellow at 3rd position on dut
    # blf key is solid red at 4th position on dut
    Then verify the led state of ${line3} as ${blink} on ${phone1}
    Then press hardkey as ${holdState} on ${phone3}
    # blf key is solid red at 3rd position on dut
    And disconnect the call from ${phone2}

763691: BLF/XFER in Hold State (Local Hold)
    [Tags]    Owner:Anuj    Reviewer:    blf    notApplicableFor6910    763691
    Given On ${phone1} program ${blf} key on position 3 with ${phone2} value
    Then On ${phone1} program ${blf} key on position 4 with ${phone3} value
    Then On ${phone1} verify display message blf
    Then i want to make a two party call between ${phone2} and ${phone3} using ${loudspeaker}
    Then answer the call on ${phone3} using ${loudspeaker}
    Then verify audio path between ${phone2} and ${phone3}
    Then press hardkey as ${holdState} on ${phone2}
    # blf key is yellow at 3rd position on dut
    # blf key is solid red at 4th position on dut
    Then verify the led state of ${line3} as ${blink} on ${phone1}
    Then press hardkey as ${holdState} on ${phone2}
    # blf key is solid red at 3rd position on dut
    And disconnect the call from ${phone2}

762512: TC_18
    [Tags]    Owner:Anuj    Reviewer:    brightness    notApplicableFor6910    776149
#    Given verify scrren backlight is black on ${phone1}
    Then press hardkey as ${holdState} on ${phone1}
#    Given verify scrren backlight is active on ${phone1}

762513: TC_30
    [Tags]    Owner:Anuj    Reviewer:    brightness    notApplicableFor6910    776149
#    Given verify scrren backlight is black on ${phone1}
    Then press hardkey as ${holdState} on ${phone1}
    Then Disconnect the call from ${phone1}
    Then on ${phone1} verify display message Date
    i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    disconnect the call from ${phone2}
    Then on ${phone1} verify display message ${missed}

762032: Audio_11: DEF29537
   [Tags]    Owner:Anuj    Reviewer:    audio
    i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
     answer the call on ${phone1} using ${line1}
    i want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
    Then I want to press line key ${line1} on phone ${phone1}
    press hardkey as ${goodbye} on ${phone1}
    verify the led state of ${line2} as ${blink} on ${phone1}
    Then Verify the led state of ${message_waiting} as ${blink} on ${phone1}
    press hardkey as ${goodbye} on ${phone2}
    on ${phone1} verify display message ${phone1}
    Then I want to press line key ${line1} on phone ${phone1}
    verify the led state of ${line2} as ${blink} on ${phone1}
    verify the led state of ${speaker} as ${blink} on ${phone1}
    press hardkey as ${goodbye} on ${phone1}

762033: Audio_18: DEF26795
    [Tags]    Owner:Anuj    Reviewer:    audio
    i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    answer the call on ${phone1} using ${offhook}
    verify the led state of ${line1} as ${on} on ${phone1}
    Then verify audio path between ${phone1} and ${phone2}
    press hardkey as ${holdstate} on ${phone1}
    verify the led state of ${line1} as ${blink} on ${phone1}
    press hardkey as ${goodbye} on ${phone1}
    verify the led state of ${line1} as ${blink} on ${phone1}
    press hardkey as ${holdstate} on ${phone1}
    Then verify audio path between ${phone1} and ${phone2}
    press hardkey as ${goodbye} on ${phone1}


762034: Audio_19: DEF26790
    [Tags]    Owner:Anuj    Reviewer:    audio
    i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    answer the call on ${phone1} using ${line1}
    verify the led state of ${line1} as ${on} on ${phone1}
    verify the led state of ${speaker} as ${blink} on ${phone1}
    press hardkey as ${holdstate} on ${phone1}
    verify the led state of ${line1} as ${blink} on ${phone1}
    verify the led state of ${speaker} as ${blink} on ${phone1}
    press hardkey as ${goodbye} on ${phone1}
    verify the led state of ${line1} as ${blink} on ${phone1}
    verify the led state of ${speaker} as ${blink} on ${phone1}
    Press hardkey as ${handsFree} on ${phone1}
    press hardkey as ${goodbye} on ${phone1}
    verify the led state of ${line1} as ${blink} on ${phone1}
    verify the led state of ${speaker} as ${on} on ${phone1}
    press hardkey as ${holdstate} on ${phone1}
    verify the led state of ${line1} as ${on} on ${phone1}
    verify audio path between ${phone1} and ${phone2}
    press hardkey as ${goodbye} on ${phone1}

762030: Audio 08: DEF29874
    [Tags]    Owner:Anuj    Reviewer:    audio
    i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    answer the call on ${phone1} using ${offhook}
    verify the led state of ${line1} as ${on} on ${phone1}
    Then verify audio path between ${phone1} and ${phone2}
    press hardkey as ${holdstate} on ${phone1}
    verify the led state of ${line1} as ${blink} on ${phone1}
    i want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
    verify the led state of ${line2} as ${blink} on ${phone1}
    verify the led state of ${speaker} as ${blink} on ${phone1}
    Then I want to press line key ${line1} on phone ${phone1}
    Then verify audio path between ${phone1} and ${phone2}
    press hardkey as ${goodbye} on ${phone1}

762516: TC_39-A
    [Tags]    Owner:Anuj    Reviewer:    image
    &{Details} =  Create Dictionary    DownloadProtocol=FTP    FTP_Server=10.112.123.107    FTP_Username=desktop    FTP_Password=desktop    FTP_Path=ftp://desktop:desktop@10.112.123.107/BGImages/image.jpg
    Given I want to configure ConfigurationServer parameters using ${Details} for ${phone1}
    Change the screensaver mode to ${mode4} and timer to 4 seconds on ${phone1}
    &{parameters} =  Create Dictionary       screenSaverIsSet= True    isTimeShown=True    missedCallIndicator=True
    Check the screensaver display on ${phone1} using ${screenSaverDetails}


762517: Screen saver refresh timer
    [Tags]    Owner:Anuj    Reviewer:    image
    &{Details} =  Create Dictionary    DownloadProtocol=FTP    FTP_Server=10.112.123.107    FTP_Username=desktop    FTP_Password=desktop    FTP_Path=ftp://desktop:desktop@10.112.123.107/BGImages/image.jpg
    &{parameters} =  Create Dictionary      screen saver refresh timer=5
    Given I want to configure ConfigurationServer parameters using ${Details} for ${phone1}
    Given I want to copy startup.cfg on ${phone1} using tftp with ${parameters}
    &{parameters} =  Create Dictionary       screenSaverIsSet= True    isTimeShown=True    missedCallIndicator=True
    Check the screensaver display on ${phone1} using ${screenSaverDetails}

762418: Bw_05:
    [Tags]    Owner:Anuj    Reviewer:    park/pickup
    &{Details} =  Create Dictionary    DownloadProtocol=FTP    FTP_Server=10.112.123.107    FTP_Username=desktop    FTP_Password=desktop    FTP_Path=vdp
    &{parameters} =  Create Dictionary       softkey1 type= park    softkey1 states= connected    softkey1 value= broadworks;*68    softkey2 type= pickup    softkey2 states= "idle outgoing"    softkey2 value= broadworks;*88
    Given I want to configure ConfigurationServer parameters using ${Details} for ${phone1}
    Then Create ${mac_cfg} file using ${parameters}
    Then Send ${mac_cfg} file in vdp folder on FTP server
    Then i want to make a two party call between ${phone1} and ${phone3} using ${loudspeaker}
    Then I want to press line key ${line1} on phone ${phone1}
    Then on ${phone1} enter number ${phone2}
    Then I want to press line key ${line2} on phone ${phone1}
    Then disconnect the call from ${phone1}
    Then I want to press line key ${line2} on phone ${phone1}
    Then on ${phone1} enter number ${phone3}
    Then verify audio path between ${phone1} and ${phone3}
    And disconnect the call from ${phone1}

762031: Audio_10: DEF29803
    [Tags]    Owner:Anuj    Reviewer:    audio
    i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Verify the led state of message_waiting as ${blink} on ${phone1}
    answer the call on ${phone1} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    press hardkey as ${holdstate} on ${phone1}
    i want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
    answer the call on ${phone1} using ${line2}
    i want to make a two party call between ${phone4} and ${phone1} using ${loudspeaker}
    Verify the led state of ${line3} as ${blink} on ${phone1}
    Verify the led state of message_waiting as ${blink} on ${phone1}
    Then I want to press line key ${programKey1} on phone ${phone1}
    Verify the led state of ${line2} as ${blink} on ${phone1}
    Verify the led state of ${line3} as ${blink} on ${phone1}
    Verify the led state of message_waiting as ${blink} on ${phone1}
    verify audio path between ${phone1} and ${phone2}
    disconnect the call from ${phone2}

763476: Icom_024
    [Tags]    Owner:Anuj    Reviewer:    intercom
    Given i want to use fac ${intercom} on ${phone1} to ${phone2}
    Verify the led state of ${line1} as ${blink} on ${phone2}
    disconnect the call from ${phone1}
    on ${phone1} verify display message ${phone1}

763478: Icom_053
    [Tags]    Owner:Anuj    Reviewer:    intercom
    Given i want to use fac ${intercom} on ${phone1} to ${phone2}
    Verify the led state of ${line1} as ${blink} on ${phone2}
    On ${phone1} verify ${line1} icon state as intercomIdle
    And disconnect the call from ${phone2}


763509: SideCarddisplay_12
    [Tags]    Owner:Anuj    Reviewer:
    &{Details} =  Create Dictionary    DownloadProtocol=FTP    FTP_Server=10.112.123.107    FTP_Username=desktop    FTP_Password=desktop    FTP_Path=vdp
    &{parameters} =  Create Dictionary       keys nomame hidden= 0     keys nomame hidden= " "
    Given I want to configure ConfigurationServer parameters using ${Details} for ${phone1}
    Then Create ${mac_cfg} file using ${parameters}
    Then Send ${mac_cfg} file in vdp folder on FTP server
    Then Reboot ${phone1}
    Then I want to verify on ${phone1} negative display message ${blf}

763510: SideCarddisplay_16
    [Tags]    Owner:Anuj    Reviewer:
    &{Details} =  Create Dictionary    DownloadProtocol=FTP    FTP_Server=10.112.123.107    FTP_Username=desktop    FTP_Password=desktop    FTP_Path=vdp
    &{parameters} =  Create Dictionary       keys nomame hidden= 0     keys nomame hidden= "string"
    Given I want to configure ConfigurationServer parameters using ${Details} for ${phone1}
    Then Create ${mac_cfg} file using ${parameters}
    Then Send ${mac_cfg} file in vdp folder on FTP server
    Then Reboot ${phone1}
    Then on ${phone1} verify display message ${blf}

763511: SideCarddisplay_18
    [Tags]    Owner:Anuj    Reviewer:
    &{Details} =  Create Dictionary    DownloadProtocol=FTP    FTP_Server=10.112.123.107    FTP_Username=desktop    FTP_Password=desktop    FTP_Path=vdp
    &{parameters} =  Create Dictionary       keys nomame hidden= 0     keys nomame hidden= "string"
    Given I want to configure ConfigurationServer parameters using ${Details} for ${phone1}
    Then Create ${mac_cfg} file using ${parameters}
    Then Send ${mac_cfg} file in vdp folder on FTP server
    Then Reboot ${phone1}
    Then on ${phone1} verify display message ${blf}
    &{parameters} =  Create Dictionary       keys nomame hidden= 0     keys nomame hidden= "string"
    Given I want to configure ConfigurationServer parameters using ${Details} for ${phone1}
    Then Create ${mac_cfg} file using ${parameters}
    Then Send ${mac_cfg} file in vdp folder on FTP server
    Then Reboot ${phone1}
    Then on ${phone1} verify display message ?

763564: TC02: LLDP
    [Tags]    Owner:Anuj    Reviewer:
    &{Details} =  Create Dictionary    DownloadProtocol=TFTP    Primary_Server=10.112.123.107
    &{parameters} =  Create Dictionary      upload_system_info_server=1    paramone=user config URL: ${vdpdetails}
    Given I want to configure ConfigurationServer parameters using ${Details} for ${phone1}
    Given I want to copy startup.cfg on ${phone1} using tftp with ${parameters}
    Then reboot ${phone1}
    Then I want to program bottomkey softkey with hotdesklogin on position 1 for ${phone1}
    Then on ${phone1} press ${softkey} ${bottomKey1} for 1 times
    Then on ${phone1} enter number 4165142501
    Then on ${phone1} press ${softkey} ${bottomKey1} for 1 times
    &{configurationDetails}=    CREATE DICTIONARY    lldp= 0    lldp interval: 45
    Given Configure parameters on ${phone1} using ${configurationDetails}
    Then using ${phonewui} log into ${phone1} url
    Then Using ${Phone_wui} Navigate to go to ${TroubleShootingMenu} page on ${phone1} URL
    Then Using ${Phone_wui} click on the ${TroubleShootingMenu['local_cfg']} on ${phone1} URL
    ### need to write verification method
    Then disconnect the call from ${phone1}Then using ${phonewui} log into ${phone1} url
    Then Using ${Phone_wui} Navigate to go to ${TroubleShootingMenu} page on ${phone1} URL
    Then Using ${Phone_wui} click on the ${TroubleShootingMenu['local_cfg']} on ${phone1} URL
    ### need to write verification method
    Then disconnect the call from ${phone1}
    &{configurationDetails}=    CREATE DICTIONARY    lldp= 1    lldp interval: 45
    Given I want to copy startup.cfg on ${phone1} using tftp with ${parameters}
    Then reboot ${phone1}
    Then I want to program bottomkey softkey with hotdesklogin on position 1 for ${phone1}
    Then on ${phone1} press ${softkey} ${bottomKey1} for 1 times
    Then on ${phone1} enter number 4165142501
    Then on ${phone1} press ${softkey} ${bottomKey1} for 1 times
    Given Configure parameters on ${phone1} using ${configurationDetails}
    Then using ${phonewui} log into ${phone1} url
    Then Using ${Phone_wui} Navigate to go to ${TroubleShootingMenu} page on ${phone1} URL
    Then Using ${Phone_wui} click on the ${TroubleShootingMenu['local_cfg']} on ${phone1} URL
    ### need to write verification method
    Then disconnect the call from ${phone1}

763565: TC03: Config server settings
    [Tags]    Owner:Anuj    Reviewer:
    &{Details} =  Create Dictionary    DownloadProtocol=TFTP    Primary_Server=10.112.123.107
    &{parameters} =  Create Dictionary      upload_system_info_server=1    paramone=user config URL: ${vdpdetails}
    Given I want to configure ConfigurationServer parameters using ${Details} for ${phone1}
    Given I want to copy startup.cfg on ${phone1} using tftp with ${parameters}
    Then reboot ${phone1}
    Then I want to program bottomkey softkey with hotdesklogin on position 1 for ${phone1}
    Then on ${phone1} press ${softkey} ${bottomKey1} for 1 times
    Then on ${phone1} enter number 4165142501
    Then on ${phone1} press ${softkey} ${bottomKey1} for 1 times
    Then using ${phonewui} log into ${phone1} url
    Then Using ${Phone_wui} Navigate to go to ${TroubleShootingMenu} page on ${phone1} URL
    Then Using ${Phone_wui} click on the ${TroubleShootingMenu['local_cfg']} on ${phone1} URL
    ### need to write verification method
    Then disconnect the call from ${phone1}
    &{parameters} =  Create Dictionary       download protocol= FTP     ftp server= 10.112.123.107    ftp path= systeminfo    ftp username= desktop    ftp password= desktop

    Given I want to configure ConfigurationServer parameters using ${Details} for ${phone1}
    Given I want to copy startup.cfg on ${phone1} using tftp with ${parameters}
    Then reboot ${phone1}
    Then I want to program bottomkey softkey with hotdesklogin on position 1 for ${phone1}
    Then on ${phone1} press ${softkey} ${bottomKey1} for 1 times
    Then on ${phone1} enter number 4165142501
    Then on ${phone1} press ${softkey} ${bottomKey1} for 1 times
    Then using ${phonewui} log into ${phone1} url
    Then Using ${Phone_wui} Navigate to go to ${TroubleShootingMenu} page on ${phone1} URL
    Then Using ${Phone_wui} click on the ${TroubleShootingMenu['local_cfg']} on ${phone1} URL
    ### need to write verification method
    Then disconnect the call from ${phone1}

763567: TC05: Action URI settings
    [Tags]    Owner:Anuj    Reviewer:     vdp    763573
    &{configurationDetails}=    CREATE DICTIONARY    download protocol=TFTP    tftp server=10.112.123.107    log server ip=10.112.123.107    action uri poll=http://10.112.123.89/weather.xml    action uri poll=30
    Given Configure parameters on ${phone1} using ${configurationDetails}
    Then using ${phonewui} log into ${phone1} url
    Then Using ${Phone_wui} Navigate to go to ${TroubleShootingMenu} page on ${phone1} URL
    Then Using ${Phone_wui} click on the ${TroubleShootingMenu['local_cfg']} on ${phone1} URL
    ### need to write verification method
    &{configurationDetails}=    CREATE DICTIONARY    download protocol=TFTP    tftp server=10.112.123.107    log server ip=10.112.123.107    action uri poll=http://10.112.123.89/weather.xml    action uri poll=0
    Given Configure parameters on ${phone1} using ${configurationDetails}
    Then using ${phonewui} log into ${phone1} url
    Then Using ${Phone_wui} Navigate to go to ${TroubleShootingMenu} page on ${phone1} URL
    Then Using ${Phone_wui} click on the ${TroubleShootingMenu['local_cfg']} on ${phone1} URL
    ### need to write verification method

763571: TC09: Verify TC3 by making changes via TUI
    [Tags]    Owner:Anuj    Reviewer:
    &{Details} =  Create Dictionary    DownloadProtocol=TFTP    Primary_Server=10.112.123.107
    &{parameters} =  Create Dictionary      upload_system_info_server=1    paramone=user config URL: ${vdpdetails}
    Given I want to configure ConfigurationServer parameters using ${Details} for ${phone1}
    Given I want to copy startup.cfg on ${phone1} using tftp with ${parameters}
    Then reboot ${phone1}
    Then I want to program bottomkey softkey with hotdesklogin on position 1 for ${phone1}
    Then on ${phone1} press ${softkey} ${bottomKey1} for 1 times
    Then on ${phone1} enter number 4165142501
    Then on ${phone1} press ${softkey} ${bottomKey1} for 1 times
    Then using ${phonewui} log into ${phone1} url
    Then Using ${Phone_wui} Navigate to go to ${TroubleShootingMenu} page on ${phone1} URL
    Then Using ${Phone_wui} click on the ${TroubleShootingMenu['local_cfg']} on ${phone1} URL
    ### need to write verification method
    Then disconnect the call from ${phone1}
    &{parameters} =  Create Dictionary       download protocol= FTP     ftp server= 10.112.123.107    ftp path= systeminfo    ftp username= desktop    ftp password= desktop

    Given I want to configure ConfigurationServer parameters using ${Details} for ${phone1}
    Given I want to copy startup.cfg on ${phone1} using tftp with ${parameters}
    Then reboot ${phone1}
    Then I want to program bottomkey softkey with hotdesklogin on position 1 for ${phone1}
    Then on ${phone1} press ${softkey} ${bottomKey1} for 1 times
    Then on ${phone1} enter number 4165142501
    Then on ${phone1} press ${softkey} ${bottomKey1} for 1 times
    Then using ${phonewui} log into ${phone1} url
    Then Using ${Phone_wui} Navigate to go to ${TroubleShootingMenu} page on ${phone1} URL
    Then Using ${Phone_wui} click on the ${TroubleShootingMenu['local_cfg']} on ${phone1} URL
    ### need to write verification method
    Then disconnect the call from ${phone1}

763563: TC01: "Verify: When blacklist parameter value changed back to same value as server.cfg - parameters are deleted from local.cfg
    [Tags]    Owner:Anuj    Reviewer:    vdp    763563
    &{Details} =  Create Dictionary    DownloadProtocol=TFTP    Primary_Server=10.112.123.107
    &{parameters} =  Create Dictionary      upload_system_info_server=1    paramone=sip xml notify event: 1   paramtwo=user config URL: ${vdpdetails}
    Given I want to configure ConfigurationServer parameters using ${Details} for ${phone1}
    Given I want to copy startup.cfg on ${phone1} using tftp with ${parameters}
    Then reboot ${phone1}
    Then I want to program bottomkey softkey with hotdesklogin on position 1 for ${phone1}
    Then on ${phone1} press ${softkey} ${bottomKey1} for 1 times
    Then on ${phone1} enter number 4165142501
    Then on ${phone1} press ${softkey} ${bottomKey1} for 1 times
    &{configurationDetails}=    CREATE DICTIONARY    log module linemgr= 65533    log server ip= 10.112.123.107   log server port= 513
    Given Configure parameters on ${phone1} using ${configurationDetails}
    Then using ${phonewui} log into ${phone1} url
    Then Using ${Phone_wui} Navigate to go to ${TroubleShootingMenu} page on ${phone1} URL
    Then Using ${Phone_wui} click on the ${TroubleShootingMenu['local_cfg']} on ${phone1} URL
    ### need to write verification method
    Then disconnect the call from ${phone1}
    Then on ${phone1} press ${softkey} ${bottomKey1} for 1 times
    Then on ${phone1} press ${softkey} ${bottomKey1} for 1 times
    Then on ${phone} press ${softkey} ${bottomKey1} for 1 times
    Then on ${phone1} enter number 4165142501
    Then on ${phone} press ${softkey} ${bottomKey1} for 1 times
    Then using ${phonewui} log into ${phone1} url
    Then Using ${Phone_wui} Navigate to go to ${TroubleShootingMenu} page on ${phone1} URL
    Then Using ${Phone_wui} click on the ${TroubleShootingMenu['local_cfg']} on ${phone1} URL
    ### need to write verification method



    &{configurationDetails}=    CREATE DICTIONARY    log module linemgr= 65533    log server ip= 10.112.123.107   log server port= 513
    Given Configure parameters on ${phone1} using ${configurationDetails}
    Then using ${phonewui} log into ${phone1} url
    Then Using ${Phone_wui} Navigate to go to ${TroubleShootingMenu} page on ${phone1} URL
    Then Using ${Phone_wui} click on the ${TroubleShootingMenu['local_cfg']} on ${phone1} URL
    ### need to write verification method
    Then disconnect the call from ${phone1}
    Then on ${phone} press ${softkey} ${bottomKey1} for 1 times
    Then on ${phone} press ${softkey} ${bottomKey1} for 1 times

    Then on ${phone} press ${softkey} ${bottomKey1} for 1 times
    Then on ${phone1} enter number 4165142501
    Then on ${phone} press ${softkey} ${bottomKey1} for 1 times
    Then using ${phonewui} log into ${phone1} url
    Then Using ${Phone_wui} Navigate to go to ${TroubleShootingMenu} page on ${phone1} URL
    Then Using ${Phone_wui} click on the ${TroubleShootingMenu['local_cfg']} on ${phone1} URL
    ### need to write verification method
    Then reboot ${phone1}
    Then using ${phonewui} log into ${phone1} url
    Then Using ${Phone_wui} Navigate to go to ${TroubleShootingMenu} page on ${phone1} URL
    Then Using ${Phone_wui} click on the ${TroubleShootingMenu['local_cfg']} on ${phone1} URL
    ### need to write verification method

762198: ConfigCrashFile_Retriev_06-C-1
    [Tags]    Owner:Anuj    Reviewer:    crash    762198
    &{Details} =  Create Dictionary    DownloadProtocol=FTP    FTP_Server=10.112.123.107    FTP_Username=desktop    FTP_Password=desktop     FTP_Path=systeminfo
    &{parameters} =  Create Dictionary       upload system info manual option= 1     upload system info server=${serverDetails}

    Given I want to configure ConfigurationServer parameters using ${Details} for ${phone1}
    &{fileName}=    Create Dictionary    fileName=["server.cfg","local.cfg"]
    Then Create ${startUp} file using ${parameters}
    Then Create ${systeminfo} folder on HTTP server
    Then Send ${startUp} file in ${systeminfo} folder on HTTP server
    Then reboot ${phone1}
    Then on the WUI of ${phone1} click on the ${uploadButton}
    Then check ${fileSent} text in the webUI on ${phone}
    Then Using ${phone1} verify configuration ${fileName} files in sysinfo folder on FTP server

762199: ConfigCrashFile_Retriev_07-B-1
    [Tags]    Owner:Anuj    Reviewer:    crash    762199
    &{Details} =  Create Dictionary    DownloadProtocol=TFTP    Primary_Server=10.112.91.70
    &{parameters} =  Create Dictionary      upload_system_info_server=1    paramone=upload system info manual option: 1    paramtwo=config files mandatory download: "startup.cfg"     paramthree=config files number of reattempt: -1    paramfour=config files max delay: 60    paramfive=config files skip key enabled: 1
    &{fileName}=    Create Dictionary    fileName=["server.cfg","local.cfg"]
    Given I want to configure ConfigurationServer parameters using ${Details} for ${phone1}
    Given I want to copy startup.cfg on ${phone1} using tftp with ${parameters}
    Then reboot ${phone1}
    Then on the WUI of ${phone1} click on the ${uploadButton}
    Then check ${fileSent} text in the webUI on ${phone}
    Then Using ${phone1} verify configuration ${fileName} files in sysinfo folder on FTP server

762200:ConfigCrashFile_Retriev_07-C-1
    [Tags]    Owner:Anuj    Reviewer:    crash    762200
    &{Details} =  Create Dictionary    DownloadProtocol=TFTP    Primary_Server=10.112.91.70
    &{parameters} =  Create Dictionary      upload_system_info_server=1    paramone=upload system info manual option: 1    paramtwo=config files mandatory download: "startup.cfg"     paramthree=config files number of reattempt: -1    paramfour=config files max delay: 60    paramfive=config files skip key enabled: 1
    &{fileName}=    Create Dictionary    fileName=["server.cfg","local.cfg"]
    Given I want to configure ConfigurationServer parameters using ${Details} for ${phone1}
    Given I want to copy startup.cfg on ${phone1} using tftp with ${parameters}
    Then reboot ${phone1}
    Then on the WUI of ${phone1} click on the ${uploadButton}
    Then check ${fileSent} text in the webUI on ${phone}
    Then Using ${phone1} verify configuration ${fileName} files in sysinfo folder on FTP server

841127: Mandatory file mandatory download for tuz files - startup/model/mac
    [Tags]    Owner:Anuj    Reviewer:    configcrash
    &{Details} =  Create Dictionary    DownloadProtocol=FTP    FTP_Server=10.112.123.107    FTP_Username=desktop    FTP_Password=desktop    FTP_Path=systeminfo
    &{parameters} =  Create Dictionary       upload system info manual option= 1     config files mandatory download= ["startup.tuz","aastra.tuz","model.tuz",mac.tuz"]    config files number of reattempt= -1    config files max delay= 60    config files skip key enabled= 1    upload system info server=${serverDetails}
    Given I want to configure ConfigurationServer parameters using ${Details} for ${phone1}
    Then Create ${startUp} file using ${parameters}
    Then Create ${systeminfo} folder on FTP server
    Then Send ${startUp} file in ${systeminfo} folder on FTP server
    Then reboot ${phone1}
    Then on the WUI of ${phone1} click on the ${uploadButton}
    &{fileName}=    Create Dictionary    fileName=["model.cfg"]
    Then Using ${phone1} delete configuration ${fileName} files from ${folderName} folder on ${server} server



