*** Variables ***
${toneSet}    tone set
${france}    France
${idleState}    idle
${ringingState}    Ringing
${answerState}    Answer
${holdState}    Hold
${voiceMailState}    VoiceMail
${hold}    hold
${unhold}    Unhold
${on}    on
${off}    off
${blink}    blink
${loudspeaker}    Loudspeaker
${offHook}    OffHook
${onHook}    OnHook
${show}    Show
${line1}    Line1
${line2}    Line2
${line3}    Line3
${line4}    Line4
${line5}    Line5

${programKey1}    ProgramKey1
${programKey2}    ProgramKey2
${programKey3}    ProgramKey3
${programKey4}    ProgramKey4
${programKey5}    ProgramKey5
${programKey6}    ProgramKey6
${programKey7}    ProgramKey7
${programKey8}    ProgramKey8
${programKey9}    ProgramKey9
${programKey10}    ProgramKey10

${fac67}    FAC67
${callerId_blocked}    Caller ID
${enable}   1
${disable}  0
${pfserver}    2
${pfphone}    1
${pflineone}   1
${pflinetwo}   2
${intercomTypetwo}  2

#Call HIstory
${outgoing}    Outgoing
${incomming}   incomming
${all}    All
${missed}    Missed
${received}    Received

#-----------------------------#
#Hard key definations
#-----------------------------#

${scrollLeft}    ScrollLeft
${scrollRight}    ScrollRight
${scrollUp}    ScrollUp
${scrollDown}    ScrollDown
${settings}    Settings
${handsFree}    HandsFree
${increaseVolume}    IncreaseVolume
${decreaseVolume}    DecreaseVolume
${voicemail}    VoiceMail
${transfer}    Transfer
${conference}    Conference
${directory}    Directory
${callersList}    CallersList
${enter}    Enter
${consultiveCall}    ConsultiveCall

#-----------------------------
#Softkey definations
#-----------------------------

${bottomKey1}    1
${bottomKey2}    2
${bottomKey3}    3
${bottomKey4}    4
${bottomKey5}    5

${more}    More
${callBack}    CallBack
${open}    Open

${voicemailPassword}    12345

${enterprise}    Enterprise
${mobile}    Mobile
${quit}    Quit
${details}    Details
${intercom}   Intercom
${pickup}    Pickup
${park}    Park
${unPark}    UnPark
${conference}    Conference
${directConference}    DirectConference
${consultiveConference}    ConsultiveConference
${conferenceIntercom}     Conference Intercom
${conferenceBlind}      Conference Blind
${drop}    Drop
${leave}    Leave
${transfer}    Transfer
${dial}    Dial
${answer}    Answer

${fac}    FAC
${consult}    Consult
${displayVoiceMail}    Voice Mail
${default}    default
${timeout}    timeout
${digitTerminator}    digitTerminator
${terminatorString}    TerminatorString
${callHistory}    Call History
${toVm}    ToVm
${cancel}    Cancel
${dialing}    dialing
${state}    State
${backspace}    Backspace
${auto}    auto
&{message}    ringing=Ringing    missedCallCount=2    callHistory=Call History

#Transfer type
${consultiveTransfer}    ConsultiveTransfer
${blindTransfer}    BlindTransfer
${semiAttendedTransfer}    SemiAttendedTransfer

${invalidExtension}    4987
${idle}    Idle
${forward}    Forward
${menu}    Menu
${backupAutoAttendant}    Backup Auto
${userSettings}    User Settings - Login
${play}    Play
${receiptConfirmation}    Receipt Confirmation
${goodBye}    GoodBye
${delete}    Delete
${one}    1
${voiceMailLogin}    Voice Mail Login
&{voicemailDisplay}    inbox=Inbox    saved=Saved    deleted=Deleted    quit=Quit
&{voicemailscreen}    play=Play    callback=Call Back    delete=Delete
${invalidNumber}    1234567890128888
${invalid}    234567890128888
${inMeeting}    In a meeting
${extendedAbsence}    Extended Absence
${doNotDisturb}    Do not disturb
${noAnswer}    No Answer
${number}    Number
${name}    Name
${back}    Back
${hardKey}    HardKey
${softKey}    SoftKey
${start}    Start
${stop}    Stop
${send}    Send
${available}    Available
${never}    Never
${always}    Always
${stopPlay}    StopPlay
${reply}    Reply
${callVM}    Call VM
${select}    Select
${save}    Save
${userAvailability}    UserAvailability
${audio}    Audio
${availability}    Availability
${playInt}    Play Int
${login}    Login
${logIssue}    Log Issue
${diagnostics}    Diagnostics
${capture}    Capture
${capturing}    Capturing
${inbox}    Inbox
${assigned}    Assigned
${edit}    Edit
${loginVoicemail}    12345#
${wrongVoicemailpassword}    4321#
${incorrectPassword}    Incorrect password
${unassignExtn}   732#
${voicemailUserLogin}    Voicemail User Login
${enterVoicemailPassword}    Enter Voicemail Password
${visualVoicemailScreen}    Voicemail
${assignUser}    Assign user
${extension}    Extension
${password}    Password
${outOfOffice}    Out of office
${noMode}    No Mode
${vm}    VM
${custom}    Custom
${moreBack}    moreBack
${mute}    Mute
${unmute}   Unmute
${ringing}   Ringing
${iscalling}    Is Calling
${callHistory}    Call History
${actionNotPermitted}    Action not permitted
${enterprise}    Enterprise

${miVoicevoicemailNumber}    4101
${micloudVoicemailNumber}    7101
#${voicemailNumber}    4105
${inboxToSaved}    InboxToSaved
${deleteToInbox}    DeleteToInbox
${savedToDelete}    SavedToDelete
${xferNotAllowed}    Transfer not permitted on this call
${xconfNotAllowed}    Conference not permitted on this call
${notPermittedOnThisCall}    Not Permitted on this call
${unPark}    UnPark
${none}    none
&{directoryAction}    default=default    searchOnly=searchOnly    searchWithDial=searchWithDial    close=close    quit=quit    whisper=whisper    searchMultiple=searchMultiple    searchInvalid=searchInvalid    mainMenu=mainMenu    selectOnly=selectOnly    dialvoicemail=dialvoicemail
&{extensionNum}    ext1=4001    ext2=4002    ext3=4003    ext4=4004
&{voiceExtensionNum}    ext1=4001    ext2=4002    ext3=4003    ext4=4004
&{cloudExtensionNum}    ext1=1001    ext2=1002    ext3=1003    ext4=1004
${copy}    copy
${edit}    Edit
${speed}    Speed
${local}    local
${byFirst}    By First
${byLast}     By Last
${directory}    Directory
${enterprise}    Enterprise
${directoryFormat}    directoryFormat
${firstLast}    FirstLast
${lastFirst}    LastFirst
${nothing}    Nothing
${whisper}    Whisper
${assign}    Assign
${merge}    Merge
${ping}    Ping
${callParked}    Call Parked
${timeZone}    Time Zone
${enabled}    True
${disabled}    False
${alwaysDestination}    Always destination
${simulRing}    Simulring
${voicemailInbox}    Voicemail Inbox
${playVoicemail}    Voicemail Play
${pauseVoicemail}    Voicemail Pause
${stopVoicemail}    Voicemail Stop
${ucbNumber}    4801
${wrongAccessCode}    1234#
${accessCode}    20800675#
${linePark}    linePark
${restart}    Restart
${privateCall}    Privatecall
${busy}    Busy
${redial}    Redial
&{conferenceDisplay}    conference=Conference        conference_6910= 1.auto user    offhook= >

${conferenceExt}    Conference Ext
${traceroute}   Traceroute
${tracerouting}   traceroute to
${ipaddrstr}    8.8.8.8
${ipaddrstr_two}    8.8.4.4
${debugon}    Debug on
${debugoff}    Debug off
${log_upload}    log_upload
${callVMInbox}    Call Inbox VM
${callVMSaved}    Call Saved VM
${resume}    Resume
${BCATransfer}    BCATransfer
${agentLogin}    Agent Login
${agentLogout}    Agent Logout
${agentWrapUp}    Agent Wrap Up
${agentWrapU}    Agent Wrap U
${changeDefaultAudioPath}    change default audio path
${changeDefau}    change defau
${advanced}    Advanced
${anonymous}    Anonymous
${parknPage}    Park and Page
${parkAndPag}    Park and Pag
${unassignUser}     Unassign user
${pause}        Pause
${lock}    Lock
${pick}    PickUp
${replyPlay}    ReplyPlay
${voicemailReply}    Voicemail
${saveReply}    SaveReply
${bca}    BCA
${unlock}    Unlock
${voicemaildelete}    VoicemailDelete
${talk}    Talk
${parkCancel}    Park Cancel
${partialExtension}    10
${invalidPhoneNumber}    Invalid Phone Number
${messageWaitingIndicator}    message_waiting
${callTransferred}    Call Transferred
${numberofrings}    Number of Rings
${fivedigit}    fiveDigit
${firsttwo}    firstTwo
${lasttwo}    lastTwo
${bothdigits}    both
${logging_issue}    Logging Issue
${unAssigned}    UnAssigned
${autoUser1}    auto user4001
${firstPhone}    4001
${startplay}    startPlay
${Transferwithpartialdial}    TransferWpd
${requestDenied}    Request denied
${SemiAttendedTransferVSK}   SemiAttendedTransferVSK
${vacation}    Vacation
${callForwardMode}    Call Forward Mode
${vmpasschangewindow}    New voicemail password
${confirmnvm}   Confirm
${newvmpass}   123456
${callerBlocked}    Caller ID Blocked
${consultiveTransfervp}    ConsultiveTransfervp
${sendf}   SendF
${lineInUse}    Line in use

${whisperPageFAC}    Whisperpage
${busyOutHuntGroupFAC}    Busyouthuntgroup
${silentCoachFAC}    Silentcoach
${bargeInFAC}    Bargein
${silentMonitorFAC}    Silentmonitor
${fivedigitnumber}    12345
${mobilecontacts}    Mobile Contacts
${reset}    Reset
${traceroutecommand}    Traceroute Command
${unattendedtransfer}    unattendedtransfer
${defaultRingNumber}    5
${timedate}    Time and Date
${close}    Close
${wrong_number}    4444
${transfer_invalid_number}    Phone number is invalid or not properly formatted
${newVMpassword}    New Voicemail password
${newVoicemailPassword}    123456
${callVMSaved}    Call Saved VM
${invalidHost}    Invalid Hostname
${invalidHostName}    Please enter a valid Hostname

${callAppearanceIncoming}    CALL_APPEARANCE_INCOMING
${callAppearanceActive}    CALL_APPEARANCE_ACTIVE
${callAppearanceDND}    CALL_APPEARANCE_DND
${callAppearanceIdle}    CALL_APPEARANCE_IDLE
${callAppearanceLocalHold}    CALL_APPEARANCE_LOCAL_HOLD
${callAppearanceRemoteHold}    CALL_APPEARANCE_REMOTE_HOLD
${callAppearanceConfActive}    CALL_APPEARANCE_CONFERENCE

${callHistoryReceived}    CALL_HISTORY_INCOMING_RECEIVED
${callHistoryOutgoing}    CALL_HISTORY_OUTGOING
${callHistoryMissed}    CALL_HISTORY_MISSED
${callHistoryAll}    CALL_HISTORY_ALL
${numberOfPackets}    Number of Packets
${VMInbox}    VOICE_MAIL_INBOX
${VMSaved}    VOICE_MAIL_SAVED
${VMDeleted}    VOICE_MAIL_DELETED

${standard}    Standard
${ringTones}    Ring Tones
${audioMode}    Audio Mode
${startCapture}    startCapture

${Executives}    1
${Executives_RK}    13
${Executives_AB}    11


${yes}    Yes
${no}    No

${speedDial}    Speeddial
${speeddialxfer}    speeddialxfer
${speeddialconf}    speeddialconf
${none}    None

${Asterisk_ip}   10.112.123.89
${perferences}  Preferences
${callForward}    Call Fwd

${red}    Red
${orange}    Orange
${green}    Green

${conferenceLeader}    Conference le
${conferenceMember}    Conference mem
${blf}    blf
${callTerminated}      Call Terminated
${ignore}      Ignore
${silence}      Silence
${startUp}    startup.cfg
${submit}    Submit
${MxOne}    MxOne
${MiV5000}    MiV5000
${automationTestingFolder}    AutomationTesting
${automationTestingFolderPath}    ${automationTestingFolder}/
${audioDiagnostics}    Audio Diagnostics

${directory_1_path}     ftp://desktop:desktop@10.112.123.107:21/systeminfo/companylist.csv
${directory_2_path}     ftp://desktop:desktop@10.112.123.107:21/systeminfo/homelist.csv
${systeminfo}    systeminfo
${serverDetails}     ftp://desktop:desktop@10.112.123.107:21/systeminfo
${uploadButton}    //*[@id="content"]//td[2]/input
${filesSent}    Files Sent
${sysInfo}    Sys_Info
${fileSent}    //*[@id="content"]
${upload_Xpath}    //*[@id="content"]/table/tbody//td[2]/input
${httpserverDetails}     http://root:Jafe@20_20@10.112.123.89:22/systeminfo
${pfserver}    2
${pfphone}    1
${pflineone}   1
${pflinetwo}   2
${intercomTypetwo}  2

${logIp}    10.112.123.89
${logPort}  514

${emergencydialplan}     emergency dial plan
#${emergencydialplanvalue}   333|222|777|137'
${configurationServer}    configurationServer
${transportProtocol}    sip transport protocol
${rtpEncryption}    sip srtp mode
${sipBlocking}    sip register blocking
${httpsClientMethod}    https client method

${startWireshark}    start
${stopWireshark}     stop
${TLS}  TLS
${version}  Version
#${tlsversionstring}     TLS 1.2
${configurationServer}    configurationServer
${transportProtocol}    sip transport protocol
${rtpEncryption}    sip srtp mode
${sipBlocking}    sip register blocking
${httpsClientMethod}    https client method
${urlxml}    http://10.112.91.53/

${language}    Language
${screenLanguage}    Screen Language
${inputLanguage}    Input Language
${status}    Status
${english}    English
${italiano}    Italiano
${configurationFolderAbsolutePath}    http://10.112.123.107/${automationTestingFolderPath}
${dnd}    DND
${icom}    Icom
${root}    root
${speaker}    speaker

${dialPad0}    DialPad0
${dialPad1}    DialPad1
${dialPad2}    DialPad2
${dialPad3}    DialPad3
${dialPad4}    DialPad4
${dialPad5}    DialPad5
${dialPad6}    DialPad6
${dialPad7}    DialPad7
${dialPad8}    DialPad8
${dialPad9}    DialPad9

${ist}    IN-Kolkata
${addNew}    Add New
${asia}    Asia
${cet}    DE-Berlin

${mode1}    Mode 1
${mode2}    Mode 2
${mode3}    Mode 3
${backgroundImage}    Background Image
${ftp}    FTP
${bgImages}    BGImages

${httpServer}    http://10.112.123.89
${myPhone}    My Phone
${conferenced3Calls}    Conferenced 3 calls
${network}    Network
${802.1x}    802.1x
${eapmd5}    EAP-MD5
${eaptls}    EAP-TLS
${lldp}    LLDP
${favourites}    Favourites
${clearLog}    Clear log

# ICONS
&{softLineIcon}    CallHistory=SOFT_FEATURE_CALL_HISTORY    CallersList=SOFT_FEATURE_CALLERS_LIST    Conference=SOFT_FEATURE_CONFERENCE
...              Contacts=SOFT_FEATURE_CONTACTS    Directory=SOFT_FEATURE_DIRECTORY    Flash=SOFT_FEATURE_FLASH
...              Intercom=SOFT_FEATURE_INTERCOM    Login=SOFT_FEATURE_LOGIN    Park=SOFT_FEATURE_PARK    Pickup=SOFT_FEATURE_PICKUP
...              RedialList=SOFT_FEATURE_REDIAL_LIST    Transfer=SOFT_FEATURE_TRANSFER    LineActive=SOFT_LINE_ACTIVE
...              ActiveSIP=SOFT_LINE_ACTIVE_SIP    LineHold=SOFT_LINE_HOLD    LineIdle=SOFT_LINE_IDLE    IdleSIP=SOFT_LINE_IDLE_SIP
...              LineRinging=SOFT_LINE_RING    blfIdle=STATUS_BLF_GREEN    blfUnsubscribed=STATUS_BLF_QUESTION
...              blfBusy=STATUS_BLF_RED    blfBlink=STATUS_BLF_YELLOW

&{Tones}    Dial=Dial    Ringing=Ringing    CallWaiting=CallWaiting
${diagnosticsServer}    diagnostic_server
${logUpload}    log_upload
${upload}    Upload
${ftp}    FTP
${tftp}    TFTP
${http}    HTTP

${startUp}    startup.cfg
${mac_cfg}    mac.cfg
${empty}
${blfStatusGreen}    STATUS_BLF_GREEN
${blfStatusQuestion}    STATUS_BLF_QUESTION
${blfStatusQuestion}    STATUS_BLF_RED

${availabilityVacation}    Vacation

${Unconditional}    Unconditional
${NoResponse}    NoResponse
${BusyForward}    Busy
${DNDForward}    DND

























