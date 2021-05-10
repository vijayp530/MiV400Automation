*** Settings ***
Resource   ../RobotKeywords/Setup_And_Teardown.robot
Resource    ../RobotKeywords/WebUI_Keywords.robot
Library    ../lib/MyListner.py


Test Timeout  25 minutes
Suite Setup  Phones Initialization
Test Setup   Check Phone Connection
Test Teardown  Generic Test Teardown
Suite Teardown    Run Keywords   Check Phone Connection    Generic Test Teardown

*** Test Cases ***
762168: TC036
    [Tags]   Owner:Ram    Reviewer:     callersList
    Given delete ${all} call entries in call history on ${phone1}
    Then I want to make a two party call between ${phone2} and ${phone1} using ${offHook}
    Then disconnect the call from ${phone2}
    Then using ${PhoneWUI} Log Into ${phone1} URL
    Then using ${PhoneWUI} Navigate to go to ${DirectoryMenu} page on ${phone1} URL
    Then using ${PhoneWUI} click on the ${DirectoryLink['CallersList']} on ${phone1} URL
    Then verify the ${callerListFile} file is downloaded
    Then Read the downloaded ${callerListFile} file of ${phone1}
    And using ${PhoneWUI} logoff ${phone1} URL

762499: Export Local Directory from Desktop phone through Web UI
    [Tags]   Owner:Ram    Reviewer:     directoryList
    Given using ${PhoneWUI} Log Into ${phone1} URL
    Then using ${PhoneWUI} Navigate to go to ${DirectoryMenu} page on ${phone1} URL
    Then using ${PhoneWUI} click on the ${DirectoryLink['DirectoryList']} on ${phone1} URL
    Then verify the ${directoryFile} file is downloaded
    And using ${PhoneWUI} logoff ${phone1} URL

763495: auto ip - http WUI access
    [Tags]   Owner:Ram    Reviewer:     WebUI
    Given using ${PhoneWUI} Log Into ${phone1} URL
    Then Check ${LogoffMenu} is present on the WUI of ${phone1}
    And using ${PhoneWUI} logoff ${phone1} URL

763150: TC-01 Start tcpdump from WUI
    [Tags]   Owner:Ram    Reviewer:     TCPdump
    Given using ${PhoneWUI} Log Into ${phone1} URL
    Then using ${PhoneWUI} Navigate to go to ${CaptureMenu} page on ${phone1} URL
    Then using ${PhoneWUI} click on the ${CaptureLink['Port']} on ${phone1} URL
    Then Using ${PhoneWUI} send ${port} value for ${CaptureLink['Port']} to ${phone1} URL
    Then using ${PhoneWUI} click on the ${CaptureLink['Start']} on ${phone1} URL
    Then using ${PhoneWUI} Navigate to go to ${CaptureMenu} page on ${phone1} URL
    Then Verify text ${stop} for ${CaptureLink['Stop']} on the ${phone1} URL
    Then using ${PhoneWUI} click on the ${CaptureLink['Stop']} on ${phone1} URL
    And using ${PhoneWUI} logoff ${phone1} URL

763302: TC06 : Capturing in phone`s flash memory over reboot
    [Tags]   Owner:Ram    Reviewer:     Capture
    Given using ${PhoneWUI} Log Into ${phone1} URL
    Then using ${PhoneWUI} Navigate to go to ${CaptureMenu} page on ${phone1} URL
    Then using ${PhoneWUI} click on the ${CaptureLink['Start']} on ${phone1} URL
    Then I want to make a two party call between ${phone2} and ${phone1} using ${offHook}
    Then answer the call on ${phone1} using ${offHook}
    Then disconnect the call from ${phone1}
    Then reboot ${phone1}
    Then using ${PhoneWUI} Navigate to go to ${CaptureMenu} page on ${phone1} URL
    Then Verify text ${start} for ${CaptureLink['Start']} on the ${phone1} URL
    And using ${PhoneWUI} logoff ${phone1} URL

845554:TC053: Upload to directory
    [Tags]   Owner:Ram    Reviewer:     uploadFile
    {Details} =  Create Dictionary     firstName=HCL     lastName=Noida
    Given using ${PhoneWUI} Log Into ${phone1} URL
    Then press hardkey as ${directory} on ${phone1}
    Then Delete all entries from directry of ${phone1}
    Then delete ${all} call entries in call history on ${phone1}
    Then create ${directoryFile} file for ${phone2} using ${details}
    Then Using ${PhoneWUI} click on the ${DirectoryMenu} on ${phone1} URL
    Then using ${PhoneWUI} click on the ${DirectoryLink['DirectoryList']} on ${phone1} URL
    Then Read the downloaded ${directoryFile} file of ${phone1}
    Then using ${PhoneWUI} click on the ${DirectoryLink['CallersList']} on ${phone1} URL
    Then Read the downloaded ${callerListFile} file of ${phone1}
    Then Using ${PhoneWUI} click on the ${DirectoryMenu} on ${phone1} URL
    Then using ${PhoneWUI} select the ${DirectoryLink['ChooseFile']} and upload file ${directoryFile} on ${phone1} URL
    And using ${PhoneWUI} logoff ${phone1} URL

810763: TC048: Directory Upload
    [Tags]   Owner:Ram    Reviewer:     uploadDirectory
    {Details} =  Create Dictionary     firstName=HCL     lastName=Noida
    Given using ${PhoneWUI} Log Into ${phone1} URL
    Then press hardkey as ${directory} on ${phone1}
    Then Delete all entries from directry of ${phone1}
    Then delete ${all} call entries in call history on ${phone1}
    Then create ${directoryFile} file for ${phone2} using ${details}
    Then Using ${PhoneWUI} click on the ${DirectoryMenu} on ${phone1} URL
    Then using ${PhoneWUI} select the ${DirectoryLink['ChooseFile']} and upload file ${directoryFile} on ${phone1} URL
    Then using ${PhoneWUI} click on the ${DirectoryLink['DirectoryList']} on ${phone1} URL
    Then Read the downloaded ${directoryFile} file of ${phone1}
    Then using ${PhoneWUI} click on the ${DirectoryLink['CallersList']} on ${phone1} URL
    Then Read the downloaded ${callerListFile} file of ${phone1}
    And using ${PhoneWUI} logoff ${phone1} URL

762500: Import a directory through Web UI to another desktop phone
    [Tags]   Owner:Ram    Reviewer:     UploadFile
    {Details} =  Create Dictionary     firstName=HCL     lastName=Noida
    Given using ${PhoneWUI} Log Into ${phone1} URL
    Then Delete all entries from directry of ${phone1}
    Then create ${directoryFile} file for ${phone2} using ${details}
    Then Using ${PhoneWUI} click on the ${DirectoryMenu} on ${phone1} URL
    Then using ${PhoneWUI} select the ${DirectoryLink['ChooseFile']} and upload file ${directoryFile} on ${phone1} URL
    Then using ${PhoneWUI} logoff ${phone1} URL
    Then press hardkey as ${directory} on ${phone1}
    Then on ${phone1} verify display message ${phone2}
    And Delete all entries from directry of ${phone1}

762501: Minimun 1 record is required to import a file
    [Tags]    Owner:Ram        Reviewer:       importFile
    Given using ${PhoneWUI} Log Into ${phone1} URL
    Then Delete all entries from directry of ${phone1}
    &{Details} =  Create Dictionary
    Then create ${directoryFile} file for ${phone2} using ${details}
    Then Using ${PhoneWUI} click on the ${DirectoryMenu} on ${phone1} URL
    Then using ${PhoneWUI} select the ${DirectoryLink['ChooseFile']} and upload file ${directoryFile} on ${phone1} URL
    Then Using ${PhoneWUI} Verify text Upload failed - No record detected in csv file for ${uploadFile} on the ${phone1} URL
    &{Details} =  Create Dictionary     firstName=HCL     lastName=Noida
    Then create ${directoryFile} file for ${phone2} using ${details}
#    Then Using ${PhoneWUI} click on the ${DirectoryMenu} on ${phone1} URL
    Then using ${PhoneWUI} select the ${DirectoryLink['ChooseFile']} and upload file ${directoryFile} on ${phone1} URL
    Then Using ${PhoneWUI} Verify text Upload performed - 1 records created for ${uploadFile} on the ${phone1} URL
    Then using ${PhoneWUI} logoff ${phone1} URL
    Then press hardkey as ${directory} on ${phone1}
    Then on ${phone1} verify display message ${phone2}
    And Delete all entries from directry of ${phone1}

762502: Import a file with duplicate data.
    [Tags]    Owner:Ram        Reviewer:       duplicateData
    &{Details} =  Create Dictionary     firstName=HCL     lastName=Noida
    Given using ${PhoneWUI} Log Into ${phone1} URL
    Then Delete all entries from directry of ${phone1}
    Then create ${directoryFile} file for ${phone2} using ${details}
    Then Using ${PhoneWUI} click on the ${DirectoryMenu} on ${phone1} URL
    Then using ${PhoneWUI} select the ${DirectoryLink['ChooseFile']} and upload file ${directoryFile} on ${phone1} URL
    Then Using ${PhoneWUI} Verify text Upload performed - 1 records created for ${uploadFile} on the ${phone1} URL
    Then using ${PhoneWUI} select the ${DirectoryLink['ChooseFile']} and upload file ${directoryFile} on ${phone1} URL
    Then Using ${PhoneWUI} Verify text Upload performed - 1 records created for ${uploadFile} on the ${phone1} URL
    Then using ${PhoneWUI} logoff ${phone1} URL
    Then press hardkey as ${directory} on ${phone1}
    Then on ${phone1} verify display message ${phone2}
    And Delete all entries from directry of ${phone1}

762505: Modify the file by deleting all the name columns
    [Tags]    Owner:Ram        Reviewer:       withoutName
    Given using ${PhoneWUI} Log Into ${phone1} URL
    &{Details} =  Create Dictionary
    Then create ${directoryFile} file for ${phone2} using ${details}
    Then Using ${PhoneWUI} click on the ${DirectoryMenu} on ${phone1} URL
    Then using ${PhoneWUI} select the ${DirectoryLink['ChooseFile']} and upload file ${directoryFile} on ${phone1} URL
    Then Using ${PhoneWUI} Verify text Upload failed - No record detected in csv file for ${uploadFile} on the ${phone1} URL
    And using ${PhoneWUI} logoff ${phone1} URL

762503: Maximum 1000 records can be imported
    [Tags]    Owner:Ram        Reviewer:       1000records
    &{Details} =  Create Dictionary    firstName=HCL     lastName=Noida    numberOfRecords=1000
    Given using ${PhoneWUI} Log Into ${phone1} URL
    Then Delete all entries from directry of ${phone1}
    Then create ${directoryFile} file for ${phone2} using ${details}
    Then Using ${PhoneWUI} click on the ${DirectoryMenu} on ${phone1} URL
    Then using ${PhoneWUI} select the ${DirectoryLink['ChooseFile']} and upload file ${directoryFile} on ${phone1} URL
    Then Using ${PhoneWUI} Verify text Upload performed - 1000 records created for ${uploadFile} on the ${phone1} URL
    Then using ${PhoneWUI} logoff ${phone1} URL
    And Delete all entries from directry of ${phone1}

762504: Import 995 record file into desktop phone with 10 already saved records in directory.
    [Tags]    Owner:Ram        Reviewer:       995records    100
    &{Details} =  Create Dictionary    firstName=HCL     lastName=Noida    numberOfRecords=10
    &{Details1} =  Create Dictionary    firstName=HCL     lastName=Noida    numberOfRecords=995
    Given using ${PhoneWUI} Log Into ${phone1} URL
    Then Delete all entries from directry of ${phone1}
    Then create ${directoryFile} file for ${phone2} using ${details}
    Then Using ${PhoneWUI} click on the ${DirectoryMenu} on ${phone1} URL
    Then using ${PhoneWUI} select the ${DirectoryLink['ChooseFile']} and upload file ${directoryFile} on ${phone1} URL
    Then Using ${PhoneWUI} Verify text Upload performed - 10 records created for ${uploadFile} on the ${phone1} URL
    Then create ${directoryFile} file for ${phone2} using ${details1}
#    Then Using ${PhoneWUI} click on the ${DirectoryMenu} on ${phone1} URL
    Then using ${PhoneWUI} select the ${DirectoryLink['ChooseFile']} and upload file ${directoryFile} on ${phone1} URL
    Then Using ${PhoneWUI} Verify text Upload performed - 1 records created for ${uploadFile} on the ${phone1} URL
    Then using ${PhoneWUI} logoff ${phone1} URL
    And Delete all entries from directry of ${phone1}

762195: ConfigCrashFile_Retriev_01
    [Tags]    Owner:Ram        Reviewer:       UploadSyslog
    &{Details} =��Create Dictionary    DownloadProtocol=FTP
    &{parameters} =��Create Dictionary       upload system info manual option= 1     upload system info server=${serverDetails}
    Given I want to configure ConfigurationServer parameters using ${Details} for ${phone1}
    Then Create ${startUp} file using ${parameters}
    Then Create ${sysinfo} folder on FTP server
    Then Send ${startUp} file on FTP server
    Then reboot ${phone1}
    And Using ${PhoneWUI} click on the ${uploadButton} on ${phone1} URL
    And Check ${uploadButton} is present on the WUI of ${phone1}
    And on the WUI of ${phone1} check ${uploadButton} is present

762196: ConfigCrashFile_Retriev_03
    [Tags]    Owner:Ram        Reviewer:       UploadSyslog
    &{Details} =��Create Dictionary    DownloadProtocol=FTP
    &{parameters} =��Create Dictionary       upload system info manual option=0
    Given I want to configure ConfigurationServer parameters using ${Details} for ${phone1}
    Then Create ${startUp} file using ${parameters}
    Then Create ${sysinfo} folder on FTP server
    Then Send ${startUp} file on FTP server
    Then reboot ${phone1}
    And Check ${uploadButton} is not present on the WUI of ${phone1}
#    And on the WUI of ${phone1} check ${uploadButton} is not present

762200: ConfigCrashFile_Retriev_07-C-1
    [Tags]    Owner:Ram        Reviewer:       crashFile
    &{Details} =��Create Dictionary    DownloadProtocol=TFTP
    &{parameters} =��Create Dictionary       upload system info manual option= 1     upload system info server=${tftpserverDetails}
    Given I want to configure ConfigurationServer parameters using ${Details} for ${phone1}
    Then Create ${startUp} file using ${parameters}
    Then Create ${sysinfo} folder on FTP server
    Then Send ${startUp} file on FTP server
    Then reboot ${phone1}
    Then using ${PhoneWUI} Log Into ${phone1} URL
    Then Using ${PhoneWUI} click on the ${uploadButton} on ${phone1} URL
    Then Using ${PhoneWUI} logoff ${phone1} URL

762215: Encrypt 01
    [Tags]    Owner:Ram        Reviewer:       Encrypt
    Given Using password anacrypt aastra.cfg file with 1234567 as password
    Then Verify anacrypted aastra.cfg files are present in the folder
    Then Using password anacrypt 00085D1610ED.cfg file with 1234567 as password
    Then Rename 00085D1610ED.tuz filename to 00085D161237.tuz
    And Verify renamed 00085D161237.tuz files is present in the folder

762218: Encrypt 12
    [Tags]    Owner:Ram        Reviewer:       Encrypt
    Given Using password anacrypt aastra.cfg file with 1234567 as password
    And Verify text aastra.cfg files not present in the folder

762219: Encrypt 22
    [Tags]    Owner:Ram        Reviewer:       Encrypt
    Given Using mac anacrypt 00085D001012.cfg file with 1234567 as password
    And Verify mac-anacrypted 00085D001012.cfg files are present in the folder

761995: Check config encryption key in server.cfg
    [Tags]    Owner:Ram        Reviewer:       Encrypt
    &{Details} =��Create Dictionary    DownloadProtocol=FTP
    &{parameters} =��Create Dictionary       config encryption key=1234567     upload system info manual option= 1     upload system info server=${serverDetails}
    Given I want to configure ConfigurationServer parameters using ${Details} for ${phone1}
    Then Create ${startUp} file using ${parameters}
    Then Create ${sysinfo} folder on FTP server
    Then Send ${startUp} file on FTP server
    Then reboot ${phone1}
    Then using ${PhoneWUI} Log Into ${phone1} URL
    Then Using ${PhoneWUI} click on the ${uploadButton} on ${phone1} URL
    Then Using ${PhoneWUI} logoff ${phone1} URL
    And Verify config encryption key parameter is present in the ${serverFile} on ${sysinfo} folder on FTP server

762588: mask sip password: 1 - mask local.cfg
    [Tags]    Owner:Ram        Reviewer:       maskPassword
    &{Details} =��Create Dictionary    DownloadProtocol=FTP
    &{parameters} =��Create Dictionary       upload system info manual option= 1     upload system info server=${serverDetails}    mask sip password=1
    Given I want to configure ConfigurationServer parameters using ${Details} for ${phone1}
    Then Create ${startUp} file using ${parameters}
    Then Create ${sysinfo} folder on FTP server
    Then Send ${startUp} file on FTP server
    Then reboot ${phone1}
    Then using ${PhoneWUI} Log Into ${phone1} URL
    Then Using ${PhoneWUI} click on the ${uploadButton} on ${phone1} URL
    Then Using ${PhoneWUI} register line1-9 of ${phone1} with ${phone1}
    Then Using ${PhoneWUI} logoff ${phone1} URL
    And Verify sip line 1-9 password parameter are masked in the ${serverFile} on ${sysinfo} folder on FTP server

766571: Long press ( about 750 ms) digit '0' _idle state
    [Tags]    Owner:Ram        Reviewer:       longPress
    Given Long press hardkey as DialPad0 on ${phone1}
    Then On ${phone1} verify display message >+
    And press hardkey as ${goodBye} on ${phone1}

766573: Long press ( about 750 ms) digit '0' _dialing state
    [Tags]    Owner:Ram        Reviewer:       longPress
    Given press hardkey as ${offHook} on ${phone1}
    Then Long press hardkey as DialPad0 on ${phone1}
    Then On ${phone1} verify display message >+
    And press hardkey as ${goodBye} on ${phone1}

766580: Keypad Speed Dial_TUI
    [Tags]    Owner:Ram        Reviewer:       longPress
    Given Long press hardkey as DialPad1 on ${phone1}
    Then On ${phone1} verify display message Speed Dial 1
    Then press hardkey as ${goodBye} on ${phone1}
    Then Long press hardkey as DialPad2 on ${phone1}
    Then On ${phone1} verify display message Speed Dial 2
    Then press hardkey as ${goodBye} on ${phone1}
    Then Long press hardkey as DialPad3 on ${phone1}
    Then On ${phone1} verify display message Speed Dial 3
    Then press hardkey as ${goodBye} on ${phone1}
    Then Long press hardkey as DialPad4 on ${phone1}
    Then On ${phone1} verify display message Speed Dial 4
    Then press hardkey as ${goodBye} on ${phone1}
    Then Long press hardkey as DialPad5 on ${phone1}
    Then On ${phone1} verify display message Speed Dial 5
    Then press hardkey as ${goodBye} on ${phone1}
    Then Long press hardkey as DialPad6 on ${phone1}
    Then On ${phone1} verify display message Speed Dial 6
    Then press hardkey as ${goodBye} on ${phone1}
    Then Long press hardkey as DialPad7 on ${phone1}
    Then On ${phone1} verify display message Speed Dial 7
    Then press hardkey as ${goodBye} on ${phone1}
    Then Long press hardkey as DialPad8 on ${phone1}
    Then On ${phone1} verify display message Speed Dial 8
    Then press hardkey as ${goodBye} on ${phone1}
    Then Long press hardkey as DialPad9 on ${phone1}
    Then On ${phone1} verify display message Speed Dial 9
    Then Long press hardkey as DialPad0 on ${phone1}
    Then on ${phone1} enter number ${phone2}
    Then on ${phone1} Press ${softKey} ${bottomKey1} for 1 times
    Then Using ${PhoneWUI} Start the capture on all port on ${phone1} URL
    Then Long press hardkey as DialPad9 on ${phone1}
    Then on ${phone1} verify display message +
    Then on ${phone1} verify display message ${phone2}
    Then Using ${PhoneWUI} ${stop} the capture from ${phone1} URL
    Then Using ${PhoneWUI} ${download} the capture from ${phone1} URL
    Then Verify the captureFile contains from=${phone2} inside ${Protocols['HTTP']} packets
    Then Verify the captureFile contains user=${phone2} inside ${Protocols['HTTP']} packets

763545: SDE �050
    [Tags]    Owner:Ram        Reviewer:       speedDial
    Given Long press hardkey as DialPad1 on ${phone1}
    Then On ${phone1} verify display message Speed Dial 1
    Then on ${phone1} enter number 123
    Then on ${phone1} Press ${softKey} ${bottomKey1} for 1 times
    Then using ${PhoneWUI} log into ${phone1} url
    Then Using ${PhoneWUI} click on the ${KeypadSpeedDialMenu} on ${phone1} URL
    Then Using ${PhoneWUI} Verify text 123 for ${keyPad1} on the ${phone1} URL
    And using ${PhoneWUI} logoff ${phone1} url

762514: TC_31
   [Tags]   Owner:Ram    Reviewer:     ScreenSaver    notapplicablefor6865
   &{parameters} =��Create Dictionary    screen save time= 2
   &{screenSaverDetails} =��Create Dictionary    screenSaverIsSet=TRUE
   Given Create ${startUp} file using ${parameters}
   Then Create ${sysinfo} folder on FTP server
   Then Send ${startUp} file on FTP server
   Then reboot ${phone1}
   Then On ${phone1} Wait for 2 seconds
   Then Check the screensaver display on ${phone1} using ${screenSaverDetails}
   Then Set the screensaver timer to 3 seconds on ${phone1}
   Then On ${phone1} Wait for 3 seconds
   And Check the screensaver display on ${phone1} using ${screenSaverDetails}
   [Teardown]     Default screen saver settings

762524:TC01 : Outgoing intercom - phone side (stateless proxy, feature enabled)
    [Tags]    Owner:Ram        Reviewer:       Intercom    100
    &{Details} =��Create Dictionary    intercomType=1
    Given I want to configure Preferences parameters using ${Details} for ${phone1}
    Then i want to use fac ${intercom} on ${phone1} to ${phone2}
    Then verify audio path between ${phone1} and ${phone2}
    And disconnect the call from ${phone2}
    [Teardown]    Default Preferences settings

762515: TC_32
   [Tags]   Owner:Ram    Reviewer:     ScreenSaver    notapplicablefor6865
   &{parameters} =��Create Dictionary    screen save time= 0
   &{screenSaverDetails} =��Create Dictionary    screenSaverIsSet=False
   Given Set the screensaver timer to 3 seconds on ${phone1}
   Then Create ${startUp} file using ${parameters}
   Then Create ${sysinfo} folder on FTP server
   Then Send ${startUp} file on FTP server
   Then reboot ${phone1}
   Then On ${phone1} Wait for 5 seconds
   And Check the screensaver display on ${phone1} using ${screenSaverDetails}
   [Teardown]     Default screen saver settings

762519: On screen Time Check
    [Tags]   Owner:Ram    Reviewer:     ScreenSaver    notapplicablefor6865
    &{parameters} =��Create Dictionary    screen save time= 2
    &{screenSaverDetails} =��Create Dictionary    isTimeShown=TRUE
    Given Create ${startUp} file using ${parameters}
    Then Create ${sysinfo} folder on FTP server
    Then Send ${startUp} file on FTP server
    Then reboot ${phone1}
    Then On ${phone1} Wait for 2 seconds
    And Check the screensaver display on ${phone1} using ${screenSaverDetails}
    [Teardown]     Default screen saver settings

763538: SDE �014
    [Tags]   Owner:Ram    Reviewer:     PKM   notapplicablefor6865
    Given On PKM Long press hardkey as ${programKey1} on ${phone1}
    Then on ${phone1} verify display message Speed Dial Edit
    Then press hardkey as ${goodBye} on ${phone1}
    And verify the led state of ${line1} as ${off} on ${phone1}

763539: SDE �020
    [Tags]   Owner:Ram    Reviewer:     PKM    notapplicablefor6865
    Given I want to program dnd key on position 3 on ${phone1}
    Then On ${phone1} program blf key on position 4 with ${phone2} value
    Then press softkey ${programKey3} on ${phone1}
    Then i want to make a two party call between ${phone3} and ${phone2} using ${offHook}
    Then answer the call on ${phone2} using ${offHook}
    Then On PKM Long press hardkey as ${programKey1} on ${phone1}
    Then verify the led state of ${line3} as ${on} on ${phone1}
    Then verify the led state of ${line4} as ${on} on ${phone1}
    Then on ${phone1} verify display message Speed Dial Edit
    Then verify the led state of ${line3} as ${off} on ${phone1}
    Then verify the led state of ${line4} as ${off} on ${phone1}
    Then press hardkey as ${goodBye} on ${phone1}
    Then verify the led state of ${line3} as ${on} on ${phone1}
    And verify the led state of ${line4} as ${on} on ${phone1}


763681: Softkey icon in Hold state(Remote Hold).
    [Tags]   Owner:Ram    Reviewer:     RemoteHold
    Given I want to make a two party call between ${phone2} and ${phone1} using ${offHook}
    Then answer the call on ${phone1} using ${offHook}
    Then put the linekey ${line1} of ${phone2} on ${hold}
    Then On ${phone1} verify ${line1} icon state as CALL_APPEARANCE_REMOTE_HOLD
    Then put the linekey ${line1} of ${phone2} on ${unhold}
    Then On ${phone1} verify ${line1} icon state as CALL_APPEARANCE_ACTIVE
    Then disconnect the call from ${phone2}

762320: Single BLF monitoring and barge in:
    [Tags]   Owner:Ram    Reviewer:     BLF
    Given On ${phone1} program blf key on position 4 with ${phone2} value
    Then On ${phone1} verify ${line1} icon state as STATUS_BLF_GREEN
    Then I want to make a two party call between ${phone3} and ${phone2} using ${offHook}
    Then On ${phone1} verify ${line1} icon state as STATUS_BLF_YELLOW
    Then answer the call on ${phone2} using ${offHook}
    Then On ${phone1} verify ${line1} icon state as STATUS_BLF_RED
    And disconnect the call from ${phone2}
    [Teardown]     Remove program button

762321: DCP–014
    [Tags]   Owner:Ram    Reviewer:     BLF
    Given On ${phone1} program blf key on position 4 with ${phone2} value
    Then On ${phone1} verify ${line1} icon state as STATUS_BLF_GREEN
    Then I want to make a two party call between ${phone2} and ${phone3} using ${offHook}
    Then On ${phone1} verify ${line1} icon state as STATUS_BLF_RED
    Then answer the call on ${phone3} using ${offHook}
    Then On ${phone1} verify ${line1} icon state as STATUS_BLF_RED
    And disconnect the call from ${phone2}
    [Teardown]     Remove program button

762323: DCP–016
    [Tags]   Owner:Ram    Reviewer:     BLF
    Given On ${phone1} program blf key on position 4 with ${phone2} value
    Then On ${phone1} verify ${line1} icon state as STATUS_BLF_GREEN
    Then I want to make a two party call between ${phone2} and ${phone3} using ${offHook}
    Then On ${phone1} verify ${line1} icon state as STATUS_BLF_RED
    Then answer the call on ${phone3} using ${offHook}
    Then On ${phone1} verify ${line1} icon state as STATUS_BLF_RED
    Then on ${phone1} press ${softkey} ${programKey4} for 1 times
    Then on ${phone1} verify display message Call Failed
    Then disconnect the call from ${phone1}
    And disconnect the call from ${phone2}
    [Teardown]     Remove program button





763821: Verify_Status
    [Tags]    Owner:Aman        Reviewer:       verify_status    regressionChineseSupport
    Given press hardkey as ${menu} on ${phone1}
    Then on ${phone1} verify display message ${Status_C}
    Then press hardkey as ${enter} on ${phone1}
    Then on ${phone1} verify display message ${Firmware_Info_C}
    Then press hardkey as ${scrollDown} on ${phone1}
    Then on ${phone1} verify display message ${Network_C}
    Then press hardkey as ${scrollDown} on ${phone1}
    Then on ${phone1} verify display message ${Storage_C}
    Then press hardkey as ${scrollDown} on ${phone1}
    Then on ${phone1} verify display message ${Error_Messages_C}
    Then on ${phone1} verify display message ${Status_C}
    And press hardkey as ${goodBye} on ${phone1}

763828: Call Conference
    [Tags]    Owner:Aman        Reviewer:       conference    regressionChineseSupport
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then on ${phone2} wait for 2 seconds
    Then on ${phone2} press ${softKey} ${bottomKey1} for 1 times
    Then On ${phone2} verify display message ${drop_C}
    Then on ${phone1} press the softkey ${conference} in AnswerState
    Then on ${phone1} enter number ${phone3}
    Then on ${phone1} press ${softKey} ${bottomKey1} for 1 times
    Then on ${phone3} wait for 2 seconds
    Then on ${phone3} press ${softKey} ${bottomKey1} for 1 times
    Then on ${phone3} wait for 2 seconds
    Then on ${phone1} press the softkey ${conference} in AnswerState
    Then conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then On ${phone1} verify display message ${drop_C}
    Then On ${phone1} verify display message ${leave_C}
    Then i want to press line key ${programKey2} on phone ${phone1}
    Then on ${phone1} enter number ${phone4}
    Then on ${phone1} press ${softKey} ${bottomKey1} for 1 times
    Then on ${phone4} wait for 2 seconds
    Then on ${phone4} press ${softKey} ${bottomKey1} for 1 times
    Then on ${phone1} press the softkey ${conference} in AnswerState
    Then i want to press line key ${programKey1} on phone ${phone1}
    Then Four party Conference call audio verification between ${phone1} ${phone2} ${phone3} and ${phone4}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone3}
    And disconnect the call from ${phone4}

763824: Verify Bluetooth_DUT 6930
    [Tags]    Owner:Aman    Reviewer:    bluetooth    regressionChineseSupport    notApplicableFor6920    notApplicableFor6910
    Given Press hardkey as ${menu} on ${phone1}
    Then on ${phone1} press ${hardKey} ${scrollRight} for 1 times
    Then On ${phone1} verify display message ${bluetooth_C}
    Then on ${phone1} press ${hardKey} ${enter} for 1 times
    Then On ${phone1} verify display message ${bluetooth_C}
    Then On ${phone1} verify display message ${turnOn_C}
    Then On ${phone1} verify display message ${close_C}
    Then on ${phone1} press ${softKey} ${bottomKey1} for 1 times
    Then On ${phone1} verify display message ${enableBluetooth_C}
    Then on ${phone1} Wait for 5 seconds
    Then On ${phone1} verify display message ${pairedDevices_C}
    Then On ${phone1} verify display message ${availableDevices_C}
    Then On ${phone1} verify display message ${turnOff_C}
    Then on ${phone1} press ${softKey} ${bottomKey1} for 1 times
    Then on ${phone1} Wait for 2 seconds
    Then On ${phone1} verify display message ${turnOn_C}
    And press hardkey as ${goodBye} on ${phone1}

763830: "Call failed" _Wrong number dialling
    [Tags]    Owner:Aman    Reviewer:    call    regressionChineseSupport
    Given on ${phone1} enter number 40
    Then on ${phone1} press the softkey ${dial} in DialingState
    Then on ${phone1} verify display message ${callFailed_C}
    Then Press hardkey as ${goodBye} on ${phone1}
    Then I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then on ${phone1} verify display message ${ringing_C}
    And Press hardkey as ${goodBye} on ${phone1}

763820: Time and date_Settings
    [Tags]    Owner:Aman    Reviewer:    time    regressionChineseSupport
    Given Press hardkey as ${menu} on ${phone1}
    Then on ${phone1} press ${hardKey} ${scrollLeft} for 4 times
    Then On ${phone1} verify display message ${timeAndDate_C}
    Then On ${phone1} verify display message ${settings_C}
    Then press hardkey as ${enter} on ${phone1}
    Then On ${phone1} verify display message ${timeFormat_C}
    Then On ${phone1} verify display message 12小时    # Verifying '12 Hour'
    Then On ${phone1} verify display message 24小时    # Verifying '24 Hour'
    Then on ${phone1} press ${hardKey} ${scrollDown} for 1 times
    Then On ${phone1} verify display message ${daylightSavings_C}
    Then On ${phone1} verify display message 关    # Verifying 'Off'
    Then On ${phone1} verify display message 夏季30分钟    # Verifying '30min summertime'
    Then On ${phone1} verify display message 夏季1小时    # Verifying '1h summertime'
    Then On ${phone1} verify display message 自动    # Verifying 'Automatic'
    Then on ${phone1} press ${hardKey} ${scrollDown} for 1 times
    Then On ${phone1} verify display message ${dateFormat_C}
    Then On ${phone1} verify display message YYYY-MM-DD    # Verifying 'YYYY-MM-DD'
    And Press hardkey as ${goodBye} on ${phone1}

763826: Navigation Key
    [Tags]    Owner:Aman    Reviewer:    navigation    regressionChineseSupport
    Given on ${phone1} press ${hardKey} ${scrollRight} for 1 times
    Then On ${phone1} verify display message 1号线    # Verifying 'Line 1'
    Then On ${phone1} verify display message 2号线    # Verifying 'Line 2'
    Then on ${phone1} press ${hardKey} ${scrollDown} for 1 times
    Then on ${phone1} press ${hardKey} ${scrollUp} for 1 times
    Then On ${phone1} verify display message 新来电    # Verifying 'New Call'
    And Press hardkey as ${goodBye} on ${phone1}

763822: Verify_Diagnostics
    [Tags]    Owner:Aman    Reviewer:    diagnostics    regressionChineseSupport
    Given Press hardkey as ${menu} on ${phone1}    # Go to Advance Setting
    Then on ${phone1} press ${hardKey} ${scrollRight} for 2 times
    Then On ${phone1} verify display message ${diagnostics_C}
    Then on ${phone1} press ${hardKey} ${scrollDown} for 6 times
    Then press hardkey as ${enter} on ${phone1}
    Then On ${phone1} verify display message ${audioDiagnostics_C}
    Then on ${phone1} press ${softKey} ${bottomKey1} for 1 times
    Then On ${phone1} verify display message 捕捉    # Verifying 'Capturing'
    Then on ${phone1} press ${softKey} ${bottomKey1} for 1 times
    Then On ${phone1} verify display message 收集日志    # Verifying 'Collecting Logs'
    Then On ${phone1} Wait for 3 seconds
    Then On ${phone1} verify display message 完成    # Verifying 'Complete'
    And Press hardkey as ${goodBye} on ${phone1}
    Given Press hardkey as ${menu} on ${phone1}    # Go to Advance Setting
    Then on ${phone1} press ${hardKey} ${scrollRight} for 2 times
    Then On ${phone1} verify display message ${diagnostics_C}
    Then on ${phone1} press ${hardKey} ${scrollDown} for 6 times
    Then press hardkey as ${enter} on ${phone1}
    Then On ${phone1} verify display message ${audioDiagnostics_C}
    Then On ${phone1} verify display message ${timeout_C}
    Then on ${phone1} press ${softKey} ${bottomKey2} for 2 times
    Then on ${phone1} enter number 6
    Then on ${phone1} press ${softKey} ${bottomKey1} for 1 times
    Then On ${phone1} verify display message 请输入1到5分钟之间的时长    # Verifying 'Please input a duration between 1 and 5 minutes'
    And Press hardkey as ${goodBye} on ${phone1}

763833: Configure last softkey_Top Soft key
    [Tags]    Owner:Anuj    Reviewer:    softkey_chinese    763831
    &{configurationDetails}=    create dictionary    topsoftkey2 type=speeddial    topsoftkey2 label=speeddial    topsoftkey2 value=${phone2}
    Given Configure parameters on ${phone1} using ${configurationDetails}
    Then on ${phone1} verify display message ${speeddial_c}
    &{configurationDetails}=    create dictionary    topsoftkey2 type=speeddial    topsoftkey2 label=speeddl    topsoftkey2 value=${phone2}
    Given Configure parameters on ${phone1} using ${configurationDetails}
    Then on ${phone1} verify display message ${speeddl_c}
    Then i want to press line key ${programKey3} on phone ${phone1}
    Then on ${phone2} verify display message ${iscalling_c}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify the caller id on ${phone1} and ${phone2} display
    Then verify audio path between ${phone1} and ${phone2}
    Then disconnect the call from ${phone2}

763832: Configure 12th softkey_Long Label Name_Bottom Softkey
    [Tags]    Owner:Aman    Reviewer:    softkey
    &{configurationDetails}=    create dictionary    topsoftkey11 type=speeddial    topsoftkey11 label=speeddial!    topsoftkey11 value=${phone2}
    Given Configure parameters on ${phone1} using ${configurationDetails}
    Then on ${phone1} verify display message ${speeddial!_c}
    Then i want to press line key ${programKey12} on phone ${phone1}
    Then on ${phone2} verify display message ${iscalling_c}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify the caller id on ${phone1} and ${phone2} display
    Then disconnect the call from ${phone2}
    &{configurationDetails}=    create dictionary    topsoftkey11 type=none
    And Configure parameters on ${phone1} using ${configurationDetails}

763834: Configure 1st softkey_PKM_Page 1
    [Tags]    Owner:Aman    Reviewer:    pkm    123443211
    &{details}=    CREATE DICTIONARY    page_number=page1    label=callforward    position=2    function=callforward
    Given I want to configure expandableModule parameters using ${details} for ${phone1}
    Then verify display message ${call_forward_c} on PKM for ${phone1}
    Then I want to program callforward key on page1 on position 2 with callfwd on ${phone1}
    Then verify display message ${forward_c} on PKM for ${phone1}
    Then I want to program callforward key on page1 on position 2 with callfwd on ${phone1}
    Then verify display message ${forward_c} on PKM for ${phone1}
    Then I want to program None key on page1 on position 2 with callfwd on ${phone1}

763842: Global Line Configuration_Screen Name_Web Page
    [Tags]    Owner:Aman    Reviewer:    globalSIP    regressionChineseSupport
    &{details}=    CREATE DICTIONARY    ScreenName=自动化用户
    Given I want to configure GlobalSettings parameters using ${Details} for ${phone1}
    Then On ${phone1} verify display message 自动化用户    # Verifying 'Automation User'
   # Set screen name Automation User Account
    Then On ${phone1} verify display message 自动化用户帐户...    # Verifying 'Automation User Acc...'

762106: BLFholdpickup_08
    [Tags]    Owner:Aman    Reviewer:    blf    Execute    762106
	&{configurationDetails}=    CREATE DICTIONARY    collapsed softkey screen=0    topsoftkey4 type=blf    topsoftkey4 label=blf    topsoftkey4 value=${phone2}
    Given configure parameters on ${phone1} using ${configurationdetails}

	&{configurationDetails}=    CREATE DICTIONARY    directed call pickup=1    directed call pickup prefix=*98
	Given configure parameters on ${phone1} using ${configurationdetails}

	Then i want to make a two party call between ${phone3} and ${phone2} using ${loudspeaker}
	Then verify the led state of ${line4} as ${blink} on ${phone1}
	Then answer the call on ${phone2} using ${loudspeaker}
	Then verify the led state of ${line4} as ${on} on ${phone1}
	Then verify audio path between ${phone3} and ${phone2}
	Then press hardkey as ${holdState} on ${phone2}
	Then verify the led state of ${line1} as ${blink} on ${phone2}
	Then verify the led state of ${line4} as ${blink} on ${phone1}
	Then i want to press line key ${programKey4} on phone ${phone1}
	Then verify audio path between ${phone1} and ${phone3}
    Then Transfer call from ${phone1} to ${phone4} using ${blindTransfer}
    Then Verify the Caller id on ${phone3} and ${phone4} display
	Then verify audio path between ${phone3} and ${phone4}
    Then disconnect the call from ${phone4}
	&{configurationDetails}=    CREATE DICTIONARY    directed call pickup=0
	Then configure parameters on ${phone1} using ${configurationdetails}
	And I want to program ${none} key on position 4 on ${phone1}

762107: BLFholdpickup_09
    [Tags]    Owner:Aman    Reviewer:    blf    Execute
	&{configurationDetails}=    CREATE DICTIONARY    collapsed softkey screen=0    topsoftkey4 type=blf    topsoftkey4 label=blf    topsoftkey4 value=${phone2}
    Given configure parameters on ${phone1} using ${configurationdetails}
	&{configurationDetails}=    CREATE DICTIONARY    directed call pickup=1    directed call pickup prefix=**
	Given configure parameters on ${phone1} using ${configurationdetails}
	Then i want to make a two party call between ${phone3} and ${phone2} using ${loudspeaker}
	Then verify the led state of ${line4} as ${blink} on ${phone1}
	Then answer the call on ${phone2} using ${loudspeaker}
	Then verify the led state of ${line4} as ${on} on ${phone1}
	Then verify audio path between ${phone3} and ${phone2}
	Then press hardkey as ${holdState} on ${phone2}
	Then verify the led state of ${line1} as ${blink} on ${phone2}
	Then verify the led state of ${line4} as ${blink} on ${phone1}
	Then i want to press line key ${programKey4} on phone ${phone1}
	Then i want to make a conference call between ${phone1},${phone3} and ${phone4} using ${consultiveConference}
	Then conference call audio verify between ${phone1} ${phone3} and ${phone4}
    Then disconnect the call from ${phone3}
    Then disconnect the call from ${phone4}
	&{configurationDetails}=    CREATE DICTIONARY    directed call pickup=0
	Then configure parameters on ${phone1} using ${configurationdetails}
	And I want to program ${none} key on position 4 on ${phone1}

862445: BLFholdpickup_22_a
    [Tags]    Owner:Aman    Reviewer:    blf    Execute
	&{configurationDetails}=    CREATE DICTIONARY    collapsed softkey screen=0    topsoftkey4 type=blfxfer    topsoftkey4 label=blf    topsoftkey4 value=${phone2}
    Given configure parameters on ${phone1} using ${configurationdetails}
	&{configurationDetails}=    CREATE DICTIONARY    directed call pickup=1    directed call pickup prefix=**
	Given configure parameters on ${phone1} using ${configurationdetails}
	Then i want to make a two party call between ${phone3} and ${phone2} using ${offhook}
	Then verify the led state of ${line4} as ${blink} on ${phone1}
	Then answer the call on ${phone2} using ${offhook}
	Then verify the led state of ${line4} as ${on} on ${phone1}
	Then verify audio path between ${phone3} and ${phone2}
	Then i want to press line key ${programKey4} on phone ${phone1}
	Then verify audio path between ${phone1} and ${phone3}
    Then disconnect the call from ${phone1}
	Then i want to make a two party call between ${phone3} and ${phone2} using ${loudspeaker}
	Then verify the led state of ${line4} as ${blink} on ${phone1}
	Then answer the call on ${phone2} using ${loudspeaker}
	Then verify the led state of ${line4} as ${on} on ${phone1}
	Then verify audio path between ${phone3} and ${phone2}
	Then i want to press line key ${programKey4} on phone ${phone1}
	Then verify audio path between ${phone1} and ${phone3}
    Then disconnect the call from ${phone1}
	&{configurationDetails}=    CREATE DICTIONARY    directed call pickup=0
	Then configure parameters on ${phone1} using ${configurationdetails}
	And I want to program ${none} key on position 4 on ${phone1}

762109: BLFholdpickup_23
    [Tags]    Owner:Aman    Reviewer:    blf    Execute     miv5000
	&{configurationDetails}=    CREATE DICTIONARY    collapsed softkey screen=0    topsoftkey4 type=blfxfer    topsoftkey4 label=blf    topsoftkey4 value=${phone2}
    Given configure parameters on ${phone1} using ${configurationdetails}
	&{configurationDetails}=    CREATE DICTIONARY    directed call pickup=1    directed call pickup prefix=**
	Given configure parameters on ${phone1} using ${configurationdetails}
	Then i want to make a two party call between ${phone3} and ${phone2} using ${loudspeaker}
	Then verify the led state of ${line4} as ${blink} on ${phone1}
	Then answer the call on ${phone2} using ${loudspeaker}
	Then verify the led state of ${line4} as ${on} on ${phone1}
	Then verify audio path between ${phone3} and ${phone2}
	Then press hardkey as ${holdState} on ${phone2}
	Then verify the led state of ${line1} as ${blink} on ${phone2}
	Then verify the led state of ${line4} as ${blink} on ${phone1}
	Then i want to press line key ${programKey4} on phone ${phone1}
	Then verify audio path between ${phone1} and ${phone3}
    Then Transfer call from ${phone1} to ${phone4} using ${blindTransfer}
    Then Verify the Caller id on ${phone3} and ${phone4} display
	Then verify audio path between ${phone3} and ${phone4}
    Then disconnect the call from ${phone4}
	&{configurationDetails}=    CREATE DICTIONARY    directed call pickup=0
	Then configure parameters on ${phone1} using ${configurationdetails}
	And I want to program ${none} key on position 4 on ${phone1}

762046: Restart when directory1 file was modified. The directory1 URL was in aastra.cfg and the resync mode was configuration
    [Tags]    Owner:Aman    Reviewer:    directory
    &{parameters}=    CREATE DICTIONARY     auto resync mode=1   auto resync time=05:30     directory 1 enabled=1   directory 1: ${directory_1_path}
    Given Create ${startUp} file using ${parameters}
    Then Create ${systeminfo} folder on FTP server
    Then Send ${startUp} file in ${systeminfo} folder on FTP server
    Then update date as Today and time as 05:29:00 on ${phone1}
    Then On ${phone1} Wait for 200 seconds
    Then in directory search ${phone2} on ${phone1}
    Then verify extension number of ${phone2} on ${phone1}
    And press hardkey as ${goodBye} on ${phone1}
    [Teardown]  Default Directory Detail in Startup File

762047: Restart when directory2 file was modified. The directory2 URL was in aastra.cfg and the mode was Both.
    [Tags]    Owner:Aman    Reviewer:    directory
    &{parameters}=    CREATE DICTIONARY     auto resync mode=3   auto resync time=05:30     directory 2 enabled=1   directory 2: ${directory_2_path}
    Given Create ${startUp} file using ${parameters}
    Then Create ${systeminfo} folder on FTP server
    Then Send ${startUp} file in ${systeminfo} folder on FTP server
    Then update date as Today and time as 05:29:00 on ${phone1}
    Then On ${phone1} Wait for 200 seconds
    Then in directory search ${phone2} on ${phone1}
    Then verify extension number of ${phone2} on ${phone1}
    And press hardkey as ${goodBye} on ${phone1}
    [Teardown]  Default Directory Detail in Startup File

763424: TC014
   [Tags]    Owner:Aman    Reviewer:    timeUS      Execute
   &{configurationDetails}=    CREATE DICTIONARY    collapsed softkey screen=0    topsoftkey3 type=xml    topsoftkey3 label=Time US XML
                               ...  topsoftkey3 value=http://10.112.123.89/XML/DesktopXML/AastraIPPhoneInputScreen/timeus.xml
   Given configure parameters on ${phone1} using ${configurationdetails}
   Then i want to press line key ${programKey3} on phone ${phone1}
   Then On ${phone1} verify display message US Time
   Then On ${phone1} verify display message AM/PM
   Then on ${phone1} press ${softKey} ${bottomKey2} for 1 times
   Then On ${phone1} verify display message PM
   And Press hardkey as ${goodBye} on ${phone1}
   [Teardown]  I want to program ${none} key on position 3 on ${phone1}

763419: Verify done action in an image screen
    [Tags]    Owner:Aman    Reviewer:    doneAction     763419      Execute
	&{configurationDetails}=    CREATE DICTIONARY    collapsed softkey screen=0    topsoftkey3 type=xml    topsoftkey3 label=DoneAction XML
	                            ...  topsoftkey3 value=http://10.112.123.89/XML/DesktopXML/AastraIPPhoneImageScreen/image.xml
    Given configure parameters on ${phone1} using ${configurationdetails}
    Then i want to press line key ${programKey3} on phone ${phone1}
    Then on ${phone1} press ${softKey} ${bottomKey5} for 1 times
    Then On ${phone1} verify display message Application
    Then on ${phone1} press ${hardKey} ${scrollLeft} for 1 times
    And Verify extension ${number} of ${phone1} on ${phone1}
   [Teardown]  I want to program ${none} key on position 3 on ${phone1}

763414: Verify destroy on exit set to yes
    [Tags]    Owner:Aman    Reviewer:    doneAction     763414      Execute
	&{configurationDetails}=    CREATE DICTIONARY    collapsed softkey screen=0    topsoftkey3 type=xml    topsoftkey3 label=Image XML
	                            ...  topsoftkey3 value=http://10.112.123.89/XML/DesktopXML/AastraIPPhoneImageScreen/image1.xml
	&{configurationDetails1}=    CREATE DICTIONARY    collapsed softkey screen=0    topsoftkey4 type=xml    topsoftkey4 label=Space XML
	                            ...  topsoftkey4 value=http://10.112.123.89/XML/DesktopXML/AastraIPPhoneImageScreen/space1.xml
    Given configure parameters on ${phone1} using ${configurationdetails}
    Given configure parameters on ${phone1} using ${configurationdetails1}
    Then i want to press line key ${programKey3} on phone ${phone1}
    Then On ${phone1} verify display message Application
    Then Press hardkey as ${goodBye} on ${phone1}
    Then i want to press line key ${programKey4} on phone ${phone1}
    Then On ${phone1} verify display message Application 22
    Then Press hardkey as ${goodBye} on ${phone1}
    And Verify extension ${number} of ${phone1} on ${phone1}
	&{configurationDetails}=    CREATE DICTIONARY    topsoftkey3 type=none      topsoftkey4 type=none
    [Teardown]  configure parameters on ${phone1} using ${configurationDetails}

763442: Verify the value of $$REMOTENUMBER$$ defined in an Incoming Call action URI
    [Tags]    Owner:Aman    Reviewer:    actionURI     763442       Execute
    &{details}=    CREATE DICTIONARY    incomingField=http://10.112.123.89/XML/DesktopXML/action-uri-variables/weather.xml?Remote-Number=$$REMOTENUMBER$$
    Given Using ${PhoneWUI} log into ${phone1} URL
    Then I want to configure ActionUrl parameters using ${Details} for ${phone1}
    Then Using ${PhoneWUI} Start the capture on all port on ${phone1} URL
    Then I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then press hardkey as ${goodBye} on ${phone1}
	Then answer the call on ${phone1} using ${loudspeaker}
    Then verify the caller id on ${phone1} and ${phone2} display
    Then disconnect the call from ${phone1}
    Then Using ${PhoneWUI} ${stop} the capture from ${phone1} URL
    Then Using ${PhoneWUI} ${download} the capture from ${phone1} URL
    Then Verify the captureFile contains Remote-Number=${phone2} inside ${Protocols['HTTP']} packets
    [Teardown]  Default ActionURI Configuration


763443: Verify the value of $$CALLDIRECTION$$ in an Incoming Call Action URI
    [Tags]    Owner:Aman    Reviewer:    actionURI     763443       Execute
    &{details}=    CREATE DICTIONARY    incomingField=http://10.112.123.89/XML/DesktopXML/action-uri-variables/weather.xml?call-direction=$$CALLDIRECTION$$
    Given Using ${PhoneWUI} log into ${phone1} URL
    Then I want to configure ActionUrl parameters using ${Details} for ${phone1}
    Then Using ${PhoneWUI} Start the capture on all port on ${phone1} URL
    Then I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then on ${phone1} wait for 2 seconds
    Then disconnect the call from ${phone1}
    Then Using ${PhoneWUI} ${stop} the capture from ${phone1} URL
    Then Using ${PhoneWUI} ${download} the capture from ${phone1} URL
    Then Verify the captureFile contains call-direction=Incoming inside ${Protocols['HTTP']} packets
    [Teardown]  Default ActionURI Configuration


763444: Verify the variable $$LINESTATE$$ for an Incoming Call Action URI
    [Tags]    Owner:Aman    Reviewer:    actionURI     763444       Execute
    &{details}=    CREATE DICTIONARY    incomingField=http://10.112.123.89/XML/DesktopXML/action-uri-variables/weather.xml?line-state=$$LINESTATE$$
    Given Using ${PhoneWUI} log into ${phone1} URL
    Then I want to configure ActionUrl parameters using ${Details} for ${phone1}
    Then Using ${PhoneWUI} log into ${phone1} URL
    Then Using ${PhoneWUI} Start the capture on all port on ${phone1} URL
    Then I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then on ${phone1} wait for 2 seconds
    Then disconnect the call from ${phone1}
    Then Using ${PhoneWUI} ${stop} the capture from ${phone1} URL
    Then Using ${PhoneWUI} ${download} the capture from ${phone1} URL
    Then Verify the captureFile contains line-state=INCOMING inside ${Protocols['HTTP']} packets
    [Teardown]  Default ActionURI Configuration


763445: Verify the value of the variable $$SIPAUTHNAME$$ in a Successful Registration Action URI
    [Tags]    Owner:Aman    Reviewer:    actionURI     763445       Execute
    &{details}=    CREATE DICTIONARY    registeredField=http://10.112.123.89/XML/DesktopXML/action-uri-variables/weather.xml?sip-auth-name=$$IPAUTHNAME$$
    Given Using ${PhoneWUI} log into ${phone1} URL
    Then I want to configure ActionUrl parameters using ${Details} for ${phone1}
    Then Using ${PhoneWUI} Start the capture on all port on ${phone1} URL
    Then Reboot ${phone1}
    Then Using ${PhoneWUI} ${stop} the capture from ${phone1} URL
    Then Using ${PhoneWUI} ${download} the capture from ${phone1} URL
    Then Verify the captureFile contains sip-auth-name=${phone2} inside ${Protocols['HTTP']} packets
    [Teardown]  Default ActionURI Configuration


763446: Verify the accurate value of $$REGISTRATIONCODE$$ variable in a Successful Registration Action URI
    [Tags]    Owner:Aman    Reviewer:    actionURI     763446
    &{details}=    CREATE DICTIONARY    registeredField=http://10.112.123.89/XML/DesktopXML/action-uri-variables/weather.xml?registration-code=$$REGISTRATIONCODE$$
    Given Using ${PhoneWUI} log into ${phone1} URL
    Then I want to configure ActionUrl parameters using ${Details} for ${phone1}
    Then Using ${PhoneWUI} Start the capture on all port on ${phone1} URL
    Then Reboot ${phone1}
    Then Using ${PhoneWUI} ${stop} the capture from ${phone1} URL
    Then Using ${PhoneWUI} ${download} the capture from ${phone1} URL
    Then Verify the captureFile contains registration-code=${phone2} inside ${Protocols['HTTP']} packets
    [Teardown]  Default ActionURI Configuration


763447: Verify $$SIPUSERNAME$$ variable for an Outgoing Call Action URI
    [Tags]    Owner:Aman    Reviewer:    actionURI     763447       Execute
    &{details}=    CREATE DICTIONARY    outgoingField=http://10.112.123.89/XML/DesktopXML/action-uri-variables/weather.xml?sip-username=$$SIPUSERNAME$$
    Given Using ${PhoneWUI} log into ${phone1} URL
    Then I want to configure ActionUrl parameters using ${Details} for ${phone1}
    Then Using ${PhoneWUI} Start the capture on all port on ${phone1} URL
    Then I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then on ${phone1} wait for 2 seconds
    Then disconnect the call from ${phone1}
    Then Using ${PhoneWUI} ${stop} the capture from ${phone1} URL
    Then Using ${PhoneWUI} ${download} the capture from ${phone1} URL
    Then Verify the captureFile contains sip-username=${phone2} inside ${Protocols['HTTP']} packets
    [Teardown]  Default ActionURI Configuration

763498: TC02a: Verify barge-in normal works
    [Tags]    Owner:Aman    Reviewer:    bargeIn     763498
    &{sipmessagedetail} =  Create Dictionary    sip_message=INVITE    sip_message_value=VQSessionReport
    Given I want to make a two party call between ${phone2} and ${phone5} using ${loudspeaker}
    Then on ${phone5} wait for 3 seconds
	Then answer the call on ${phone5} using ${loudspeaker}
    Then i want to press line key ${programKey4} on phone ${phone1}
    Then on ${phone1} wait for 2 seconds
    Then Capture the ${outgoing} packets from ${phone1} and verifiy the ${sipmessagedetail} on ${phone2}
    Then Conference call audio verify between ${phone1} ${phone2} and ${phone5}
    Then press hardkey as ${goodBye} on ${phone1}
    And press hardkey as ${goodBye} on ${phone2}

763500: TC04b: remote party hangs up
    [Tags]    Owner:Aman    Reviewer:    bargeIn     763500
    Given I want to make a two party call between ${phone2} and ${phone5} using ${loudspeaker}
    Then on ${phone5} wait for 3 seconds
	Then answer the call on ${phone5} using ${loudspeaker}
	Then verify the led state of ${line4} as ${on} on ${phone1}
    Then i want to press line key ${programKey4} on phone ${phone1}
    Then Conference call audio verify between ${phone1} ${phone2} and ${phone5}
    Then press hardkey as ${goodBye} on ${phone2}
	Then verify the led state of ${line4} as ${off} on ${phone1}
	Then verify the led state of ${line1} as ${off} on ${phone1}
	Then verify the led state of ${line1} as ${off} on ${phone2}
	And verify the led state of ${line1} as ${off} on ${phone5}

763501: TC05b: Barger holds
    [Tags]    Owner:Aman    Reviewer:    bargeIn     763501
    Given I want to make a two party call between ${phone2} and ${phone5} using ${loudspeaker}
    Then on ${phone5} wait for 3 seconds
	Then answer the call on ${phone5} using ${loudspeaker}
	Then verify the led state of ${line4} as ${on} on ${phone1}
    Then i want to press line key ${programKey4} on phone ${phone1}
    Then Conference call audio verify between ${phone1} ${phone2} and ${phone5}
    Then press hardkey as ${holdState} on ${phone1}
    Then Verify audio path between ${phone2} and ${phone5}
    Then press hardkey as ${holdState} on ${phone1}
    Then Conference call audio verify between ${phone1} ${phone2} and ${phone5}
    Then press hardkey as ${goodBye} on ${phone1}
    Then press hardkey as ${goodBye} on ${phone2}
    And press hardkey as ${goodBye} on ${phone5}

763502: TC06b: Bargee holds
    [Tags]    Owner:Aman    Reviewer:    bargeIn     763502
    Given I want to make a two party call between ${phone2} and ${phone5} using ${loudspeaker}
    Then on ${phone5} wait for 3 seconds
	Then answer the call on ${phone5} using ${loudspeaker}
	Then verify the led state of ${line4} as ${on} on ${phone1}
    Then i want to press line key ${programKey4} on phone ${phone1}
    Then Conference call audio verify between ${phone1} ${phone2} and ${phone5}
    Then press hardkey as ${holdState} on ${phone5}
    Then Verify audio path between ${phone1} and ${phone2}
    Then press hardkey as ${holdState} on ${phone5}
    Then Conference call audio verify between ${phone1} ${phone2} and ${phone5}
    Then press hardkey as ${goodBye} on ${phone1}
    Then press hardkey as ${goodBye} on ${phone2}
    And press hardkey as ${goodBye} on ${phone5}

763503: TC07b: Remote Party holds
    [Tags]    Owner:Aman    Reviewer:    bargeIn     763503
    Given I want to make a two party call between ${phone2} and ${phone5} using ${loudspeaker}
    Then on ${phone5} wait for 3 seconds
	Then answer the call on ${phone5} using ${loudspeaker}
	Then verify the led state of ${line4} as ${on} on ${phone1}
    Then i want to press line key ${programKey4} on phone ${phone1}
    Then Conference call audio verify between ${phone1} ${phone2} and ${phone5}
    Then press hardkey as ${holdState} on ${phone2}
    Then Verify audio path between ${phone1} and ${phone5}
    Then press hardkey as ${holdState} on ${phone2}
    Then Conference call audio verify between ${phone1} ${phone2} and ${phone5}
    Then press hardkey as ${goodBye} on ${phone1}
    Then press hardkey as ${goodBye} on ${phone2}
    And press hardkey as ${goodBye} on ${phone5}

763318: TC002
    [Tags]    Owner:Aman    Reviewer:    UTF-8     763318
    &{configurationDetails}=    CREATE DICTIONARY    collapsed softkey screen=0    topsoftkey3 type=xml    topsoftkey3 label=Russian XML
                               ...  topsoftkey3 value=http://10.112.123.89/XML/DesktopXML/UTF-8/russian.xml
    Given configure parameters on ${phone1} using ${configurationDetails}
    Then i want to press line key ${programKey3} on phone ${phone1}
    Then On ${phone1} verify display message А Б В Г Д Е Ё Ж З И Й К Л М Н О П Р С Т У Ф Х Ц Ч Ш Щ Ъ Ы Ь Э Ю Я
    Then On ${phone1} verify display message а б в г д е ё ж з и й к л м н о п р с т у ф х ц ч ш щ ъ ы ь э ю я
    And Press hardkey as ${goodBye} on ${phone1}
    [Teardown]  I want to program ${none} key on position 3 on ${phone1}

763319: TC007
    [Tags]    Owner:Aman    Reviewer:    UTF-8     763319
   &{configurationDetails}=    CREATE DICTIONARY    collapsed softkey screen=0    topsoftkey3 type=xml    topsoftkey3 label=French XML
                               ...  topsoftkey3 value=http://10.112.123.89/XML/DesktopXML/UTF-8/french_diacritics.xml
   Given configure parameters on ${phone1} using ${configurationDetails}
   Then i want to press line key ${programKey3} on phone ${phone1}
   Then On ${phone1} verify display message à è À È é É â ê î ô û Â Ê Î Ô Û ä ë ï ö ü Ä Ë Ï Ö Ü æ Æ œ Œ ç Ç
   And Press hardkey as ${goodBye} on ${phone1}
   [Teardown]  I want to program ${none} key on position 3 on ${phone1}

763320: TC009
    [Tags]    Owner:Aman    Reviewer:    UTF-8     763320
    &{details}=    CREATE DICTIONARY    ScreenName=Ààâ
    Given I want to configure GlobalSettings parameters using ${Details} for ${phone1}
    Then On ${phone1} verify display message Ààâ
    [Teardown]  Default Phone state

763321: TC010
    [Tags]    Owner:Aman    Reviewer:    UTF-8     763321
    &{details}=    CREATE DICTIONARY    ScreenName=Ààâ
    Given I want to configure GlobalSettings parameters using ${Details} for ${phone1}
    Then On ${phone1} verify display message Ààâ
    [Teardown]  Default Phone state

762780: Basic TC 1a: Default Registration Renewal timer (RRT)=15sec
    [Tags]    Owner:Aman    Reviewer:    registration   762780      Execute
    &{details}=    CREATE DICTIONARY    registrationPeriod=0
    Given I want to configure GlobalSettings parameters using ${Details} for ${phone1}
    Then unregister the ${phone1} from ${MxOne} pbx
    Then Register the ${phone1} on ${MxOne} pbx
    &{sipmessagedetail} =  Create Dictionary    sip_message=REGISTER      sip_message_value=
    Then Capture the ${outgoing} packets from ${phone1} and verifiy the ${sipmessagedetail} on ${phone1}
    &{details}=    CREATE DICTIONARY    registrationPeriod=120      regRenewal=15
    Given I want to configure GlobalSettings parameters using ${Details} for ${phone1}
    Then on ${phone1} wait for 105 seconds
    &{sipmessagedetail} =  Create Dictionary    sip_message=REGISTER      sip_message_value=
    And Capture the ${outgoing} packets from ${phone1} and verifiy the ${sipmessagedetail} on ${phone1}
    [Teardown]  Default Phone state

762781: Basic TC 2b:Default Registration Renewal timer (RRT)=15sec
    [Tags]    Owner:Aman    Reviewer:    registration   762781
    &{details}=    CREATE DICTIONARY    registrationPeriod=20      regRenewal=15
    Given I want to configure GlobalSettings parameters using ${Details} for ${phone1}
    Then Register the ${phone1} on ${Asterisk} pbx
    &{sipmessagedetail} =  Create Dictionary    sip_message=REGISTER      sip_message_value=
    Then Capture the ${outgoing} packets from ${phone1} and verifiy the ${sipmessagedetail} on ${phone1}
    Then on ${phone1} wait for 10 seconds
    &{sipmessagedetail} =  Create Dictionary    sip_message=REGISTER      sip_message_value=
    And Capture the ${outgoing} packets from ${phone1} and verifiy the ${sipmessagedetail} on ${phone1}
    [Teardown]  Default Phone state

762782: Basic TC 3c:Registration Renewal timer (RRT)=20sec
    [Tags]    Owner:Aman    Reviewer:    registration   762782      Execute
    &{details}=    CREATE DICTIONARY    registrationPeriod=0    regRenewal=20
    Given I want to configure GlobalSettings parameters using ${Details} for ${phone1}
    Then unregister the ${phone1} from ${MxOne} pbx
    Then Register the ${phone1} on ${MxOne} pbx
    &{sipmessagedetail} =  Create Dictionary    sip_message=REGISTER      sip_message_value=
    Then Capture the ${outgoing} packets from ${phone1} and verifiy the ${sipmessagedetail} on ${phone1}
    &{details}=    CREATE DICTIONARY    registrationPeriod=40
    Then I want to configure Line1 parameters using ${details} for ${phone1}
    Then on ${phone1} wait for 20 seconds
    &{sipmessagedetail} =  Create Dictionary    sip_message=REGISTER      sip_message_value=
    Then Capture the ${outgoing} packets from ${phone1} and verifiy the ${sipmessagedetail} on ${phone1}
    &{details}=    CREATE DICTIONARY    registrationPeriod=0
    Then I want to configure Line1 parameters using ${details} for ${phone1}
    [Teardown]  Default Phone state


861958: Redial
    [Tags]    Owner:Aman    Reviewer:    redial   regressionArabicSupport
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then on ${phone1} wait for 3 seconds
    Then press hardkey as ${goodBye} on ${phone1}
    Then press hardkey as ${redial} on ${phone1}
    Then on ${phone1} wait for 2 seconds
    Then on ${phone1} verify display message ${callHistory_ar}
    Then on ${phone1} press ${hardKey} ${scrollRight} for 1 times
    Then on ${phone1} verify display message ${dial_ar}
    And press hardkey as ${goodBye} on ${phone1}

861959: Call History
    [Tags]    Owner:Aman    Reviewer:    callHistory   regressionArabicSupport
    Given press hardkey as ${callersList} on ${phone1}
    Then on ${phone1} wait for 3 seconds
    Then on ${phone1} verify display message ${callHistory_ar}
    And press hardkey as ${goodBye} on ${phone1}

861916: Time and date_Settings
    [Tags]    Owner:Aman    Reviewer:    time    regressionArabicSupport
    Given Press hardkey as ${menu} on ${phone1}
    Then on ${phone1} press ${hardKey} ${scrollLeft} for 4 times
    Then On ${phone1} verify display message ${timeAndDate_ar}
    Then On ${phone1} verify display message ${settings_ar}
    Then press hardkey as ${enter} on ${phone1}
    Then On ${phone1} verify display message ${timeFormat_ar}
    Then On ${phone1} verify display message ﺔﻋﺎﺳ12    # Verifying '12 Hour'
    Then On ${phone1} verify display message ﺔﻋﺎﺳ24    # Verifying '24 Hour'
    Then on ${phone1} press ${hardKey} ${scrollDown} for 1 times
    Then On ${phone1} verify display message ${daylightSavings_ar}
    Then On ${phone1} verify display message ﻖﻠﻐﻣ    # Verifying 'Off'
    Then On ${phone1} verify display message ﻲﻔﻴﺻ ﺔﻘﻴﻗﺩ30    # Verifying '30min summertime'
    Then On ${phone1} verify display message ﻲﻔﻴﺻ ﺔﻋﺎﺳ    # Verifying '1h summertime'
    Then On ${phone1} verify display message ﻲﺋﺎﻘﻠﺗ    # Verifying 'Automatic'
    Then on ${phone1} press ${hardKey} ${scrollDown} for 1 times
    Then On ${phone1} verify display message ${dateFormat_ar}
    Then On ${phone1} verify display message YYYY-MM-DD    # Verifying 'YYYY-MM-DD'
    And Press hardkey as ${goodBye} on ${phone1}

861935: Verify Bluetooth_DUT 6930
    [Tags]    Owner:Aman    Reviewer:    bluetooth    regressionArabicSupport    notApplicableFor6920    notApplicableFor6910
    Given Press hardkey as ${menu} on ${phone1}
    Then on ${phone1} press ${hardKey} ${scrollRight} for 1 times
    Then On ${phone1} verify display message ${bluetooth_ar}
    Then on ${phone1} press ${hardKey} ${enter} for 1 times
    Then On ${phone1} verify display message ${bluetooth_ar}
    Then On ${phone1} verify display message ${turnOn_ar}
    Then On ${phone1} verify display message ${close_ar}
    Then on ${phone1} press ${softKey} ${bottomKey1} for 1 times
    Then On ${phone1} verify display message ${enableBluetooth_ar}
    Then On ${phone1} verify display message ${pairedDevices_ar}
    Then On ${phone1} verify display message ${availableDevices_ar}
    Then On ${phone1} verify display message ${turnOff_ar}
    Then on ${phone1} press ${softKey} ${bottomKey1} for 1 times
    Then on ${phone1} Wait for 2 seconds
    Then On ${phone1} verify display message ${turnOn_ar}
    And press hardkey as ${goodBye} on ${phone1}

861967: Call Conference
    [Tags]    Owner:Aman        Reviewer:       conference    regressionArabicSupport
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then on ${phone2} wait for 2 seconds
    Then on ${phone2} press the softkey ${answer} in RingingState
    Then On ${phone2} verify display message ${drop_ar}
    Then on ${phone1} press the softkey ${conference} in AnswerState
    Then on ${phone1} enter number ${phone3}
    Then on ${phone1} press the softkey ${consult} in ConferenceCallState
    Then on ${phone3} wait for 2 seconds
    Then on ${phone3} press the softkey ${answer} in RingingState
    Then On ${phone3} verify display message ${drop_ar}
    Then on ${phone3} wait for 2 seconds
    Then on ${phone1} press the softkey ${conference} in AnswerState
    Then conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then I want to make a two party call between ${phone1} and ${phone4} using ${programKey2}
    Then on ${phone4} wait for 2 seconds
    Then on ${phone4} press the softkey ${answer} in RingingState
    Then On ${phone4} verify display message ${drop_ar}
    Then on ${phone1} press the softkey ${conference} in AnswerState
    Then i want to press line key ${programKey1} on phone ${phone1}
    Then Four party Conference call audio verification between ${phone1} ${phone2} ${phone3} and ${phone4}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone3}
    And disconnect the call from ${phone4}

861934: Verify_Restart
    [Tags]    Owner:Aman    Reviewer:    restart    regressionArabicSupport
    Given Press hardkey as ${menu} on ${phone1}
    Then on ${phone1} press ${hardKey} ${scrollRight} for 6 times
    Then On ${phone1} verify display message ${restart_ar}
    Then on ${phone1} press ${hardKey} ${enter} for 1 times
    Then On ${phone1} verify display message ${yes_ar}
    Then On ${phone1} verify display message ${no_ar}
    Then on ${phone1} press ${hardKey} ${enter} for 1 times
    Then On ${phone1} verify display message ${restart_ar}
    Then press hardkey as ${goodBye} on ${phone1}
    Then Reboot ${phone1}
    And verify extension number of ${phone1} on ${phone1}

862080: Verify wether.xml with Arabic Character
    [Tags]    Owner:Aman    Reviewer:    XML    regressionArabicSupport     862080
    &{configurationDetails}=    CREATE DICTIONARY    collapsed softkey screen=0    topsoftkey3 type=xml    topsoftkey3 label=Arabic XML
                               ...  topsoftkey3 value=http://10.112.123.89/XML/DesktopXML/Misc/weather_arabic.xml
    Given configure parameters on ${phone1} using ${configurationDetails}
    Then i want to press line key ${programKey3} on phone ${phone1}
    Then On ${phone1} verify display message ﺲﻘﻄﻟا ﺭﺎﺒﺧﺃ
    Then On ${phone1} verify display message ﺔﻠﻴﻠﻗ ﻡﻮﻴﻏ ﻊﻣ ﺲﻤﺸﻟا ﺔﻌﺷﺃ :ﻡﻮﻴﻟا
    Then Press hardkey as ${goodBye} on ${phone1}
    [Teardown]  And I want to program ${none} key on position 3 on ${phone1}

862082: Configured_Action URI_Off Hook
    [Tags]    Owner:Aman    Reviewer:    actionURI    regressionArabicSupport
    &{details}=    CREATE DICTIONARY    offhookField=http://10.112.123.89/XML/DesktopXML/Misc/weather_arabic.xml
    Given Using ${PhoneWUI} log into ${phone1} URL
    Then I want to configure ActionUrl parameters using ${details} for ${phone1}
    Then Press hookMode ${offHook} on phone ${phone1}
    Then On ${phone1} verify display message ﺲﻘﻄﻟا ﺭﺎﺒﺧﺃ
    Then On ${phone1} verify display message ﺔﻠﻴﻠﻗ ﻡﻮﻴﻏ ﻊﻣ ﺲﻤﺸﻟا ﺔﻌﺷﺃ :ﻡﻮﻴﻟا
    And Press hardkey as ${goodBye} on ${phone1}
    [Teardown]  Default ActionURI Configuration

862109: Blind Xfer
    [Tags]    Owner:Aman    Reviewer:    transfer    regressionArabicSupport
    Given i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then on ${phone1} wait for 2 seconds
    Then on ${phone1} press the softkey ${answer} in RingingState
    Then On ${phone1} verify display message ${drop_ar}
    Then on ${phone1} press the softkey ${transfer} in AnswerState
    Then on ${phone1} enter number ${phone3}
    Then on ${phone1} press the softkey ${transfer} in TransferState
    Then on ${phone1} wait for 2 seconds
    &{sipmessagedetail} =  Create Dictionary    sip_message=REFER      sip_message_value=
    Then Capture the ${outgoing} packets from ${phone1} and verifiy the ${sipmessagedetail} on ${phone1}
	Then verify the led state of ${line1} as ${blink} on ${phone3}
    Then on ${phone3} press the softkey ${answer} in RingingState
    Then on ${phone3} wait for 2 seconds
    Then verify the caller id on ${phone2} and ${phone3} display
    Then Verify audio path between ${phone2} and ${phone3}
    And disconnect the call from ${phone3}

862110: Blind Xfer - When Ringing(Semi-Attended Xfer)
    [Tags]    Owner:Aman    Reviewer:    transfer    regressionArabicSupport
    Given i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then on ${phone1} wait for 2 seconds
    Then on ${phone1} press the softkey ${answer} in RingingState
    Then On ${phone1} verify display message ${drop_ar}
    Then on ${phone1} press the softkey ${transfer} in AnswerState
    Then on ${phone1} enter number ${phone3}
    Then on ${phone1} press the softkey ${consult} in TransferState
    Then on ${phone1} wait for 4 seconds
    Then on ${phone1} press the softkey ${blindTransfer} in TransferState
    Then on ${phone1} wait for 2 seconds
	Then verify the led state of ${line1} as ${off} on ${phone1}
	Then verify the led state of ${line1} as ${blink} on ${phone3}
    &{sipmessagedetail}=  Create Dictionary    sip_message=REFER      sip_message_value=
    Then Capture the ${outgoing} packets from ${phone1} and verifiy the ${sipmessagedetail} on ${phone1}
    Then on ${phone3} press the softkey ${answer} in RingingState
    Then verify the caller id on ${phone2} and ${phone3} display
    Then Verify audio path between ${phone2} and ${phone3}
    And disconnect the call from ${phone3}

862111: Consultative Xfer(Attended Xfer)
    [Tags]    Owner:Aman    Reviewer:    transfer    regressionArabicSupport
    Given i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then on ${phone1} wait for 2 seconds
    Then on ${phone1} press the softkey ${answer} in RingingState
    Then On ${phone1} verify display message ${drop_ar}
    Then on ${phone1} press the softkey ${transfer} in AnswerState
    Then on ${phone1} enter number ${phone3}
    Then on ${phone1} press the softkey ${consult} in TransferState
    Then on ${phone3} wait for 2 seconds
    Then on ${phone3} press the softkey ${answer} in RingingState
    Then On ${phone3} verify display message ${drop_ar}
    Then Verify audio path between ${phone1} and ${phone3}
    Then on ${phone1} press the softkey ${transfer} in TransferState
    Then on ${phone1} wait for 2 seconds
	Then verify the led state of ${line1} as ${off} on ${phone1}
    &{sipmessagedetail} =  Create Dictionary    sip_message=REFER      sip_message_value=
    Then Capture the ${outgoing} packets from ${phone1} and verifiy the ${sipmessagedetail} on ${phone1}
    Then verify the caller id on ${phone2} and ${phone3} display
    Then Verify audio path between ${phone2} and ${phone3}
    And disconnect the call from ${phone3}

763351: WTDG_001
    [Tags]    Owner:Surender    Reviewer:    watchdog
    Given Using ${PhoneWUI} log into ${phone1} URL
    Then Using ${PhoneWUI} Navigate to go to ${TroubleShootingMenu} page on ${phone1} URL
    Then verify ${checkbox} is ${selected} for ${TroubleshootLink['Watchdog']}
    And Using ${PhoneWUI} logoff ${phone1} URL

763352: WTDG_003
    [Tags]    Owner:Surender    Reviewer:    watchdog
    Given Using ${PhoneWUI} log into ${phone1} URL
    Then Using ${PhoneWUI} Navigate to go to ${TroubleShootingMenu} page on ${phone1} URL
    Then verify ${checkbox} is ${selected} for ${TroubleshootLink['Watchdog']}

    Then Using ${PhoneWUI} click on the ${TroubleshootLink['Watchdog']} on ${phone1} URL
    Then verify ${checkbox} is ${unSelected} for ${TroubleshootLink['Watchdog']}

    Then Using ${PhoneWUI} click on the ${TroubleshootLink['Watchdog']} on ${phone1} URL
    Then verify ${checkbox} is ${selected} for ${TroubleshootLink['Watchdog']}

    Then Using ${PhoneWUI} click on the ${TroubleshootLink['Watchdog']} on ${phone1} URL
    And Using ${PhoneWUI} logoff ${phone1} URL

763353: WTDG_006
    [Tags]    Owner:Surender    Reviewer:    watchdog
    Given Using ${PhoneWUI} log into ${phone1} URL
    Then Using ${PhoneWUI} Navigate to go to ${TroubleShootingMenu} page on ${phone1} URL
    Then verify ${checkbox} is ${selected} for ${TroubleshootLink['Watchdog']}

    Then Using ${PhoneWUI} click on the ${TroubleshootLink['Watchdog']} on ${phone1} URL
    Then verify ${checkbox} is ${unSelected} for ${TroubleshootLink['Watchdog']}

    Then Using ${PhoneWUI} click on the ${TroubleshootLink['Watchdog']} on ${phone1} URL
    Then verify ${checkbox} is ${selected} for ${TroubleshootLink['Watchdog']}

    Then Using ${PhoneWUI} click on the ${TroubleshootLink['SaveSetting']} on ${phone1} URL
    And Using ${PhoneWUI} logoff ${phone1} URL

763354: WTDG_013
    [Tags]    Owner:Surender    Reviewer:    watchdog
    Given Using ${PhoneWUI} log into ${phone1} URL
    Then Using ${PhoneWUI} Navigate to go to ${TroubleShootingMenu} page on ${phone1} URL
    Then Using ${PhoneWUI} verify ${TroubleshootLink['CrashLog']} is present on ${phone1} URL
    Then Using ${PhoneWUI} verify ${TroubleshootLink['LogFiles']} is present on ${phone1} URL
    And Using ${PhoneWUI} logoff ${phone1} URL

763528: DSIP_002
    [Tags]    Owner:Surender    Reviewer:    lineStatus
    Given Using ${PhoneWUI} register ${Line['third']} of ${phone1} with ${phone1}
    Then Using ${PhoneWUI} verify ${Line['third']} is registered on ${phone1}
    Then Using ${PhoneWUI} ${partially} unregister ${Line['third']} of ${phone1}
    And Using ${PhoneWUI} logoff ${phone1} URL

763529: DSIP_004
    [Tags]    Owner:Surender    Reviewer:    lineStatus
    [Setup]    Default Line Registeration Setup
    Given Using ${PhoneWUI} log into ${phone1} URL
    Then Using ${PhoneWUI} ${partially} unregister ${Line['all']} of ${phone1}
    Then Using ${PhoneWUI} register ${Line['first']} of ${phone1} with ${phone1}
    Then Using ${PhoneWUI} Navigate to go to ${LineOneMenu} page on ${phone1} URL
    Then Using ${PhoneWUI} send ${TimeoutServer} value for ${ConfiguartionLine['ProxyServer']} to ${phone1} URL
    Then Using ${PhoneWUI} send ${TimeoutServer} value for ${ConfiguartionLine['OutboundProxyServer']} to ${phone1} URL
    Then Using ${PhoneWUI} send ${TimeoutServer} value for ${ConfiguartionLine['RegistrarServer']} to ${phone1} URL
    Then Using ${PhoneWUI} click on the ${ConfiguartionLine['SaveSettings']} on ${phone1} URL
    Then On ${phone1} Wait for 5 seconds
    Then Using ${PhoneWUI} Navigate to go to ${SystemInfoMenu} page on ${phone1} URL
    Then Verify text ${LineStatus['Timeout']} for ${SystemInformation['Line1Status']} on the ${phone1} URL
    Then Using ${PhoneWUI} verify ${SystemInformation['Line2Status']} is not present on ${phone1} url

    Then Using ${PhoneWUI} ${partially} unregister ${Line['first']} of ${phone1}
    Then Using ${PhoneWUI} register ${Line['all']} of ${phone1} with ${phone1}
    And Using ${PhoneWUI} logoff ${phone1} URL
    [Teardown]    Default Line Registeration Teardown

763527: DSIP_001
    [Tags]    Owner:Surender    Reviewer:    lineStatus
    Given Using ${PhoneWUI} log into ${phone1} URL
    Then Using ${PhoneWUI} ${partially} unregister ${Line['all']} of ${phone1}
    Then Using ${PhoneWUI} ${fully} unregister ${Line['second']} of ${phone1}

    Then Using ${PhoneWUI} register ${Line['first']} of ${phone1} with ${phone1}
    Then Using ${PhoneWUI} verify ${Line['first']} is registered on ${phone1}
    Then Using ${PhoneWUI} verify ${SystemInformation['Line2Status']} is not present on ${phone1} URL

    Then Using ${PhoneWUI} ${partially} unregister ${Line['first']} of ${phone1}
    Then Using ${PhoneWUI} ${partially} unregister ${Line['second']} of ${phone1}
    Then Using ${PhoneWUI} register ${Line['all']} of ${phone1} with ${phone1}
    And Using ${PhoneWUI} logoff ${phone1} URL

763530: DSIP_006
    [Tags]    Owner:Surender    Reviewer:    lineStatus
    Given Using ${PhoneWUI} log into ${phone1} URL
    Then Using ${PhoneWUI} ${partially} unregister ${Line['all']} of ${phone1}
    Then Using ${PhoneWUI} register ${Line['first']} of ${phone1} with ${phone1}
    Then Using ${PhoneWUI} register ${Line['second']} of ${phone1} with ${phone1}
    Then Using ${PhoneWUI} register ${Line['third']} of ${phone1} with ${phone1}
    Then Using ${PhoneWUI} register ${Line['fourth']} of ${phone1} with ${phone1}
    Then Using ${PhoneWUI} register ${Line['fifth']} of ${phone1} with ${phone1}
    Then Using ${PhoneWUI} register ${Line['sixth']} of ${phone1} with ${phone1}
    Then Using ${PhoneWUI} register ${Line['seventh']} of ${phone1} with ${phone1}
    Then Using ${PhoneWUI} register ${Line['eighth']} of ${phone1} with ${phone1}
    Then Using ${PhoneWUI} register ${Line['ninth']} of ${phone1} with ${phone1}

    Then Using ${PhoneWUI} Navigate to go to ${LineOneMenu} page on ${phone1} URL
    Then Using ${PhoneWUI} send ${InvalidPassword} value for ${ConfiguartionLine['Password']} to ${phone1} URL
    Then Using ${PhoneWUI} click on the ${ConfiguartionLine['SaveSettings']} on ${phone1} URL

    Then Using ${PhoneWUI} Navigate to go to ${SystemInfoMenu} page on ${phone1} URL
    Then Verify text ${LineStatus['Forbidden']} for ${SystemInformation['Line1Status']} on the ${phone1} URL
    Then Verify text ${LineStatus['Forbidden']} for ${SystemInformation['Line2Status']} on the ${phone1} URL

    Then Using ${PhoneWUI} ${partially} unregister ${Line['first']} of ${phone1}
    Then Using ${PhoneWUI} ${partially} unregister ${Line['second']} of ${phone1}
    Then Using ${PhoneWUI} ${partially} unregister ${Line['third']} of ${phone1}
    Then Using ${PhoneWUI} ${partially} unregister ${Line['fourth']} of ${phone1}
    Then Using ${PhoneWUI} ${partially} unregister ${Line['fifth']} of ${phone1}
    Then Using ${PhoneWUI} ${partially} unregister ${Line['sixth']} of ${phone1}
    Then Using ${PhoneWUI} ${partially} unregister ${Line['seventh']} of ${phone1}
    Then Using ${PhoneWUI} ${partially} unregister ${Line['eighth']} of ${phone1}
    Then Using ${PhoneWUI} ${partially} unregister ${Line['ninth']} of ${phone1}

    Then Using ${PhoneWUI} register ${Line['all']} of ${phone1} with ${phone1}
    And Using ${PhoneWUI} logoff ${phone1} URL

763531: DSIP_007
    [Tags]    Owner:Surender    Reviewer:    lineStatus
    Given Using ${PhoneWUI} log into ${phone1} URL
    Then Using ${PhoneWUI} ${partially} unregister ${Line['all']} of ${phone1}
    Then using ${PhoneWUI} register ${Line['first']} of ${phone1} with ${phone1}
    Then using ${PhoneWUI} register ${Line['second']} of ${phone1} with ${phone2}
    Then using ${PhoneWUI} register ${Line['third']} of ${phone1} with ${phone3}

    Then Using ${PhoneWUI} Navigate to go to ${LineTwoMenu} page on ${phone1} URL
    Then Using ${PhoneWUI} send ${TimeoutServer} value for ${ConfiguartionLine['ProxyServer']} to ${phone1} URL
    Then Using ${PhoneWUI} send ${TimeoutServer} value for ${ConfiguartionLine['OutboundProxyServer']} to ${phone1} URL
    Then Using ${PhoneWUI} send ${TimeoutServer} value for ${ConfiguartionLine['RegistrarServer']} to ${phone1} URL
    Then Using ${PhoneWUI} click on the ${ConfiguartionLine['SaveSettings']} on ${phone1} URL

    Then Using ${PhoneWUI} Navigate to go to ${LineThreeMenu} page on ${phone1} URL
    Then Using ${PhoneWUI} send ${InvalidPassword} value for ${ConfiguartionLine['Password']} to ${phone1} URL
    Then Using ${PhoneWUI} click on the ${ConfiguartionLine['SaveSettings']} on ${phone1} URL

    Then On ${phone1} Wait for 5 seconds
    Then Using ${PhoneWUI} Navigate to go to ${SystemInfoMenu} page on ${phone1} URL
    Then Verify text ${LineStatus['Registered']} for ${SystemInformation['Line1Status']} on the ${phone1} URL
    Then Verify text ${LineStatus['Timeout']} for ${SystemInformation['Line2Status']} on the ${phone1} URL
    Then Verify text ${LineStatus['Forbidden']} for ${SystemInformation['Line3Status']} on the ${phone1} URL

    Then Using ${PhoneWUI} ${partially} unregister ${Line['first']} of ${phone1}
    Then Using ${PhoneWUI} ${partially} unregister ${Line['second']} of ${phone1}
    Then Using ${PhoneWUI} ${partially} unregister ${Line['third']} of ${phone1}
    Then using ${PhoneWUI} register ${Line['all']} of ${phone1} with ${phone1}
    And Using ${PhoneWUI} logoff ${phone1} URL

763532: DSIP_009
    [Tags]    Owner:Surender    Reviewer:    lineStatus
    Given Using ${PhoneWUI} log into ${phone1} URL
    Then Using ${PhoneWUI} ${partially} unregister ${Line['all']} of ${phone1}
    Then Using ${PhoneWUI} register ${Line['first']} of ${phone1} with ${phone1}
    Then Using ${PhoneWUI} register ${Line['second']} of ${phone1} with ${phone2}
    Then Using ${PhoneWUI} register ${Line['third']} of ${phone1} with ${phone3}

    Then Using ${PhoneWUI} Navigate to go to ${LineOneMenu} page on ${phone1} URL
    Then Using ${PhoneWUI} send ${TimeoutServer} value for ${ConfiguartionLine['ProxyServer']} to ${phone1} URL
    Then Using ${PhoneWUI} send ${TimeoutServer} value for ${ConfiguartionLine['OutboundProxyServer']} to ${phone1} URL
    Then Using ${PhoneWUI} send ${TimeoutServer} value for ${ConfiguartionLine['RegistrarServer']} to ${phone1} URL

    Then Using ${PhoneWUI} send ${Asterisk} value for ${ConfiguartionLine['BackupProxyServer']} to ${phone1} URL
    Then Using ${PhoneWUI} send ${port} value for ${ConfiguartionLine['BackupProxyPort']} to ${phone1} URL
    Then Using ${PhoneWUI} send ${Asterisk} value for ${ConfiguartionLine['BackupOutboundProxyServer']} to ${phone1} URL
    Then Using ${PhoneWUI} send ${port} value for ${ConfiguartionLine['BackupOutboundProxyPort']} to ${phone1} URL
    Then Using ${PhoneWUI} send ${Asterisk} value for ${ConfiguartionLine['BackupRegistrarServer']} to ${phone1} URL
    Then Using ${PhoneWUI} send ${port} value for ${ConfiguartionLine['BackupRegistrarPort']} to ${phone1} URL
    Then Using ${PhoneWUI} click on the ${ConfiguartionLine['SaveSettings']} on ${phone1} URL

    Then Using ${PhoneWUI} Navigate to go to ${LineTwoMenu} page on ${phone1} URL
    Then Using ${PhoneWUI} send ${TimeoutServer} value for ${ConfiguartionLine['ProxyServer']} to ${phone1} URL
    Then Using ${PhoneWUI} send ${TimeoutServer} value for ${ConfiguartionLine['OutboundProxyServer']} to ${phone1} URL
    Then Using ${PhoneWUI} send ${TimeoutServer} value for ${ConfiguartionLine['RegistrarServer']} to ${phone1} URL

    Then Using ${PhoneWUI} send ${TimeoutServer} value for ${ConfiguartionLine['BackupProxyServer']} to ${phone1} URL
    Then Using ${PhoneWUI} send ${port} value for ${ConfiguartionLine['BackupProxyPort']} to ${phone1} URL
    Then Using ${PhoneWUI} send ${TimeoutServer} value for ${ConfiguartionLine['BackupOutboundProxyServer']} to ${phone1} URL
    Then Using ${PhoneWUI} send ${port} value for ${ConfiguartionLine['BackupOutboundProxyPort']} to ${phone1} URL
    Then Using ${PhoneWUI} send ${TimeoutServer} value for ${ConfiguartionLine['BackupRegistrarServer']} to ${phone1} URL
    Then Using ${PhoneWUI} send ${port} value for ${ConfiguartionLine['BackupRegistrarPort']} to ${phone1} URL
    Then Using ${PhoneWUI} click on the ${ConfiguartionLine['SaveSettings']} on ${phone1} URL

    Then Using ${PhoneWUI} Navigate to go to ${LineThreeMenu} page on ${phone1} URL
    Then Using ${PhoneWUI} send ${InvalidPassword} value for ${ConfiguartionLine['Password']} to ${phone1} URL
    Then Using ${PhoneWUI} send ${TimeoutServer} value for ${ConfiguartionLine['ProxyServer']} to ${phone1} URL
    Then Using ${PhoneWUI} send ${TimeoutServer} value for ${ConfiguartionLine['OutboundProxyServer']} to ${phone1} URL
    Then Using ${PhoneWUI} send ${TimeoutServer} value for ${ConfiguartionLine['RegistrarServer']} to ${phone1} URL

    Then Using ${PhoneWUI} send ${Asterisk} value for ${ConfiguartionLine['BackupProxyServer']} to ${phone1} URL
    Then Using ${PhoneWUI} send ${port} value for ${ConfiguartionLine['BackupProxyPort']} to ${phone1} URL
    Then Using ${PhoneWUI} send ${Asterisk} value for ${ConfiguartionLine['BackupOutboundProxyServer']} to ${phone1} URL
    Then Using ${PhoneWUI} send ${port} value for ${ConfiguartionLine['BackupOutboundProxyPort']} to ${phone1} URL
    Then Using ${PhoneWUI} send ${Asterisk} value for ${ConfiguartionLine['BackupRegistrarServer']} to ${phone1} URL
    Then Using ${PhoneWUI} send ${port} value for ${ConfiguartionLine['BackupRegistrarPort']} to ${phone1} URL
    Then Using ${PhoneWUI} click on the ${ConfiguartionLine['SaveSettings']} on ${phone1} URL

    Then On ${phone1} Wait for 5 seconds
    Then Using ${PhoneWUI} Navigate to go to ${SystemInfoMenu} page on ${phone1} URL
    Then Verify text ${LineStatus['Registered']} for ${SystemInformation['Line1Status']} on the ${phone1} URL
    Then Verify text ${LineStatus['Timeout']} for ${SystemInformation['Line2Status']} on the ${phone1} URL
    Then Verify text ${LineStatus['Forbidden']} for ${SystemInformation['Line3Status']} on the ${phone1} URL

    Then Using ${PhoneWUI} ${partially} unregister ${Line['first']} of ${phone1}
    Then Using ${PhoneWUI} ${partially} unregister ${Line['second']} of ${phone1}
    Then Using ${PhoneWUI} ${partially} unregister ${Line['third']} of ${phone1}

    Then Using ${PhoneWUI} register ${Line['all']} of ${phone1} with ${phone1}
    And Using ${PhoneWUI} logoff ${phone1} URL

763533: DSIP_012
    [Tags]    Owner:Surender    Reviewer:    lineStatus
    Given Using ${PhoneWUI} log into ${phone1} URL
    Then Using ${PhoneWUI} Navigate to go to ${GlobalSIPMenu} page on ${phone1} URL
    Then Go to the ${GlobalSIP['TransportProtocol']} option and select the ${TLS} value
    Then Using ${PhoneWUI} click on the ${GlobalSIP['SaveSettings']} on ${phone1} URL
    Then Using ${PhoneWUI} logoff ${phone1} URL
    Then Reboot ${phone1}

    Then Using ${PhoneWUI} log into ${phone1} URL
    Then Using ${PhoneWUI} Navigate to go to ${SystemInfoMenu} page on ${phone1} URL
    Then Verify text ${LineStatus['ServiceUnavailable']} for ${SystemInformation['Line1Status']} on the ${phone1} URL
    Then Verify text ${LineStatus['ServiceUnavailable']} for ${SystemInformation['Line2Status']} on the ${phone1} URL

    Then Using ${PhoneWUI} Navigate to go to ${GlobalSIPMenu} page on ${phone1} URL
    Then Go to the ${GlobalSIP['TransportProtocol']} option and select the ${UDP} value
    Then Using ${PhoneWUI} click on the ${GlobalSIP['SaveSettings']} on ${phone1} URL
    Then Using ${PhoneWUI} logoff ${phone1} URL
    And Reboot ${phone1}


# Support for WebUI Access and Lockup feature Ver10.0
763106: TC_02
    [Tags]    Owner:Surender    Reviewer:    lockUI
    Given Using ${PhoneWUI} log into ${phone1} URL with ${wrongPassword}
    Then Using ${PhoneWUI} verify ${SystemInformation['Title']} is not present on ${phone1} URL
    Then Using ${PhoneWUI} verify ${PageTitle['Forbidden']} is not present on ${phone1} URL
    Then Close the browser window

    Then Using ${PhoneWUI} log into ${phone1} URL with ${wrongPassword}
    Then Using ${PhoneWUI} verify ${SystemInformation['Title']} is not present on ${phone1} URL
    Then Using ${PhoneWUI} verify ${PageTitle['Forbidden']} is not present on ${phone1} URL
    Then Close the browser window

    Then Using ${PhoneWUI} log into ${phone1} URL with ${wrongPassword}
    Then Using ${PhoneWUI} verify ${SystemInformation['Title']} is not present on ${phone1} URL
    Then Using ${PhoneWUI} verify ${PageTitle['Forbidden']} is not present on ${phone1} URL
    Then Close the browser window

    Then Using ${PhoneWUI} log into ${phone1} URL with ${wrongPassword}
    Then Using ${PhoneWUI} verify ${SystemInformation['Title']} is not present on ${phone1} URL
    Then Using ${PhoneWUI} verify ${PageTitle['Forbidden']} is not present on ${phone1} URL
    Then Close the browser window

    Then Using ${PhoneWUI} log into ${phone1} URL with ${wrongPassword}
    Then Using ${PhoneWUI} verify ${SystemInformation['Title']} is not present on ${phone1} URL
    Then Using ${PhoneWUI} verify ${PageTitle['Forbidden']} is not present on ${phone1} URL
    Then Close the browser window

    Then Using ${PhoneWUI} log into ${phone1} URL with ${wrongPassword}
    Then Using ${PhoneWUI} verify ${SystemInformation['Title']} is not present on ${phone1} URL
    Then Using ${PhoneWUI} verify ${AccessForbidden} is present on ${phone1} URL
    Then Close the browser window

    And Reboot ${phone1}

763107: TC_03
    [Tags]    Owner:Surender    Reviewer:
    Given Using ${PhoneWUI} log into ${phone1} URL with ${wrongPassword}
    Then Using ${PhoneWUI} verify ${SystemInformation['Title']} is not present on ${phone1} URL
    Then Using ${PhoneWUI} verify ${PageTitle['Forbidden']} is not present on ${phone1} URL
    Then Close the browser window

    Then Using ${PhoneWUI} log into ${phone1} URL with ${wrongPassword}
    Then Using ${PhoneWUI} verify ${SystemInformation['Title']} is not present on ${phone1} URL
    Then Using ${PhoneWUI} verify ${PageTitle['Forbidden']} is not present on ${phone1} URL
    Then Close the browser window

    Then Using ${PhoneWUI} log into ${phone1} URL with ${wrongPassword}
    Then Using ${PhoneWUI} verify ${SystemInformation['Title']} is not present on ${phone1} URL
    Then Using ${PhoneWUI} verify ${PageTitle['Forbidden']} is not present on ${phone1} URL
    Then Close the browser window

    Then Using ${PhoneWUI} log into ${phone1} URL with ${wrongPassword}
    Then Using ${PhoneWUI} verify ${SystemInformation['Title']} is not present on ${phone1} URL
    Then Using ${PhoneWUI} verify ${PageTitle['Forbidden']} is not present on ${phone1} URL
    Then Close the browser window

    Then Using ${PhoneWUI} log into ${phone1} URL with ${wrongPassword}
    Then Using ${PhoneWUI} verify ${SystemInformation['Title']} is not present on ${phone1} URL
    Then Using ${PhoneWUI} verify ${PageTitle['Forbidden']} is not present on ${phone1} URL
    Then Close the browser window

    Then Using ${PhoneWUI} log into ${phone1} URL with ${wrongPassword}
    Then Using ${PhoneWUI} verify ${SystemInformation['Title']} is not present on ${phone1} URL
    Then Using ${PhoneWUI} verify ${AccessForbidden} is present on ${phone1} URL
    Then Close the browser window

    Then On ${phone1} wait for 65 seconds
    Then Using ${PhoneWUI} log into ${phone1} URL
    Then Using ${PhoneWUI} verify ${SystemInformation['Title']} is present on ${phone1} URL
    Then Close the browser window

763109: TC_34
    [Tags]    Owner:Surender    Reviewer:
    Given Using ${PhoneWUI} log into ${phone1} URL
    Then Using ${PhoneWUI} verify ${SystemInformation['Title']} is present on ${phone1} URL
    Then Using ${PhoneWUI} logoff ${phone1} URL

    &{configurationDetails}=  CREATE DICTIONARY    secure web service=1
    Given Configure parameters on ${phone1} using ${configurationDetails}
    Then Reboot ${phone1}
    Then Using ${PhoneWUI} log into ${phone} URL
    Then Using ${PhoneWUI} verify ${SystemInformation['Title']} is not present on ${phone1} URL
    &{configurationDetails}=  CREATE DICTIONARY    secure web service=0
    Then Configure parameters on ${phone1} using ${configurationDetails}
    And Reboot ${phone1}

#Branding Feature v10.0
762128: Brand_061
    [Tags]    Owner:Surender    Reviewer:
    Given Using ${PhoneWUI} log into ${phone1} URL
    Then Verify PhoneModel of ${phone1} for ${SystemInformation['PhoneModel']} on the ${phone1} URL
    And Using ${PhoneWUI} logoff ${phone1} URL

762129: Brand_063
    [Tags]    Owner:Surender    Reviewer:
    Given Using ${PhoneWUI} log into ${phone1} URL
    Then Using ${PhoneWUI} click on the ${SystemInformation['MitelLogo']} on ${phone1} URL
    Then Verify ${URL['mitel']} opened on the browser window
    And Using ${PhoneWUI} logoff ${phone1} URL

763110: TC_35
    [Tags]    Owner:Surender    Reviewer:
    Given Using ${PhoneWUI} log securely into ${phone1} URL
    Then Using ${PhoneWUI} verify ${SystemInformation['Title']} is present on ${phone1} URL
    Then Using ${PhoneWUI} logoff ${phone1} URL

    &{configurationDetails}=  CREATE DICTIONARY    secure web service=1
    Given Configure parameters on ${phone1} using ${configurationDetails}
    Then Reboot ${phone1}
    Then Using ${PhoneWUI} log into ${phone} URL
    Then Using ${PhoneWUI} verify ${SystemInformation['Title']} is not present on ${phone1} URL
    &{configurationDetails}=  CREATE DICTIONARY    secure web service=0
    Then Configure parameters on ${phone1} using ${configurationDetails}
    And Reboot ${phone1}

763108: TC_25
    [Tags]    Owner:Surender     Reviewer:
    Given Using ${PhoneWUI} log securely into ${phone1} URL
    Then Using ${PhoneWUI} verify ${SystemInformation['Title']} is present on ${phone1} URL
    And Using ${PhoneWUI} logoff ${phone1} URL

    # logging in with user account
    Then Using ${PhoneWUI} log securely into ${phone1} URL with ${user} user
    Then Using ${PhoneWUI} verify ${SystemInformation['Title']} is present on ${phone1} URL
    And Using ${PhoneWUI} logoff ${phone1} URL


763151: TC-04 tcpdump file can be displayed by wireshark.
    [Tags]    Owner:Surender    Reviewer:    testing    packetsverification
    Given Using ${PhoneWUI} log into ${phone1} URL
    Then Using ${PhoneWUI} start the capture on all port on ${phone1} URL
    Then Using ${PhoneWUI} ${stop} the capture from ${phone1} URL
    Then Using ${PhoneWUI} ${download} the capture from ${phone1} URL
    Then Verify the captureFile.pcap file is downloaded
    Then Using ${PhoneWUI} logoff ${phone1} URL

763152: TC-07 the tcpdump can capture incoming and outgoing traffic
    [Tags]      Owner:Surender    Reviewer:    packetVerification_sip
    Given Using ${PhoneWUI} log into ${phone1} URL
    Then Using ${PhoneWUI} start the capture on all port on ${phone1} URL
    Then I want to make a two party call between ${phone1} and ${phone2} using ${offHook}
    Then Answer the call on ${phone2} using ${offHook}
    Then Disconnect the call from ${phone1}
    Then Using ${PhoneWUI} ${stop} the capture from ${phone1} URL
    Then Using ${PhoneWUI} ${download} the capture from ${phone1} URL
    Then Verify the ${sip} packets in the Capture File of ${phone1}
    Then Using ${PhoneWUI} logoff ${phone1} URL

763153: TC-12 the filter range symbol ":"
    [Tags]    Owner:Surender    Reviewer:    packetsVerification_multiple
    Given Using ${PhoneWUI} log into ${phone1} URL
    Then Using ${PhoneWUI} Start the capture on 1:5060 port on ${phone1} URL
    # http traffic
    Then On ${phone1} program ${blf} key on position 4 with ${phone2} value
    Then I want to program ${none} key on position 4 on ${phone1}
    # SIP traffic
    Then I want to make a two party call between ${phone1} and ${phone2} using ${offHook}
    Then Answer the call on ${phone2} using ${offHook}
    Then Disconnect the call from ${phone1}

    Then Using ${PhoneWUI} ${stop} the capture from ${phone1} URL
    Then Using ${PhoneWUI} ${download} the capture from ${phone1} URL
    Then Verify the ${sip} packets in the Capture File of ${phone1}
    Then Verify the ${http} packets in the Capture File of ${phone1}
    Then Verify the ${telnet} packets in the Capture File of ${phone1}
    And Using ${PhoneWUI} logoff ${phone1} URL


763154: TC-13 the filter range symbol "-"
    [Tags]    Owner:Surender    Reviewer:    packetsVerification_multiple
    Given Using ${PhoneWUI} log into ${phone1} URL
    Then Using ${PhoneWUI} Start the capture on 1-5060 port on ${phone1} URL

    Then On ${phone1} program ${blf} key on position 4 with ${phone2} value
    Then I want to program ${none} key on position 4 on ${phone1}

    Then I want to make a two party call between ${phone1} and ${phone2} using ${offHook}
    Then Answer the call on ${phone2} using ${offHook}
    Then Disconnect the call from ${phone1}

    Then Using ${PhoneWUI} ${stop} the capture from ${phone1} URL
    Then Using ${PhoneWUI} ${download} the capture from ${phone1} URL
    Then Verify the ${sip} packets in the Capture File of ${phone1}
    Then Verify the ${http} packets in the Capture File of ${phone1}
    Then Verify the ${telnet} packets in the Capture File of ${phone1}
    And Using ${PhoneWUI} logoff ${phone1} URL


763155: TC-14 the filter add multiple symbol ";"
    [Tags]    Owner:Surender    Reviewer:    packetsVerification_multiple
    Given Using ${PhoneWUI} log into ${phone1} URL
    Then Using ${PhoneWUI} Start the capture on 5060;23;80 port on ${phone1} URL

    Then On ${phone1} program ${blf} key on position 4 with ${phone2} value
    Then I want to program ${none} key on position 4 on ${phone1}

    Then I want to make a two party call between ${phone1} and ${phone2} using ${offHook}
    Then Answer the call on ${phone2} using ${offHook}
    Then Disconnect the call from ${phone1}

    Then Using ${PhoneWUI} ${stop} the capture from ${phone1} URL
    Then Using ${PhoneWUI} ${download} the capture from ${phone1} URL
    Then Verify the ${sip} packets in the Capture File of ${phone1}
    Then Verify the ${http} packets in the Capture File of ${phone1}
    Then Verify the ${telnet} packets in the Capture File of ${phone1}
    And Using ${PhoneWUI} logoff ${phone1} URL


763156: TC-15 Capture automatically stop after time out
    [Tags]    Owner:Surender    Reviewer:    captureStartStopVerification
    Given Using ${PhoneWUI} log into ${phone1} URL
    Then Using ${PhoneWUI} Start the capture on ${default} port with 1 hours timeout on ${phone1} URL
    Then Using ${PhoneWUI} logoff ${phone1} URL

    Then Using ${PhoneWUI} log into ${phone1} URL
    Then Using ${PhoneWUI} Navigate to go to ${CaptureMenu} page on ${phone1} URL
    Then Verify text ${stop} for ${CaptureLink['Stop']} on the ${phone1} URL
    Then Using ${PhoneWUI} logoff ${phone1} URL

762534: LLDP_005
    [Tags]    Owner:Surender    Reviewer:    lldp_disable
    Given Using ${PhoneWUI} log into ${phone1} URL
    Then Using ${PhoneWUI} Navigate to go to ${NetworkMenu} page on ${phone1} URL
    Then Using ${PhoneWUI} click on the ${NetworkLink['LLDP']} on ${phone1} URL
    Then Using ${PhoneWUI} click on the ${NetworkLink['SaveSettings']} on ${phone1} URL
    Then Using ${PhoneWUI} Navigate to go to ${NetworkMenu} page on ${phone1} URL
    Then Verify ${checkbox} is ${unChecked} for ${NetworkLink['LLDP']}
    # Reverting the changes
    Then Using ${PhoneWUI} click on the ${NetworkLink['LLDP']} on ${phone1} URL
    Then Using ${PhoneWUI} click on the ${NetworkLink['SaveSettings']} on ${phone1} URL
    Then Using ${PhoneWUI} logoff ${phone1} URL

762535: LLDP_007
    [Tags]    Owner:Surender    Reviewer:    lldp_interval
    Given Using ${PhoneWUI} log into ${phone1} URL
    Then Using ${PhoneWUI} Navigate to go to ${NetworkMenu} page on ${phone1} URL
    Then Verify text 30 for ${NetworkLink['LLDPPacketInterval']} on the ${phone1} URL
    Then Using ${PhoneWUI} logoff ${phone1} URL

762565: Lock-Param 02
    [Tags]    Owner:Surender    Reviewer:    lockParameter
    &{configurationDetails}=    CREATE DICTIONARY    topsoftkey4 type=blf    topsoftkey4 value=${phone2}
    ...                                              topsoftkey4 label=BLF
    Given Configure parameters on ${phone1} using ${configurationDetails}

    &{configurationDetails}=    CREATE DICTIONARY    topsoftkey4 locked=1
    Then Configure parameters on ${phone1} using ${configurationDetails}

    Then Using ${PhoneWUI} log into ${phone1} URL
    Then Using ${PhoneWUI} Navigate to go to ${SoftkeysAndXMLMenu} page on ${phone1} URL
    Then Using ${PhoneWUI} Navigate to go to ${TopSoftKeyMenu} page on ${phone1} URL
    Then Verify ${TopsoftKeyLink['TopSoftkey4Type']} is not clickable on the ${phone1} URL

    &{configurationDetails}=    CREATE DICTIONARY    topsoftkey4 locked=0
    Then Configure parameters on ${phone1} using ${configurationDetails}

    &{configurationDetails}=    CREATE DICTIONARY    topsoftkey4 type=none    topsoftkey4 value=
    ...                                              topsoftkey4 label=
    And Configure parameters on ${phone1} using ${configurationDetails}


762566: Lock-Param 04
    [Tags]    Owner:Surender    Reviewer:    lockParameter
    &{configurationDetails}=    CREATE DICTIONARY    topsoftkey4 type=blf    topsoftkey4 value=${phone2}
    ...                                              topsoftkey4 label=BLF
    Given Configure parameters on ${phone1} using ${configurationDetails}

    &{configurationDetails}=    CREATE DICTIONARY    topsoftkey4 locked=1
    Then Configure parameters on ${phone1} using ${configurationDetails}

    Then Using ${PhoneWUI} log into ${phone1} URL
    Then Using ${PhoneWUI} Navigate to go to ${SoftkeysAndXMLMenu} page on ${phone1} URL
    Then Using ${PhoneWUI} Navigate to go to ${TopSoftKeyMenu} page on ${phone1} URL
    Then Verify ${TopsoftKeyLink['TopSoftkey4Type']} is not clickable on the ${phone1} URL

    &{configurationDetails}=    CREATE DICTIONARY    topsoftkey4 locked=0
    Then Configure parameters on ${phone1} using ${configurationDetails}

    &{configurationDetails}=    CREATE DICTIONARY    topsoftkey4 type=none    topsoftkey4 value=
    ...                                              topsoftkey4 label=
    And Configure parameters on ${phone1} using ${configurationDetails}

766629: Enable "log issue" and "audio diagnostic" via startup.cfg
    [Tags]    Owner:Surender    Reviewer:    confgupdate    onlyApplicableFor5.1
    &{parameters}=    CREATE DICTIONARY    log issue=1    audio diagnostics=1
    Given Create startup.cfg file using ${parameters}
    Then Create ${configurationFolder} folder on FTP server
    Then Send startup.cfg file to ${configurationFolder} folder on FTP server
    &{configurationDetails}=    CREATE DICTIONARY    download protocol=FTP    ftp server=10.112.123.107
    ...                         ftp path=${configurationFolderPath}    ftp username=desktop    ftp password=desktop
    Then Configure parameters on ${phone1} using ${configurationDetails}
    Then Reboot ${phone1}
    Then Press hardkey as ${menu} on ${phone1}
    Then On ${phone1} verify display message ${logIssue}
    Then Press hardkey as ${goodBye} on ${phone1}
    Then on ${phone1} navigate to ${diagnostics} settings
    Then On ${phone1} verify display message ${diagnostics}
    And Press hardkey as ${goodBye} on ${phone1}

763832: Configure 12th softkey_Long Label Name_Bottom Softkey
    [Tags]    Owner:Surender    Reviewer:
    &{parameters}=    CREATE DICTIONARY    topsoftkey4 type=blf    topsoftkey4 value=${phone2}
    ...                                    topsoftkey4 label=${blf}@763832
    Given Create aastra.cfg file using ${parameters}
    Then Create ${configurationFolder} folder on FTP server
    Then Send aastra.cfg file to ${configurationFolder} folder on FTP server
    &{configurationDetails}=    CREATE DICTIONARY    download protocol=FTP    ftp server=10.112.123.107
    ...                         ftp path=${configurationFolderPath}    ftp username=desktop    ftp password=desktop
    Then Configure parameters on ${phone1} using ${configurationDetails}
    Then Reboot ${phone1}
    Then On ${phone1} verify display message ${blf}@763832
    Then Using ${PhoneWUI} log into ${phone1} URL
    Then Using ${PhoneWUI} Navigate to go to ${SoftkeysAndXMLMenu} page on ${phone1} URL
    Then Using ${PhoneWUI} Navigate to go to ${TopSoftKeyMenu} page on ${phone1} URL
    Then Verify ${TopsoftKeyLink['TopSoftkey4Type']} is clickable on the ${phone1} URL
    Then Using ${PhoneWUI} logoff ${phone1} URL
    Then I want to make a two party call between ${phone3} and ${phone2} using ${offHook}
    Then Verify the led state of ${line4} as ${blink} on ${phone1}
    Then Disconnect the call from ${phone3}
    &{configurationDetails}=    CREATE DICTIONARY    topsoftkey4 type=none    topsoftkey4 value=
    ...                                              topsoftkey4 label=
    And Configure parameters on ${phone1} using ${configurationDetails}

766678: TC001: Set log issue:1 in config file
    [Tags]    Owner:Surender    Reviewer:    logIssue    onlyApplicableFor5.1
    &{parameters}=    CREATE DICTIONARY    log issue=1
    Given Create startup.cfg file using ${parameters}
    Then Create ${configurationFolder} folder on FTP server
    Then Send startup.cfg file to ${configurationFolder} folder on FTP server
    &{configurationDetails}=    CREATE DICTIONARY    download protocol=FTP    ftp server=10.112.123.107
    ...                         ftp path=${configurationFolderPath}    ftp username=desktop    ftp password=desktop
    Then Configure parameters on ${phone1} using ${configurationDetails}
    Then Reboot ${phone1}
    Then Using ${PhoneWUI} log into ${phone1} URL
    Then Using ${PhoneWUI} Navigate to go to ${TroubleShootingMenu} page on ${phone1} URL
    Then Verify text 65535 for ${TroubleshootLink['LINEMGR']} on the ${phone1} URL
    Then Verify text 65535 for ${TroubleshootLink['UI']} on the ${phone1} URL
    Then Verify text 65535 for ${TroubleshootLink['MISC']} on the ${phone1} URL
    Then Verify text 65535 for ${TroubleshootLink['PROVI']} on the ${phone1} URL
    Then Verify text 1 for ${TroubleshootLink['SIP']} on the ${phone1} URL
    Then Verify text 1 for ${TroubleshootLink['DIS']} on the ${phone1} URL
    &{parameters}=    CREATE DICTIONARY
    Given Create startup.cfg file using ${parameters}
    Then Create ${configurationFolder} folder on FTP server
    Then Send startup.cfg file to ${configurationFolder} folder on FTP server
    Then Reboot ${phone1}

766680: TC003: Set log issue:0
# ENTA-4764, DTP-55257
    [Tags]    Owner:Surender    Reviewer:    logIssue    onlyApplicableFor5.1
    &{parameters}=    CREATE DICTIONARY    log issue=0
    Given Create startup.cfg file using ${parameters}
    Then Create ${configurationFolder} folder on FTP server
    Then Send startup.cfg file to ${configurationFolder} folder on FTP server
    &{configurationDetails}=    CREATE DICTIONARY    download protocol=FTP    ftp server=10.112.123.107
    ...                         ftp path=${configurationFolderPath}    ftp username=desktop    ftp password=desktop
    Then Configure parameters on ${phone1} using ${configurationDetails}
    Then Reboot ${phone1}
    Then Using ${PhoneWUI} log into ${phone1} URL
    Then Using ${PhoneWUI} Navigate to go to ${TroubleShootingMenu} page on ${phone1} URL
    Then Verify text 1 for ${TroubleshootLink['LINEMGR']} on the ${phone1} URL
    Then Verify text 1 for ${TroubleshootLink['UI']} on the ${phone1} URL
    Then Verify text 1 for ${TroubleshootLink['MISC']} on the ${phone1} URL
    Then Verify text 1 for ${TroubleshootLink['PROVI']} on the ${phone1} URL
    Then Verify text 1 for ${TroubleshootLink['SIP']} on the ${phone1} URL
    Then Verify text 1 for ${TroubleshootLink['DIS']} on the ${phone1} URL
    &{parameters}=    CREATE DICTIONARY
    Given Create startup.cfg file using ${parameters}
    Then Create ${configurationFolder} folder on FTP server
    Then Send startup.cfg file to ${configurationFolder} folder on FTP server
    Then Reboot ${phone1}


766630: Enable "log issue" and disable "audio diagnostic" via startup.cfg
    [Tags]    Owner:Surender    Reviewer:    startupConf    onlyApplicableFor5.1
    &{parameters}=    CREATE DICTIONARY    log issue=1    audio diagnostics=0
    Given Create startup.cfg file using ${parameters}
    Then Create ${configurationFolder} folder on FTP server
    Then Send startup.cfg file to ${configurationFolder} folder on FTP server
    &{configurationDetails}=    CREATE DICTIONARY    download protocol=FTP    ftp server=10.112.123.107
    ...                         ftp path=${configurationFolderPath}    ftp username=desktop    ftp password=desktop
    Then Configure parameters on ${phone1} using ${configurationDetails}
    Then Reboot ${phone1}
    Then On ${phone1} navigate to ${diagnostics} settings
    Then I want to verify on ${phone1} negative display message ${diagnostics}
    &{configurationDetails}=    CREATE DICTIONARY    download protocol=TFTP    ftp server=10.112.95.41
    Then Configure parameters on ${phone1} using ${configurationDetails}
    And Reboot ${phone1}


766669: Check "Time Zone" in phone TUI
    [Tags]    Owner:Surender    Reviewer:    timeZone
    Given on ${phone1} navigate to ${timeZone} settings
    Then Verify ${in} time zone is present under ${asia} in time zone settings of ${phone1}
    And Press hardkey as ${goodBye} on ${phone1}


766641: Check audio logs when "audio diagnostic" enable
    [Tags]    Owner:Surender    Reviewer:    logIssue
    {parameters}=    CREATE DICTIONARY    log issue=1    audio diagnostics=1
    Given Create startup.cfg file using ${parameters}
    Then Create ${configurationFolder} folder on FTP server
    Then Send startup.cfg file to ${configurationFolder} folder on FTP server
    &{configurationDetails}=    CREATE DICTIONARY    download protocol=FTP    ftp server=10.112.123.107
    ...                         ftp path=${configurationFolderPath}    ftp username=desktop    ftp password=desktop
    Then Configure parameters on ${phone1} using ${configurationDetails}
    Then Reboot ${phone1}
    Then on ${phone1} move to ${diagnostics} to ${audioDiagnostics} settings
    Then On ${phone1} dial number 5
    Then On ${phone} press the softkey ${start} in SettingState
    Then Press hardkey as ${goodBye} on ${phone1}
    Then I want to make a two party call between ${phone1} and ${phone2} using ${offHook}
    Then Answer the call on ${phone2} using ${offHook}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Disconnect the call from ${phone2}
    Then on ${phone1} navigate to ${default} settings
    Then On ${phone1} press the softkey ${logIssue} in SettingState
    Then Using ${PhoneWUI} log into ${phone1} URL
    Then Using ${PhoneWUI} Navigate to go to ${TroubleShootingMenu} page on ${phone1} URL
    Then Using ${PhoneWUI} click on the ${TroubleshootLink['Get Log Files']} on ${phone1} URL
    Then Verify the ${audioFile} file is downloaded


762777: 6731i_Redial_List_46 - outgoing calls for Conf
    [Tags]    Owner:Surender    Reviewer:    redial
    Given I want to make a two party call between ${phone1} and ${phone2} using ${offHook}
    Then Answer the call on ${phone2} using ${offHook}
    Then I want to make a conference call between ${phone1},${phone2} and ${phone3} using ${consultiveConference}
    Then Conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then Disconnect the call from ${phone1}
    Then Disconnect the call from ${phone2}
    Then Press ${none} key in Redial menu on ${phone1}
    Then On ${phone1} verify display message ${phone2}
    Then On ${phone1} verify display message ${phone3}
    Then Press ${dial} key in Redial menu on ${phone1}
    Then Verify ringing state on ${phone1} and ${phone3}
    And Disconnect the call from ${phone1}


763449: Verify the value of $$PROXYURL$$ defined in an Offhook Action URI
    [Tags]    Owner:Surender    Reviewer:    actionURI
    &{details}=    CREATE DICTIONARY    offhookField=http://10.112.123.89/XML/XML/action-uri-variables/offhook.xml?proxy-ip=$$PROXYURL$$
    Given I want to configure ActionUrl parameters using ${Details} for ${phone1}
    Then Using ${PhoneWUI} log into ${phone1} URL
    Then Using ${PhoneWUI} Start the capture on all port on ${phone1} URL
    Then Press hardkey as ${offHook} on ${phone1}
    Then Using ${PhoneWUI} ${stop} the capture from ${phone1} URL
    Then Using ${PhoneWUI} ${download} the capture from ${phone1} URL
    Then Verify the captureFile contains proxy-ip=${SystemIP} inside ${Protocols['HTTP']} packets
    &{details}=    CREATE DICTIONARY    offhookField=
    And I want to configure ActionUrl parameters using ${Details} for ${phone1}


763450: Verify Offhook Action URI is executed when Speaker/Headset button is pressed.
    [Tags]    Owner:Surender    Reviewer:    actionURI
    &{details}=    CREATE DICTIONARY    offhookField=http://10.112.123.89/XML/XML/action-uri-variables/offhook.xml?proxy-ip=$$PROXYURL$$
    Given I want to configure ActionUrl parameters using ${Details} for ${phone1}
    Then Using ${PhoneWUI} log into ${phone1} URL
    Then Using ${PhoneWUI} Start the capture on all port on ${phone1} URL
    Then Press hardkey as ${handsFree} on ${phone1}
    Then Using ${PhoneWUI} ${stop} the capture from ${phone1} URL
    Then Using ${PhoneWUI} ${download} the capture from ${phone1} URL
    Then Verify the captureFile contains proxy-ip=${SystemIP} inside ${Protocols['HTTP']} packets
    &{details}=    CREATE DICTIONARY    offhookField=
    And I want to configure ActionUrl parameters using ${Details} for ${phone1}


763451: Verify the value of $$REMOTENUMBER$$ in an Onhook Action URI
    [Tags]    Owner:Surender    Reviewer:    actionURI
    &{details}=    CREATE DICTIONARY    onHookField=http://10.112.123.89/XML/XML/action-uri-variables/offhook.xml?Remote-Number=$$REMOTENUMBER$$
    Given I want to configure ActionUrl parameters using ${Details} for ${phone1}
    Then Using ${PhoneWUI} log into ${phone1} URL
    Then Using ${PhoneWUI} Start the capture on all port on ${phone1} URL
    Then Press hardkey as ${handsFree} on ${phone1}
    Then Using ${PhoneWUI} ${stop} the capture from ${phone1} URL
    Then Using ${PhoneWUI} ${download} the capture from ${phone1} URL
    Then Verify the captureFile contains proxy-ip=${PhoneDetails['IPAddress']} inside ${Protocols['HTTP']} packets
    &{details}=    CREATE DICTIONARY    onHookField=
    And I want to configure ActionUrl parameters using ${Details} for ${phone1}


763452: Verify the value of $$CALLDURATION$$ in a Disconnected Action URI
    [Tags]    Owner:Surender    Reviewer:    actionURI
    &{details}=    CREATE DICTIONARY    disconnectedField=http://10.112.123.89/XML/XML/action-uri-variables/offhook.xml?Call-Duration=$$CALLDURATION$$
    Given I want to configure ActionUrl parameters using ${Details} for ${phone1}
    Then Using ${PhoneWUI} log into ${phone1} URL
    Then Using ${PhoneWUI} Start the capture on all port on ${phone1} URL
    Then I want to make a two party call between ${phone1} and ${phone2} using ${offHook}
    Then Answer the call on ${phone2} using ${offHook}
    Then On ${phone1} wait for 30 seconds
    Then Disconnect the call from ${phone1}
    Then Using ${PhoneWUI} ${stop} the capture from ${phone1} URL
    Then Using ${PhoneWUI} ${download} the capture from ${phone1} URL
    Then Verify the captureFile contains Call-Duration=30 inside ${Protocols['HTTP']} packets
    &{details}=    CREATE DICTIONARY    disconnectedField=
    And I want to configure ActionUrl parameters using ${Details} for ${phone1}


763454: Verify the value of variable $$ACTIVEPROXY$$ when phone is on main server
    [Tags]    Owner:Surender    Reviewer:    actionURI
    [Setup]    Default Line Registeration Setup
    &{details}=    CREATE DICTIONARY    offhookField=http://$$ACTIVEPROXY$$/weather.xml
    Given I want to configure ActionUrl parameters using ${Details} for ${phone1}
    Then Using ${PhoneWUI} log into ${phone1} URL
    Then Using ${PhoneWUI} ${fully} unregister ${Line['all']} of ${phone1}
    Then Using ${PhoneWUI} register ${Line['all']} of ${phone1} with ${phone1}
    Then Using ${PhoneWUI} Start the capture on ${all} port on ${phone1} URL
    Then Press hardkey as ${offHook} on ${phone1}
    Then Using ${PhoneWUI} ${stop} the capture from ${phone1} URL
    Then Using ${PhoneWUI} ${download} the capture from ${phone1} URL
    Then Verify the captureFile contains http://${${pbx}IP}/ inside ${Protocols['HTTP']} packets
    &{details}=    CREATE DICTIONARY    offhookField=
    And I want to configure ActionUrl parameters using ${Details} for ${phone1}
    [Teardown]    Default Line Registeration Teardown


763455: Verify the value of variable $$ACTIVEPROXY$$ when phone is on backup server
    [Tags]    Owner:Surender    Reviewer:    actionURI
    &{details}=    CREATE DICTIONARY    offhookField=http://$$ACTIVEPROXY$$/weather.xml
    Given I want to configure ActionUrl parameters using ${Details} for ${phone1}
    Then Using ${PhoneWUI} log into ${phone1} URL
    Then Using ${PhoneWUI} Navigate to go to ${GlobalSIPMenu} page on ${phone1} URL
    Then Using ${PhoneWUI} send ${defaultProxy} value for ${GlobalSIP['ProxyServer']} to ${phone1} URL
    Then Using ${PhoneWUI} send ${defaultProxy} value for ${GlobalSIP['OutboundProxyServer']} to ${phone1} URL
    Then Using ${PhoneWUI} send ${defaultProxy} value for ${GlobalSIP['RegistrarServer']} to ${phone1} URL

    Then Using ${PhoneWUI} send ${MxOneIP} value for ${GlobalSIP['BackupProxyServer']} to ${phone1} URL
    Then Using ${PhoneWUI} send ${port} value for ${GlobalSIP['BackupProxyPort']} to ${phone1} URL
    Then Using ${PhoneWUI} send ${MxOneIP} value for ${GlobalSIP['BackupOutboundProxyServer']} to ${phone1} URL
    Then Using ${PhoneWUI} send ${port} value for ${GlobalSIP['BackupOutboundProxyPort']} to ${phone1} URL
    Then Using ${PhoneWUI} send ${MxOneIP} value for ${GlobalSIP['BackupRegistrarServer']} to ${phone1} URL
    Then Using ${PhoneWUI} send ${port} value for ${GlobalSIP['BackupRegistrarPort']} to ${phone1} URL
    Then Using ${PhoneWUI} click on the ${GlobalSIP['SaveSettings']} on ${phone1} URL

    Then Using ${PhoneWUI} Start the capture on ${all} port on ${phone1} URL
    Then Press hardkey as ${offHook} on ${phone1}
    Then Using ${PhoneWUI} ${stop} the capture from ${phone1} URL
    Then Using ${PhoneWUI} ${download} the capture from ${phone1} URL
    Then Verify the captureFile contains http://${${pbx}IP} inside ${Protocols['HTTP']} packets

    Then Using ${PhoneWUI} Navigate to go to ${GlobalSIPMenu} page on ${phone1} URL
    Then Using ${PhoneWUI} send ${${pbx}IP} value for ${GlobalSIP['ProxyServer']} to ${phone1} URL
    Then Using ${PhoneWUI} send ${${pbx}IP} value for ${GlobalSIP['OutboundProxyServer']} to ${phone1} URL
    Then Using ${PhoneWUI} send ${${pbx}IP} value for ${GlobalSIP['RegistrarServer']} to ${phone1} URL

    Then Using ${PhoneWUI} send ${DefaultProxy} value for ${GlobalSIP['BackupProxyServer']} to ${phone1} URL
    Then Using ${PhoneWUI} send 0 value for ${GlobalSIP['BackupProxyPort']} to ${phone1} URL
    Then Using ${PhoneWUI} send ${DefaultProxy} value for ${GlobalSIP['BackupOutboundProxyServer']} to ${phone1} URL
    Then Using ${PhoneWUI} send 0 value for ${GlobalSIP['BackupOutboundProxyPort']} to ${phone1} URL
    Then Using ${PhoneWUI} send ${DefaultProxy} value for ${GlobalSIP['BackupRegistrarServer']} to ${phone1} URL
    Then Using ${PhoneWUI} send 0 value for ${GlobalSIP['BackupRegistrarPort']} to ${phone1} URL
    Then Using ${PhoneWUI} click on the ${GlobalSIP['SaveSettings']} on ${phone1} URL

    &{details}=    CREATE DICTIONARY    offhookField=
    Then I want to configure ActionUrl parameters using ${Details} for ${phone1}
    And Using ${PhoneWUI} logoff ${phone1} URL


763535: SDE -001
    [Tags]    Owner:Surender    Reviewer:    speeddial
    &{configurationDetails}=  CREATE DICTIONARY    expmod1 key1 type=speeddial    expmod1 key1 label=SpeedDial
    ...                                            expmod1 key1 value=${phone2}
    Given Configure parameters on ${phone1} using ${configurationDetails}
    Then verify display message SpeedDial on PKM for ${phone1}

    &{configurationDetails}=  CREATE DICTIONARY    expmod1 key1 type=none    expmod1 key1 label=    expmod1 key1 value=
    Then Configure parameters on ${phone1} using ${configurationDetails}
    And on ${phone1} PKM verify negative display message SpeedDial


763536: SDE -005
    [Tags]    Owner:Surender    Reviewer:    speeddial
    &{configurationDetails}=  CREATE DICTIONARY    expmod1 key1 type=speeddial    expmod1 key1 label=SpeedDial
    ...                                            expmod1 key1 value=${phone2}
    Given Configure parameters on ${phone1} using ${configurationDetails}
    Then verify display message SpeedDial on PKM for ${phone1}
    Then I want to press PKM line key ${programKey1} on ${phone1}
    Then Verify ringing state on ${phone1} and ${phone2}
    Then Verify the Caller id on ${phone1} and ${phone2} display
    Then Disconnect the call from ${phone1}

    &{configurationDetails}=  CREATE DICTIONARY    expmod1 key1 type=none    expmod1 key1 label=    expmod1 key1 value=
    Then Configure parameters on ${phone1} using ${configurationDetails}
    And on ${phone1} PKM verify negative display message SpeedDial


763537: SDE -008
    [Tags]    Owner:Surender    Reviewer:    speeddial12
    &{configurationDetails}=  CREATE DICTIONARY    expmod1 key1 type=speeddial    expmod1 key1 label=SpeedDial
    ...                                            expmod1 key1 value=${phone2}
    Given Configure parameters on ${phone1} using ${configurationDetails}
    Then verify display message SpeedDial on PKM for ${phone1}
    Then I want to press PKM line key ${programKey1} on ${phone1}
    Then Verify the Caller id on ${phone1} and ${phone2} display
    Then Disconnect the call from ${phone1}

    &{configurationDetails}=  CREATE DICTIONARY    expmod1 key1 type=speeddial    expmod1 key1 label=SpeedDial
    ...                                            expmod1 key1 value=${phone3}
    Given Configure parameters on ${phone1} using ${configurationDetails}
    Then verify display message SpeedDial on PKM for ${phone1}
    Then I want to press PKM line key ${programKey1} on ${phone1}
    Then Verify the Caller id on ${phone1} and ${phone3} display
    Then Disconnect the call from ${phone1}

    &{configurationDetails}=  CREATE DICTIONARY    expmod1 key1 type=none    expmod1 key1 label=    expmod1 key1 value=
    Then Configure parameters on ${phone1} using ${configurationDetails}
    And on ${phone1} PKM verify negative display message SpeedDial


763540: SDE -021
    [Tags]    Owner:Surender    Reviewer:    speeddial
    &{configurationDetails}=  CREATE DICTIONARY    expmod1 key1 type=speeddial    expmod1 key1 label=SpeedDial
    ...                                            expmod1 key1 value=${phone2}
    Given Configure parameters on ${phone1} using ${configurationDetails}
    Then verify display message SpeedDial on PKM for ${phone1}

    &{configurationDetails}=  CREATE DICTIONARY    expmod1 key1 type=none    expmod1 key1 label=    expmod1 key1 value=
    Then Configure parameters on ${phone1} using ${configurationDetails}
    And on ${phone1} PKM verify negative display message SpeedDial

858559: Sip 01
    [Tags]    Owner:Surender    Reviewer:    rtcp
    ${ipAddress}=    Get System IP Address
    &{configurationDetails}=    CREATE DICTIONARY    sip rtcp summary reports=1
    ...                         sip rtcp summary report collector=collector@${ipAddress}
    ...                         sip rtcp summary reports transport protocol=1
    ...                         sip rtcp summary report collector port=5062
    Given Configure parameters on ${phone1} using ${configurationDetails}
    Then Using ${PhoneWUI} log into ${phone1} URL
    Then Using ${PhoneWUI} Start the capture on 5060 port on ${phone1} URL
    Then I want to make a two party call between ${phone1} and ${phone2} using ${offHook}
    Then Verify the Caller id on ${phone1} and ${phone2} display
    Then Verify ringing state on ${phone1} and ${phone2}
    Then Answer the call on ${phone2} using ${offHook}
    Then On ${phone1} wait for 10 seconds
    Then Disconnect the call from ${phone1}

    Then Using ${PhoneWUI} ${stop} the capture from ${phone1} URL
    Then Using ${PhoneWUI} ${download} the capture from ${phone1} URL
    Then Verify the captureFile contains Delay: inside ${Protocols['SIP(Publish)']} packets
    Then Verify the captureFile contains BurstGapLoss: inside ${Protocols['SIP(Publish)']} packets
    Then Verify the captureFile contains JitterBuffer: inside ${Protocols['SIP(Publish)']} packets
    Then Using ${PhoneWUI} logoff ${phone1} URL
    &{configurationDetails}=    CREATE DICTIONARY    sip rtcp summary reports=0
    ...                         sip rtcp summary report collector=
    ...                         sip rtcp summary reports transport protocol=1
    ...                         sip rtcp summary report collector port=
    And Configure parameters on ${phone1} using ${configurationDetails}


858560: SIP 05
    [Tags]    Owner:Surender    Reviewer:    rtcp
    ${ipAddress}=    Get System IP Address
    &{configurationDetails}=    CREATE DICTIONARY    sip rtcp summary reports=1
    ...                         sip rtcp summary report collector=collector@${ipAddress}
    ...                         sip rtcp summary reports transport protocol=1
    ...                         sip rtcp summary report collector port=5062
    Given Configure parameters on ${phone1} using ${configurationDetails}
    Then Configure parameters on ${phone2} using ${configurationDetails}
    Then Using ${PhoneWUI} log into ${phone1} URL
    Then Using ${PhoneWUI} Start the capture on 5060 port on ${phone1} URL
    Then Using ${PhoneWUI} logoff ${phone1} URL

    Then Using ${PhoneWUI} log into ${phone2} URL
    Then Using ${PhoneWUI} Start the capture on 5060 port on ${phone2} URL
    Then Using ${PhoneWUI} logoff ${phone2} URL
    Then Using ${PhoneWUI} log into ${phone1} URL

    Then I want to make a two party call between ${phone1} and ${phone2} using ${offHook}
    Then Verify the Caller id on ${phone1} and ${phone2} display
    Then Answer the call on ${phone2} using ${offHook}
    Then On ${phone1} wait for 10 seconds
    Then Disconnect the call from ${phone1}
    Then Using ${PhoneWUI} ${stop} the capture from ${phone1} URL
    Then Using ${PhoneWUI} ${download} the capture from ${phone1} URL
    Then Verify the captureFile contains Delay: inside ${Protocols['SIP(Publish)']} packets
    Then Verify the captureFile contains BurstGapLoss: inside ${Protocols['SIP(Publish)']} packets
    Then Verify the captureFile contains JitterBuffer: inside ${Protocols['SIP(Publish)']} packets
    Then Using ${PhoneWUI} logoff ${phone1} URL

    Then Using ${PhoneWUI} log into ${phone2} URL
    Then Using ${PhoneWUI} ${stop} the capture from ${phone2} URL
    Then Using ${PhoneWUI} ${download} the capture from ${phone2} URL
    Then Verify the captureFile contains Delay: inside ${Protocols['SIP(Publish)']} packets
    Then Verify the captureFile contains BurstGapLoss: inside ${Protocols['SIP(Publish)']} packets
    Then Verify the captureFile contains JitterBuffer: inside ${Protocols['SIP(Publish)']} packets
    Then Using ${PhoneWUI} logoff ${phone2} URL

    &{configurationDetails}=    CREATE DICTIONARY    sip rtcp summary reports=0
    ...                         sip rtcp summary report collector=
    ...                         sip rtcp summary reports transport protocol=1
    ...                         sip rtcp summary report collector port=0
    And Configure parameters on ${phone1} using ${configurationDetails}
    And Configure parameters on ${phone2} using ${configurationDetails}

858564: SIP 29
    [Tags]    Owner:Surender    Reviewer:    rtcp
    ${ipAddress}=    Get System IP Address
    &{configurationDetails}=    CREATE DICTIONARY    sip rtcp summary reports=1
    ...                         sip rtcp summary report collector=collector@${ipAddress}
    ...                         sip rtcp summary reports transport protocol=1
    ...                         sip rtcp summary report collector port=5062
    Given Configure parameters on ${phone1} using ${configurationDetails}
    Then Using ${PhoneWUI} log into ${phone1} URL
    Then Using ${PhoneWUI} Start the capture on 5060 port on ${phone1} URL

    Then I want to make a two party call between ${phone1} and ${phone2} using ${offHook}
    Then Verify the Caller id on ${phone1} and ${phone2} display
    Then Answer the call on ${phone2} using ${offHook}
    Then On ${phone1} wait for 10 seconds
    Then Disconnect the call from ${phone1}
    Then Using ${PhoneWUI} ${stop} the capture from ${phone1} URL
    Then Using ${PhoneWUI} ${download} the capture from ${phone1} URL
    Then Verify the captureFile contains Event: vq-rtcpxr inside ${Protocols['SIP(Publish)']} packets
    Then Using ${PhoneWUI} logoff ${phone1} URL

    &{configurationDetails}=    CREATE DICTIONARY    sip rtcp summary reports=0
    ...                         sip rtcp summary report collector=
    ...                         sip rtcp summary reports transport protocol=1
    ...                         sip rtcp summary report collector port=0
    And Configure parameters on ${phone1} using ${configurationDetails}

858562: SIP 20
    [Tags]    Owner:Surender    Reviewer:    rtcp
    ${ipAddress}=    Get System IP Address
    &{configurationDetails}=    CREATE DICTIONARY    sip rtcp summary reports=1
    ...                         sip rtcp summary report collector=collector@${ipAddress}
    ...                         sip rtcp summary reports transport protocol=1
    ...                         sip rtcp summary report collector port=5062
    Given Configure parameters on ${phone1} using ${configurationDetails}
    Then Using ${PhoneWUI} log into ${phone1} URL
    Then Using ${PhoneWUI} Start the capture on 5060 port on ${phone1} URL

    Then I want to make a two party call between ${phone1} and ${phone2} using ${offHook}
    Then Answer the call on ${phone2} using ${offHook}
    Then I want to make a conference call between ${phone1},${phone2} and ${phone3} using ${consultiveConference}
    Then Verify the Caller id on ${phone1} and ${phone2} display
    Then Verify the Caller id on ${phone1} and ${phone3} display
    Then Disconnect the call from ${phone1}
    Then Disconnect the call from ${phone2}

    Then Using ${PhoneWUI} ${stop} the capture from ${phone1} URL
    Then Using ${PhoneWUI} ${download} the capture from ${phone1} URL
    Then Verify the captureFile contains Event: vq-rtcpxr inside ${Protocols['SIP(Publish)']} packets of ${phone1}
    Then Using ${PhoneWUI} logoff ${phone1} URL

    &{configurationDetails}=    CREATE DICTIONARY    sip rtcp summary reports=0
    ...                         sip rtcp summary report collector=
    ...                         sip rtcp summary reports transport protocol=0
    ...                         sip rtcp summary report collector port=0
    Given Configure parameters on ${phone1} using ${configurationDetails}


858563: SIP 25
    [Tags]    Owner:Surender    Reviewer:    rtcp
    ${ipAddress}=    Get System IP Address
    &{configurationDetails}=    CREATE DICTIONARY    sip rtcp summary reports=1
    ...                         sip rtcp summary report collector=collector@${ipAddress}
    ...                         sip rtcp summary report collector port=65000
    Given Configure parameters on ${phone1} using ${configurationDetails}
    Then Using ${PhoneWUI} log into ${phone1} URL
    Then Using ${PhoneWUI} Start the capture on 5060 port on ${phone1} URL

    Then I want to make a two party call between ${phone1} and ${phone2} using ${offHook}
    Then Answer the call on ${phone2} using ${offHook}
    Then On ${phone1} Wait for 10 seconds
    Then Disconnect the call from ${phone}

    Then Using ${PhoneWUI} ${stop} the capture from ${phone1} URL
    Then Using ${PhoneWUI} ${download} the capture from ${phone1} URL
    Then Verify the captureFile contains Event: vq-rtcpxr inside ${Protocols['SIP(Publish)']} packets of ${phone1}
    Then Using ${PhoneWUI} logoff ${phone1} URL

    &{configurationDetails}=    CREATE DICTIONARY    sip rtcp summary reports=0
    ...                         sip rtcp summary report collector=
    ...                         sip rtcp summary report collector port=0
    And Configure parameters on ${phone1} using ${configurationDetails}

858566: sip rtcp summary reports transport protocol TC2: sip use UDP, rtcp-xr use TCP, no OB
	[Tags]    Owner:Surender    Reviewer:    rtcp
	${ipAddress}=    Get System IP Address
    &{configurationDetails}=    CREATE DICTIONARY    sip rtcp summary reports=1
    ...                         sip rtcp summary report collector=collector@${ipAddress}
    ...                         sip rtcp summary report collector port=5062
    ...                         sip rtcp summary reports transport protocol=2
    ...                         sip transport protocol=1
    ...                         sip outbound proxy=${DefaultProxy}

    Given Configure parameters on ${phone1} using ${configurationDetails}
    Then Using ${PhoneWUI} log into ${phone1} URL
    Then Using ${PhoneWUI} Start the capture on 5060 port on ${phone1} URL

    Then I want to make a two party call between ${phone1} and ${phone2} using ${offHook}
    Then Answer the call on ${phone2} using ${offHook}
    Then On ${phone} Wait for 10 seconds
    Then Disconnect the call from ${phone1}

    Then Using ${PhoneWUI} ${stop} the capture from ${phone1} URL
    Then Using ${PhoneWUI} ${download} the capture from ${phone1} URL
    Then Verify the captureFile contains transport=UDP inside ${Protocols['SIP(Invite)']} packets of ${phone1}
    Then Verify the captureFile contains transport=tcp inside ${Protocols['SIP(Publish)']} packets of ${phone1}
    Then Using ${PhoneWUI} logoff ${phone1} URL

    &{configurationDetails}=    CREATE DICTIONARY    sip rtcp summary reports=0
    ...                         sip rtcp summary report collector=
    ...                         sip rtcp summary report collector port=0
    ...                         sip rtcp summary reports transport protocol=1
    ...                         sip transport protocol=-1
    ...                         sip outbound proxy=${${pbx}IP}

    And Configure parameters on ${phone1} using ${configurationDetails}


858567: sip rtcp summary reports transport protocol TC8: sip use TCP/UDP, rtcp-xr use TCP, no OB
    [Tags]    Owner:Surender    Reviewer:    rtcp
    ${ipAddress}=    Get System IP Address
    &{configurationDetails}=    CREATE DICTIONARY    sip rtcp summary reports=1
    ...                         sip rtcp summary report collector=collector@${ipAddress}
    ...                         sip rtcp summary report collector port=5062
    ...                         sip rtcp summary reports transport protocol=2
    ...                         sip transport protocol=0
    ...                         sip outbound proxy=${DefaultProxy}

    Given Configure parameters on ${phone1} using ${configurationDetails}
    Then Using ${PhoneWUI} log into ${phone1} URL
    Then Using ${PhoneWUI} Start the capture on 5060 port on ${phone1} URL

    Then I want to make a two party call between ${phone1} and ${phone2} using ${offHook}
    Then Answer the call on ${phone2} using ${offHook}
    Then On ${phone} Wait for 10 seconds
    Then Disconnect the call from ${phone1}

    Then Using ${PhoneWUI} ${stop} the capture from ${phone1} URL
    Then Using ${PhoneWUI} ${download} the capture from ${phone1} URL
    Then Verify the captureFile contains transport=UDP inside ${Protocols['SIP(Invite)']} packets
    Then Verify the captureFile contains transport=tcp inside ${Protocols['SIP(Publish)']} packets
    Then Using ${PhoneWUI} logoff ${phone1} URL

    &{configurationDetails}=    CREATE DICTIONARY    sip rtcp summary reports=0
    ...                         sip rtcp summary report collector=
    ...                         sip rtcp summary report collector port=0
    ...                         sip rtcp summary reports transport protocol=1
    ...                         sip transport protocol=-1
    ...                         sip outbound proxy=${${pbx}IP}

    And Configure parameters on ${phone1} using ${configurationDetails}


858569: sip rtcp summary reports transport protocol TC16: sip use UDP, rtcp-xr use UDP, with OB
    [Tags]    Owner:Surender   Reviewer:    rtcp
    ${ipAddress}=    Get System IP Address
    &{configurationDetails}=    CREATE DICTIONARY    sip rtcp summary reports=1
    ...                         sip rtcp summary report collector=collector@${ipAddress}
    ...                         sip rtcp summary report collector port=5062
    ...                         sip rtcp summary reports transport protocol=1
    ...                         sip transport protocol=1
    ...                         sip outbound proxy=${${pbx}IP}

    Given Configure parameters on ${phone1} using ${configurationDetails}
    Then Using ${PhoneWUI} log into ${phone1} URL
    Then Using ${PhoneWUI} Start the capture on 5060 port on ${phone1} URL

    Then I want to make a two party call between ${phone1} and ${phone2} using ${offHook}
    Then Answer the call on ${phone2} using ${offHook}
    Then On ${phone} Wait for 10 seconds
    Then Disconnect the call from ${phone1}

    Then Using ${PhoneWUI} ${stop} the capture from ${phone1} URL
    Then Using ${PhoneWUI} ${download} the capture from ${phone1} URL
    Then Verify the captureFile contains transport=UDP inside ${Protocols['SIP(Invite)']} packets of ${phone1}
    Then Verify the captureFile contains transport=udp inside ${Protocols['SIP(Publish)']} packets of ${phone1}
    Then Using ${PhoneWUI} logoff ${phone1} URL

    &{configurationDetails}=    CREATE DICTIONARY    sip rtcp summary reports=0
    ...                         sip rtcp summary report collector=
    ...                         sip rtcp summary report collector port=0
    ...                         sip rtcp summary reports transport protocol=1
    ...                         sip transport protocol=-1
    ...                         sip outbound proxy=${${pbx}IP}

    And Configure parameters on ${phone1} using ${configurationDetails}


858565: SIP 35
    [Tags]    Owner:Surender    Reviewer:    rtcp
    ${ipAddress}=    Get System IP Address
    &{configurationDetails}=    CREATE DICTIONARY    sip rtcp summary reports=1
    ...                         sip rtcp summary report collector=collector@${ipAddress}
    ...                         sip rtcp summary report collector port=5062
    ...                         sip outbound proxy=${${pbx}IP}

    Given Configure parameters on ${phone1} using ${configurationDetails}
    Then Using ${PhoneWUI} log into ${phone1} URL
    Then Using ${PhoneWUI} Start the capture on 5060 port on ${phone1} URL

    Then I want to make a two party call between ${phone1} and ${phone2} using ${offHook}
    Then Answer the call on ${phone2} using ${offHook}
    Then On ${phone} Wait for 10 seconds
    Then Disconnect the call from ${phone1}

    Then Using ${PhoneWUI} ${stop} the capture from ${phone1} URL
    Then Using ${PhoneWUI} ${download} the capture from ${phone1} URL
    Then Verify the captureFile contains transport=UDP inside ${Protocols['IP']} packets
    Then Verify the captureFile contains transport=udp inside ${Protocols['SIP(Publish)']} packets
    Then Using ${PhoneWUI} logoff ${phone1} URL

    &{configurationDetails}=    CREATE DICTIONARY    sip rtcp summary reports=0
    ...                         sip rtcp summary report collector=
    ...                         sip rtcp summary report collector port=0
    ...                         sip outbound proxy=${${pbx}IP}

    And Configure parameters on ${phone1} using ${configurationDetails}

763000: Flash 28
    [Tags]    Owner:Surender    Reviewer:    sipinfo
    Given Using ${PhoneWUI} log into ${phone1} URL
    Then Using ${PhoneWUI} Navigate to go to ${globalSIPMenu} page on ${phone1} URL
    Then Go to the ${GlobalSIP['DTMFMethod']} option and select the ${SIPInfo} value
    Then Using ${PhoneWUI} click on the ${GlobalSIP['SaveSettings']} on ${phone1} URL
    Then Using ${PhoneWUI} Navigate to go to ${globalSIPMenu} page on ${phone1} URL
    Then Verify text ${SIPInfo} for ${GlobalSIP['DTMFMethod']} on the ${phone1} URL
    Then Go to the ${GlobalSIP['DTMFMethod']} option and select the ${rtp} value
    Then Using ${PhoneWUI} click on the ${GlobalSIP['SaveSettings']} on ${phone1} URL
    And Using ${PhoneWUI} logoff ${phone1} URL

763001: Flash 31
    [Tags]    Owner:Surender    Reviewer:    rtp
    &{configurationDetails}=    CREATE DICTIONARY    topsoftkey3 type=Flash    topsoftkey3 label=Flash
    Given Configure parameters on ${phone1} using ${configurationDetails}

    Then Using ${PhoneWUI} log into ${phone1} URL
    Then Using ${PhoneWUI} Navigate to go to ${globalSIPMenu} page on ${phone1} URL
    Then Go to the ${GlobalSIP['DTMFMethod']} option and select the ${rtp} value
    Then Using ${PhoneWUI} click on the ${GlobalSIP['SaveSettings']} on ${phone1} URL
    Then Using ${PhoneWUI} start the capture on all port on ${phone1} URL
    Then I want to make a two party call between ${phone2} and ${phone1} using ${offHook}
    Then Answer the call on ${phone1} using ${offHook}
    Then On ${phone1} press ${softkey} ${programKey3} for 1 times
    Then Using ${PhoneWUI} ${stop} the capture from ${phone1} URL
    Then Using ${PhoneWUI} ${download} the capture from ${phone1} URL
    Then Verify the captureFile contains Event ID: Flash (16) inside ${Protocols['RTPEvent']} packets of ${phone1}

    &{configurationDetails}=    CREATE DICTIONARY    topsoftkey3 type=none    topsoftkey3 label=
    And Configure parameters on ${phone1} using ${configurationDetails}

763681: Softkey icon in Hold state(Remote Hold)
    [Tags]    Owner:Surender    Reviewer:    icon
    Given I want to make a two party call between ${phone2} and ${phone1} using ${offHook}
    Then Answer the call on ${phone1} using ${offHook}
    Then On ${phone1} verify ${line1} icon state as ${callAppearanceActive}
    Then Put the linekey ${line1} of ${phone2} on ${hold}
    Then On ${phone1} verify ${line1} icon state as ${callAppearanceRemoteHold}
    Then Verify the led state of ${line1} as ${blink} on ${phone1}
    Then Put the linekey ${line1} of ${phone2} on ${unHold}
    Then On ${phone1} verify ${line1} icon state as ${callAppearanceActive}
    And Disconnect the call from ${phone1}

763682: Line softkey icon in Hold State (Local Hold)
    [Tags]    Owner:Surender    Reviewer:    icon
    Given I want to make a two party call between ${phone1} and ${phone2} using ${offHook}
    Then Answer the call on ${phone2} using ${offHook}
    Then On ${phone1} verify ${line1} icon state as ${callAppearanceActive}
    Then Put the linekey ${line1} of ${phone1} on ${hold}
    Then On ${phone1} verify ${line1} icon state as ${callAppearanceLocalHold}
    Then Put the linekey ${line1} of ${phone1} on ${unHold}
    Then On ${phone1} verify ${line1} icon state as ${callAppearanceActive}
    And Disconnect the call from ${phone2}

763683: Check for softkey line icon during Incoming call on both lines
    [Tags]    Owner:Surender    Reviewer:    lineIcon
    Given On ${phone1} verify ${line1} icon state as ${callAppearanceIdle}
    Then On ${phone1} verify ${line2} icon state as ${callAppearanceIdle}
    Then I want to make a two party call between ${phone2} and ${phone1} using ${offHook}
    Then I want to make a two party call between ${phone3} and ${phone1} using ${offHook}
    Then On ${phone1} verify ${line1} icon state as ${callAppearanceIncoming}
    Then On ${phone1} verify ${line2} icon state as ${callAppearanceIncoming}
    Then Disconnect the call from ${phone2}
    And Disconnect the call from ${phone3}

763685: Check for behavior of BLF softkey (Incoming)
    [Tags]    Owner:Surender    Reviewer:   blf
    &{configurationDetails}=    CREATE DICTIONARY    topsoftkey3 type=${blf}    topsoftkey3 value=${phone2}
    ...                                              topsoftkey3 label=${blf}
    Given Configure parameters on ${phone1} using ${configurationDetails}
    Then I want to make a two party call between ${phone3} and ${phone2} using ${offHook}
    Then Verify ringing state on ${phone3} and ${phone2}
    Then Verify the led state of ${line3} as ${blink} on ${phone1}
    Then On ${phone1} verify ${line3} icon state as ${blfBlink}
    Then Disconnect the call from ${phone3}
    Then On ${phone1} verify ${line3} icon state as ${blfIdle}
    &{configurationDetails}=    CREATE DICTIONARY    topsoftkey3 type=${blf}    topsoftkey3 value=${phone2}
    ...                                              topsoftkey3 label=${blf}
    And Configure parameters on ${phone1} using ${configurationDetails}

763686: BLF in Hold state(Remote Hold)
    [Tags]    Owner:Surender    Reviewer:    blf
    &{configurationDetails}=    CREATE DICTIONARY    topsoftkey3 type=${blf}    topsoftkey3 value=${phone2}
    ...                                              topsoftkey3 label=${blf}
    Given Configure parameters on ${phone1} using ${configurationDetails}

    &{configurationDetails}=    CREATE DICTIONARY    topsoftkey3 type=${blf}    topsoftkey3 value=${phone3}
    ...                                              topsoftkey3 label=${blf}
    Then Configure parameters on ${phone1} using ${configurationDetails}

    Then I want to make a two party call between ${phone2} and ${phone3} using ${offHook}
    Then Verify ringing state on ${phone2} and ${phone3}
    Then Verify the led state of ${line4} as ${blink} on ${phone1}
    Then On ${phone1} verify ${line4} icon state as ${blfBlink}
    Then Answer the call on ${phone3} using ${offHook}
    Then Put the linekey ${line1} of ${phone3} on ${hold}
    Then On ${phone1} verify ${line4} icon state as ${blfBlink}
    Then On ${phone1} verify ${line3} icon state as ${blfActive}
    Then Put the linekey ${line1} of ${phone3} on ${unHold}
    Then On ${phone1} verify ${line4} icon state as ${blfActive}
    Then On ${phone1} verify ${line3} icon state as ${blfActive}

761990: AstBLF_015
    [Tags]    Owner:Surender    Reviewer:    blf
    &{configurationDetails}=    CREATE DICTIONARY    expmod1 key3 type=${blf}    expmod1 key3 value=${phone2}
    ...                                              expmod1 key3 label=${blf}
    Given Configure parameters on ${phone1} using ${configurationDetails}

    Then Using ${PhoneWUI} log into ${phone1} URL
    Then Using ${PhoneWUI} start the capture on 5060 port on ${phone1} URL
    Then Using ${PhoneWUI} ${stop} the capture from ${phone1} URL

    Then I want to make a two party call between ${phone3} and ${phone2} using ${offHook}
    Then Answer the call on ${phone2} using ${offHook}
    Then Verify the PKM led state of ${line3} as ${on} on ${phone1}
    Then Using ${PhoneWUI} ${download} the capture from ${phone1} URL
    Then Verify the ${Protocols['SIP(Notify)']} packets in the captured packet file of ${phone1}

762509: TC_03
    [Tags]    Owner:Surender    Reviewer:    brightnessCheck
    &{parameters}=    CREATE DICTIONARY    bl on time=30    backlight mode=1    brightness level=4
    ...                                    inactivity brightness level=1
    Given Create aastra.cfg file using ${parameters}
    Then Send aastra.cfg file to ${root} folder on FTP server

    &{configurationDetails}=    CREATE DICTIONARY    download protocol=FTP    ftp server=10.112.123.107
    ...                         ftp username=desktop    ftp password=desktop
    Then Configure parameters on ${phone1} using ${configurationDetails}
    Then Reboot ${phone1}

    Then Press hardkey as ${goodBye} on ${phone1}
    Then Verify the brightness level of ${phone1} as 4
    Then On ${phone1} wait for 30 seconds
    Then Verify the brightness level of ${phone1} as 1

    &{parameters}=    CREATE DICTIONARY
    Given Create startup.cfg file using ${parameters}
    Then Send aastra.cfg file to ${root} folder on FTP server

    ${systemIP}=    GET SYSTEM IP ADDRESS
    &{configurationDetails}=    CREATE DICTIONARY    download protocol=TFTP    tftp server=${systemIP}
    Then Configure parameters on ${phone1} using ${configurationDetails}
    Then Reboot ${phone1}

762510: TC_10
    [Tags]    Owner:Surender    Reviewer:    brightnessCheck
    &{parameters}=    CREATE DICTIONARY    bl on time=30    backlight mode=1    brightness level=3
    ...                                    inactivity brightness level=0
    Given Create aastra.cfg file using ${parameters}
    Then Send aastra.cfg file to ${root} folder on FTP server

    &{configurationDetails}=    CREATE DICTIONARY    download protocol=FTP    ftp server=10.112.123.107
    ...                         ftp username=desktop    ftp password=desktop
    Then Configure parameters on ${phone1} using ${configurationDetails}
    Then Reboot ${phone1}

    Then I want to make a two party call between ${phone1} and ${phone2} using ${offHook}
    Then Answer the call on ${phone2} using ${answerModeValue}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Disconnect the call from ${phone1}
    Then Verify the brightness level of ${phone1} as 3
    Then On ${phone1} wait for 30 seconds
    Then Verify the brightness level of ${phone1} as 0

    &{parameters}=    CREATE DICTIONARY
    Given Create startup.cfg file using ${parameters}
    Then Create ${automationTestingFolder} folder on FTP server
    Then Send startup.cfg file to ${automationTestingFolder} folder on FTP server

    ${systemIP}=    GET SYSTEM IP ADDRESS
    &{configurationDetails}=    CREATE DICTIONARY    download protocol=TFTP    tftp server=${systemIP}
    Then Configure parameters on ${phone1} using ${configurationDetails}
    And Reboot ${phone1}

762511: TC_16
    [Tags]    Owner:Surender    Reviewer:    brightnessCheck
    &{parameters}=    CREATE DICTIONARY    bl on time=30    backlight mode=1    brightness level=3
    ...                                    inactivity brightness level=0
    Given Create aastra.cfg file using ${parameters}
    Then Send aastra.cfg file to ${root} folder on FTP server

    &{configurationDetails}=    CREATE DICTIONARY    download protocol=FTP    ftp server=10.112.123.107
    ...                         ftp username=desktop    ftp password=desktop
    Then Configure parameters on ${phone1} using ${configurationDetails}
    Then Reboot ${phone1}

    Then Press hardkey as ${callersList} on ${phone1}
    Then Press hardkey as ${goodBye} on ${phone1}
    Then Verify the brightness level of ${phone1} as 3
    Then On ${phone1} wait for 30 seconds
    Then Verify the brightness level of ${phone1} as 0

761924: Enable sip keepalive support:15a
    [Tags]    Owner:Surender    Reviewer:    keepalive
    &{parameters}=    CREATE DICTIONARY    sip keepalive timer=30    sip transport protocol=1  #UDP
    Given Create aastra.cfg file using ${parameters}
    Then Send aastra.cfg file to ${root} folder on FTP server

    &{configurationDetails}=    CREATE DICTIONARY    download protocol=FTP    ftp server=10.112.123.107
    ...                         ftp username=desktop    ftp password=desktop
    Then Configure parameters on ${phone1} using ${configurationDetails}
    Then Reboot ${phone1}

    Then Using ${PhoneWUI} log into ${phone1} URL
    Then Using ${PhoneWUI} start the capture on ${all} port on ${phone1} URL
    Then On ${phone1} wait for 90 seconds
    Then Using ${PhoneWUI} ${stop} the capture from ${phone1} URL
    Then Using ${PhoneWUI} ${download} the capture from ${phone1} URL

    &{filters}=    CREATE DICTIONARY    ip.addr==${${pbx}IP}
    Then Filter the captured packets using ${filters} on ${phone1}
    Then Verify the time between ${protocols['SIP']} packets as 30 seconds on ${phone1}
    And Using ${PhoneWUI} logoff ${phone1} URL

763680: Check for behavior of softkey icons for Line Keys (Incoming)
    [Tags]    Owner:Surender    Reviewer:    iconVerify
    Given unregister the ${phone1} from MxOne pbx
    Then I want to verify on ${phone1} negative display message ${phone1}
    Then register the ${phone1} on MxOne pbx
    Then On ${phone1} verify display message ${phone1}
    Then On ${phone1} verify ${line1} icon state as ${callApparanceIdle}
    Then I want to make a two party call between ${phone2} and ${phone1} using ${offHook}
    Then Verify the led state of ${line1} as ${blink} on ${phone1}
    Then On ${phone1} verify ${line1} icon state as ${callAppearanceIncoming}
    Then Disconnect the call from ${phone2}
    And On ${phone1} verify ${line1} icon state as ${callApparanceIdle}

763644: TC11: 69xx + M695
    [Tags]    Owner:Surender    Reviewer:    pkmSupport
    &{configurationDetails}=  CREATE DICTIONARY    expmod1 key1 type=${blf}    expmod1 key1 label=${blf}
    ...                                            expmod1 key1 value=${phone2}
    Given Configure parameters on ${phone1} using ${configurationDetails}
    Then verify display message ${blf} on PKM for ${phone1}

    &{configurationDetails}=  CREATE DICTIONARY    expmod1 key1 type=none    expmod1 key1 label=
    ...                                            expmod1 key1 value=
    And Configure parameters on ${phone1} using ${configurationDetails}

858561: SIP 09
    [Tags]    Owner:Surender    Reviewer:    rtcp
    Given Using ${PhoneWUI} log into ${phone1} URL
    Then Using ${PhoneWUI} Navigate to go to ${GlobalSIPMenu} page on ${phone1} URL
    Then Verify ${RTCPReportCollector} option is not present on the Web UI of ${phone1}
    Then Using ${PhoneWUI} logoff ${phone1} URL

    ${ipAddress}=    Get System IP Address
    &{parameters}=    CREATE DICTIONARY    sip rtcp summary reports=1
    ...               sip rtcp summary report collector=collector@${ipAddress}
    ...               sip rtcp summary reports transport protocol=1
    ...               sip rtcp summary report collector port=5062
    Given Create startup.cfg file using ${parameters}
    Then Create ${automationTestingFolder} folder on FTP server
    Then Send startup.cfg file to ${automationTestingFolder} folder on FTP server
    &{configurationDetails}=    CREATE DICTIONARY    download protocol=FTP    ftp server=10.112.123.107
    ...                         ftp path=${automationTestingFolderPath}    ftp username=desktop    ftp password=desktop
    Then Configure parameters on ${phone1} using ${configurationDetails}
    Then Reboot ${phone1}

    Then Using ${PhoneWUI} log into ${phone1} URL
    Then Using ${PhoneWUI} Start the capture on 5060 port on ${phone1} URL

    Then I want to make a two party call between ${phone1} and ${phone2} using ${offHook}
    Then Verify the Caller id on ${phone1} and ${phone2} display
    Then Answer the call on ${phone2} using ${offHook}
    Then On ${phone1} wait for 10 seconds
    Then Disconnect the call from ${phone1}
    Then Using ${PhoneWUI} ${stop} the capture from ${phone1} URL
    Then Using ${PhoneWUI} ${download} the capture from ${phone1} URL
    Then Verify the ${Protocols['SIP(Publish)']} packets in the captured packet file of ${phone1}
    And Using ${PhoneWUI} logoff ${phone1} URL

    &{configurationDetails}=    CREATE DICTIONARY    sip rtcp summary reports=0
    ...                         sip rtcp summary report collector=
    ...                         sip rtcp summary report collector port=0
    ...                         sip outbound proxy=${${pbx}IP}

    And Configure parameters on ${phone1} using ${configurationDetails}

766601: Transfer calls
    [Tags]    Owner:Surender    Reviewer:    longPress
    Given Long press hardkey as ${dialPad0} on ${phone1}
    Then On ${phone1} enter number ${phone2}
    Then On ${phone1} verify display message +
    Then On ${phone1} press the softkey ${dial} in DialingState
    Then Answer the call on ${phone2} using ${offHook}
    Then On ${phone1} press the softkey ${transfer} in AnswerState
    Then Long press hardkey as ${dialPad0} on ${phone1}
    Then On ${phone1} enter number ${phone3}
    Then On ${phone1} verify display message +
    Then On ${phone1} press the softkey ${transfer} in TransferState
    Then Verify ringing state on ${phone2} and ${phone3}
    And Disconnect the call from ${phone2}

766603: Directory_01
    [Tags]    Owner:Surender    Reviewer:    longPress
    &{configurationDetails}=    CREATE DICTIONARY    topsoftkey3 type=${directory}    topsoftkey3 label=${directory}
    Then Configure parameters on ${phone1} using ${configurationDetails}
    Then On ${phone1} verify display message ${directory}
    Then Add number of ${phone2} in the directory with + prefix by pressing ${programKey3} key of ${phone1}
    Then On ${phone1} verify message ${phone2} with + as prefix
    And Delete ${all} entries from directry of ${phone1}

762483: BACKGROUND_IMAGE_04
    [Tags]    Owner:Surender    Reviewer:    backgroundImage
    Given Send ${backgroundImage} file to ${bgImages} folder on ${ftp} server
    Then Set ${custom} background image on ${phone1} using ${ftp} server
    And Verify ${custom} background image is set on ${phone1}
    [Teardown]    Default Background Configuration

762484: BACKGROUND_IMAGE_05
    [Tags]    Owner:Surender    Reviewer:    backgroundImage
    Given Send ${backgroundImage} file to ${bgImages} folder on ${http} server
    Then Set ${custom} background image on ${phone1} using ${http} server
    And Verify ${custom} background image is set on ${phone1}
    [Teardown]    Default Background Configuration

762520: Ftp uses for image updation
    [Tags]    Owner:Surender    Reviewer:    backgroundImage
    Given Send ${backgroundImage} file to ${bgImages} folder on ${ftp} server
    Then Set Custom screensaver image on ${phone1} using ${ftp} server

    &{screenSaverDetails}=    CREATE DICTIONARY    screenSaverType=${custom}
    And Check the screensaver display on ${phone1} using ${screenSaverDetails}
    [Teardown]    Default Background Configuration

762521: Http uses for image updation
    [Tags]    Owner:Surender    Reviewer:    backgroundImage
    Given Send ${backgroundImage} file to ${bgImages} folder on ${http} server
    Then Set Custom screensaver image on ${phone1} using ${http} server

    &{screenSaverDetails}=    CREATE DICTIONARY    screenSaverType=${custom}
    And Check the screensaver display on ${phone1} using ${screenSaverDetails}
    [Teardown]    Default Background Configuration

763584: Verify phone TUI support selecting custom ring tone
    [Tags]    Owner:Surender    Reviewer:    ringTone
    Given On ${phone1} move to ${audio} to ${ringTones} settings
    Then Press hardkey as ${enter} on ${phone1}
    Then On ${phone1} verify display message ${ringTones}
    Then Press hardkey as ${scrollDown} on ${phone1}
    Then On ${phone1} press the softkey ${save} in SettingState
    Then Press hardkey as ${goodBye} on ${phone1}
    Then Using ${PhoneWUI} log into ${phone1} URL
    Then Using ${PhoneWUI} Navigate to go to ${PreferencesMenu} page on ${phone1} URL
    Then Verify text Tone 2 for ${Preferences['GlobalRingTones']} on the ${phone1} URL
    Then Using ${PhoneWUI} logoff ${phone1} URL
    Then On ${phone1} move to ${audio} to ${ringTones} settings
    Then Press hardkey as ${enter} on ${phone1}
    Then On ${phone1} verify display message ${ringTones}
    Then Press hardkey as ${scrollUp} on ${phone1}
    Then On ${phone1} press the softkey ${save} in SettingState
    And Press hardkey as ${goodBye} on ${phone1}

762588: mask sip password: 1 - mask local.cfg
    [Tags]    Owner:Surender    Reviewer:    maskPassword
    [Setup]  Default Line Registeration Setup
    Given Using ${PhoneWUI} log into ${phone1} URL
    Then Using ${PhoneWUI} ${fully} unregister ${Line['all']} of ${phone1}
    Then Using ${PhoneWUI} logoff ${phone1} URL

    &{parameters}=    CREATE DICTIONARY    mask sip password=1
    Then Create startup.cfg file using ${parameters}
    Then Create ${automationTestingFolder} folder on FTP server
    Then Send startup.cfg file to ${automationTestingFolder} folder on FTP server
    &{configurationDetails}=    CREATE DICTIONARY    download protocol=FTP    ftp server=10.112.123.107
    ...                         ftp path=${automationTestingFolderPath}    ftp username=desktop    ftp password=desktop
    Then Configure parameters on ${phone1} using ${configurationDetails}
    Then Reboot ${phone1}

    Then Using ${PhoneWUI} log into ${phone1} URL
    Then Using ${PhoneWUI} register ${Line['all']} of ${phone1} with ${phone1}
    Then Using ${PhoneWUI} verify ${Line['first']} is registered on ${phone1}
    Then Using ${PhoneWUI} verify ${Line['second']} is registered on ${phone1}

    Then Using ${PhoneWUI} Navigate to go to ${TroubleShootingMenu} page on ${phone1} URL
    Then Using ${PhoneWUI} click on the ${TroubleshootLink['Get Local.cfg']} on ${phone1} URL
    Then Verify local.cfg file contains sip password:** of ${phone1}
    Then Using ${PhoneWUI} logoff ${phone1} URL
    [Teardown]    Default Line Registeration Teardown

762589: mask sip password: 1 - mask server.cfg -password in aastra.cfg
    [Tags]    Owner:Surender    Reviewer:    maskPassword
    [Setup]  Default Line Registeration Setup
    Given Using ${PhoneWUI} log into ${phone1} URL
    Then Using ${PhoneWUI} ${fully} unregister ${Line['all']} of ${phone1}
    Then Using ${PhoneWUI} logoff ${phone1} URL

    &{parameters}=    CREATE DICTIONARY    mask sip password=1    sip auth name=${phone1}    sip password=${phone1}
    ...                                    sip user name=${phone1}    sip display name=${phone1}
    ...                                    sip screen name=${phone1}    sip screen name 2=${phone1}
    ...                                    sip proxy ip=${${pbx}IP}    sip proxy port=5060
    ...                                    sip registrar ip=${${pbx}IP}    sip registrar port=5060
    ...                                    sip outbound proxy=${${pbx}IP}    sip outbound proxy port=5060
    Then Create aastra.cfg file using ${parameters}
    Then Create ${automationTestingFolder} folder on FTP server
    Then Send startup.cfg file to ${automationTestingFolder} folder on FTP server
    &{configurationDetails}=    CREATE DICTIONARY    download protocol=FTP    ftp server=10.112.123.107
    ...                         ftp path=${automationTestingFolderPath}    ftp username=desktop    ftp password=desktop
    Then Configure parameters on ${phone1} using ${configurationDetails}
    Then Reboot ${phone1}

    Then Using ${PhoneWUI} log into ${phone1} URL
    Then Using ${PhoneWUI} register ${Line['all']} of ${phone1} with ${phone1}
    Then Using ${PhoneWUI} verify ${Line['first']} is registered on ${phone1}
    Then Using ${PhoneWUI} verify ${Line['second']} is registered on ${phone1}

    Then Using ${PhoneWUI} Navigate to go to ${TroubleShootingMenu} page on ${phone1} URL
    Then Using ${PhoneWUI} click on the ${TroubleshootLink['Get Server.cfg']} on ${phone1} URL
    Then Verify server.cfg file contains sip password:** of ${phone1}
    Then Using ${PhoneWUI} logoff ${phone1} URL
    [Teardown]    Default Line Registeration Teardown

762590: mask sip password: 0 - unmask server.cfg
    [Tags]    Owner:Surender    Reviewer:    unmaskPassword
    [Setup]  Default Line Registeration Setup
    Given Using ${PhoneWUI} log into ${phone1} URL
    Then Using ${PhoneWUI} ${fully} unregister ${Line['all']} of ${phone1}
    Then Using ${PhoneWUI} logoff ${phone1} URL

    ${macAddress}=    Using ${PhoneWUI} Get MAC Address of ${phone1}
    &{parameters}=    CREATE DICTIONARY    mask sip password=0    sip auth name=${phone1}    sip password=${phone1}
    ...                                    sip user name=${phone1}    sip display name=${phone1}
    ...                                    sip screen name=${phone1}    sip screen name 2=${phone1}
    ...                                    sip proxy ip=${${pbx}IP}    sip proxy port=5060
    ...                                    sip registrar ip=${${pbx}IP}    sip registrar port=5060
    ...                                    sip outbound proxy=${${pbx}IP}    sip outbound proxy port=5060
    Then Create ${macAddress}.cfg file using ${parameters}
    Then Create ${automationTestingFolder} folder on FTP server
    Then Send ${macAddress}.cfg file to ${automationTestingFolder} folder on FTP server
    &{configurationDetails}=    CREATE DICTIONARY    download protocol=FTP    ftp server=10.112.123.107
    ...                         ftp path=${automationTestingFolderPath}    ftp username=desktop    ftp password=desktop
    Then Configure parameters on ${phone1} using ${configurationDetails}
    Then Reboot ${phone1}

    Then Using ${PhoneWUI} log into ${phone1} URL
    Then Using ${PhoneWUI} register ${Line['all']} of ${phone1} with ${phone1}
    Then Using ${PhoneWUI} verify ${Line['first']} is registered on ${phone1}
    Then Using ${PhoneWUI} verify ${Line['second']} is registered on ${phone1}

    Then Using ${PhoneWUI} Navigate to go to ${TroubleShootingMenu} page on ${phone1} URL
    Then Using ${PhoneWUI} click on the ${TroubleshootLink['Get Server.cfg']} on ${phone1} URL
    Then Verify server.cfg file contains sip password:${phone1} of ${phone1}
    And Using ${PhoneWUI} logoff ${phone1} URL
    [Teardown]    Default Line Registeration Teardown

763633: TC01: "Icon:CallFwdActive"
    [Tags]    Owner:Surender    Reviewer:    icon
    ${messageAttributes}=    CREATE DICTIONARY    index=1    type=icon
    ${attributesDetails}=    CREATE DICTIONARY    Message=${messageAttributes}
    ${xmlParameters}=    CREATE DICTIONARY    Session=Session    Message=DN    IconList=<Icon index="1">Icon:CallFwdActive</Icon>
    Given Create AastraIPPhoneStatus XML with the ${xmlParameters} and ${attributesDetails} for ${phone1}
    Then Send Automation.xml file to ${automationTesting} folder on HTTP server

    &{configurationDetails}=    CREATE DICTIONARY    top softkey3 type=xml    top softkey3 value=${httpServer}/${automationTesting}/Automation.xml
    ...                                              top softkey3 label=xml
    Given Configure parameters on ${phone1} using ${configurationDetails}
    Then On ${phone1} verify display message xml
    Then On ${phone1} press ${softkey} ${programKey3} for 1 times
    Then Verify ${callFwdActive} icon on banner of ${phone1}

    ${messageAttributes}=    CREATE DICTIONARY    index=1    type=icon
    ${attributesDetails}=    CREATE DICTIONARY    Message=${messageAttributes}
    ${xmlParameters}=    CREATE DICTIONARY    Session=Session    Message=DN    IconList=<Icon index="1">Icon:None</Icon>
    Given Create AastraIPPhoneStatus XML with the ${xmlParameters} and ${attributesDetails} for ${phone1}
    Then Send Automation.xml file to ${automationTesting} folder on HTTP server

    Then On ${phone1} press ${softkey} ${programKey3} for 1 times
    Then Verify ${callFwdActive} icon is not on banner of ${phone1}

    &{configurationDetails}=    CREATE DICTIONARY    top softkey3 type=none    top softkey3 value=
    ...                                              top softkey3 label=
    And Configure parameters on ${phone1} using ${configurationDetails}
    [Teardown]    Generic Test Teardown

763634: TC14: "Icon:RecordingOn"
    [Tags]    Owner:Surender    Reviewer:    icon
    ${messageAttributes}=    CREATE DICTIONARY    index=1    type=icon
    ${attributesDetails}=    CREATE DICTIONARY    Message=${messageAttributes}
    ${xmlParameters}=    CREATE DICTIONARY    Session=Session    Message=DN    IconList=<Icon index="1">Icon:RecordingOn</Icon>
    Given Create AastraIPPhoneStatus XML with the ${xmlParameters} and ${attributesDetails} for ${phone1}
    Then Send Automation.xml file to ${automationTesting} folder on HTTP server

    &{configurationDetails}=    CREATE DICTIONARY    top softkey3 type=xml    top softkey3 value=${httpServer}/${automationTesting}/Automation.xml
    ...                                              top softkey3 label=xml
    Given Configure parameters on ${phone1} using ${configurationDetails}
    Then On ${phone1} verify display message xml
    Then On ${phone1} press ${softkey} ${programKey3} for 1 times
    Then Verify ${callFwdActive} icon on banner of ${phone1}

    ${messageAttributes}=    CREATE DICTIONARY    index=1    type=icon
    ${attributesDetails}=    CREATE DICTIONARY    Message=${messageAttributes}
    ${xmlParameters}=    CREATE DICTIONARY    Session=Session    Message=DN    IconList=<Icon index="1">Icon:None</Icon>
    Given Create AastraIPPhoneStatus XML with the ${xmlParameters} and ${attributesDetails} for ${phone1}
    Then Send Automation.xml file to ${automationTesting} folder on HTTP server

    Then On ${phone1} press ${softkey} ${programKey3} for 1 times
    Then Verify ${callFwdActive} icon is not on banner of ${phone1}

    &{configurationDetails}=    CREATE DICTIONARY    top softkey3 type=none    top softkey3 value=
    ...                                              top softkey3 label=
    And Configure parameters on ${phone1} using ${configurationDetails}
    [Teardown]    Generic Test Teardown

763374: SIP 08
    [Tags]    Owner:Surender    Reviewer:    icon
    [Setup]  Default Line Registeration Setup
    &{parameters}=    CREATE DICTIONARY    sip aastra id=1
    Then Create startup.cfg file using ${parameters}
    Then Create ${automationTestingFolder} folder on FTP server
    Then Send startup.cfg file to ${automationTestingFolder} folder on FTP server
    &{configurationDetails}=    CREATE DICTIONARY    download protocol=FTP    ftp server=10.112.123.107
    ...                         ftp path=${automationTestingFolderPath}    ftp username=desktop    ftp password=desktop
    Then Configure parameters on ${phone1} using ${configurationDetails}
    Then Reboot ${phone1}

    ${firmwareVersion}=    Get Firmware Version of ${phone1}

    Then Using ${PhoneWUI} log into ${phone1} URL
    Then Using ${PhoneWUI} ${partially} unregister ${Line['all']} of ${phone1}
    Then Using ${PhoneWUI} Start the capture on ${all} port on ${phone1} URL
    Then Using ${PhoneWUI} register ${Line['all']} of ${phone1} with ${phone1}
    Then Using ${PhoneWUI} verify ${Line['first']} is registered on ${phone1}
    Then Using ${PhoneWUI} verify ${Line['second']} is registered on ${phone1}
    Then Using ${PhoneWUI} ${stop} the capture from ${phone1} URL
    Then Using ${PhoneWUI} ${download} the capture from ${phone1} URL
    Then Verify the captureFile.pcap contains version=${firmwareVersion} inside ${Protocols['SIP(Register)']} packets of ${phone1}
    Then Using ${PhoneWUI} logoff ${phone1} URL
    [Teardown]    Default Line Registeration Teardown

762877: TC012
    [Tags]    Owner:Surender    Reviewer:    icon
    &{configurationDetails}=    CREATE DICTIONARY    collapsed softkey screen=0    expmod1 key2 type=${blf}
    ...                         expmod1 key2 label=${blf}    expmod1 key2 value=${phone2}    expmod1 key4 type=${blf}
    ...                         expmod1 key4 label=${blf}    expmod1 key4 value=${phone2}
    Given Configure parameters on ${phone1} using ${configurationDetails}
    Then verify display message ${blf} on PKM for ${phone1}
    Then I want to make a two party call between ${phone1} and ${phone2} using ${offHook}
    Then Verify ringing state on ${phone1} and ${phone2}
    Then Verify the PKM led state of ${line1} as ${off} on ${phone1}
    Then Verify the PKM led state of ${line2} as ${blink} on ${phone1}
    Then Verify the PKM led state of ${line3} as ${off} on ${phone1}
    Then Verify the PKM led state of ${line4} as ${blink} on ${phone1}
    Then Disconnect the call from ${phone1}

    &{configurationDetails}=    CREATE DICTIONARY    expmod1 key2 type=none    expmod1 key2 label=    expmod1 key2 value=
    ...                         expmod1 key4 type=none    expmod1 key4 label=    expmod1 key4 value=
    And Configure parameters on ${phone1} using ${configurationDetails}

761930: TC_44
    [Tags]    Owner:Surender    Reviewer:    uploadDirectory
    ${details}=    Create Dictionary     firstName=HCL     lastName=Noida    number=${phone2}
    Given Delete all entries from directry of ${phone1}
    Then Create ${directoryFile} file using ${details}
    Then using ${PhoneWUI} Log Into ${phone1} URL
    Then create ${directoryFile} file for ${phone2} using ${details}
    Then Using ${PhoneWUI} click on the ${DirectoryMenu} on ${phone1} URL
    Then using ${PhoneWUI} select the ${DirectoryLink['ChooseFile']} and upload file ${directoryFile} on ${phone1} URL
    Then using ${PhoneWUI} logoff ${phone1} URL
    Then press hardkey as ${directory} on ${phone1}
    Then on ${phone1} verify display message HCL
    And Delete all entries from directry of ${phone1}

761931: TC_45
    [Tags]    Owner:Surender    Reviewer:
    ${details}=    Create Dictionary     firstName=HCL     lastName=Noida    number=${phone2}
    Given Delete all entries from directry of ${phone1}
    Then Create ${directoryFile} file using ${details}
    Then using ${PhoneWUI} Log Into ${phone1} URL
    Then create ${directoryFile} file for ${phone2} using ${details}
    Then Using ${PhoneWUI} click on the ${DirectoryMenu} on ${phone1} URL
    Then using ${PhoneWUI} select the ${DirectoryLink['ChooseFile']} and upload file ${directoryFile} on ${phone1} URL
    Then using ${PhoneWUI} logoff ${phone1} URL
    Then press hardkey as ${directory} on ${phone1}
    Then on ${phone1} verify display message ${phone2}
    And Delete all entries from directry of ${phone1}

762533: LLDP_004
    [Tags]    Owner:Vikhyat    Reviewer:    lldp    Vikhyat112    22/09/2020
    Given On ${phone1} move to ${network} to ${lldp} settings
    Then Press hardkey as ${scrollUp} on ${phone1}
    Then On ${phone1} press the softkey ${save} in SettingState
    Then Press hardkey as ${enter} on ${phone1}
    Then Press hardkey as ${goodBye} on ${phone1}
    Then On ${phone1} move to ${network} to ${lldp} settings
    Then Verify Disabled text is highlighted on screen of ${phone1}
    Then Press hardkey as ${scrollDown} on ${phone1}
    Then Verify Enabled text is highlighted on screen of ${phone1}
    Then Press hardkey as ${enter} on ${phone1}
    And Press hardkey as ${goodBye} on ${phone1}


762164: TC008
    &{parameters} =  Create Dictionary    image server uri: http://10.211.43.105/Images/3003.png
    Then Create ${startUp} file using ${parameters}
    Then Create ${systeminfo} folder on FTP server
    Then Send ${startUp} file to ${systeminfo} folder on FTP server
    Then reboot ${phone2}
    Then i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then Verify the led state of ${line1} as ${on} on ${phone2}
    Then disconnect the call from ${phone1}
    Then Press the call history button on ${phone1} and folder ${outgoing} and ${nothing}
    Then Verify ${pictureId} icons on ${phone1}
    And Press hardkey as ${goodBye} on ${phone1}

763368: TC24 - DTMF (SIP INFO) - asymmetric tls signalling
    [Tags]    Owner:Milind    Reviewer:    Ramkumar
    &{Details} =  Create Dictionary    DownloadProtocol=FTP    FTP_Server=10.112.123.107    FTP_Username=desktop    FTP_Password=desktop    FTP_Path=systeminfo
    &{parameters} =  Create Dictionary    sips symmetric tls signaling= 0    sip contact port override= 1
    Given I want to configure ConfigurationServer parameters using ${Details} for ${phone1}
    Then Create ${startUp} file using ${parameters}
    Then Create ${systeminfo} folder on FTP server
    Then Send ${startUp} file to ${systeminfo} folder on FTP server
    Then using ${PhoneWUI} Log Into ${phone1} URL
    Then using ${PhoneWUI} Navigate to go to ${GlobalSIPMenu} page on ${phone1} URL
    Then Go to the ${GlobalSIP['TransportProtocol']} option and select the ${PersistentTLS} value
    Then Go to the ${GlobalSIP['DTMFMethod']} option and select the ${SIPINFO} value
    Then Using ${PhoneWUI} click on the ${GlobalSIP['SaveSettings']} on ${phone1} URL
    Then Using ${PhoneWUI} logoff ${phone1} URL
    Then reboot ${phone1}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then Press DTMF key ${dialPad1} on ${phone1} and verify tone played on ${phone1}
    Then Press DTMF key ${dialPad2} on ${phone1} and verify tone played on ${phone1}
    Then Press DTMF key ${dialPad3} on ${phone1} and verify tone played on ${phone1}
    Then Press DTMF key ${dialPad4} on ${phone1} and verify tone played on ${phone1}
    Then Press DTMF key ${dialPad1} on ${phone1} and verify tone played on ${phone2}
    Then Press DTMF key ${dialPad2} on ${phone1} and verify tone played on ${phone2}
    Then Press DTMF key ${dialPad3} on ${phone1} and verify tone played on ${phone2}
    Then Press DTMF key ${dialPad4} on ${phone1} and verify tone played on ${phone2}

    Then Press DTMF key ${dialPad5} on ${phone2} and verify tone played on ${phone2}
    Then Press DTMF key ${dialPad6} on ${phone2} and verify tone played on ${phone2}
    Then Press DTMF key ${dialPad7} on ${phone2} and verify tone played on ${phone2}
    Then Press DTMF key ${dialPad8} on ${phone2} and verify tone played on ${phone2}
    Then Press DTMF key ${dialPad9} on ${phone2} and verify tone played on ${phone2}
    Then Press DTMF key ${dialPad5} on ${phone2} and verify tone played on ${phone1}
    Then Press DTMF key ${dialPad6} on ${phone2} and verify tone played on ${phone1}
    Then Press DTMF key ${dialPad7} on ${phone2} and verify tone played on ${phone1}
    Then Press DTMF key ${dialPad8} on ${phone2} and verify tone played on ${phone1}
    Then Press DTMF key ${dialPad9} on ${phone2} and verify tone played on ${phone1}
    Then disconnect the call from ${phone1}

763369: TC45 - DTMF (SIP INO) - symmetric UDP signalling, port override disabled
    [Tags]    Owner:Milind    Reviewer:    Ramkumar
    &{Details} =  Create Dictionary    DownloadProtocol=FTP    FTP_Server=10.112.123.107    FTP_Username=desktop    FTP_Password=desktop    FTP_Path=systeminfo
    &{parameters} =  Create Dictionary    sip symmetric udp signaling= 1    sip contact port override= 0
    Given I want to configure ConfigurationServer parameters using ${Details} for ${phone1}
    Then Create ${startUp} file using ${parameters}
    Then Create ${systeminfo} folder on FTP server
    Then Send ${startUp} file to ${systeminfo} folder on FTP server
    Then using ${PhoneWUI} Log Into ${phone1} URL
    Then using ${PhoneWUI} Navigate to go to ${GlobalSIPMenu} page on ${phone1} URL
    Then Go to the ${GlobalSIP['TransportProtocol']} option and select the ${UDP} value
    Then Go to the ${GlobalSIP['DTMFMethod']} option and select the ${SIPINFO} value
    Then Using ${PhoneWUI} click on the ${GlobalSIP['SaveSettings']} on ${phone1} URL
    Then Using ${PhoneWUI} logoff ${phone1} URL
    Then reboot ${phone1}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then Press DTMF key ${dialPad1} on ${phone1} and verify tone played on ${phone1}
    Then Press DTMF key ${dialPad2} on ${phone1} and verify tone played on ${phone1}
    Then Press DTMF key ${dialPad3} on ${phone1} and verify tone played on ${phone1}
    Then Press DTMF key ${dialPad4} on ${phone1} and verify tone played on ${phone1}
    Then Press DTMF key ${dialPad1} on ${phone1} and verify tone played on ${phone2}
    Then Press DTMF key ${dialPad2} on ${phone1} and verify tone played on ${phone2}
    Then Press DTMF key ${dialPad3} on ${phone1} and verify tone played on ${phone2}
    Then Press DTMF key ${dialPad4} on ${phone1} and verify tone played on ${phone2}

    Then Press DTMF key ${dialPad5} on ${phone2} and verify tone played on ${phone2}
    Then Press DTMF key ${dialPad6} on ${phone2} and verify tone played on ${phone2}
    Then Press DTMF key ${dialPad7} on ${phone2} and verify tone played on ${phone2}
    Then Press DTMF key ${dialPad8} on ${phone2} and verify tone played on ${phone2}
    Then Press DTMF key ${dialPad9} on ${phone2} and verify tone played on ${phone2}
    Then Press DTMF key ${dialPad5} on ${phone2} and verify tone played on ${phone1}
    Then Press DTMF key ${dialPad6} on ${phone2} and verify tone played on ${phone1}
    Then Press DTMF key ${dialPad7} on ${phone2} and verify tone played on ${phone1}
    Then Press DTMF key ${dialPad8} on ${phone2} and verify tone played on ${phone1}
    Then Press DTMF key ${dialPad9} on ${phone2} and verify tone played on ${phone1}
    Then disconnect the call from ${phone1}

763371: TC58 - DTMF (SIP INO) - asymmetric UDP signalling
    [Tags]    Owner:Milind    Reviewer:    Ramkumar
    &{Details} =  Create Dictionary    DownloadProtocol=FTP    FTP_Server=10.112.123.107    FTP_Username=desktop    FTP_Password=desktop    FTP_Path=systeminfo
    &{parameters} =  Create Dictionary    sip symmetric udp signaling= 0    sip contact port override= 1    sip outbound support= 1
    Given I want to configure ConfigurationServer parameters using ${Details} for ${phone1}
    Then Create ${startUp} file using ${parameters}
    Then Create ${systeminfo} folder on FTP server
    Then Send ${startUp} file to ${systeminfo} folder on FTP server
    Then using ${PhoneWUI} Log Into ${phone1} URL
    Then using ${PhoneWUI} Navigate to go to ${GlobalSIPMenu} page on ${phone1} URL
    Then Go to the ${GlobalSIP['TransportProtocol']} option and select the ${UDP} value
    Then Go to the ${GlobalSIP['DTMFMethod']} option and select the ${SIPINFO} value
    Then Using ${PhoneWUI} click on the ${GlobalSIP['SaveSettings']} on ${phone1} URL
    Then Using ${PhoneWUI} logoff ${phone1} URL
    Then reboot ${phone1}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then Press DTMF key ${dialPad1} on ${phone1} and verify tone played on ${phone1}
    Then Press DTMF key ${dialPad2} on ${phone1} and verify tone played on ${phone1}
    Then Press DTMF key ${dialPad3} on ${phone1} and verify tone played on ${phone1}
    Then Press DTMF key ${dialPad4} on ${phone1} and verify tone played on ${phone1}
    Then Press DTMF key ${dialPad1} on ${phone1} and verify tone played on ${phone2}
    Then Press DTMF key ${dialPad2} on ${phone1} and verify tone played on ${phone2}
    Then Press DTMF key ${dialPad3} on ${phone1} and verify tone played on ${phone2}
    Then Press DTMF key ${dialPad4} on ${phone1} and verify tone played on ${phone2}

    Then Press DTMF key ${dialPad5} on ${phone2} and verify tone played on ${phone2}
    Then Press DTMF key ${dialPad6} on ${phone2} and verify tone played on ${phone2}
    Then Press DTMF key ${dialPad7} on ${phone2} and verify tone played on ${phone2}
    Then Press DTMF key ${dialPad8} on ${phone2} and verify tone played on ${phone2}
    Then Press DTMF key ${dialPad9} on ${phone2} and verify tone played on ${phone2}
    Then Press DTMF key ${dialPad5} on ${phone2} and verify tone played on ${phone1}
    Then Press DTMF key ${dialPad6} on ${phone2} and verify tone played on ${phone1}
    Then Press DTMF key ${dialPad7} on ${phone2} and verify tone played on ${phone1}
    Then Press DTMF key ${dialPad8} on ${phone2} and verify tone played on ${phone1}
    Then Press DTMF key ${dialPad9} on ${phone2} and verify tone played on ${phone1}
    Then disconnect the call from ${phone1}

763125: Switch on `suppress incoming dtmf playback` in <mac>.cfg config file and check that the incoming DTMF codes in SIP INFO packets are not played back
    [Tags]    Owner:Milind    Reviewer:    Ramkumar
    &{Details} =  Create Dictionary    DownloadProtocol=FTP    FTP_Server=10.112.123.107    FTP_Username=desktop    FTP_Password=desktop    FTP_Path=systeminfo
    &{parameters} =  Create Dictionary    suppress incoming dtmf playback= 1
    Given I want to configure ConfigurationServer parameters using ${Details} for ${phone1}
    ${macAddress}=    Using ${PhoneWUI} Get MAC Address of ${phone1}
    Then Create ${macAddress}.cfg file using ${parameters}
    Then Send ${macAddress}.cfg file to systeminfo folder on FTP server
    Given using ${PhoneWUI} Log Into ${phone1} URL
    Then using ${PhoneWUI} Navigate to go to ${GlobalSIPMenu} page on ${phone1} URL
    Then Go to the ${GlobalSIP['TransportProtocol']} option and select the ${UDP} value
    Then Go to the ${GlobalSIP['DTMFMethod']} option and select the ${SIPINFO} value
    Then Using ${PhoneWUI} click on the ${GlobalSIP['SaveSettings']} on ${phone1} URL
    Then Using ${PhoneWUI} logoff ${phone1} URL
    Then reboot ${phone1}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then Press DTMF key ${dialPad1} on ${phone2} and verify tone is not played on ${phone1}
    Then Press DTMF key ${dialPad2} on ${phone2} and verify tone is not played on ${phone1}
    Then Press DTMF key ${dialPad3} on ${phone2} and verify tone is not played on ${phone1}
    Then Press DTMF key ${dialPad4} on ${phone2} and verify tone is not played on ${phone1}
    Then Press DTMF key ${dialPad5} on ${phone2} and verify tone is not played on ${phone1}
    Then Press DTMF key ${dialPad6} on ${phone2} and verify tone is not played on ${phone1}
    Then Press DTMF key ${dialPad7} on ${phone2} and verify tone is not played on ${phone1}
    Then Press DTMF key ${dialPad8} on ${phone2} and verify tone is not played on ${phone1}
    Then Press DTMF key ${dialPad9} on ${phone2} and verify tone is not played on ${phone1}
    Then Press DTMF key ${dialPad*} on ${phone2} and verify tone is not played on ${phone1}
    Then Press DTMF key ${dialPad#} on ${phone2} and verify tone is not played on ${phone1}
    Then disconnect the call from ${phone1}

763126: Switch on `suppress incoming dtmf playback` and check that outgoing DTMF codes are properly sent in SIP INFO packets
    [Tags]    Owner:Milind    Reviewer:    Ramkumar
    &{Details} =  Create Dictionary    DownloadProtocol=FTP    FTP_Server=10.112.123.107    FTP_Username=desktop    FTP_Password=desktop    FTP_Path=systeminfo
    &{parameters} =  Create Dictionary    suppress incoming dtmf playback= 1
    Given using ${PhoneWUI} Log Into ${phone1} URL
    Then using ${PhoneWUI} Navigate to go to ${GlobalSIPMenu} page on ${phone1} URL
    Then Go to the ${GlobalSIP['TransportProtocol']} option and select the ${UDP} value
    Then Go to the ${GlobalSIP['DTMFMethod']} option and select the ${SIPINFO} value
    Then Using ${PhoneWUI} click on the ${GlobalSIP['SaveSettings']} on ${phone1} URL
    Then Using ${PhoneWUI} logoff ${phone1} URL
    Given I want to configure ConfigurationServer parameters using ${Details} for ${phone1}
    Then Create ${startUp} file using ${parameters}
    Then Create ${systeminfo} folder on FTP server
    Then Send ${startUp} file to ${systeminfo} folder on FTP server
    Then reboot ${phone1}
    Then Using ${PhoneWUI} Start the capture on all port on ${phone1} URL
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then Using ${PhoneWUI} Start the capture on all port on ${phone1} URL
    Then press hardkey as DialPad1 on ${phone1}
    Then press hardkey as DialPad2 on ${phone1}
    Then press hardkey as DialPad3 on ${phone1}
    Then press hardkey as DialPad4 on ${phone1}
    Then press hardkey as DialPad5 on ${phone1}
    Then press hardkey as DialPad6 on ${phone1}
    Then press hardkey as DialPad7 on ${phone1}
    Then press hardkey as DialPad8 on ${phone1}
    Then press hardkey as DialPad9 on ${phone1}
    Then On ${phone1} Wait for 3 seconds
    Then disconnect the call from ${phone1}
    Then Using ${PhoneWUI} ${stop} the capture from ${phone1} URL
    Then Using ${PhoneWUI} ${download} the capture from ${phone1} URL
    Then Verify the captureFile contains Signal= 1 inside ${Protocols[‘SIP(Info)’]} packets of ${phone1}
    Then Verify the captureFile contains Signal= 2 inside ${Protocols[‘SIP(Info)’]} packets of ${phone1}
    Then Verify the captureFile contains Signal= 3 inside ${Protocols[‘SIP(Info)’]} packets of ${phone1}
    Then Verify the captureFile contains Signal= 4 inside ${Protocols[‘SIP(Info)’]} packets of ${phone1}
    Then Verify the captureFile contains Signal= 5 inside ${Protocols[‘SIP(Info)’]} packets of ${phone1}
    Then Verify the captureFile contains Signal= 6 inside ${Protocols[‘SIP(Info)’]} packets of ${phone1}
    Then Verify the captureFile contains Signal= 7 inside ${Protocols[‘SIP(Info)’]} packets of ${phone1}
    Then Verify the captureFile contains Signal= 8 inside ${Protocols[‘SIP(Info)’]} packets of ${phone1}
    Then Verify the captureFile contains Signal= 9 inside ${Protocols[‘SIP(Info)’]} packets of ${phone1}

763127 Switch on `suppress incoming dtmf playback` in aastra.cfg config file and check that the incoming DTMF codes in telephone-events SRTP packets are not played back
    [Tags]    Owner:Milind    Reviewer:    Ramkumar
    &{Details} =  Create Dictionary    DownloadProtocol=FTP    FTP_Server=10.112.123.107    FTP_Username=desktop    FTP_Password=desktop    FTP_Path=systeminfo
    &{parameters} =  Create Dictionary    suppress incoming dtmf playback= 1
    Given using ${PhoneWUI} Log Into ${phone1} URL
    Then using ${PhoneWUI} Navigate to go to ${GlobalSIPMenu} page on ${phone1} URL
    Then Go to the ${GlobalSIP['TransportProtocol']} option and select the ${UDP} value
    Then Go to the ${GlobalSIP['DTMFMethod']} option and select the ${RTP} value
    Then Using ${PhoneWUI} click on the ${GlobalSIP['SaveSettings']} on ${phone1} URL
    Then Using ${PhoneWUI} logoff ${phone1} URL
    Given I want to configure ConfigurationServer parameters using ${Details} for ${phone1}
    Given Create aastra.cfg file using ${parameters}
    Then Create ${systeminfo} folder on FTP server
    Then Send aastra.cfg file to ${systeminfo} folder on FTP server
    Then reboot ${phone1}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Press DTMF key ${dialPad1} on ${phone2} and verify tone is not played on ${phone1}
    Press DTMF key ${dialPad2} on ${phone2} and verify tone is not played on ${phone1}
    Press DTMF key ${dialPad3} on ${phone2} and verify tone is not played on ${phone1}
    Press DTMF key ${dialPad4} on ${phone2} and verify tone is not played on ${phone1}
    Press DTMF key ${dialPad5} on ${phone2} and verify tone is not played on ${phone1}
    Press DTMF key ${dialPad6} on ${phone2} and verify tone is not played on ${phone1}
    Press DTMF key ${dialPad7} on ${phone2} and verify tone is not played on ${phone1}
    Press DTMF key ${dialPad8} on ${phone2} and verify tone is not played on ${phone1}
    Press DTMF key ${dialPad9} on ${phone2} and verify tone is not played on ${phone1}
    Then disconnect the call from ${phone1}

763426: TC057
    [Tags]    Owner:Milind    Reviewer:    Ramkumar
    &{configurationDetails}=    CREATE DICTIONARY    collapsed softkey screen=0    topsoftkey3 type=xml    topsoftkey3 label=Title
                               ...  topsoftkey3 value=http://10.112.123.89/XML/DesktopXML/AastraIPPhoneInputScreen/DefaultTopTitle.xml
    Given configure parameters on ${phone1} using ${configurationdetails}
    Then i want to press line key ${programKey3} on phone ${phone1}
    Then On ${phone1} Wait for 2 seconds
    Then On ${phone1} verify display message Application
    And Press hardkey as ${goodBye} on ${phone1}
    [Teardown]  I want to program ${none} key on position 3 on ${phone1}

763427: TC058
    [Tags]    Owner:Milind    Reviewer:    Ramkumar
    &{configurationDetails}=    CREATE DICTIONARY    collapsed softkey screen=0    topsoftkey3 type=xml    topsoftkey3 label=Title
                               ...  topsoftkey3 value=http://10.112.123.89/XML/DesktopXML/AastraIPPhoneInputScreen/TopTitleProvided.xml
    Given configure parameters on ${phone1} using ${configurationdetails}
    Then i want to press line key ${programKey3} on phone ${phone1}
    Then On ${phone1} Wait for 2 seconds
    Then On ${phone1} verify display message TopTitle
    And Press hardkey as ${goodBye} on ${phone1}
    [Teardown]  I want to program ${none} key on position 3 on ${phone1}

763434: TC068
    [Tags]    Owner:Milind    Reviewer:    Ramkumar
    &{configurationDetails}=    CREATE DICTIONARY    collapsed softkey screen=0    topsoftkey3 type=xml    topsoftkey3 label=Title
                               ...  topsoftkey3 value=http://10.112.123.89/XML/DesktopXML/AastraIPPhoneTextMenu//TopTitleProvided.xml
    Given configure parameters on ${phone1} using ${configurationdetails}
    Then i want to press line key ${programKey3} on phone ${phone1}
    Then On ${phone1} Wait for 2 seconds
    Then On ${phone1} verify display message TextMenuTopTitle
    And Press hardkey as ${goodBye} on ${phone1}
    [Teardown]  I want to program ${none} key on position 3 on ${phone1}

766583: Long Press_DTMF tone_dtmf method:RTP_sip out-of-band dtmf: Disabled
    [Tags]    Owner:Milind    Reviewer:    Ramkumar
    Given using ${PhoneWUI} Log Into ${phone1} URL
    Then using ${PhoneWUI} Navigate to go to ${GlobalSIPMenu} page on ${phone1} URL
    Then Go to the ${GlobalSIP['TransportProtocol']} option and select the ${UDP} value
    Then Go to the ${GlobalSIP['DTMFMethod']} option and select the ${RTP} value
    Then Using ${PhoneWUI} click on the ${GlobalSIP['SaveSettings']} on ${phone1} URL
    Then Using ${PhoneWUI} logoff ${phone1} URL
    Then Using ${PhoneWUI} start the capture on all port on ${phone1} URL
    Given I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then Long Press DTMF key ${dialPad0} on ${phone1} and verify tone played on ${phone1}
    Then Long Press DTMF key ${dialPad0} on ${phone1} and verify tone played on ${phone2}
    Then On ${phone1} Wait for 3 seconds
    Then Using ${PhoneWUI} ${stop} the capture from ${phone1} URL
    Then Using ${PhoneWUI} ${download} the capture from ${phone1} URL
    Then Verify the captureFile contains Event ID: Flash (16) inside ${Protocols['RTPEvent']} packets of ${phone1}

761911: Call on ringing phone can be pickup
    [Tags]    Owner:Milind    Reviewer:Vikyat
    &{configurationDetails}=    CREATE DICTIONARY    collapsed softkey screen=0     directed call pickup=1     directed call pickup prefix=*86
    Given Configure parameters on ${phone1} using ${configurationDetails}
    Then On ${phone1} program ${blf} key on position 4 with ${phone2} value
    Then On ${phone1} verify display message ${blf}
    Then I want to make a two party call between ${phone3} and ${phone2} using ${loudspeaker}
    Then verify the led state of ${line4} as ${blink} on ${phone1}
    Then answer the call on ${phone1} using ${programKey4}
    Then Verify audio path between ${phone1} and ${phone3}
    Then verify the caller id on ${phone1} and ${phone3} display
    Then disconnect the call from ${phone3}
    And I want to program ${none} key on position 4 on ${phone1}

761912: Held Call Pickup on softkey
    [Tags]    Owner:Milind    Reviewer:Vikyat
    &{configurationDetails}=    CREATE DICTIONARY    collapsed softkey screen=0     directed call pickup=1     directed call pickup prefix=*86
    Given Configure parameters on ${phone1} using ${configurationDetails}
    Then On ${phone1} program ${blf} key on position 4 with ${phone2} value
    Then On ${phone1} verify display message ${blf}
    Then I want to make a two party call between ${phone3} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then press hardkey as ${holdState} on ${phone2}
    Then verify the led state of ${line1} as ${blink} on ${phone2}
    Then press softkey ${programKey4} on ${phone1}
    Then verify the led state of ${line1} as ${on} on ${phone1}
    Then Verify audio path between ${phone1} and ${phone3}
    Then verify the caller id on ${phone1} and ${phone3} display
    Then disconnect the call from ${phone3}
    And I want to program ${none} key on position 4 on ${phone1}

761988: AstBLF_009
    [Tags]    Owner:Milind    Reviewer:Vikyat
    &{configurationDetails}=  CREATE DICTIONARY    expmod1 key1 type=blf    expmod1 key1 label=BLF
    ...                                            expmod1 key1 value=${phone2}
    Given Configure parameters on ${phone1} using ${configurationDetails}
    Then verify display message BLF on PKM for ${phone1}
    Then I want to make a two party call between ${phone3} and ${phone2} using ${loudspeaker}
    Then Verify the PKM led state of ${line1} as ${blink} on ${phone1}
    Then disconnect the call from ${phone3}
     &{configurationDetails}=  CREATE DICTIONARY    expmod1 key1 type=none    expmod1 key1 label=    expmod1 key1 value=
    Then Configure parameters on ${phone1} using ${configurationDetails}

#BLF Subscirption
762376: CODEC –002
    [Tags]    Owner:Milind    Reviewer:Vikyat    notAplicableFor6865
    &{configurationDetails}=    CREATE DICTIONARY    collapsed softkey screen=0
    &{globalSipdetails}=    CREATE DICTIONARY    AuthName=${phone4}
    Given Configure parameters on ${phone1} using ${configurationDetails}
    Then On ${phone1} program ${blf} key on position 4 with ${phone2} value
    Then On ${phone1} verify display message ${blf}
    Then On ${phone1} verify ${line4} icon state as ${blfStatusGreen}
    Then I want to configure GlobalSettings parameters using &{globalSipdetails} for ${phone1}
    Then On ${phone1} Wait for 3 seconds
    Then On ${phone1} verify ${line4} icon state as ${blfStatusQuestion}
    Then On ${phone1} Wait for 15 seconds
    Then On ${phone1} verify ${line4} icon state as ${blfStatusGreen}
    Then Register the ${phone1} on ${MxOne} pbx
    Then On ${phone1} Wait for 5 seconds
    Then I want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then I want to configure GlobalSettings parameters using &{globalSipdetails} for ${phone1}
    Then On ${phone1} Wait for 5 seconds
    Then On ${phone1} verify ${line4} icon state as ${blfStatusGreen}
    Then disconnect the call from ${phone3}
    Then On ${phone1} Wait for 5 seconds
    Then On ${phone1} verify ${line4} icon state as ${blfStatusQuestion}
    Then Register the ${phone1} on ${MxOne} pbx
    Then On ${phone1} Wait for 5 seconds
    Then On ${phone1} verify ${line4} icon state as ${blfStatusGreen}
    Then Register the ${phone4} on ${MxOne} pbx
    [Teardown]  Default Phone state

762377: CODEC –006
    [Tags]    Owner:Milind    Reviewer:Vikyat    notAplicableFor6865
    &{configurationDetails}=    CREATE DICTIONARY    collapsed softkey screen=0
    Given Configure parameters on ${phone1} using ${configurationDetails}
    Then On ${phone1} program ${blf} key on position 4 with ${phone2} value
    Then On ${phone1} verify display message ${blf}
    Then On ${phone1} verify ${line4} icon state as ${blfStatusGreen}
    Then Using ${PhoneWUI} log into ${phone1} URL
    Then Using ${PhoneWUI} Navigate to go to ${GlobalSIPMenu} page on ${phone1} URL
    Then Using ${PhoneWUI} send ${empty} value for ${GlobalSIP['ProxyServer']} to ${phone1} URL
    Then Using ${PhoneWUI} click on the ${GlobalSIP['SaveSettings']} on ${phone1} URL
    Then Using ${PhoneWUI} logoff ${phone1} URL
    Then On ${phone1} Wait for 2 seconds
    Then On ${phone1} verify ${line4} icon state as ${blfStatusQuestion}
    Then Register the ${phone1} on ${MxOne} pbx
    Then On ${phone1} Wait for 5 seconds
    Then On ${phone1} verify ${line4} icon state as ${blfStatusGreen}
    Then I want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then I want to configure GlobalSettings parameters using &{globalSipdetails} for ${phone1}
    Then On ${phone1} Wait for 5 seconds
    Then On ${phone1} verify ${line4} icon state as ${blfStatusGreen}
    Then disconnect the call from ${phone3}
    Then On ${phone1} Wait for 5 seconds
    Then On ${phone1} verify ${line4} icon state as ${blfStatusQuestion}
    Then Register the ${phone1} on ${MxOne} pbx
    Then On ${phone1} Wait for 5 seconds
    Then On ${phone1} verify ${line4} icon state as ${blfStatusGreen}
    Then Register the ${phone4} on ${MxOne} pbx
    [Teardown]  Default Phone state

762380: CODEC –047
    [Tags]    Owner:Milind    Reviewer:Vikyat    notAplicableFor6865
    &{configurationDetails}=    CREATE DICTIONARY    collapsed softkey screen=0
    Given Configure parameters on ${phone1} using ${configurationDetails}
    Then On ${phone1} program ${blf} key on position 4 with ${phone2} value
    Then On ${phone1} verify display message ${blf}
    Then On ${phone1} verify ${line4} icon state as ${blfStatusGreen}
    Then Using ${PhoneWUI} log into ${phone1} URL
    Then Using ${PhoneWUI} Navigate to go to ${GlobalSIPMenu} page on ${phone1} URL
    Then Using ${PhoneWUI} click on the ${GlobalSIP['ExplicitMessageWaitingSubscription']} on ${phone1} URL
    Then Using ${PhoneWUI} send ${empty} value for ${GlobalSIP['ProxyServer']} to ${phone1} URL
    Then Using ${PhoneWUI} click on the ${GlobalSIP['SaveSettings']} on ${phone1} URL
    Then Using ${PhoneWUI} logoff ${phone1} URL
    Then On ${phone1} Wait for 2 seconds
    Then On ${phone1} verify ${line4} icon state as ${blfStatusQuestion}
    Then Register the ${phone1} on ${MxOne} pbx
    Then On ${phone1} Wait for 5 seconds
    Then On ${phone1} verify ${line4} icon state as ${blfStatusGreen}
    Then I want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then Using ${PhoneWUI} log into ${phone1} URL
    Then Using ${PhoneWUI} Navigate to go to ${GlobalSIPMenu} page on ${phone1} URL
    Then Using ${PhoneWUI} send ${empty} value for ${GlobalSIP['ProxyServer']} to ${phone1} URL
    Then Using ${PhoneWUI} click on the ${GlobalSIP['SaveSettings']} on ${phone1} URL
    Then Using ${PhoneWUI} logoff ${phone1} URL
    Then On ${phone1} Wait for 5 seconds
    Then On ${phone1} verify ${line4} icon state as ${blfStatusGreen}
    Then disconnect the call from ${phone3}
    Then On ${phone1} Wait for 5 seconds
    Then On ${phone1} verify ${line4} icon state as ${blfStatusQuestion}
    Then Register the ${phone1} on ${MxOne} pbx
    Then On ${phone1} Wait for 5 seconds
    Then On ${phone1} verify ${line4} icon state as ${blfStatusGreen}
    [Teardown]  Default Phone state

762378: CODEC –013
    [Tags]    Owner:Milind    Reviewer:Vikhyat    notAplicableFor6865
    &{configurationDetails}=    CREATE DICTIONARY    collapsed softkey screen=0
    Given Configure parameters on ${phone1} using ${configurationDetails}
    Then On ${phone1} program ${blf} key on position 4 with ${phone2} value
    Then On ${phone1} verify display message ${blf}
    Then On ${phone1} verify ${line4} icon state as ${blfStatusGreen}
    Then Using ${PhoneWUI} log into ${phone1} URL
    Then Using ${PhoneWUI} Navigate to go to ${GlobalSIPMenu} page on ${phone1} URL
    Then Using ${PhoneWUI} send ${empty} value for ${GlobalSIP['PhoneNumber']} to ${phone1} URL
    Then Using ${PhoneWUI} logoff ${phone1} URL
    Then On ${phone1} Wait for 3 seconds
    Then On ${phone1} verify ${line4} icon state as ${blfStatusQuestion}
    Then Register the ${phone1} on ${MxOne} pbx
    Then On ${phone1} Wait for 5 seconds
    Then On ${phone1} verify ${line4} icon state as ${blfStatusGreen}
    Then I want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then Using ${PhoneWUI} Navigate to go to ${GlobalSIPMenu} page on ${phone1} URL
    Then Using ${PhoneWUI} send ${empty} value for ${GlobalSIP['PhoneNumber']} to ${phone1} URL
    Then Using ${PhoneWUI} logoff ${phone1} URL
    Then On ${phone1} Wait for 5 seconds
    Then On ${phone1} verify ${line4} icon state as ${blfStatusGreen}
    Then disconnect the call from ${phone3}
    Then On ${phone1} Wait for 5 seconds
    Then On ${phone1} verify ${line4} icon state as ${blfStatusQuestion}
    Then Register the ${phone1} on ${MxOne} pbx
    Then On ${phone1} Wait for 5 seconds
    Then On ${phone1} verify ${line4} icon state as ${blfStatusGreen}
    [Teardown]  Default Phone state


762230: Call waiting tone period set to 10 sec
    [Tags]    Owner:Milind    Reviewer:    Ramkumar
    &{Details}=    Create Dictionary    CallWaiting=1
    Given I want to configure GlobalSettings parameters using ${Details} for ${phone1}
    Given using ${PhoneWUI} Log Into ${phone1} URL
    Then Using ${PhoneWUI} Navigate to go to ${PreferencesMenu} page on ${phone1} URL
    Then using ${PhoneWUI} click on the ${CallWaitingTonePeriod} on ${phone1} URL
    Then Using ${PhoneWUI} send 10 value for ${CallWaitingTonePeriod} to ${phone1} URL
    Then Using ${PhoneWUI} click on the ${Preferences['SaveSettings']} on ${phone1} URL
    Then I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${line1}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then I want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
    Then Verify the led state of ${line2} as ${blink} on ${phone1}
    Then Verify ${Tones['CallWaiting']} tone is played on ${phone1}
    Then On ${phone1} Wait for 8 seconds
    Then Verify ${Tones['CallWaiting']} tone is played on ${phone1}
    Then answer the call on ${phone1} using ${line2}
    Then Verify ${Tones['CallWaiting']} tone is not played on ${phone1}
    Then disconnect the call from ${phone1}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone3}

    Then I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${line1}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then I want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
    Then Verify the led state of ${line2} as ${blink} on ${phone1}
    Then Verify ${Tones['CallWaiting']} tone is played on ${phone1}
    Then On ${phone1} Wait for 8 seconds
    Then Verify ${Tones['CallWaiting']} tone is played on ${phone1}
    Then on ${phone1} press the softkey ${ignore} in RingingState
    Then Verify ${Tones['CallWaiting']} tone is not played on ${phone1}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone3}

762231: Call waiting tone can be heard from speaker
    [Tags]    Owner:Milind    Reviewer:    Ramkumar
    Given I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${line1}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then I want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${line2}
    Then Verify the led state of ${line1} as ${blink} on ${phone1}
    Then Verify the led state of ${line2} as ${on} on ${phone1}
    Then I want to make a two party call between ${phone4} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${line3}
    Then Verify the led state of ${line1} as ${blink} on ${phone1}
    Then Verify the led state of ${line2} as ${blink} on ${phone1}
    Then Verify the led state of ${line3} as ${on} on ${phone1}
    Then I want to make a two party call between ${phone5} and ${phone1} using ${loudspeaker}
    Then Verify the led state of ${line4} as ${blink} on ${phone1}
    Then Verify ${Tones['CallWaiting']} tone is played on ${phone1}
    Then on ${phone1} press the softkey ${ignore} in RingingState
    Then Verify ${Tones['CallWaiting']} tone is not played on ${phone1}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone3}
    Then disconnect the call from ${phone4}
    Then disconnect the call from ${phone5}

762031: Audio_10: DEF29803
    [Tags]    Owner:Milind    Reviewer:    Ramkumar
    &{Details}=    Create Dictionary    CallWaiting=1
    Given I want to configure GlobalSettings parameters using ${Details} for ${phone1}
    Given using ${PhoneWUI} Log Into ${phone1} URL
    Then Using ${PhoneWUI} Navigate to go to ${PreferencesMenu} page on ${phone1} URL
    Then using ${PhoneWUI} click on the ${CallWaitingTonePeriod} on ${phone1} URL
    Then Using ${PhoneWUI} send 5 value for ${CallWaitingTonePeriod} to ${phone1} URL
    Then Using ${PhoneWUI} click on the ${Preferences['SaveSettings']} on ${phone1} URL
    Given I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${line1}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then I want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${line2}
    Then Verify the led state of ${line1} as ${blink} on ${phone1}
    Then Verify the led state of ${line2} as ${on} on ${phone1}
    Then I want to make a two party call between ${phone4} and ${phone1} using ${loudspeaker}
    Then Verify ringing state on ${phone1} and ${phone4}
    Then Verify the led state of ${line1} as ${blink} on ${phone1}
    Then Verify the led state of ${line2} as ${on} on ${phone1}
    Then Verify the led state of ${line3} as ${blink} on ${phone1}
    Then On ${phone1} verify the led state of ${message_waiting} as ${blink} and led color as Red
    Then Verify ${Tones['CallWaiting']} tone is played on ${phone1}
    Then i want to press line key ${programKey1} on phone ${phone1}
    Then Verify the led state of ${line2} as ${blink} on ${phone1}
    Then Verify the led state of ${line3} as ${blink} on ${phone1}
    Then On ${phone1} verify the led state of ${message_waiting} as ${blink} and led color as Red
    Then Verify ${Tones['CallWaiting']} tone is played on ${phone1}
    Then verify audio path between ${phone1} and ${phone2}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone3}
    Then disconnect the call from ${phone4}
    Then disconnect the call from ${phone1}

763361: TC01 - Registeration - symmetric tls signalling, port override disabled
    [Tags]    Owner:Milind    Reviewer:Vikyat
    &{Details} =  Create Dictionary    DownloadProtocol=FTP    FTP_Server=10.112.123.107    FTP_Username=desktop    FTP_Password=desktop    FTP_Path=systeminfo
    &{parameters} =  Create Dictionary    sips symmetric tls signaling= 1    sip contact port override= 0
    Given I want to configure ConfigurationServer parameters using ${Details} for ${phone1}
    Then Create ${startUp} file using ${parameters}
    Then Create ${systeminfo} folder on FTP server
    Then Send ${startUp} file to ${systeminfo} folder on FTP server
    Then using ${PhoneWUI} Log Into ${phone1} URL
    Then using ${PhoneWUI} Navigate to go to ${GlobalSIPMenu} page on ${phone1} URL
    Then Go to the ${GlobalSIP['TransportProtocol']} option and select the ${PersistentTLS} value
    Then Using ${PhoneWUI} click on the ${GlobalSIP['SaveSettings']} on ${phone1} URL
    Then Using ${PhoneWUI} logoff ${phone1} URL
    Then unregister the ${phone1} from ${MxOne} pbx
    Then On ${phone1} Wait for 2 seconds
    Then On ${phone1} verify display message No Service
    Then reboot ${phone1}
    Then Using ${PhoneWUI} Start the capture on all port on ${phone1} URL
    Then On ${phone1} Wait for 2 seconds
    Register the ${phone1} on ${MxOne} pbx
    Then On ${phone1} Wait for 2 seconds
    Then Using ${PhoneWUI} ${stop} the capture from ${phone1} URL
    Then Using ${PhoneWUI} ${download} the capture from ${phone1} URL
    Then Verify the captureFile contains Status Code: 200 inside ${Protocols['SIP(Register)']} packets of ${phone1}
    Then Verify the captureFile contains Contact URI Host Port: 5061 inside ${Protocols['SIP(Register)']} packets of ${phone1}

751390: TC008 - User can change the value from WebUI
    [Tags]    Owner:Milind    Reviewer:Vikyat    micloud
    Given Using ${PhoneWUI} log into ${phone1} URL with 1234
    Then Using ${PhoneWUI} Navigate to go to ${NetworkMenu} page on ${phone1} URL
    Then Using ${PhoneWUI} send ${primaryDNSIP} value for ${NetworkLink['PrimaryDNS']} to ${phone1} URL
    Then Using ${PhoneWUI} send ${secondaryDNSIP} value for ${NetworkLink['SecondaryDNS']} to ${phone1} URL
    Then Verify text ${primaryDNSIP} for ${NetworkLink['PrimaryDNS']} on the ${phone1} URL
    Then Verify text ${secondaryDNSIP} for ${NetworkLink['SecondaryDNS']} on the ${phone1} URL
    And using ${PhoneWUI} logoff ${phone1} URL

177356: TC009 - Change the settings from WebUI
    [Tags]    Owner:Milind    Reviewer:Vikyat    micloud
    Given Using ${PhoneWUI} log into ${phone1} URL with 1234
    Then Using ${PhoneWUI} Navigate to go to ${NetworkMenu} page on ${phone1} URL
    ${primaryDNS}=    Using ${PhoneWUI} Get text of ${NetworkLink['PrimaryDNS']} on the Web UI of ${phone1}
    ${secondaryDNS}=    Using ${PhoneWUI} Get text of ${NetworkLink['SecondaryDNS']} on the Web UI of ${phone1}
    Then Using ${PhoneWUI} send ${primaryDNS} value for ${NetworkLink['PrimaryDNS']} to ${phone1} URL
    Then Using ${PhoneWUI} send ${secondaryDNS} value for ${NetworkLink['SecondaryDNS']} to ${phone1} URL
    Then Using ${PhoneWUI} click on the ${NetworkLink['SaveSettings']} on ${phone1} URL
    Then On ${phone1} Wait for 2 seconds
    Then Verify text Provisioning complete is present on the Web UI of ${phone1}
    And using ${PhoneWUI} logoff ${phone1} URL