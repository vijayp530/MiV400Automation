*** Settings ***
Library    Collections

*** Keywords ***

I want to make a two party call between ${phone1} and ${phone2} using ${dialingModeValue}
    CALL METHOD    ${phone1}    makeCall    phoneObj=${phone2}    dialingMode=${dialingModeValue}
	
Verify ringing state on ${phone1} and ${phone2}
    CALL METHOD    ${phone2}    verifyDisplayRinging    phoneObj=${phone1}

Answer the call on ${phone2} using ${answerModeValue}
    CALL METHOD    ${phone2}    answerCall    answerMode=${answerModeValue}

Disconnect the call from ${phone}
    CALL METHOD    ${phone}    clearCall

I want to make a conference call between ${phoneA},${phoneB} and ${phoneC} using ${ConferenceMethodValue}
    CALL METHOD    ${phoneA}    makeConference    phoneObj=${phoneC}    ConferenceMode=${ConferenceMethodValue}    pbx=${pbx}

Add the ${phoneObj} in ${numberOfParties} parties conference call on ${phone}
    CALL METHOD    ${phone}    addUserInConferenceCall    phoneObj=${phoneObj}    numberOfParties=${numberOfParties}

Put the linekey ${lineValue} of ${phone} on ${hold_unhold_value}
    CALL METHOD    ${phone}    holdUnhold    line=${lineValue}    hold_unhold=${hold_unhold_value}    pbx=${pbx}

Verify the ${line} of ${phone} at state ${state}
    CALL METHOD    ${phone}    verify_call_hold_unhold    line=${line}    hold_unhold=${state}    pbx=${pbx}

The ${phone1} Merged ${phone2} and ${phone3} and ${phone4} using ${Softkey3}
    CALL METHOD    ${phone1}   pressSoftkey   Softkey=${Softkey3}
    CALL METHOD    ${phone1}   pressSoftkey   Softkey= SoftKey1
    CALL METHOD    ${phone1}   waitTill    timeInSeconds=5
    CALL METHOD    ${phone1}   pressSoftkey   Softkey=${Softkey3}
    CALL METHOD    ${phone1}   pressSoftkey   Softkey= SoftKey1
	
On ${phone1} press the softkey ${Softkey} in VoiceMailState
    CALL METHOD    ${phone1}    pressSoftkeyInVoiceMailState    softKey=${Softkey}

On ${phone1} press the softkey ${Softkey} in RingingState
    CALL METHOD    ${phone1}    pressSoftkeyInRingingState    softKey=${Softkey}

On ${phone1} press the softkey ${Softkey} in AnswerState
    CALL METHOD    ${phone1}    pressSoftkeyInAnswerState    softKey=${Softkey}    pbx=${pbx}

On ${phone1} press the softkey ${Softkey} in ConferenceCallState
    CALL METHOD    ${phone1}    pressSoftkeyInConferenceCall    softKey=${Softkey}

On ${phone1} press the softkey ${Softkey} in TransferState
	 CALL METHOD    ${phone1}    pressSoftKeyInTransferState    softKey=${Softkey}    pbx=${pbx}

On ${phone1} press the softkey ${Softkey} in DialingState
    CALL METHOD    ${phone1}    pressSoftkeyInDialingState    softKey=${Softkey}

On ${phone} press the softkey ${Softkey} in SettingState
    CALL METHOD    ${phone}    pressSoftkeyInSettingState    softKey=${Softkey}

On ${phone} press the key ${key} in state ${State}
    CALL METHOD    ${phone}    pressKeyInState    ${key}    ${State}

Verify the led state of ${ledTypeValue} as ${ledModeValue} on ${phone1}
    CALL METHOD    ${phone1}     verifyLedState     ledType=${ledTypeValue}     ledMode=${ledModeValue}

On ${phone1} verify the led state of ${ledTypeValue} as ${ledModeValue} and led color as ${ledColor}
    CALL METHOD    ${phone1}    verifyLedState     ledType=${ledTypeValue}     ledMode=${ledModeValue}    ledColor=${ledColor}

Verify the line state as ${lineStateValue} on ${phone1}
    CALL METHOD    ${phone1}    verifyLineState    lineState=${lineStateValue}

Press hardkey as ${keyValue} on ${phone}
    CALL METHOD    ${phone}    pressHardkey    key=${keyValue}

Press hardkey on ${phone} as ${key} ${number} of times for navigation between calls
    CALL METHOD    ${phone}    pressHardkeynavigation    key=${key}    number=${number}

Check Connection and disconnect the ${phone}
    CALL METHOD    ${phone}    disconnectTerminal

I want to Park the call from ${phone1} on ${phone2_obj} using ${mode} and ${initiateMode}
    CALL METHOD    ${phone1}    callPark    phoneObj=${phone2_obj}    mode=${mode}    initiateMode=${initiateMode}

I want to unPark the call from ${phone2} on ${phone1} using ${mode} and ${initiatemode}
    CALL METHOD    ${phone1}    callUnPark    phoneObj=${phone2}    mode=${mode}    initiateMode=${initiatemode}

Initiate Transfer on ${phone1} to ${phone2_obj} using ${initiateModeValue}
	CALL METHOD    ${phone1}    initiateTransfer    phoneObj=${phone2_obj}    initiateMode=${initiateModeValue}    pbx=${pbx}

On ${phone} Wait for ${timeInSecondsValue} seconds
	CALL METHOD    ${phone}    waitTill    timeInSeconds=${timeInSecondsValue}

Press hookMode ${phoneHookModeValue} on phone ${phone}
    CALL METHOD    ${phone}    pressPhoneHook    phoneHookMode=${phoneHookModeValue}

Verify the Caller id on ${phone1} and ${phone2} display
    CALL METHOD    ${phone1}    verifyCallid    phoneObj=${phone2}    pbx=${pbx}

On ${phone1} verify the softkeys in ${phoneState}
    CALL METHOD    ${phone1}    verifySoftkeysInDifferentPhoneState    phoneState=${phoneState}
	
Login into voicemailBox for ${phone1} using ${voicemailPassword}
    CALL METHOD    ${phone1}    voicemailUserLogin    passCode=${voicemailPassword}    pbx=${pbx}

Press the call history button on ${phone} and folder ${folderNameValue} and ${action}
    CALL METHOD    ${phone}    pressCallHistory    folderName=${folderNameValue}    action=${action}    pbx=${pbx}

Leave voicemail message from ${phone1} on ${phone2}
    CALL METHOD    ${phone1}    leaveVoiceMailMessage    phone=${phone2}

I want to press line key ${linekey} on phone ${phone}
    CALL METHOD  ${phone}    pressLineKey   lineKey=${linekey}

On ${phone1} press directory and ${action} of ${phone2}
	CALL METHOD    ${phone1}    directoryAction    action=${action}    phoneObj=${phone2}    pbx=${pbx}

on ${phone} navigate to ${option} settings
    CALL METHOD    ${phone}    userSettings    option=${option}    pbx=${pbx}

Modify call handler mode on ${phone} to ${mode} in ${availability}
    CALL METHOD    ${phone}    callHandlerMode    mode=${mode}    availability=${availability}

On ${phone} dial number ${number}
    CALL METHOD    ${phone}    dialNumber  number=${number}

On ${phone} enter number ${phone2}
    CALL METHOD    ${phone}    enterNumber    phoneObj=${phone2}

On ${phone} press ${key} ${keyValue} for ${numberOfTimes} times
    CALL METHOD    ${phone}    pressKey    keyValue=${keyValue}    number=${numberOfTimes}    keyType=${key}

Change the phone state to default state on ${phone}
    CALL METHOD    ${phone}    ChangePhoneToDefaultState

Delete voicemail message on ${option} for ${phone} using ${voicemailPassword}
    CALL METHOD    ${phone}    deleteVoicemailMsg    option=${option}    passCode=${voicemailPassword}

Move voicemail message from ${folder} folder for ${phone}
    CALL METHOD    ${phone}    moveVoicemailMsg    folder=${folder}

On ${phone1} verify directory with ${action} of ${phone2}
    CALL METHOD    ${phone1}    verifyDirectoryAction    directoryAction=${action}    phoneObj=${phone2}    pbx=${pbx}

I want to verify on ${phone} negative display message ${negativemessage}
    CALL METHOD    ${phone}    verifyNegativeMessage    negMessage=${negativemessage}

Press softkey ${key} on ${phone1}
    CALL METHOD    ${phone1}    pressKeys    keyName=${key}

Change the directory format to ${format} on ${phone1}
    CALL METHOD    ${phone1}    changeDirectoryNameFormat    dirFormat=${format}

Reboot ${phone1}
	CALL METHOD    ${phone1}    rebootPhone

Reboot ${phone} without waiting for it to come online
    CALL METHOD    ${phone}    rebootPhone    waitTillPhoneComesOnline=False

Verify audio path between ${phone1} and ${phone2}
#    SLEEP    5 seconds
    CALL METHOD     ${phone1}    verifyVoicepathBetweenPhones    ${phone2}

Go to assign user on ${phone1} and ${action} in ${state}
    CALL METHOD    ${phone1}    assignUser    phone=${action}    state=${state}

Conference call audio verify between ${phone1} ${phone2} and ${phone3}
#    SLEEP    5 seconds
    CALL METHOD    ${phone1}    threePartyVoicePath    phoneB_obj=${phone2}    phoneC_obj=${phone3}

Four party Conference call audio verification between ${phone1} ${phone2} ${phone3} and ${phone4}
#    SLEEP    5 seconds
    CALL METHOD    ${phone1}    fourPartyVoicePath    phoneB_obj=${phone2}    phoneC_obj=${phone3}    phoneD_obj=${phone4}

Factory default ${phone1}
	CALL METHOD    ${phone1}    factoryReset

Verify Sip message ${msgToVerify} on ${phone1} for ${sipMethod} method and ${sipHeader} header using ${in_out} sip message
    CALL METHOD    ${phone1}    sipMessageVerification    phoneObj=${phone1}    sipMethod=${sipMethod}    sipHeader=${sipHeader}    msgToVerify=${msgToVerify}    messageDirection=${in_out}

On the ${phone1} verify softkeys in different state using ${mode}
    CALL METHOD    ${phone1}    verifySoftkeysInDifferentPhoneState    phoneState=${mode}

Go to ${option} settings and enter ${value} on ${phone1}
    CALL METHOD    ${phone1}    pingSettings    option=${option}    value=${value}    pbx=${pbx}

I want to use fac ${feature} on ${phone1} to ${phone2}
    CALL METHOD    ${phone1}    type_FAC    feature=${feature}   phoneObj=${phone2}

Verify no audio path from ${phone1} to ${phone2}
    CALL METHOD    ${phone1}    VerifyNoAudioPathBetweenPhones     phoneObj=${phone2}

Verify one way audio from ${phone1} to ${phone2}
    CALL METHOD    ${phone1}    VerifyOneWayAudio    phoneObj=${phone2}

Verify extension ${type} of ${phone2} on ${phone1}
    CALL METHOD    ${phone1}    extensionType    type=${type}    phoneObj=${phone2}

On ${phone1} press the softkey ${Softkey} in Transfertovm
    CALL METHOD    ${phone1}    transferTovm    softKey=${Softkey}

On call conferenc_hold_tc as ${keyValue} on ${phone1} with ${flag} and ${number_ch} and ${f_name} and ${messageValue} and ${messageValue_two}
    CALL METHOD    ${phone1}    conferenc_hold_tc    key=${keyValue}    Flag=${flag}    number=${number_ch}    f_name=${f_name}    message=${messageValue}    messageValue_two=${messageValue_two}

on ${phone1} display verify ${conferenceDisplay}
    CALL METHOD    ${phone1}    display_verifier    mydict=${conferenceDisplay}

Transfer call from ${phoneA} to ${phoneC} using ${transferMode}
    CALL METHOD  ${phoneA}    transferCall    phoneObj=${phoneC}   transferMode=${transferMode}

Enable Call forwarding from ${phone1} to ${phone3} for mode ${forwardMode}
    CALL METHOD  ${phone1}    forwardCall    phoneObj=${phone3}   forwardMode=${forwardMode}

Disable call forwarding on ${phone}
    CALL METHOD    ${phone}    disableCallForward

verify display ringing on ${phone2} and ${phone3} in call forwared from ${phone1} in ${forwardMode} mode
    CALL METHOD    ${phone2}    verifyCallForwardRinging    phoneObj1=${phone1}    phoneObj2=${phone3}    forwardMode=${forwardMode}

on ${phone1} ${transfer} call to ${phone2} using directory
	CALL METHOD    ${phone1}    directoryTransfer    transfer=${transfer}    phoneObj=${phone2}    pbx=${pbx}

Verify Ethernet values edit mode display on ${phone1}
	CALL METHOD    ${phone1}    ethernetSettings

Enter ${ipaddrstr} on ${phone1} to ${subsetting} settings
   CALL METHOD    ${phone1}    ipAddressDialer    ipAddress=${ipaddrstr}    opt_sub=${subsetting}

validate ip object in phone display content on ${phone1}
   CALL METHOD    ${phone1}    ip_validatorFdsp_Content_caller

On ${phone1} move to ${option} to ${subsetting} settings
    CALL METHOD    ${phone1}    userSettings    option=${option}    opt_sub=${subsetting}    pbx=${pbx}

on ${phone1} move to settings ${option} to ${subsetting} settings with ${Flag}
    CALL METHOD    ${phone1}    advanced_Setting    option=${option}    opt_sub=${subsetting}    Flag=${Flag}    pbx=${pbx}

I want to bargein ${phone} into ${phone_obj} using ${mode} and ${initiateMode}
    CALL METHOD    ${phone}    bargeIn    phoneObj=${phone_obj}    mode=${mode}    initiateMode=${initiateMode}

I want to pickup call from ${phone1} of ${phone2_obj} using ${mode} and ${initiateMode}
    CALL METHOD    ${phone1}    pickup_call    phoneObj=${phone2_obj}    mode=${mode}    initiateMode=${initiateMode}

On ${phone1} verify extension ${extNum} in directory
    RUN KEYWORD IF    "${pbx}" == "MiVoice"    CALL METHOD    ${phone1}    verifyDisplayMessage    message=${voiceExtensionNum['${extNum}']}    pbx=${pbx}
    ...    ELSE IF    "${pbx}" == "MiCloud"    CALL METHOD    ${phone1}    verifyDisplayMessage    message=${cloudExtensionNum['${extNum}']}    pbx=${pbx}

On ${phone1} dial partial number of ${phone2} with ${condition}
    CALL METHOD    ${phone1}    dialPartialNumber    phoneObj=${phone2}    type=${condition}

Five party Conference call audio verification between ${phone1} ${phone2} ${phone3} ${phone4} and ${phone5}
    CALL METHOD    ${phone1}    fivePartyVoicePath    phoneB_obj=${phone2}    phoneC_obj=${phone3}    phoneD_obj=${phone4}    phoneE_obj=${phone5}

Verify Caller Id of ${phone2} on Show Screen of ${phone1} during ${numberOfParties} party call
    CALL METHOD    ${phone1}    verifyCallerIdOnShow    phoneObj=${phone2}    numberOfParties=${numberOfParties}

Change voicemail password from ${oldPassword} to ${newPassword} for ${phone}
    SET SUITE VARIABLE    ${newPassword}
    CALL METHOD   ${phone}    changeVoicemailPassword     newPassword=${newPassword}    oldPassword=${oldPassword}

Set number of rings to ${number} on ${phone1}
   CALL METHOD    ${phone1}   setRings    number=${number}    pbx=${pbx}

On ${phone1} due to action ${action_name} popup raised verify message ${message} with wait of ${waitinsec}
    CALL METHOD    ${phone1}    popup_Message_verifier    action_name_dict=&{action_name}    message=${message}    wait=${waitinsec}    pbx=${pbx}

On ${phone1} verify display message ${messageValue}
    CALL METHOD    ${phone1}    verifyDisplayMessage    message=${messageValue}    pbx=${pbx}

On ${phone1} verify ${line} icon state as ${state}
    CALL METHOD   ${phone1}    verifyLineIconState    state=${state}    line=${line}

Verify ${state} state icon on ${phone1}
     CALL METHOD   ${phone1}    verifyAvailabilityStateIcon    state=${state}

verify MOH audio on ${phone} for ${value} frequency
    CALL METHOD    ${phone}    check_audio_on_hold    expectedFreq=${value}

Verify no MOH audio on ${phone}
    CALL METHOD    ${phone}    check_no_audio_on_hold

Verify ${icons} icons on ${phone}
    CALL METHOD    ${phone}    verify_call_history_icon    icons=${icons}

I want to press PKM line key ${linekey} on ${phone}
    CALL METHOD  ${phone}    pressPKMLineKey   lineKey=${linekey}

Verify the PKM led state of ${ledTypeValue} as ${ledModeValue} on ${phone1}
    CALL METHOD    ${phone1}     verifyPKMLedState     lineType=${ledTypeValue}     ledMode=${ledModeValue}

verify display message ${messageValue} on PKM for ${phone1}
    CALL METHOD    ${phone1}    verifyDisplayMessageOnPKM   message=${messageValue}

Verify ${line} icon state as ${state} on PKM for ${phone1}
    CALL METHOD   ${phone1}    verify_PKM_icon_state    state=${state}    line=${line}

on ${phone} PKM verify negative display message ${negativemessage}
    CALL METHOD    ${phone}    verifyPKMNegativeMessage    negMessage=${negativemessage}

verify voicemail windows ${option} icons value as ${value} on ${phone}
    CALL METHOD   ${phone}    verify_voice_mail_window_icons    option=${option}    value=${value}

delete ${option} call entries in call history on ${phone}
    CALL METHOD   ${phone}    deleteCallHistory    option=${option}

I want to configure ${value} parameters using ${Details} for ${phone}
    CALL METHOD   ${phone}    configurePhoneParameters     parameters=${value}     &{Details}    pbx=${pbx}

Load Test Data
     log to console  ${SUITE SOURCE}

register the ${phone} on ${platform} pbx
    CALL METHOD    ${phone}    regPhone    pbx=${pbx}

unregister the ${phone} from ${platform} pbx
    CALL METHOD    ${phone}    unregPhone    pbx=${platform}

restart all the phones
    CALL METHOD    ${phone1}    restartPhone    phoneObj1=${phone1}    phoneObj2=${phone2}    phoneObj3=${phone3}    phoneObj4=${phone4}    phoneObj5=${phone5}    phoneObj6=${phone6}

I want to program ${funcKey} key on position ${number} on ${phone1}
    CALL METHOD    ${phone1}    configureProgramButton    function=${funcKey}    position=${number}

On ${phone1} program ${funcKey} key on position ${number} with ${value} value
    CALL METHOD    ${phone1}    configureProgramButton    function=${funcKey}    position=${number}    value=${value}    pbx=${pbx}

I want to program ${funcKey} key on ${pageNumber} on position ${number} with ${label} on ${phone1}
    CALL METHOD    ${phone1}    configureExpensionModule    page_number=${pageNumber}    function=${funcKey}    position=${number}    label=${label}

Upgrade the firmware using ${Details} for ${phone}
    CALL METHOD   ${phone}    updatePhoneFirmware     &{Details}

Add number of ${phone2} in the directory of ${phone1}
    CALL METHOD    ${phone1}    addInDirectory    phone=${phone2}

Configure parameters on ${phone1} using ${configurationDetails}
    CALL METHOD    ${phone1}    configureXMLParameter    &{configurationDetails}

In directory search ${number} on ${phone}
    CALL METHOD    ${phone}    directorySearch    action=${number}

Delete ${phoneToDelete} entries from directry of ${phoneA}
    CALL METHOD    ${phoneA}    deleteFromDirectory    entryToDelete=${phoneToDelete}

update date as ${date} and time as ${time} on ${phone}
    CALL METHOD    ${phone}    updateDateTime    date=${date}       time=${time}

On ${phone1} program key type ${funcKey} on position ${number} to enable ${feature} with ${value} value
    CALL METHOD    ${phone1}    configureProgramButton    function=${funcKey}    label=${feature}    position=${number}    value=${value}

Create connection on ${server} server
    CALL METHOD    ${phone1}    createConnection     connection=${server}

Create ${name} folder on ${server} server
    CALL METHOD    ${phone1}    createConnection    connection=${server}     folderName=${name}

Create ${name} file using ${parameters}
    CALL METHOD    ${phone1}    createfile    parameter=&{parameters}    fileName=${name}

Send ${name} file to ${folder} folder on ${serverType} server
    CALL METHOD    ${phone1}     sendFileToServer     connection=${serverType}    fileName=${name}    folderName=${folder}

Send ${name} file on ${serverType} server
    CALL METHOD    ${phone1}     sendFileToServer     connection=${serverType}    fileName=${name}

Verify ${zone} time zone is present under ${area} in time zone settings of ${phone}
    CALL METHOD    ${phone}    verifyTimeZonePresent    timeZone=${zone}    area=${area}

Press ${key} key in Redial menu on ${phone}
    CALL METHOD    ${phone}    actionInRedialMenu    key=${key}

Using ${phone} verify configuration ${fileName} files in ${folderName} folder on ${server} server
    CALL METHOD    ${phone}    verifyDownloadedFile    connection=${server}     fileName=&{filename}    folderName=${folderName}

Capture the ${outgoing} packets from ${phone1} and verifiy the ${sipmessagedetail} on ${phone2}
    CALL METHOD    ${phone1}    verifySipMessage    message_type=${outgoing}    phoneObj=${phone2}    &{sipmessagedetail}

Copy file ${fileName} into http server ${parameter} for ${phone}
    CALL METHOD    ${phone}    serverConnection    fileName=${fileName}    parameter=${parameter}

et ${configuration} parameter to ${value} on ${phone1}
	CALL METHOD    ${phone1}    configureParameter_new    config=${configuration}     value=${value}

set configuration server to ${downloadProtocol}
	CALL METHOD    ${phone1}    configureServerSettings    downloadProtocol=${downloadProtocol}

Perform the wireshark operation ${operand} for ${phone1} and ${phone2} for ${operation}
    CALL METHOD    ${phone1}   wiresharkOperator    operand=${operand}   operation=${operation}   Test_name=${TEST NAME}   SUITE_SOURCE=${SUITE SOURCE}     pbx=${pbx}     phoneObj=${phone2}

Verfiy tls client Hello packet with ${header} as ${expectedValue} for ${phone1} for ${operation}
    CALL METHOD    ${phone1}   clientHelloVerifier  packt_key=${header}    packt_value=${expectedValue}   operation=${operation}

Verfiy tls Server Hello packet with ${header} as ${expectedValue} for ${phone1} for ${operation}
    CALL METHOD    ${phone1}   ServerHelloVerifier  packt_key=${header}    packt_value=${expectedValue}   operation=${operation}

Verfiy RTP event packet with ${header} as ${expectedValue} for ${phone1} for ${operation}
    CALL METHOD    ${phone1}   ServerHelloVerifier  packt_key=${header}    packt_value=${expectedValue}

modify httpdsslconf for tls version with ${value}
    CALL METHOD    ${phone1}   httpd_confupdater  tls=${value}

featurexml uploader with feature value ${value}
    CALL METHOD    ${phone1}   httpXmlPublisher  xmlName=${value}

Verfiy sip response of ${SIPMethod} with ${sip_header} as ${expectedResponse} for ${phone}
    CALL METHOD    ${phone}   resPPacketVerifier    packt_name=${SIPMethod}    packt_key=${sip_header}    packt_value=${expectedResponse}

Verfiy sip request method as ${SIPMethod} with ${sip_header} as ${expectedValue} for ${phone}
    CALL METHOD    ${phone}   reQPacketVerifier    packt_name=${SIPMethod}    packt_key=${sip_header}    packt_value=${expectedValue}

Verfiy sip request ${sip_header} of ${SIPMethod} for ${phone}
    CALL METHOD    ${phone}   reQheaderNameVerifier    packt_name=${SIPMethod}    packt_key=${sip_header}

Verfiy sip response ${sip_header} of ${SIPMethod} for ${phone}
    CALL METHOD    ${phone}   resPheaderNameVerifier    packt_name=${SIPMethod}    packt_key=${sip_header}

Verfiy sip method as ${SIPMethod} for ${phone}
    CALL METHOD    ${phone}   sipMethodNameVerifier    packt_name=${SIPMethod}

I want to copy ${configFilenm} on ${phone1} using ${server} with ${values}
    CALL METHOD    ${phone1}    phoneConfigCreator    parameters=&{values}    servertype=${server}    configfilename=${configFilenm}

Get System IP Address
    ${idAddress}=    CALL METHOD    ${phone1}    hostIpAddressGetter    proto=local
    [Return]    ${idAddress}

Create Telnet Packets on ${phone}
    CALL METHOD    ${phone}    createTelnetPackets    phoneObj=${phone}

Add number of ${phone2} with ${name} name in the directory of ${phone1}
    CALL METHOD    ${phone1}    addInDirectory    phone=${phone2}    name=${name}

Verify the ${protocol} packets in the captured packet file of ${phone}
    CALL METHOD    ${phone}    verifyProtocolInCapturedPackets    protocolToVerify=${protocol}    phoneObj=${phone}

Verify the ${protocol} packets are not present in the captured packet file of ${phone}
    CALL METHOD    ${phone}    verifyProtocolNotPresent    protocolToVerify=${protocol}

Verify the ${fileName} contains ${contentToVerify} inside ${protocol} packets of ${phone}
    CALL METHOD    ${phone}    verifyPacketContents    contentToVerify=${contentToVerify}    protocolToVerify=${protocol}

Verify the ${fileName} contains ${contentToVerify} of ${phone} inside ${protocol} packets
    CALL METHOD    ${phone}    verifyPacketContents    contentToVerify=${contentToVerify}    protocolToVerify=${protocol}
    ...                        phoneObj=${phone}

Filter the captured packets using ${filters} on ${phone}
    CALL METHOD    ${phone}     pcapConverter    filters=${filters}

Verify the time between ${protocol} packets as ${timeBetweenProtocols} seconds on ${phone}
    CALL METHOD    ${phone}    verifyTimeBetweenPackets    time=${timeBetweenProtocols}    protocol=${protocol}

Verify the brightness level of ${phone} as ${level}
    CALL METHOD    ${phone}    verifyBrightnessLevel    level=${level}

Verify ${fileName} file contains ${textToCheck} of ${phone}
    CALL METHOD    ${phone}    verifyFileContents      fileName=${fileName}    textToCheck=${textToCheck}    phone=${phone}

Create ${rootElement} XML with the ${xmlParameters} and ${attributesDetails} for ${phone}
    CALL METHOD    ${phone}    createXMLFile    rootElement=${rootElement}    kwargs=&{xmlParameters}
    ...                                         attr=&{attributesDetails}

Long press hardkey as ${keyValue} on ${phone}
    CALL METHOD    ${phone}    longPressKey    keyToPress=${keyValue}

On ${phone1} verify message ${messageValue} with ${prefix} as prefix
    CALL METHOD    ${phone1}    verifyDisplayMessage    message=${messageValue}    prefix=${prefix}    pbx=${pbx}

Add number of ${phone2} in the directory by pressing ${keyMapped} key of ${phone1}
    CALL METHOD    ${phone1}    addInDirectory    phone=${phone2}    directoryKey=${keyMapped}

Add number of ${phone2} in the directory with ${prefix} prefix by pressing ${keyMapped} key of ${phone1}
    CALL METHOD    ${phone1}    addInDirectory    phone=${phone2}    directoryKey=${keyMapped}    prefix=${prefix}

Set the screensaver mode to ${mode} on ${phone}
    CALL METHOD    ${phone}    changeScreenSaverSettings    screenSaverMode=${mode}

Set the screensaver timer to ${timeInSeconds} seconds on ${phone}
    CALL METHOD    ${phone}    changeScreenSaverSettings    screenSaverTimer=${timeInSeconds}

Change the screensaver mode to ${mode} and timer to ${timeInSeconds} seconds on ${phone}
    CALL METHOD    ${phone}    changeScreenSaverSettings    screenSaverMode=${mode}    screenSaverTimer=${timeInSeconds}

Check the screensaver display on ${phone} using ${screenSaverDetails}
    CALL METHOD    ${phone}    verifyScreenSaverDisplay    &{screenSaverDetails}

Set Custom screensaver image on ${phone} using ${serverType} server
    CALL METHOD    ${phone}    setCustomScreenSaver    server=${serverType}    saverType=Custom

Set ${typeOfImage} background image on ${phone} using ${serverType} server
    CALL METHOD    ${phone}    setBackgroundImage    server=${serverType}    typeOfImage=${typeOfImage}

Verify ${typeOfImage} background image is set on ${phone}
    CALL METHOD    ${phone}    isBackgroundImageSet    typeOfImage=${typeOfImage}

Get Firmware Version of ${phone}
    ${firmwareVersion}=    CALL METHOD    ${phone}    getFirmwareVersion
    [Return]    ${firmwareVersion}

Verify ${directoryFormat} naming directory format on ${phone}
    CALL METHOD    ${phone}    verifyDirectoryFormat    directoryFormat=${directoryFormat}    pbx=${pbx}

Verify ${textToVerify} is highlighted on ${phone}
    CALL METHOD    ${phone}    verifyHighlightedText    ${textToVerify}

On Telepo verify the led state of ${ledType} programmed key as ${ledMode} on ${phone}
    CALL METHOD    ${phone}    verifyLEDStateForTelepo    ledToVerify=${ledType}    ledMode=${ledMode}

On Telepo press the ${keyToPress} programmed key on ${phone}
    CALL METHOD    ${phone}    pressProgrammmedKeyOnTelepo    keyToPress=${keyToPress}

Disable to 802.1x settings on ${phone}
    CALL METHOD    ${phone}    changeEAPSettings    eapType=False

Change the eap-type to ${eapType} in 802.1x settings on ${phone}
    CALL METHOD    ${phone}    changeEAPSettings    eapType=${eapType}

Change the eap-type to ${eapType} in 802.1x settings with ${identity} identity and ${password} password on ${phone}
    CALL METHOD    ${phone}    changeEAPSettings    eapType=${eapType}    identity=${identity}    password=${password}

On ${phone} ${enable/disable} LLDP settings
    CALL METHOD    ${phone}    changeLLDPSettings    lldpStatus=${enable/disable}

On ${phone} verify display on a ${numberOfParties} party conference call
    CALL METHOD    ${phone}    verifyConferenceDisplay    numberOfParties=${numberOfParties}    pbx=${pbx}

Verify ${toneType} tone is played on ${phone}
    CALL METHOD    ${phone}    verifyToneIsPlayed    toneType=${toneType}

Verify ${toneType} tone is not played on ${phone}
    CALL METHOD    ${phone}    verifyToneIsPlayed    toneType=${toneType}    negativeValidation=True

Press DTMF key ${kye} on ${phone1} and verify tone played on ${phone2}
    CALL METHOD    ${phone1}    pressDTMFKeyAndVerifyToneIsPlayed    phoneObj=${phone2}    dtmfKey=${kye}

Press DTMF key ${kye} on ${phone1} and verify tone is not played on ${phone2}
    CALL METHOD    ${phone1}    pressDTMFKeyAndVerifyToneIsPlayed    phoneObj=${phone2}    dtmfKey=${kye}    negativeValidation=True

Long Press DTMF key ${kye} on ${phone1} and verify tone played on ${phone2}
    CALL METHOD    ${phone1}    pressDTMFKeyAndVerifyToneIsPlayed    phoneObj=${phone2}    dtmfKey=${kye}    longPressDTMFkey=True

#log upload
On ${phone} press the softkey ${Softkey} in Diagnostics ${subOption} Settings
    CALL METHOD    ${phone}    pressSoftkeyInDiagnosticSettingState    softKey=${Softkey}    option=${subOption}

On ${phone} remove existing diagnostic server ip
    CALL METHOD    ${phone}    clearDiagnosticServerIp

On ${phone} enter url prefix for ${serverType} server
    CALL METHOD    ${phone}    enterUrlPrefixInDiagnosticServerUrl    connection=${serverType}

On ${phone} enter diagnostic server ip as ${serverIp}
    CALL METHOD    ${phone}    enterDiagnosticServerIp    serverIp=${serverIp}

Verify display message ${messageValue} On ${phone} within ${timeInSeconds} seconds
    CALL METHOD    ${phone}    verifyMessageDisplayedOnPhone    message=${messageValue}    timeInSeconds=${timeInSeconds}

Verify ${phone} logs downloaded successfully on ${serverType} Server
    CALL METHOD    ${phone}    verifyLogFileIsDownloadedOnServer    connection=${serverType}

On ${phone} Delete existing log file from ${serverType} server
    CALL METHOD    ${phone}    deleteExistingLogFileFromServer    connection=${serverType}

On ${phone} Get this machine ip
    ${ipAddress}=    CALL METHOD    ${phone}    getThisMachineIp
    [Return]    ${ipAddress}