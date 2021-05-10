*** Variables ***

#${url}    https://portal.sit.shoretel.com/
#${username}    derek@mitel-test.com
#${bossPassword}    Mitel@123
#${url}    http://10.32.6.67/UserAccount/LogOn
#${username}    staff@shoretel.com
#${password}    Abc123!!
#${account_name}    Automation
#&{add_user_details}    part_name=SC1    Person_FirstName=Surender    Person_LastName=SS    Person_BusinessEmail=abc@test.com    loc_name=Automate    SU_Email=dm@auto.local
&{bossDetails}    account_name=Automation    part_name=SC1    button_box=0
&{bossDetailsPKM}    account_name=Automation    part_name=SC1    button_box=1

&{bossLoginDetails}    url=http://portal.sit.shoretel.com/    UserName=derek@mitel-test.com    Password=Mitel@123

#&{MiVoice}    button_box=0    pbx=MiVoice
#&{MiCloud}    account_name=Automation    part_name=SC1    button_box=0    pbx=MiCloud

#&{D2API}    ip=10.112.91.62:5478    username=desktop    password=india@123
#&{D2API}    ip=10.211.41.103:5478   username=admin    password=Mitel@123

&{D2API}    ip=10.112.91.49:5478    username=desktop    password=desktop@123
#&{D2API}    ip=10.112.91.65:5478    username=mivc    password=123456

${fullyFeatured}    Fully   Featured
${fullyFeatured_ag}    Fully Featured_AG
${transferBlind}    Transfer Blind
${conferenceConsultative}    Conference Consultative
${bargeIn}    Barge In
${bridgedCallAppearance}    Bridged Call Appearance
${callAppearance}    Call Appearance
${callMove}    Call Move
${changeAvailability}    Change Availability
${changeDefaultAudioPath}    Change Default Audio Path
${conferenceBlind}    Conference Blind
${conferenceIntercom}    Conference Intercom
${dialMailbox}     Dial Mailbox
${dialNumber}    Dial Number Speed Dial
${groupPickup}    Group Pickup
${hotline}    Hotline
${intercom}    Intercom
${mobileLine}    Mobile Line
${monitorExtension}    Monitor Extension
${page}    Page
${park}    Park
${pickup}    Pickup
${pickupUnpark}    PICK AND PARK
${pickAndUnpar}    PICK AND PAR
${recordCall}    Record Call
${recordExtension}    Record Extension
${sendDigitsOverCall}    Send Digits Over Call
${silentCoach}    Silent Coach
${silentMonitor}    Silent Monitor
${toggleHandsfree}    Toggle Handsfree
${toggleLock}    Toggle Lock/Unlock
${transferBlind}    Transfer Blind
${transferConsultative}    Transfer Consultative
${transferIntercom}    Transfer Intercom
${transferToMailbox}    Transfer To Mailbox
${transferWhisper}    Transfer Whisper
${unpark}    Unpark
${unused}    Unused
${whisperPage}    Whisper Page
${privateCall}    Privatecall
${whisperPageMute}    Whisper Page Mute
${merge}    Merge
${transferConsultative}     Transfer Consultative
${ignore}   Ignore
#${transferToWhisper}    Transfer To Whisper
#${transferToWhisper}    TRANSFER TO WHISPER
${monitor}    Monitor
${barge}    Barge
${bca}    BCA
&{displayMessage}    notPermit=Not Permitted on this call    conferenceConsult=Conference C    silentMonitor=Silent Monit
...                  transferConsult=Transfer Con    noCallsToPickup=No calls to pickup    whisperPage=Whisper Page
...                  whisperPageMute=Whisper Page Mute    conferenceIntercom=Conference I    conferenceBlind=Conference B
...                  callTransferred=Call Transferred    transferBlind=Transfer Bli    transferIntercom=Transfer Int
...                  transferToMailbox=Transfer To   dialNumber=Dial Number       dialMailbox=Dial Mailbox
...                  transferToWhisper=Transfer Whi    userSettings=User Settings    monitorExtn=Monitor Exte
...                  actionNotPermitted=Action Not Permitted    resume=Resume       noCallsToUnpark=No calls to unpark
...                  connect=Connect     bluetooth=Bluetooth

${xmonRinging}    MONITOR_EXT_RINGING
${xmonIdle}    MONITOR_EXT_IDLE
${xmonIdleMWI}    MONITOR_EXT_IDLE_MWI
${xmonIdleDND}    MONITOR_EXT_IDLE_DND
${xmonBusy}    MONITOR_EXT_BUSY
${xmonActive}    MONITOR_EXT_ACTIVE

${bcaIdle}    BCA_IDLE
${bcaIncomingCall}    BCA_INCOMING_CALL
${bcaActive}    BCA_ACTIVE
${bcaConferenceActive}    BCA_CONF_ACTIVE
${bcaNoJoin}	BCA_IN_USE_NO_JOIN
${bcaJoin}	BCA_IN_USE_YES_JOIN
${bcaLocalHold}	BCA_HOLD_OR_PARKED
${bcaRemoteHold}	BCA_REM_HOLD_OR_PARKED

${executives}    Executives
${executives_vk}    Executives_VK

&{displayMessage}    notPermit=Not Permitted on this call    conferenceConsult=Conference C    silentMonitor=Silent Monit
...                  transferConsult=Transfer Con    noCallsToPickup=No calls to pickup    whisperPage=Whisper Page
...                  whisperPageMute=Whisper Page Mute    conferenceIntercom=Conference I    conferenceBlind=Conference B
...                  callTransferred=Call Transferred    transferBlind=Transfer Bli    transferIntercom=Transfer Int
...                  transferToMailbox=Transfer To   dialNumber=Dial Number       dialMailbox=Dial Mailbox
...                  transferToWhisper=Transfer Whi    userSettings=User Settings    monitorExtn=Monitor Exte
...                  actionNotPermitted=Action Not Permitted    resume=Resume       noCallsToUnpark=No calls to unpark
...                  connect=Connect     bluetooth=Bluetooth    bargIn=Barg I    availabilityVacation=Change Avail
