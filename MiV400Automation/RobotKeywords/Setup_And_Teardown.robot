*** Settings ***
Resource    ../RobotKeywords/PhoneKeywords.robot
Resource    ../Variables/PhonesDetails.robot
#Resource    ../RobotKeywords/WebUI_Keywords.robot

#Variables  ../variables/WebUIDetails.yaml
*** Keywords ***
Phones Initialization
    Run Keyword If    "${pbx}" == "Asterisk"    Asterisk_Initialization
    ...    ELSE IF    "${pbx}" == "MxOne"       MxOne_Initialization
    ...    ELSE IF    "${pbx}" == "MiV400"      MiV400_Initialization
    ...    ELSE IF    "${pbx}" == "MiV5000"     MiV5000_Initialization
    ...    ELSE IF    "${pbx}" == "Telepo"      Telepo_Initialization
    ...    ELSE IF    "${pbx}" == "WebUI"       WebUI_Initialization
    ...    ELSE IF    "${pbx}" == "MiCloud"     MiCloud_Initialization
    ...    ELSE IF    "${pbx}" == "Clearspan"   Clearspan_Initialization
    ...    ELSE IF    "${pbx}" == "MiVoice"     MiVoice_Initialization
	...    ELSE IF    "${pbx}" == "Manual"     Manual_Phone_Initialization
    ...    ELSE       FATAL ERROR    Wrong "DUT" value passed!!!

Manual_Phone_Initialization
    IMPORT RESOURCE   ${EXEC_DIR}${/}..${/}Variables/Manual_Phone_Initialization.robot
    @{executionPhones}=    Run Keyword If    "${dut}" == "PhoneA"    Phone_A_Initialization
    ...    ELSE IF    "${dut}" == "PhoneB"    Phone_B_Initialization
    ...    ELSE IF    "${dut}" == "PhoneC"    Phone_C_Initialization
    ...    ELSE IF    "${dut}" == "PhoneD"    Phone_D_Initialization
    ${length}=    GET LENGTH    ${executionPhones}

    SET SUITE VARIABLE    @{executionPhones}
    :FOR    ${index}    IN RANGE    ${length}
    \    ${phoneNum} =    EVALUATE    ${index} + 1
    \    SET SUITE VARIABLE  ${phone${phoneNum}}    @{executionPhones}[${index}]

WebUI_Initialization
    LOG TO CONSOLE      Inside Web UI Initialization
    IMPORT RESOURCE   ${EXEC_DIR}${/}..${/}Variables/MxOne_Initialization.robot
    ${phone1}    ${phone2}    ${phone3}    ${phone4}=    Run Keyword If    "${dut}" == "PhoneA"    Phone_A_Initialization
    ...    ELSE IF    "${dut}" == "PhoneB"    Phone_B_Initialization
    ...    ELSE       FATAL ERROR    Wrong "DUT" value passed

    # Makes the phones available everywhere within the scope of the current suite
    ${PhoneWUI}=   GET LIBRARY INSTANCE    UI
    SET SUITE VARIABLE    ${PhoneWUI}
    SET SUITE VARIABLE    ${phone1}
    SET SUITE VARIABLE    ${phone2}
    SET SUITE VARIABLE    ${phone3}
    SET SUITE VARIABLE    ${phone4}
    LOG TO CONSOLE    PHONES INITIALISED

Asterisk_Initialization
    IMPORT RESOURCE   ${EXEC_DIR}${/}..${/}Variables/Asterisk_Initialization.robot
    ${phone1}    ${phone2}    ${phone3}    ${phone4}=    Run Keyword If    "${dut}" == "PhoneA"    Phone_A_Initialization
    ...    ELSE IF    "${dut}" == "PhoneB"    Phone_B_Initialization

#   Makes the phones available everywhere within the scope of the current suite
    SET SUITE VARIABLE    ${phone1}
    SET SUITE VARIABLE    ${phone2}
    SET SUITE VARIABLE    ${phone3}
    SET SUITE VARIABLE    ${phone4}

MXone_Initialization
    IMPORT RESOURCE   ${EXEC_DIR}${/}..${/}Variables/MxOne_Initialization.robot
#    ${PhoneWUI}=   GET LIBRARY INSTANCE    UI
    @{executionPhones}=    Run Keyword If    "${dut}" == "PhoneA"    Phone_A_Initialization
    ...    ELSE IF    "${dut}" == "PhoneB"    Phone_B_Initialization
    ...    ELSE IF    "${dut}" == "PhoneC"    Phone_C_Initialization
    ...    ELSE IF    "${dut}" == "PhoneD"    Phone_D_Initialization
    ...    ELSE IF    "${dut}" == "PhoneE"    Phone_E_Initialization
    ...    ELSE       FATAL ERROR    Wrong "DUT" value passed
    ${length}=    GET LENGTH    ${executionPhones}

    SET SUITE VARIABLE    @{executionPhones}
    :FOR    ${index}    IN RANGE    ${length}
    \    ${phoneNum} =    EVALUATE    ${index} + 1
    \    SET SUITE VARIABLE  ${phone${phoneNum}}    @{executionPhones}[${index}]
   ${PhoneWUI}=   GET LIBRARY INSTANCE    UI
   SET SUITE VARIABLE    ${PhoneWUI}

MiV400_Initialization
    IMPORT RESOURCE   ${EXEC_DIR}${/}..${/}MiV400Automation/Variables/MiV400_Initialization.robot
    @{executionPhones}=        Run Keyword If    "${dut}" == "PhoneA"    Phone_A_Initialization
    ...    ELSE IF    "${dut}" == "PhoneB"    Phone_B_Initialization
    ...    ELSE IF    "${dut}" == "PhoneC"    Phone_C_Initialization
    ...    ELSE IF    "${dut}" == "PhoneD"    Phone_D_Initialization
    ...    ELSE       FATAL ERROR    Wrong "DUT" value passed
     ${length}=    GET LENGTH    ${executionPhones}

#   Makes the phones available everywhere within the scope of the current suite
    SET SUITE VARIABLE    @{executionPhones}
    FOR    ${index}    IN RANGE    ${length}
           ${phoneNum} =    EVALUATE    ${index} + 1
           SET SUITE VARIABLE  ${phone${phoneNum}}    ${executionPhones}[${index}]
    END

MiV5000_Initialization
    IMPORT RESOURCE   ${EXEC_DIR}${/}..${/}Variables/MiV5000_Initialization.robot
    @{executionPhones}=    Run Keyword If    "${dut}" == "PhoneA"    Phone_A_Initialization
    ...    ELSE IF    "${dut}" == "PhoneB"    Phone_B_Initialization
    ...    ELSE IF    "${dut}" == "PhoneC"    Phone_C_Initialization
    ...    ELSE IF    "${dut}" == "PhoneD"    Phone_D_Initialization
    ...    ELSE       FATAL ERROR    Wrong "DUT" value passed
    ${length}=    GET LENGTH    ${executionPhones}

#   Makes the phones available everywhere within the scope of the current suite
    SET SUITE VARIABLE    @{executionPhones}
    :FOR    ${index}    IN RANGE    ${length}
    \    ${phoneNum} =    EVALUATE    ${index} + 1
    \    SET SUITE VARIABLE  ${phone${phoneNum}}    @{executionPhones}[${index}]

SipX_Initialization
    IMPORT RESOURCE   ${EXEC_DIR}${/}..${/}Variables/SipX_Initialization.robot
    ${phone1}    ${phone2}=    Run Keyword If    "${dut}" == "PhoneA"    SipX_PhoneA_Initialization
    ...    ELSE IF    "${dut}" == "PhoneB"    SipX_PhoneB_Initialization

#   Makes the phones available everywhere within the scope of the current suite
    SET SUITE VARIABLE    ${phone1}
    SET SUITE VARIABLE    ${phone2}

Telepo_Initialization
    LOG TO CONSOLE    Telepo Phones Initialization
    IMPORT RESOURCE   ${EXEC_DIR}${/}..${/}Variables/Telepo_Initialization.robot
    @{executionPhones}=    Run Keyword If    "${dut}" == "PhoneA"    Phone_A_Initialization
    ...    ELSE IF    "${dut}" == "PhoneB"    Phone_B_Initialization
    ...    ELSE IF    "${dut}" == "PhoneC"    Phone_C_Initialization
    ...    ELSE IF    "${dut}" == "PhoneD"    Phone_D_Initialization
    ...    ELSE IF    "${dut}" == "PhoneE"    Phone_E_Initialization
    ...    ELSE       FATAL ERROR    Wrong "DUT" value passed

    ${length}=    GET LENGTH    ${executionPhones}

    SET SUITE VARIABLE    @{executionPhones}
    :FOR    ${index}    IN RANGE    ${length}
    \    ${phoneNum} =    EVALUATE    ${index} + 1
    \    SET SUITE VARIABLE  ${phone${phoneNum}}    @{executionPhones}[${index}]

MiCloud_Initialization
    IMPORT RESOURCE   ${EXEC_DIR}${/}..${/}Variables/MiCloud_Initialization.robot
    IMPORT RESOURCE   ${EXEC_DIR}${/}..${/}Variables/BossApiDetails.robot
    IMPORT RESOURCE   ${EXEC_DIR}${/}..${/}RobotKeywords/Boss_API_Keywords.robot
    IMPORT LIBRARY    ${EXEC_DIR}${/}..${/}lib/BossApiComponent.py    &{bossLoginDetails}    WITH NAME    BOSS
    @{executionPhones}=    Run Keyword If    "${dut}" == "PhoneA"    MiCloud_PhoneA_Initialization
    ...    ELSE IF    "${dut}" == "PhoneB"    MiCloud_PhoneB_Initialization
    ...    ELSE IF    "${dut}" == "PhoneC"    MiCloud_PhoneC_Initialization
    ...    ELSE IF    "${dut}" == "PhoneD"    MiCloud_PhoneD_Initialization
    ...    ELSE IF    "${dut}" == "PhoneE"    MiCloud_PhoneE_Initialization

    ${length}=    GET LENGTH    ${executionPhones}

    ${bossPortal}=   GET LIBRARY INSTANCE    BOSS
    SET SUITE VARIABLE    ${bossPortal}
    SET SUITE VARIABLE    @{executionPhones}
    :FOR    ${index}    IN RANGE    ${length}
    \    ${phoneNum} =    EVALUATE    ${index} + 1
    \    SET SUITE VARIABLE  ${phone${phoneNum}}    @{executionPhones}[${index}]

MiVoice_Initialization
    LOG TO CONSOLE  MiVoice Initialization
    IMPORT RESOURCE   ${EXEC_DIR}${/}..${/}Variables/MiVoice_Initialization.robot
    IMPORT RESOURCE   ${EXEC_DIR}${/}..${/}Variables/BossApiDetails.robot
    IMPORT RESOURCE   ${EXEC_DIR}${/}..${/}RobotKeywords/Boss_API_Keywords.robot
    IMPORT LIBRARY    ${EXEC_DIR}${/}..${/}lib/BossApiComponent.py    &{D2API}    WITH NAME    D2

    @{executionPhones}=    RUN KEYWORD IF  "${dut}" == "PhoneA"    Phone_A_Initialization_MiVoice
    ...    ELSE IF    "${dut}" == "PhoneB"    Phone_B_Initialization_MiVoice
    ...    ELSE IF    "${dut}" == "PhoneC"    Phone_C_Initialization_MiVoice
    ...    ELSE IF    "${dut}" == "PhoneD"    Phone_D_Initialization_MiVoice
    ...    ELSE IF    "${dut}" == "PhoneE"    Phone_E_Initialization_MiVoice
    ...    ELSE IF    "${dut}" == "PhoneF"    Phone_F_Initialization_MiVoice
    ${length}=    GET LENGTH    ${executionPhones}

    ${bossPortal}=   GET LIBRARY INSTANCE    D2
    SET SUITE VARIABLE    ${bossPortal}
    SET SUITE VARIABLE    @{executionPhones}
    :FOR    ${index}    IN RANGE    ${length}
    \    ${phoneNum} =    EVALUATE    ${index} + 1
    \    SET SUITE VARIABLE  ${phone${phoneNum}}    @{executionPhones}[${index}]

Clearspan_Initialization
    IMPORT RESOURCE   ${EXEC_DIR}${/}..${/}Variables/Clearspan_Initialization.robot
    @{executionPhones}=    Run Keyword If    "${dut}" == "PhoneA"    Phone_A_Initialization
    ...    ELSE IF    "${dut}" == "PhoneB"    Phone_B_Initialization
    ...    ELSE IF    "${dut}" == "PhoneC"    Phone_C_Initialization
    ...    ELSE IF    "${dut}" == "PhoneD"    Phone_D_Initialization
    ${length}=    GET LENGTH    ${executionPhones}

    SET SUITE VARIABLE    @{executionPhones}
    :FOR    ${index}    IN RANGE    ${length}
    \    ${phoneNum} =    EVALUATE    ${index} + 1
    \    SET SUITE VARIABLE  ${phone${phoneNum}}    @{executionPhones}[${index}]

Check Phone Connection
    LOG TO CONSOLE    CHECKING CONNECTION ON PHONES

    FOR    ${phone}    IN    @{executionPhones}
           CALL METHOD    ${phone}    checkConnection
    END

Generic Test Teardown
    LOG TO CONSOLE  "Calling Generic Teardown"
    FOR    ${phone}    IN    @{executionPhones}
           CALL METHOD    ${phone}    disconnectTerminal
    END

Get DUT Details
    CALL METHOD    ${phone1}    getDutDetails

Default Line Registeration Setup
    LOG TO CONSOLE    Default Line Registeration Setup
    @{phonesToOpen}    CREATE LIST
    SET SUITE VARIABLE    ${phonesToOpen}

Default Line Registeration Teardown
    LOG TO CONSOLE    Default Line Registeration
    :FOR    ${phone}    IN    ${phonesToOpen}
    \    RUN KEYWORD IF TEST FAILED    CALL METHOD    ${PhoneWUI}    registerPhone    linesToRegister=all    phoneToOpen=${phone}    phoneToEnter=${phone}    pbx=${pbx}
    \    CALL METHOD    ${PhoneWUI}    LogOff

Register Phone
    CALL METHOD    ${phone1}    regPhone    pbx=${pbx}
    CALL METHOD    ${phone2}    regPhone    pbx=${pbx}

Remove program button
    Generic Test Teardown
    call method    ${phone1}    configureProgramButton    function=none    position=3
    call method    ${phone1}    configureProgramButton    function=none    position=4

MxOne Default Configuration
    [Documentation]    Configures default settings on the phones.
    LOG TO CONSOLE    Calling MxOne Teardown
    &{configurationDetails}=    create dictionary    call waiting=1    conference disabled=0    map conf as DTMF=0
                                ...                  map conf key to=    topsoftkey2 type=line    topsoftkey3 type=none
                                ...                  topsoftkey4 type=none    prgkey3 type=none    prgkey4 type=none
                                ...                  prgkey7 type=none    collapsed softkey screen=0
                                ...                  sip refer-to with replaces=0    sip line1 dnd=0
                                ...                  sip xml notify event=0

    :FOR    ${phone}    IN    @{executionPhones}
    \    CALL METHOD    ${phone}    configureXMLParameter    &{configurationDetails}


MiV5000 Default Configuration
    [Documentation]    Makes every configuration changed to default ones.
    &{configurationDetails}=    create dictionary    call waiting=1    directed call pickup=0    directed call pickup prefix=
                                ...                  topsoftkey3 type=none     topsoftkey4 type=none
                                ...                  topsoftkey5 type=none    prgkey3 type=none    prgkey4 type=none
                                ...                  prgkey7 type=none    collapsed softkey screen=0    topsoftkey4 locked=0

    :FOR    ${phone}    IN    @{executionPhones}
    \    CALL METHOD    ${phone}    configureXMLParameter    &{configurationDetails}


Default Account configuration
    Generic Test Teardown
    &{Details}=    CREATE DICTIONARY
    I want to configure AccountConfiguration parameters using ${Details} for ${phone1}

Default Network settings
    Generic Test Teardown
    &{Details}=    CREATE DICTIONARY
    I want to configure Network parameters using ${Details} for ${phone1}

Default Preferences settings
    Generic Test Teardown
    &{Details}=    CREATE DICTIONARY
    I want to configure Preferences parameters using ${Details} for ${phone1}

Default Global settings
    Generic Test Teardown
    &{Details}=    CREATE DICTIONARY
    I want to configure GlobalSettings parameters using ${Details} for ${phone1}

Default Phone state
    CALL METHOD    ${phone1}    regPhone    pbx=${pbx}
    Generic Test Teardown

Default ActionURI Configuration
    [Documentation]    Makes Action URI configuration changed to default ones.
    LOG TO CONSOLE    Calling Default Action URI Teardown
    &{configurationDetails}=    create dictionary    incomingField=    outgoingField=    onHookField=
                                ...                  offhookField=    connectedField=    disconnectedField=
                                ...                  regeventField=

    CALL METHOD    ${phone1}    actionUrl       &{configurationDetails}       pbx=${pbx}
    Using ${PhoneWUI} logoff ${phone1} URL

RTCP Default Teardown
    &{configurationDetails}=    CREATE DICTIONARY    sip rtcp summary reports=0
    ...                         sip rtcp summary report collector=
    ...                         sip rtcp summary report collector port=
    ...                         sip rtcp summary reports transport protocol=1
    :FOR    ${phone}    IN    @{executionPhones}
    \    CALL METHOD    ${phone}    configureXMLParameter    &{configurationDetails}


Default Background Configuration
    LOG TO CONSOLE    Setting the default image
    CALL METHOD    ${phone1}    setBackgroundImage    server=${ftp}    typeOfImage=${default}
    CALL METHOD    ${phone1}    isBackgroundImageSet    typeOfImage=${default}

Default ScreenSaver Configuration
    LOG TO CONSOLE    SETTING DEFAULT SCREENSSAVER
    CALL METHOD    ${phone1}    setCustomScreenSaver    server=${ftp}    saverType=${default}
    CALL METHOD    ${phone1}    verifyScreenSaverDisplay    screenSaverType=${default}

DND Default Configuration
    &{dndOff}=    CREATE DICTIONARY    dnd=0    parameters=AccountConfiguration
    CALL METHOD    ${phone1}    configurePhoneParameters    &{dndOff}
    RUN KEYWORD IF    "${pbx}"=="MxOne"    MxOne Default Configuration

Park/Pickup Default Configuration
    &{configurationDetails}=    CREATE DICTIONARY    sip park pickup config=70;70;asterisk
    CALL METHOD    ${phone1}    configurePhoneParameters    &{configurationDetails}

Logoff Browser Window
    CALL METHOD    ${PhoneWUI}    LogOff

##################################### MIVOICE/MICLOUD SPECIFIC SETUPS/TEARDOWNS #######################################

Default Call Appearance
#    For API Suite only
    [Documentation]    Assigns the default call appearance to the the line keys
    CALL METHOD    ${bossPortal}    addCallAppearance    user_extension=${phone1}
    CALL METHOD    ${bossPortal}    addCallAppearance    user_extension=${phone2}
    CALL METHOD    ${bossPortal}    addCallAppearance    user_extension=${phone3}

BCA Custom Setup
    [Documentation]    Creates a new list containing all the phone objects where BCA extensions are created.
    Check Phone Connection
    LOG TO CONSOLE    "BCA Setup Started"
#    Creating an empty list for storing* the BCA Extensions created in the test cases
#    * See the keyword for creating bca extensions also
    @{bcaExtensions}    CREATE LIST
    SET SUITE VARIABLE    ${bcaExtensions}

BCA Custom Teardown
    [Documentation]    Deletes the BCA extensions created if the test case fails.
    LOG TO CONSOLE    "BCA Teardown Started"
#    For every entry in the BCA Extension list, deleting the extensions.
    :FOR    ${extension}    IN    @{bcaExtensions}
    \    CALL METHOD    ${bossPortal}    deleteBCA    ExtensionNumber=${extension}
    Generic Test Teardown


Telephony Options Custom Teardown
    [Documentation]    Changes the digit waiting time period to default.
# Custom Teardown for rectifying any modification done in the digit waiting time period.
#    Generic Test Teardown
    LOG TO CONSOLE    "Calling Telephony Teardown"
    CALL METHOD    ${bossPortal}    modifyTelephoneOptions    DelayAfterCollectDigits=3000

CoS Features Custom Teardown
    [Documentation]    Changes the Class of Service (CoS) to its default settings.
    Generic Test Teardown
    CALL METHOD    ${bossPortal}    cosFeature    Name=Fully Featured

Paging Group Custom Setup
    [Documentation]    Creates a new list containing all the phone objects where paging groups are created.
# Setup to be used when crating a Paging Group
    Check Phone Connection
#    Creating a dictionary to store the Paging List name and the Paging Extension as Key and Value respectively and,
#    making it accessible across the suite
    &{pgExtensions}=    CREATE DICTIONARY
    SET SUITE VARIABLE    ${pgExtensions}

Paging Group Custom Teardown
    [Documentation]    Deletes the Paging groups created in the TC.
    Generic Test Teardown
    LOG TO CONSOLE    "Calling Paging Group Teardown"
    :FOR    ${pageListName}    IN    @{pgExtensions}
    \    ${extensionNumber}=    GET FROM DICTIONARY    ${pgExtensions}    ${pageListName}
    \    CALL METHOD    ${bossPortal}    deletePagingGroups    number=${extensionNumber}    pagingListName=${PageListName}

Hunt Group Custom Setup
    [Documentation]    Creates a new list containing all the phone objects where hunt groups are created.
    Check Phone Connection
    LOG TO CONSOLE    "Running Hunt Group Setup"
#    Creating a list containing all the Hunt Group extensions created
    @{hgExtensions}=    CREATE LIST
    SET SUITE VARIABLE    ${hgExtensions}

Hunt Group Custom Teardown
    [Documentation]    Deletes the Hunt Groups created if the test case fails.
    Generic Test Teardown
    LOG TO CONSOLE    "Running Hunt Group Teardown"
    :FOR    ${hgExtension}    IN    @{hgExtensions}
    \    CALL METHOD    ${bossPortal}    deleteHuntGroup    number=${hgExtension}

Default Availability State
    [Documentation]    Changes the phone state to its default state.
# Changing the availability state to Available and also making the other things to default options to their default values
    LOG TO CONSOLE    Changing phone state to default

    CALL METHOD    ${phone1}    ChangePhoneToDefaultState
    CALL METHOD    ${phone1}    userSettings    option=Default    pbx=${pbx}

Telephony Feature Custom Setup
    [Documentation]    Creates a new list containing all the phone objects where telephony features are updated.
    BCA Custom Setup
#    Creating a list that will contain all the phones used
    @{phones}    CREATE LIST
    SET SUITE VARIABLE    ${phones}

Telephony Feature Custom Teardown
    [Documentation]    Disables the SCA feature on the phone
    BCA Custom Teardown
    LOG TO CONSOLE    "Calling Telephony Feature Teardown"
    &{telephonydetails}=    CREATE DICTIONARY    sca_enabled=False
    :FOR    ${phone}    IN    @{phones}
    \    CALL METHOD    ${bossPortal}    modifyTelephoneFeature    phone=${phone}    &{telephonydetails}

Set Default Voicemail Password
    [Documentation]    Sets the default password on the phones.
    &{telephonydetails} =  Create Dictionary    VM_pwd_change_on_next_login=True

    # A list for storing the unique phone component objects only.
#    ${phones}    REMOVE DUPLICATES    ${phones}
    @{newPhones}    CREATE LIST
    ${newPhones}    REMOVE DUPLICATES    ${phones}

    :FOR    ${phone}    IN    @{newPhones}
    \    RUN KEYWORD IF    ${newPassword}==${voicemailPassword}    CALL METHOD    ${bossPortal}    modifyTelephoneFeature    phone=${phone}    &{telephonydetails}
    \    RUN KEYWORD IF    ${newPassword}==${voicemailPassword}    CALL METHOD    ${phone}    changeVoicemailPassword     oldPassword=${newPassword}    newPassword=${newVoiceMailPassword}
    \    RUN KEYWORD IF    ${newPassword}==${voicemailPassword}    CALL METHOD    ${phone}    pressHardkey    key=GoodBye
    \    RUN KEYWORD IF    ${newPassword}==${voicemailPassword}    CALL METHOD    ${bossPortal}    modifyTelephoneFeature    phone=${phone}    &{telephonydetails}
    \    RUN KEYWORD IF    ${newPassword}==${voicemailPassword}    CALL METHOD    ${phone}    changeVoicemailPassword     oldPassword=${newVoiceMailPassword}    newPassword=${voicemailPassword}
    \    RUN KEYWORD IF    ${newPassword}==${voicemailPassword}    CALL METHOD    ${phone}    pressHardkey    key=GoodBye
    \    EXIT FOR LOOP IF    ${newPassword}==${voicemailPassword}
    \    CALL METHOD    ${bossPortal}    modifyTelephoneFeature    phone=${phone}    &{telephonydetails}
    \    CALL METHOD    ${phone}    changeVoicemailPassword     oldPassword=${newPassword}    newPassword=${voicemailPassword}
    \    CALL METHOD    ${phone}    pressHardkey    key=GoodBye

Assign Extension Custom Setup
    Check Phone Connection
    LOG    THIS SETUP IS NOT NEEDED. USE 'CHECK PHONE CONNECTION' INSTEAD    WARN
    #    Creating a list that will contain all the phones on which numbers have been assigned/unassigned
    @{assignedPhones}    CREATE LIST
    SET SUITE VARIABLE    ${assignedPhones}

Assign Extension Custom Teardown
    [Documentation]    Assigns the original extensions to the execution phones
    Check Phone Connection
    :FOR    ${phone}    IN    @{executionPhones}
    \    CALL METHOD    ${phone}    assignUser    phone=${phone}    state=${unAssigned}

Disable MOH features Teardown
    Generic Test Teardown
    LOG TO CONSOLE    "Running Disable MOH features Teardown"
    &{MOHFeatures}=    CREATE DICTIONARY    option=0    fileName=MOH_200
    CALL METHOD    ${bossPortal}     modifyMusicOnHold    &{MOHFeatures}

Default Number of Rings
    LOG TO CONSOLE    "Running Default number of rings Teardown"
    :FOR     ${phone}    IN    @{executionPhones}
    \    CALL METHOD    ${phone}    setRings    number=5    pbx=${pbx}

Pickup Group Custom Setup
# Setup to be used when crating a Pickup Group
    Check Phone Connection
#    Creating a dictionary to store the Pickup List name and the Pickup Extension as Key and Value respectively and,
#    making it accessible across the suite
    &{pickupExtension}    CREATE DICTIONARY
    SET SUITE VARIABLE    &{pickupExtension}

Pickup Group Custom Teardown
# Teardown for deleting the created Pickup Group extensions.
    Generic Test Teardown
    LOG TO CONSOLE    "Calling Pickup Group Teardown"
#    Deleting the Pickup Group enteries in the Dictionary.
    :FOR    ${pickupListName}    IN    @{pickupExtension}
    \    ${extensionNumber}=    GET FROM DICTIONARY    ${pickupExtension}    ${pickupListName}
    \    CALL METHOD    ${bossPortal}    deletePickupGroups    number=${extensionNumber}    pickupListName=${pickUpListName}

Default Directory Settings
    sleep  5 seconds
    CALL METHOD    ${phone1}    verifyDirectoryAction    directoryAction=default    phoneObj=${phone1}    pbx=${pbx}
    CALL METHOD    ${phone1}    pressHardkey    key=GoodBye

Default LLDP Settings
    CALL METHOD    ${phone1}    changeLLDPSettings    lldpStatus=1

Default ACD Group Settings
    :FOR    ${phone}    IN    @{executionPhones}
    \    CALL METHOD    ${phone}    dialNumber    number=#28#11
    \    CALL METHOD    ${phone}    pressSoftkeyInDialingState    softKey=Dial
    \    CALL METHOD    ${phone}    waitTill    timeInSeconds=5
    \    CALL METHOD    ${phone}    pressHardkey    key=GoodBye

Default Attendant Group Settings
    :FOR    ${phone}    IN    @{executionPhones}
    \    CALL METHOD    ${phone}    dialNumber    number=#28#12
    \    CALL METHOD    ${phone}    pressSoftkeyInDialingState    softKey=Dial
    \    CALL METHOD    ${phone}    waitTill    timeInSeconds=5
    \    CALL METHOD    ${phone}    pressHardkey    key=GoodBye

Clear Call History
    CALL METHOD    ${phone1}    pressCallHistory    folderName=Clear log    action=Quit    pbx=${pbx}


Create user Setup
    @{newlyCreatedUsers}=    CREATE LIST
    SET SUITE VARIABLE    ${newlyCreatedUsers}

Create User Teardown
    :FOR    ${createdPhone}    IN    @{newlyCreatedUsers}
    \    CALL METHOD    ${bossPortal}    deleteUser    extension=${createdPhone}

Delete Directory Entries
    :FOR    ${phone}    IN    @{executionPhones}
    \    CALL METHOD    ${phone}    deleteFromDirectory    entryToDelete=All

Default Configuration Server Settings
    &{configurationDetails}=    CREATE DICTIONARY    download protocol=TFTP    tftp server=0.0.0.0
    ...                         ftp path=    ftp username=    ftp password=
    :FOR    ${phone}    IN    @{executionPhones}
    \    CALL METHOD    ${phone}    configureXMLParameter    &{configurationDetails}

Default Topsoftkey Configuration
    &{configurationDetails}=    CREATE DICTIONARY    topsoftkey4 type=none    topsoftkey4 value=
    ...                         topsoftkey4 label=    prgkey3 type=none    prgkey4 type=none    topsoftkey3 label=
    :FOR    ${phone}    IN    @{executionPhones}
    \    CALL METHOD    ${phone}    configureXMLParameter    &{configurationDetails}

    &{configurationDetails}=    CREATE DICTIONARY    topsoftkey3 locked=0    topsoftkey4 locked=0    prgkey3 locked=
    :FOR    ${phone}    IN    @{executionPhones}
    \    CALL METHOD    ${phone}    configureXMLParameter    &{configurationDetails}

Default Time Zone Settings
    &{defaultTimeZoneSettings}=    CREATE DICTIONARY    time zone name=US-Eastern
    :FOR    ${phone}    IN    @{executionPhones}
    \    CALL METHOD    ${phone}    configureXMLParameter    &{defaultTimeZoneSettings}